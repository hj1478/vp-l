#!/usr/bin/env python3
"""Dense watch on towns about to fall.

The 6-hour observatory misses last-second joiners (people hop into a snipable
town hours before it falls) and never captures their run-up activity — so the
"who inherited and how active was everyone" ground truth is incomplete exactly
for the cases we care about. This tool watches a small set of imminent-fall towns
FREQUENTLY: every run it re-fetches each town's live roster + every resident's
lastOnline/joinedTownAt, appends a snapshot to data/imminent_watch.jsonl, and
flags new joiners. When the town finally flips we have a dense, complete history.

Targets come from the watchlist (towns whose mayor is ~35-52 days idle: about to
fall, not premium) or an explicit --towns list.

Usage:
  python3 imminent_watch.py --towns Neo_Osaka,Tsu     # watch specific towns
  python3 imminent_watch.py                            # auto from data/watch_towns.json
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone

from town_observatory import _req, TOWNS, PLAYERS, BATCH, PACE_S

OUT = "data/imminent_watch.jsonl"


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resident_details(names):
    out = {}
    uniq = sorted({n for n in names if n})
    for i in range(0, len(uniq), BATCH):
        try:
            d = _req(PLAYERS, {"query": uniq[i:i + BATCH]})
        except Exception:
            d = None
        for p in (d or []):
            if isinstance(p, dict) and p.get("name"):
                ts = p.get("timestamps") or {}
                out[p["name"]] = {"lastOnline": ts.get("lastOnline"),
                                  "joinedTownAt": ts.get("joinedTownAt"),
                                  "registered": ts.get("registered"),
                                  "isOnline": bool((p.get("status") or {}).get("isOnline"))}
        time.sleep(PACE_S)
    return out


def targets_from_watchlist(path, min_idle, max_idle):
    if not os.path.exists(path):
        return []
    wl = json.load(open(path))
    out = []
    for t in wl.get("towns", []):
        idle = t.get("mayor_idle_days")
        if idle is not None and min_idle <= idle <= max_idle:
            out.append(t["name"])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--towns", default="", help="comma-separated town names (overrides watchlist)")
    ap.add_argument("--watchlist", default="data/watch_towns.json")
    ap.add_argument("--pins-file", default="imminent_towns.txt",
                    help="towns to always watch through their fall (one per line)")
    ap.add_argument("--min-idle", type=float, default=35.0, help="lower mayor-idle bound (approaching fall)")
    ap.add_argument("--max-idle", type=float, default=52.0, help="upper bound (exclude likely-premium)")
    ap.add_argument("--joiner-days", type=float, default=7.0, help="joined within N days = flagged joiner")
    ap.add_argument("--loop", action="store_true", help="keep polling (minute-resolution) for --duration")
    ap.add_argument("--interval", type=float, default=90.0, help="seconds between polls in --loop")
    ap.add_argument("--duration", type=float, default=None, help="seconds to keep fast-watching")
    ap.add_argument("--critical-only", action="store_true",
                    help="fast-watch only towns whose mayor is within ~1 day of the fall")
    ap.add_argument("--critical-idle", type=float, default=41.0,
                    help="mayor idle days at/above which a town is 'critical' (about to fall)")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args(argv)

    if args.towns:
        towns = [t.strip() for t in args.towns.split(",") if t.strip()]
    else:
        pins = []
        if args.pins_file and os.path.exists(args.pins_file):
            for line in open(args.pins_file, encoding="utf-8"):
                line = line.split("#", 1)[0].strip()
                if line:
                    pins.append(line)
        # Critical (fast-watch) mode watches only the PINNED towns — a small,
        # bounded set — so the detect pass stays cheap. The normal hourly watch
        # still covers the broad 35-52d watchlist window.
        auto = [] if args.critical_only else targets_from_watchlist(
            args.watchlist, args.min_idle, args.max_idle)
        seen, towns = set(), []
        for n in pins + auto:
            if n.lower() not in seen:
                seen.add(n.lower())
                towns.append(n)
    if not towns:
        print("No imminent-fall towns to watch.")
        return 0

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    def one_pass(names, quiet=False):
        """Snapshot each town once; append to the log; return {town: mayor_idle}."""
        now = time.time()
        ts_iso = _now_iso()
        idle_by_town = {}
        for name in names:
            # A pinned town can fall and be deleted (Neo_Osaka after its snipe),
            # so the API 404s on it. One dead town must not abort the whole watch.
            try:
                d = _req(TOWNS, {"query": [name]})
            except Exception as e:
                print(f"    (skip {name}: {e})")
                continue
            if not d or not isinstance(d[0], dict) or not d[0].get("name"):
                continue
            t = d[0]
            mayor = (t.get("mayor") or {}).get("name")
            res_names = [r.get("name") for r in (t.get("residents") or []) if r.get("name")]
            councillors = [c.get("name") for c in ((t.get("ranks") or {}).get("Councillor") or [])]
            det = resident_details(res_names + ([mayor] if mayor else []))
            mayor_idle = None
            if mayor and det.get(mayor, {}).get("lastOnline"):
                mayor_idle = round((now - det[mayor]["lastOnline"] / 1000) / 86400, 1)
            idle_by_town[t.get("name")] = mayor_idle
            residents = []
            for n in res_names:
                f = det.get(n, {})
                lo, jt = f.get("lastOnline"), f.get("joinedTownAt")
                residents.append({
                    "name": n, "lastOnline": lo, "joinedTownAt": jt,
                    "idle_days": round((now - lo / 1000) / 86400, 1) if lo else None,
                    "joined_days_ago": round((now - jt / 1000) / 86400, 1) if jt else None,
                    "isOnline": f.get("isOnline", False)})
            snap = {"ts": ts_iso, "town": t.get("name"), "mayor": mayor,
                    "mayor_idle_days": mayor_idle, "balance": (t.get("stats") or {}).get("balance"),
                    "has_councillors": len(councillors) > 0, "num_residents": len(res_names),
                    "residents": residents}
            with open(args.out, "a") as fh:
                fh.write(json.dumps(snap) + "\n")
            if not quiet:
                d2f = round(42 - mayor_idle, 1) if mayor_idle is not None else None
                print(f"=== {t.get('name')} | {snap['balance']}g | mayor {mayor} idle "
                      f"{mayor_idle}d | falls ~{d2f}d | residents {len(res_names)} ===")
                for r in sorted((x for x in residents if x["name"] != mayor),
                                key=lambda r: -(r["lastOnline"] or 0)):
                    j = " <<JOINED RECENTLY" if (r["joined_days_ago"] is not None
                                                 and r["joined_days_ago"] <= args.joiner_days) else ""
                    print(f"    {r['name'][:18]:18s} idle {r['idle_days']}d online={r['isOnline']}{j}")
        return idle_by_town

    # First pass over all candidates; optionally narrow to CRITICAL towns (mayor
    # within ~1 day of the 42-day fall) for the fast minute-resolution loop.
    idle = one_pass(towns)
    critical = [t for t, i in idle.items() if i is not None and i >= args.critical_idle]
    print(f"CRITICAL_COUNT={len(critical)}")
    if args.critical_only:
        if not critical:
            print(f"\nNo critical towns (none with mayor idle >= {args.critical_idle}d). Nothing to fast-watch.")
            return 0
        print(f"\nCRITICAL (fast-watching): {critical}")
        towns = critical

    if args.loop and args.duration:
        deadline = time.monotonic() + args.duration
        while time.monotonic() < deadline:
            time.sleep(max(1, min(args.interval, deadline - time.monotonic())))
            one_pass(towns, quiet=True)
        print(f"fast-watch window done ({args.duration}s at ~{args.interval}s).")
    print(f"\nappended snapshots to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

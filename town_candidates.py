#!/usr/bin/env python3
"""Find the towns worth focusing our logging on: those whose mayor is going
inactive and are therefore heading toward a fall.

A town only exercises the "most active resident" rule if its mayor lapses to
inactivity (≈42 days) with no councillors. So rather than log all ~5,600 towns
uniformly, we scan every town's mayor once, keep the ones whose mayor has been
offline long enough to be *approaching* the fall threshold, and hand that
watchlist to the observatory for dense logging. This concentrates effort on the
towns that will actually generate events — and captures rich resident-activity
history right through the fall.

Writes data/watch_towns.json (ranked by mayor idle time). Councillor-less towns
are flagged, since those are the pure "most active resident" cases.

Usage:
  python3 town_candidates.py                       # full scan
  python3 town_candidates.py --min-idle-days 21    # how inactive to qualify
  python3 town_candidates.py --limit 200           # scan only first N (testing)
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone

from town_observatory import _req, all_town_names, parse_town, TOWNS, BATCH, PACE_S


def scan(names):
    """Return per-town: mayor name/uuid, councillor & resident counts."""
    towns = []
    for i in range(0, len(names), BATCH):
        d = _req(TOWNS, {"query": names[i:i + BATCH]})
        for t in (d or []):
            rec = parse_town(t)
            if rec and rec["mayor_name"]:
                towns.append({"uuid": t.get("uuid"), "name": rec["name"],
                              "mayor": rec["mayor_name"], "mayor_uuid": rec["mayor_uuid"],
                              "num_councillors": len(rec["councillors"]),
                              "num_residents": len(rec["residents"])})
        time.sleep(PACE_S)
    return towns


def mayor_last_online(mayor_names):
    """{mayor_name: lastOnline_ms} via the players endpoint, batched."""
    from town_observatory import PLAYERS
    out = {}
    uniq = sorted(set(m for m in mayor_names if m))
    for i in range(0, len(uniq), BATCH):
        d = _req(PLAYERS, {"query": uniq[i:i + BATCH]})
        for p in (d or []):
            if isinstance(p, dict) and p.get("name"):
                out[p["name"]] = (p.get("timestamps") or {}).get("lastOnline")
        time.sleep(PACE_S)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-idle-days", type=float, default=21.0,
                    help="keep towns whose mayor has been offline at least this long")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("-o", "--out", default="data/watch_towns.json")
    args = ap.parse_args(argv)

    names = all_town_names()
    if not names:
        print("Could not fetch town list (rate-limited?).")
        return 1
    if args.limit:
        names = names[:args.limit]
    print(f"Scanning {len(names)} towns for inactive mayors...")
    towns = scan(names)
    los = mayor_last_online([t["mayor"] for t in towns])

    now = time.time()
    watch = []
    for t in towns:
        lo = los.get(t["mayor"])
        if not lo:
            continue
        idle = (now - lo / 1000.0) / 86400.0
        if idle >= args.min_idle_days:
            t["mayor_idle_days"] = round(idle, 1)
            t["mayor_last_online"] = datetime.fromtimestamp(lo / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
            t["days_to_fall_est"] = round(42 - idle, 1)   # negative => already past 42d
            t["councillorless"] = t["num_councillors"] == 0
            watch.append(t)

    watch.sort(key=lambda x: -x["mayor_idle_days"])
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    json.dump({"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "min_idle_days": args.min_idle_days,
               "scanned": len(names), "at_risk": len(watch),
               "towns": watch}, open(args.out, "w"), indent=2)

    cl = [w for w in watch if w["councillorless"]]
    print(f"\nAt-risk towns (mayor idle ≥ {args.min_idle_days}d): {len(watch)}  "
          f"(councillor-less, the pure cases: {len(cl)})")
    print(f"{'town':22s} {'mayor':16s} {'idle d':>7s} {'→fall':>6s} {'coun':>4s} {'res':>4s}")
    for w in watch[:25]:
        print(f"{w['name'][:22]:22s} {w['mayor'][:16]:16s} {w['mayor_idle_days']:>7.0f} "
              f"{w['days_to_fall_est']:>6.0f} {w['num_councillors']:>4d} {w['num_residents']:>4d}")
    if len(watch) > 25:
        print(f"... and {len(watch)-25} more (full list in {args.out})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
    """Return per-town: mayor, councillor & resident counts, bank gold, and the
    status flags needed for the snipe list."""
    towns = []
    for i in range(0, len(names), BATCH):
        d = _req(TOWNS, {"query": names[i:i + BATCH]})
        for t in (d or []):
            rec = parse_town(t)
            if rec and rec["mayor_name"]:
                st = t.get("status") or {}
                stats = t.get("stats") or {}
                towns.append({"uuid": t.get("uuid"), "name": rec["name"],
                              "mayor": rec["mayor_name"], "mayor_uuid": rec["mayor_uuid"],
                              "num_councillors": len(rec["councillors"]),
                              "num_residents": len(rec["residents"]),
                              "balance": float(stats.get("balance") or 0.0),
                              "is_open": bool(st.get("isOpen")),
                              "is_for_sale": bool(st.get("isForSale")),
                              "is_ruined": bool(st.get("isRuined")),
                              "is_public": bool(st.get("isPublic")),
                              "for_sale_price": stats.get("forSalePrice"),
                              "num_town_blocks": stats.get("numTownBlocks")})
        time.sleep(PACE_S)
    return towns


FALL_DAYS = 42.0          # inactivity threshold for a mayor's town to fall
OPEN_MIN_IDLE = 25.0      # an open town is only a real snipe once its mayor lapses
PREMIUM_IDLE = 60.0       # idle well past 42d without falling => almost certainly premium


def _snipe_status(t, idle):
    """Vet a town's snipability by mayor idle time."""
    if t["is_for_sale"]:
        return "for_sale", None
    if t["is_ruined"]:
        return "ruined", None
    if idle is None:               # open but mayor activity unknown
        return None, None
    d2f = FALL_DAYS - idle
    if 0 <= d2f <= (FALL_DAYS - OPEN_MIN_IDLE):
        return "falls_soon", round(d2f, 1)     # about to fall — the prime snipe
    if idle > PREMIUM_IDLE:
        return "likely_premium", round(d2f, 1)  # never falling — skip
    if d2f < 0:
        return "overdue", round(d2f, 1)          # past 42d, not premium-confirmed
    return None, None              # mayor still active enough — not snipable yet


def build_snipes(towns, los, now):
    """Snipable towns VETTED BY IDLE TIME and ranked by bank gold. A town is a
    real snipe if it's for-sale, ruined, or open with an inactive mayor heading
    for the ~42-day fall. Open towns whose mayor is still active are NOT listed
    (you can't take them); ones idle well past 42d are flagged likely-premium."""
    snipes = []
    for t in towns:
        if not (t["is_open"] or t["is_for_sale"] or t["is_ruined"]):
            continue
        lo = los.get(t["mayor"])
        idle = round((now - lo / 1000.0) / 86400.0, 1) if lo else None
        status, d2f = _snipe_status(t, idle)
        if status is None:
            continue
        snipes.append({
            "town": t["name"], "balance": round(t["balance"], 1),
            "status": status, "days_to_fall_est": d2f,
            "for_sale_price": t["for_sale_price"],
            "profit_if_bought": (round(t["balance"] - t["for_sale_price"], 1)
                                 if t["is_for_sale"] and t["for_sale_price"] is not None else None),
            "num_residents": t["num_residents"],
            "num_town_blocks": t["num_town_blocks"],
            "mayor": t["mayor"], "mayor_idle_days": idle,
        })
    # takeable-now/soon first (for_sale, ruined, falls_soon), then by gold desc
    grab = {"for_sale", "ruined", "falls_soon"}
    snipes.sort(key=lambda s: (0 if s["status"] in grab else 1, -s["balance"]))
    return snipes


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

    # --- snipe list: grabbable towns ranked by bank gold ---
    snipes = build_snipes(towns, los, now)
    snipe_path = os.path.join(os.path.dirname(args.out) or ".", "snipe_list.json")
    json.dump({"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "scanned": len(names), "snipable_towns": len(snipes),
               "towns": snipes}, open(snipe_path, "w"), indent=2)
    gold = [s for s in snipes if s["balance"] > 0]
    print(f"\nSnipe list (vetted by idle): {len(snipes)} targets ({len(gold)} with bank gold) -> {snipe_path}")
    print(f"{'town':20s} {'gold':>8s} {'falls in':>9s} {'res':>4s} {'status':16s} mayor")
    for s in snipes[:25]:
        d2f = f"~{s['days_to_fall_est']:.0f}d" if s["days_to_fall_est"] is not None else "-"
        print(f"{s['town'][:20]:20s} {s['balance']:>7.0f}g {d2f:>9s} {s['num_residents']:>4d} "
              f"{s['status']:16s} {s['mayor'][:16]}")

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

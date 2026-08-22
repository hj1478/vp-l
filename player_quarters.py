#!/usr/bin/env python3
"""Find the quarters (shops/apartments/inns/…) owned by given players.

EarthMC "quarters" are ownable sub-plots inside towns, typed SHOP/APARTMENT/INN/
STATION/etc. — the API's notion of a player's property/shops. There is no
owner index, so this lists every quarter (GET /v4/quarters), fetches details in
paced UUID batches, and keeps the ones whose owner is in the target set.

(Chest-shop contents — items/prices — are NOT in the API; those live in-world.)

Usage:
  python3 player_quarters.py --players Tendonkeys,LukeMacFarlane   # specific
  python3 player_quarters.py --players-file players.txt            # tracked list
  python3 player_quarters.py --shops-only                          # only type SHOP
"""
import argparse
import json
import os
import time
import urllib.request
import urllib.error

Q = "https://api.earthmc.net/v4/quarters"
BATCH = 40
PACE = 2.0


def _req(url, payload=None, tries=5):
    data = json.dumps(payload).encode() if payload is not None else None
    for a in range(tries):
        try:
            req = urllib.request.Request(url, data=data,
                                         method="POST" if data else "GET",
                                         headers={"Content-Type": "application/json",
                                                  "User-Agent": "quarters/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503):
                time.sleep(min(45, 4 * (a + 1) ** 2)); continue
            return None
        except (OSError, json.JSONDecodeError, ValueError):
            time.sleep(min(45, 4 * (a + 1) ** 2))
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", default="")
    ap.add_argument("--players-file", default="")
    ap.add_argument("--shops-only", action="store_true")
    ap.add_argument("--out", default="data/player_quarters.json")
    ap.add_argument("--limit", type=int, default=0, help="scan only first N quarters (testing)")
    args = ap.parse_args(argv)

    targets = set()
    if args.players:
        targets = {n.strip().lower() for n in args.players.split(",") if n.strip()}
    if args.players_file and os.path.exists(args.players_file):
        for line in open(args.players_file, encoding="utf-8"):
            line = line.split("#", 1)[0].strip()
            if line:
                targets.add(line.lower())
    if not targets:
        print("No target players. Pass --players a,b or --players-file.")
        return 1

    allq = _req(Q)
    if not allq:
        print("Could not list quarters (rate-limited).")
        return 1
    uuids = [q["uuid"] for q in allq if q.get("uuid")]
    if args.limit:
        uuids = uuids[:args.limit]
    print(f"Scanning {len(uuids)} quarters for {len(targets)} player(s)...")

    holdings = {}
    scanned = 0
    for i in range(0, len(uuids), BATCH):
        d = _req(Q, {"query": uuids[i:i + BATCH]})
        scanned += len(uuids[i:i + BATCH])
        for q in (d or []):
            owner = (q.get("owner") or {}).get("name")
            if not owner or owner.lower() not in targets:
                continue
            if args.shops_only and q.get("type") != "SHOP":
                continue
            holdings.setdefault(owner, []).append({
                "quarter": q.get("name"), "type": q.get("type"),
                "town": (q.get("town") or {}).get("name"),
                "nation": (q.get("nation") or {}).get("name"),
                "for_sale": bool((q.get("status") or {}).get("isForSale")),
                "price": (q.get("stats") or {}).get("price"),
                "volume": (q.get("stats") or {}).get("volume"),
            })
        if i % (BATCH * 20) == 0:
            print(f"  ...{scanned}/{len(uuids)} scanned")
        time.sleep(PACE)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    json.dump({"scanned": scanned, "holdings": holdings}, open(args.out, "w"), indent=2)

    print(f"\nProperty owned by tracked players (scanned {scanned} quarters):")
    if not holdings:
        print("  none found.")
    for owner, qs in sorted(holdings.items()):
        from collections import Counter
        types = Counter(q["type"] for q in qs)
        print(f"\n  {owner}: {len(qs)} quarter(s) — {dict(types)}")
        for q in qs:
            fs = f" [FOR SALE {q['price']}g]" if q["for_sale"] else ""
            print(f"     {q['type']:9s} '{q['quarter']}' in {q['town']} ({q['nation']}){fs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

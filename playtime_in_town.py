#!/usr/bin/env python3
"""Measure cumulative playtime a resident has accrued SINCE JOINING a town.

The town-inheritance "activity" term is playtime accumulated while a member of
the town (joinedTownAt -> now). The EarthMC API exposes no playtime, so we
reconstruct it from our own online-sampling (players.jsonl at ~5 min +
imminent_watch.jsonl hourly). Cumulative online time is summed over observed
online stretches (gaps > MAXGAP are treated as coverage holes, not playtime).

CRITICAL coverage caveat, reported per player:
  * COMPLETE  — our data starts at/before joinedTownAt (or within grace), so the
                measured in-town playtime is the real thing (typical for snipers
                who joined while we were watching).
  * LOWER-BOUND — we started watching after they joined; playtime before our
                first observation is unrecoverable, so the number undercounts.

Usage:
  python3 playtime_in_town.py --town Neo_Osaka
  python3 playtime_in_town.py --players johnzinnnn,Tendonkeys
"""
import argparse
import calendar
import json
import os
import time
import urllib.request
from datetime import datetime, timezone, timedelta

MAXGAP = 1200            # >20 min between online obs = coverage hole, not playtime
JOIN_GRACE = 3600        # first obs within 1h of joinedTownAt => COMPLETE
KST = timezone(timedelta(hours=9))


def _ep(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


def gather(names):
    """{name: sorted [(epoch, online_bool)]} from both logged sources."""
    obs = {n: [] for n in names}
    low = {n.lower(): n for n in names}
    if os.path.exists("data/players.jsonl"):
        for l in open("data/players.jsonl"):
            d = json.loads(l)
            n = low.get((d.get("name") or "").lower())
            if n:
                obs[n].append((_ep(d["timestamp"]), bool(d.get("online"))))
    if os.path.exists("data/imminent_watch.jsonl"):
        for l in open("data/imminent_watch.jsonl"):
            s = json.loads(l)
            for r in s.get("residents", []):
                n = low.get((r.get("name") or "").lower())
                if n:
                    obs[n].append((_ep(s["ts"]), bool(r.get("isOnline"))))
    return {n: sorted(set(v)) for n, v in obs.items()}


def playtime(rows):
    """Measured online seconds (gap-limited) and the first/last observation."""
    tot = 0
    for (t0, o0), (t1, _) in zip(rows, rows[1:]):
        if o0 and t1 - t0 <= MAXGAP:
            tot += t1 - t0
    return tot, (rows[0][0] if rows else None), (rows[-1][0] if rows else None)


def api_players(names):
    """{name: joinedTownAt_ms} — best effort (unresolvable players omitted)."""
    out = {}
    for i in range(0, len(names), 40):
        try:
            b = json.dumps({"query": names[i:i + 40]}).encode()
            req = urllib.request.Request("https://api.earthmc.net/v4/players", data=b,
                                         method="POST", headers={"Content-Type": "application/json",
                                                                 "User-Agent": "pt/1"})
            for p in json.load(urllib.request.urlopen(req, timeout=40)):
                out[p["name"]] = (p.get("timestamps") or {}).get("joinedTownAt")
        except Exception:
            pass
    return out


def town_residents(town):
    b = json.dumps({"query": [town]}).encode()
    req = urllib.request.Request("https://api.earthmc.net/v4/towns", data=b, method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "pt/1"})
    t = json.load(urllib.request.urlopen(req, timeout=40))[0]
    return [r["name"] for r in t["residents"]], (t.get("mayor") or {}).get("name")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--town", default="")
    ap.add_argument("--players", default="")
    ap.add_argument("--kst", action="store_true", help="show times in Korean time")
    args = ap.parse_args(argv)

    mayor = None
    if args.town:
        names, mayor = town_residents(args.town)
    else:
        names = [n.strip() for n in args.players.split(",") if n.strip()]
    if not names:
        print("Give --town NAME or --players a,b,c")
        return 1

    obs = gather(names)
    joined = api_players(names)
    now = time.time()

    rows = []
    for n in names:
        pt, first, last = playtime(obs[n])
        jt = (joined.get(n) or 0) / 1000.0 or None
        # completeness: did our data start at/before they joined (within grace)?
        if not obs[n]:
            cov = "NO DATA"
        elif jt and first <= jt + JOIN_GRACE:
            cov = "COMPLETE"
        else:
            cov = "LOWER-BOUND"
        rows.append((n, pt, jt, first, cov, n == mayor))

    rows.sort(key=lambda x: -x[1])
    print(f"In-town playtime (measured from our logs){' — '+args.town if args.town else ''}:")
    print(f"  {'player':16s} {'playtime':>9s} {'coverage':11s} {'joined town':12s}")
    for n, pt, jt, first, cov, ismayor in rows:
        jd = datetime.utcfromtimestamp(jt).strftime("%Y-%m-%d") if jt else "?"
        tag = " (mayor)" if ismayor else ""
        print(f"  {n[:16]:16s} {pt/3600:>7.1f}h {cov:11s} {jd:12s}{tag}")
    if any(c == "LOWER-BOUND" for *_, c, _ in rows):
        print("\n  LOWER-BOUND = they joined before we started watching; true playtime is higher.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

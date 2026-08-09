#!/usr/bin/env python3
"""Server-wide town-fall observatory (EarthMC).

Goal: accumulate the ground-truth events needed to reverse-engineer the
undisclosed "most active resident" rule that decides who inherits a town when an
inactive mayor's town falls.

Each run sweeps EVERY town (POST /v4/towns in paced batches), records a compact
structural snapshot (mayor, councillors, residents, ruined?) to data/town_state.json,
and diffs it against the previous snapshot. When a town's MAYOR CHANGES it captures
a full event to data/town_events.jsonl — including, for every resident at that
moment, the activity features we can observe (lastOnline, joinedTownAt, account
age) plus the old mayor's lastOnline and whether councillors existed. fall_analysis.py
later mines these events.

Design notes:
  * The API rejects large batches (>~50) and throttles bursts, so batches are 50
    with pacing + 403 backoff.
  * Partial sweeps are safe: towns not fetched this run keep their previous state,
    and events are only emitted for towns seen in BOTH the previous state and this
    sweep — so a rate-limited half-sweep can't fabricate "town vanished" events.

Usage:
  python3 town_observatory.py                 # full sweep
  python3 town_observatory.py --limit 200     # only first N towns (testing)
"""
import argparse
import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

TOWNS = "https://api.earthmc.net/v4/towns"
PLAYERS = "https://api.earthmc.net/v4/players"
BATCH = 50
PACE_S = 2.0
STATE = "data/town_state.json"
EVENTS = "data/town_events.jsonl"
META = "data/observatory.json"


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _req(url, payload=None, timeout=45, tries=5):
    """GET (payload None) or POST JSON, with backoff on 403/429/transient errors."""
    data = json.dumps(payload).encode() if payload is not None else None
    method = "POST" if data else "GET"
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, data=data, method=method,
                headers={"Content-Type": "application/json", "User-Agent": "town-observatory/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503):
                time.sleep(min(60, 4 * (attempt + 1) ** 2))
                continue
            raise
        except (OSError, json.JSONDecodeError, ValueError):
            time.sleep(min(60, 4 * (attempt + 1) ** 2))
    return None


def all_town_names():
    d = _req(TOWNS)
    return [t["name"] for t in (d or []) if isinstance(t, dict) and t.get("name")]


def parse_town(t):
    if not isinstance(t, dict) or not t.get("uuid"):
        return None
    mayor = t.get("mayor") or {}
    ranks = t.get("ranks") or {}
    councillors = [c.get("uuid") for c in (ranks.get("Councillor") or []) if c.get("uuid")]
    residents = [r.get("uuid") for r in (t.get("residents") or []) if r.get("uuid")]
    res_names = {r.get("uuid"): r.get("name") for r in (t.get("residents") or []) if r.get("uuid")}
    status = t.get("status") or {}
    return {
        "name": t.get("name"),
        "mayor_uuid": mayor.get("uuid"),
        "mayor_name": mayor.get("name"),
        "councillors": councillors,
        "residents": residents,
        "res_names": res_names,
        "ruined": bool(status.get("isRuined")),
    }


def sweep(names):
    """Fetch details for all names in paced batches. Returns {uuid: record}."""
    out = {}
    for i in range(0, len(names), BATCH):
        chunk = names[i:i + BATCH]
        d = _req(TOWNS, {"query": chunk})
        if d:
            for t in d:
                rec = parse_town(t)
                if rec and rec["mayor_uuid"]:
                    out[t["uuid"]] = rec
        time.sleep(PACE_S)
    return out


def player_features(names):
    """{name: {lastOnline, joinedTownAt, registered}} for the given player names."""
    feats = {}
    for i in range(0, len(names), BATCH):
        chunk = [n for n in names[i:i + BATCH] if n]
        if not chunk:
            continue
        d = _req(PLAYERS, {"query": chunk})
        for p in (d or []):
            if isinstance(p, dict) and p.get("name"):
                ts = p.get("timestamps") or {}
                feats[p["name"]] = {
                    "lastOnline": ts.get("lastOnline"),
                    "joinedTownAt": ts.get("joinedTownAt"),
                    "registered": ts.get("registered"),
                }
        time.sleep(PACE_S)
    return feats


def build_event(town_uuid, prev, cur, now_iso):
    """Full event record for a mayor change, with resident activity features."""
    prev_res_names = [prev["res_names"].get(u) for u in prev["residents"]]
    prev_res_names = [n for n in prev_res_names if n]
    # feature snapshot for all prior residents + both mayors
    lookup = list({*prev_res_names, prev.get("mayor_name"), cur.get("mayor_name")} - {None})
    feats = player_features(lookup)
    residents = []
    for u in prev["residents"]:
        nm = prev["res_names"].get(u)
        f = feats.get(nm, {})
        residents.append({"uuid": u, "name": nm,
                          "lastOnline": f.get("lastOnline"),
                          "joinedTownAt": f.get("joinedTownAt"),
                          "registered": f.get("registered")})
    return {
        "detected_at": now_iso,
        "town_uuid": town_uuid,
        "town": cur.get("name") or prev.get("name"),
        "old_mayor": {"uuid": prev["mayor_uuid"], "name": prev.get("mayor_name"),
                      "lastOnline": feats.get(prev.get("mayor_name"), {}).get("lastOnline")},
        "new_mayor": {"uuid": cur["mayor_uuid"], "name": cur.get("mayor_name"),
                      "lastOnline": feats.get(cur.get("mayor_name"), {}).get("lastOnline")},
        "new_mayor_was_resident": cur["mayor_uuid"] in prev["residents"],
        "new_mayor_was_councillor": cur["mayor_uuid"] in prev["councillors"],
        "had_councillors": len(prev["councillors"]) > 0,
        "num_councillors": len(prev["councillors"]),
        "town_ruined_now": cur["ruined"],
        "prev_num_residents": len(prev["residents"]),
        "residents": residents,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="only first N towns (testing)")
    ap.add_argument("--watchlist", default="", help="focus on towns in this "
                    "watch_towns.json (from town_candidates.py) instead of all towns")
    ap.add_argument("--state", default=STATE)
    ap.add_argument("--events", default=EVENTS)
    args = ap.parse_args(argv)

    os.makedirs("data", exist_ok=True)
    prev = {}
    if os.path.exists(args.state):
        try:
            prev = json.load(open(args.state))
        except (json.JSONDecodeError, OSError):
            prev = {}

    if args.watchlist and os.path.exists(args.watchlist):
        wl = json.load(open(args.watchlist))
        names = [t["name"] for t in wl.get("towns", []) if t.get("name")]
        print(f"Focusing on {len(names)} at-risk towns from {args.watchlist}.")
    else:
        names = all_town_names()
    if not names:
        print("No towns to sweep (rate-limited or empty watchlist). Aborting.")
        return 1
    if args.limit:
        names = names[:args.limit]
    print(f"[{_now_iso()}] sweeping {len(names)} towns (batch {BATCH}, pace {PACE_S}s)...")
    cur = sweep(names)
    print(f"fetched {len(cur)} town records; previous state has {len(prev)} towns.")

    # Detect mayor-change events only for towns present in BOTH prev and this sweep.
    events = []
    for uuid, c in cur.items():
        p = prev.get(uuid)
        if not p or not p.get("mayor_uuid"):
            continue
        if p["mayor_uuid"] != c["mayor_uuid"] and not c["ruined"]:
            events.append(build_event(uuid, p, c, _now_iso()))

    # Merge: carry forward towns we didn't fetch this run (partial-sweep safe).
    merged = dict(prev)
    merged.update(cur)
    json.dump(merged, open(args.state, "w"))

    if events:
        with open(args.events, "a") as fh:
            for e in events:
                fh.write(json.dumps(e) + "\n")
        falls = [e for e in events if e["new_mayor_was_resident"] and not e["new_mayor_was_councillor"]]
        print(f"*** {len(events)} mayor change(s); {len(falls)} look like most-active-resident falls ***")
        for e in events:
            kind = ("councillor-inherit" if e["new_mayor_was_councillor"]
                    else "most-active?" if e["new_mayor_was_resident"] else "external/handover")
            print(f"    {e['town']}: {e['old_mayor']['name']} -> {e['new_mayor']['name']} [{kind}]")
    else:
        print("no mayor changes this sweep." if prev else "first sweep — baseline recorded, no diffs yet.")

    json.dump({"generated_at": _now_iso(), "towns_in_state": len(merged),
               "towns_fetched_this_run": len(cur), "events_this_run": len(events),
               "total_towns_available": len(names)}, open(META, "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

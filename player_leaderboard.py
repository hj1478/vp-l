#!/usr/bin/env python3
"""Rank tracked players by how long they were online between two times.

Answers "who's been online the longest between A and B" from data/players.jsonl.
Reconstructs each player's sessions (same logic as player_activity.py), clips
them to the requested [--from, --to] window, sums the online time, and prints a
ranked leaderboard.

Time arguments accept either an absolute UTC timestamp
(YYYY-MM-DD, YYYY-MM-DDTHH:MM, or ...Z) or a relative age like 24h / 7d / 90m.
Defaults: --to = now (latest data), --from = 7 days before --to.

Examples:
  python3 player_leaderboard.py                         # last 7 days
  python3 player_leaderboard.py --from 24h              # last 24 hours
  python3 player_leaderboard.py --from 2026-08-01 --to 2026-08-08
  python3 player_leaderboard.py --from 2026-08-05T18:00 --to 2026-08-05T23:00
"""
import argparse
import calendar
import json
import re
import sys
from datetime import datetime, timezone, timedelta

from player_activity import load, sessions_for


def parse_when(s, ref):
    """Absolute UTC timestamp or relative age (e.g. '24h','7d','90m') → epoch."""
    if s is None:
        return None
    s = s.strip()
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([mhdw])", s)
    if m:
        n, unit = float(m.group(1)), m.group(2)
        mult = {"m": 60, "h": 3600, "d": 86400, "w": 604800}[unit]
        return ref - n * mult
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M",
                "%Y-%m-%dT%H", "%Y-%m-%d"):
        try:
            return calendar.timegm(datetime.strptime(s.rstrip("Z"), fmt.rstrip("Z")).timetuple())
        except ValueError:
            continue
    raise SystemExit(f"Could not parse time '{s}'. Use YYYY-MM-DD[THH:MM] or 24h/7d.")


def overlap_seconds(sessions, lo, hi):
    """Total online seconds within [lo, hi], clipping each session to the window."""
    total = 0.0
    for s, e, _ in sessions:
        a, b = max(s, lo), min(e, hi)
        if b > a:
            total += b - a
    return total


def fmt_dur(sec):
    sec = int(sec)
    h, m = sec // 3600, (sec % 3600) // 60
    return f"{h}h {m:02d}m" if h else f"{m}m"


def fmt_ts(epoch):
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/players.jsonl")
    ap.add_argument("--from", dest="frm", default=None, help="window start (abs or age)")
    ap.add_argument("--to", dest="to", default=None, help="window end (abs or age)")
    ap.add_argument("--top", type=int, default=0, help="show only the top N (0 = all)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args(argv)

    rows = load(args.input)
    if not rows:
        print("No player data yet (data/players.jsonl is empty).")
        return 0
    data_now = max(calendar.timegm(datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                                   .timetuple()) for r in rows)

    hi = parse_when(args.to, data_now) if args.to else data_now
    lo = parse_when(args.frm, hi) if args.frm else hi - 7 * 86400
    if lo >= hi:
        raise SystemExit("--from must be before --to.")

    by = {}
    for r in rows:
        by.setdefault(r["name"], []).append(r)

    board = []
    for name, recs in by.items():
        recs.sort(key=lambda r: r["timestamp"])
        sess = sessions_for(recs, data_now)
        online = overlap_seconds(sess, lo, hi)
        # count sessions that touched the window
        nsess = sum(1 for s, e, _ in sess if min(e, hi) > max(s, lo))
        board.append({"name": name, "online_seconds": round(online),
                      "online_human": fmt_dur(online), "sessions_in_window": nsess})
    board.sort(key=lambda x: x["online_seconds"], reverse=True)
    if args.top > 0:
        board = board[:args.top]

    if args.json:
        json.dump({"from": fmt_ts(lo) + "Z", "to": fmt_ts(hi) + "Z", "leaderboard": board},
                  sys.stdout, indent=2)
        print()
        return 0

    span = fmt_dur(hi - lo)
    print(f"Online time  {fmt_ts(lo)}Z  →  {fmt_ts(hi)}Z   (window: {span})")
    print("─" * 56)
    if not any(b["online_seconds"] for b in board):
        print("No tracked player was online in this window.")
        return 0
    for i, b in enumerate(board, 1):
        if b["online_seconds"] == 0:
            continue
        print(f"{i:2d}. {b['name']:18s} {b['online_human']:>9s}   "
              f"({b['sessions_in_window']} session{'s' if b['sessions_in_window'] != 1 else ''})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Track specific EarthMC players' online activity.

Polls the EarthMC v4 API (POST /v4/players) for a configured list of players and
appends each poll's online status to data/players.jsonl, so sessions (login →
logout) and playtime can be reconstructed later by player_activity.py.

The API exposes `status.isOnline` and `timestamps.lastOnline` per player (but NOT
live coordinates), so we can track *when* a player is online, not where they are.
`lastOnline` lets us pin the logout time precisely even if we miss the exact
poll, so sessions survive gaps between polling windows.

WHO to track: list names (one per line, # for comments) in players.txt, or pass
--players a,b,c. With no names the tracker no-ops cleanly.

Usage:
  python3 player_tracker.py --once
  python3 player_tracker.py --duration 3300 -i 300
"""
import argparse
import json
import os
import signal
import time
import urllib.request
import urllib.error

API = "https://api.earthmc.net/v4/players"
_running = True


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load_names(players_arg, players_file):
    if players_arg:
        return [n.strip() for n in players_arg.split(",") if n.strip()]
    if players_file and os.path.exists(players_file):
        out = []
        for line in open(players_file, encoding="utf-8"):
            line = line.split("#", 1)[0].strip()
            if line:
                out.append(line)
        return out
    return []


def query_players(names, timeout=30):
    """POST the name list, return {lowercased name: detail dict}. The API match is
    case-sensitive, so we key by lowercase and callers look up the same way —
    players.txt spelling case then doesn't matter. Raises on network error."""
    body = json.dumps({"query": names}).encode("utf-8")
    req = urllib.request.Request(
        API, data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "player-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return {d.get("name", "").lower(): d for d in data
            if isinstance(d, dict) and d.get("name")}


def snapshot(detail):
    st = detail.get("status", {}) or {}
    ts = detail.get("timestamps", {}) or {}
    town = (detail.get("town", {}) or {}).get("name")
    nation = (detail.get("nation", {}) or {}).get("name")
    return {
        "online": bool(st.get("isOnline")),
        "last_online": ts.get("lastOnline"),
        "town": town,
        "nation": nation,
    }


def log_line(logfile, text):
    line = f"[{_now()}] {text}"
    if logfile:
        with open(logfile, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    print(line, flush=True)


def poll_once(names, jsonfile, logfile, prev):
    """One poll of all tracked players. Logs login/logout transitions, appends a
    JSONL record per player, returns the new prev-state dict."""
    try:
        found = query_players(names)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        log_line(logfile, f"ERROR querying players: {exc!r}")
        return prev
    ts = _now()
    for name in names:
        d = found.get(name.lower())
        if d is None:
            log_line(logfile, f"WARN player not found: {name}")
            continue
        name = d.get("name", name)   # record the API's canonical spelling
        snap = snapshot(d)
        was = prev.get(name)
        if was is not None and was != snap["online"]:
            log_line(logfile, f"*** {name} {'LOGGED IN' if snap['online'] else 'LOGGED OUT'} ***")
        prev[name] = snap["online"]
        rec = {"timestamp": ts, "name": name, **snap}
        if jsonfile:
            with open(jsonfile, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec) + "\n")
    return prev


def _handle(signum, frame):
    global _running
    _running = False


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", default="", help="comma-separated names (overrides file)")
    ap.add_argument("--players-file", default="players.txt")
    ap.add_argument("-i", "--interval", type=float, default=300.0)
    ap.add_argument("--duration", type=float, default=None, help="stop after N seconds")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--json", dest="jsonfile", default="data/players.jsonl")
    ap.add_argument("--log", dest="logfile", default="data/players.log")
    args = ap.parse_args(argv)

    names = load_names(args.players, args.players_file)
    if not names:
        print("No players configured — add names to players.txt (one per line) "
              "or pass --players a,b,c. Nothing to do.")
        return 0

    if args.jsonfile:
        os.makedirs(os.path.dirname(args.jsonfile) or ".", exist_ok=True)
    signal.signal(signal.SIGINT, _handle)
    signal.signal(signal.SIGTERM, _handle)

    log_line(args.logfile, f"=== player tracker started: {', '.join(names)} ===")
    prev = {}
    if args.once:
        poll_once(names, args.jsonfile, args.logfile, prev)
        return 0

    deadline = None if args.duration is None else time.monotonic() + args.duration
    while _running:
        try:
            prev = poll_once(names, args.jsonfile, args.logfile, prev)
        except Exception as exc:  # never let one poll kill the run
            log_line(args.logfile, f"UNEXPECTED ERROR (continuing): {exc!r}")
        if deadline is not None and time.monotonic() >= deadline:
            break
        wait = args.interval
        if deadline is not None:
            wait = min(wait, max(0, deadline - time.monotonic()))
        end = time.monotonic() + wait
        while _running and time.monotonic() < end:
            time.sleep(min(1.0, end - time.monotonic()))
    log_line(args.logfile, "=== player tracker stopped ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""EarthMC vote party tracker.

Polls the EarthMC server endpoint on an interval and logs the vote party
progress (plus a snapshot of server stats) to a file. Detects when a vote
party fires and records it as a distinct event.

Usage:
    python3 voteparty_tracker.py                 # poll every 60s, log to voteparty.log
    python3 voteparty_tracker.py -i 30           # poll every 30 seconds
    python3 voteparty_tracker.py -f party.log    # custom log file
    python3 voteparty_tracker.py --once          # single poll then exit
    python3 voteparty_tracker.py --json          # also write machine-readable JSONL

No third-party dependencies — standard library only.
"""

import argparse
import json
import signal
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

DEFAULT_URL = "https://api.earthmc.net/v4/"
DEFAULT_LOGFILE = "voteparty.log"
DEFAULT_INTERVAL = 60

_running = True


def _now() -> str:
    """UTC timestamp, e.g. 2026-07-17T06:30:00Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url: str, timeout: int = 15) -> dict:
    """Fetch and parse the JSON payload from the server endpoint."""
    req = urllib.request.Request(url, headers={"User-Agent": "voteparty-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract(payload: dict) -> dict:
    """Pull the fields we care about, tolerating missing keys."""
    vp = payload.get("voteParty", {}) or {}
    stats = payload.get("stats", {}) or {}
    target = vp.get("target")
    remaining = vp.get("numRemaining")
    collected = None
    percent = None
    if isinstance(target, int) and isinstance(remaining, int):
        collected = target - remaining
        if target > 0:
            percent = round(collected / target * 100, 1)
    return {
        "target": target,
        "remaining": remaining,
        "collected": collected,
        "percent": percent,
        "players_online": stats.get("numOnlinePlayers"),
        "max_players": stats.get("maxPlayers"),
        "moon_phase": payload.get("moonPhase"),
        "num_towns": stats.get("numTowns"),
        "num_nations": stats.get("numNations"),
        "num_residents": stats.get("numResidents"),
    }


def log_line(logfile: str, text: str) -> None:
    """Append a line to the log file and echo it to stdout."""
    line = f"[{_now()}] {text}"
    with open(logfile, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def log_json(jsonfile: str, record: dict) -> None:
    """Append one JSON object per line (JSONL)."""
    with open(jsonfile, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def format_snapshot(d: dict) -> str:
    if d["target"] is None or d["remaining"] is None:
        return "voteParty data unavailable in response"
    return (
        f"vote party {d['collected']}/{d['target']} "
        f"({d['percent']}%) | {d['remaining']} remaining | "
        f"players {d['players_online']}/{d['max_players']} | moon {d['moon_phase']}"
    )


def poll_once(url: str, logfile: str, jsonfile: str | None, prev: dict | None) -> dict | None:
    """Perform a single poll, log it, and return the extracted snapshot."""
    try:
        payload = fetch(url)
    except urllib.error.URLError as exc:
        log_line(logfile, f"ERROR fetching endpoint: {exc}")
        return prev
    except (json.JSONDecodeError, ValueError) as exc:
        log_line(logfile, f"ERROR parsing response: {exc}")
        return prev

    snap = extract(payload)

    # Detect a vote party firing: remaining jumps back up toward the target
    # (i.e. the counter reset after a party) compared to the previous poll.
    if prev and prev["remaining"] is not None and snap["remaining"] is not None:
        if snap["remaining"] > prev["remaining"] + 1:
            gained = snap["remaining"] - prev["remaining"]
            log_line(
                logfile,
                f"*** VOTE PARTY FIRED! remaining reset {prev['remaining']} -> "
                f"{snap['remaining']} (+{gained}) ***",
            )

    log_line(logfile, format_snapshot(snap))

    if jsonfile:
        record = {"timestamp": _now(), **snap}
        log_json(jsonfile, record)

    return snap


def _handle_signal(signum, frame):
    global _running
    _running = False


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Track EarthMC vote party progress.")
    parser.add_argument("-u", "--url", default=DEFAULT_URL, help="server endpoint URL")
    parser.add_argument("-f", "--logfile", default=DEFAULT_LOGFILE, help="log file path")
    parser.add_argument(
        "-i", "--interval", type=int, default=DEFAULT_INTERVAL,
        help="seconds between polls (default 60)",
    )
    parser.add_argument("--once", action="store_true", help="poll once then exit")
    parser.add_argument(
        "--json", dest="jsonfile", nargs="?", const="voteparty.jsonl", default=None,
        help="also append machine-readable JSONL (default voteparty.jsonl)",
    )
    args = parser.parse_args(argv)

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    log_line(args.logfile, f"=== tracker started (interval={args.interval}s, url={args.url}) ===")

    prev = None
    if args.once:
        poll_once(args.url, args.logfile, args.jsonfile, prev)
        return 0

    while _running:
        prev = poll_once(args.url, args.logfile, args.jsonfile, prev)
        # Sleep in short slices so Ctrl+C is responsive.
        slept = 0
        while _running and slept < args.interval:
            time.sleep(min(1, args.interval - slept))
            slept += 1

    log_line(args.logfile, "=== tracker stopped ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

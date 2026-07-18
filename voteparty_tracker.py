#!/usr/bin/env python3
"""EarthMC vote party tracker.

Polls the EarthMC server endpoint and logs the vote party progress (plus a
snapshot of server stats) to a file. Detects when a vote party fires and
records it as a distinct event.

The poll interval is *adaptive*: it starts fast and, when the API rate-limits
us (HTTP 429), backs off — honouring the ``Retry-After`` header when present —
then gradually speeds back up once requests succeed again (AIMD control).

Usage:
    python3 voteparty_tracker.py                 # adaptive, base 60s
    python3 voteparty_tracker.py -i 30           # base 30s
    python3 voteparty_tracker.py --max-interval 1800
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
DEFAULT_BASE_INTERVAL = 60      # fastest poll spacing, seconds (1 minute)
DEFAULT_MAX_INTERVAL = 3600     # slowest poll spacing under heavy throttling (1 hour)

_running = True


def _now() -> str:
    """UTC timestamp, e.g. 2026-07-17T06:30:00Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RateLimited(Exception):
    """Raised when the API responds 429. Carries the server's retry hint."""

    def __init__(self, retry_after: float | None):
        super().__init__("rate limited (HTTP 429)")
        self.retry_after = retry_after


def _parse_retry_after(value: str | None) -> float | None:
    """Parse a Retry-After header (delta-seconds form) into seconds."""
    if not value:
        return None
    try:
        return max(0.0, float(value.strip()))
    except (TypeError, ValueError):
        return None  # HTTP-date form is not handled; fall back to backoff


def fetch(url: str, timeout: int = 15) -> dict:
    """Fetch and parse the JSON payload, raising RateLimited on HTTP 429."""
    req = urllib.request.Request(url, headers={"User-Agent": "voteparty-tracker/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            retry_after = _parse_retry_after(exc.headers.get("Retry-After"))
            raise RateLimited(retry_after) from exc
        raise


class AdaptiveInterval:
    """AIMD controller for the poll interval.

    Multiplicative increase on rate limiting, gentle decrease on success, so
    the tracker collects as fast as the API tolerates without hammering it.
    """

    def __init__(self, base: float, maximum: float):
        self.base = base
        self.maximum = maximum
        self.current = base

    def on_success(self) -> None:
        # Ease back toward the base interval (additive-ish decrease).
        self.current = max(self.base, self.current * 0.7)

    def on_rate_limit(self, retry_after: float | None) -> float:
        """Back off. Returns how long to actually wait before the next poll."""
        self.current = min(self.maximum, max(self.current * 2, self.base * 2))
        # Wait at least the server's hint, but never below the new interval.
        wait = self.current if retry_after is None else max(retry_after, self.current)
        return min(wait, self.maximum)

    def on_error(self) -> None:
        # Transient network/parse error: back off mildly.
        self.current = min(self.maximum, self.current * 1.5)


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


def format_snapshot(d: dict, interval: float) -> str:
    if d["target"] is None or d["remaining"] is None:
        return "voteParty data unavailable in response"
    return (
        f"vote party {d['collected']}/{d['target']} "
        f"({d['percent']}%) | {d['remaining']} remaining | "
        f"players {d['players_online']}/{d['max_players']} | moon {d['moon_phase']} "
        f"| next poll ~{round(interval)}s"
    )


def poll_once(url, logfile, jsonfile, prev, interval: "AdaptiveInterval | None"):
    """Perform a single poll, log it, and return the extracted snapshot.

    ``interval`` may be None for a one-shot poll (no adaptive state to update).
    On rate limiting the wait hint is applied by the caller / returned state.
    Returns (snapshot_or_prev, wait_override_seconds_or_None).
    """
    try:
        payload = fetch(url)
    except RateLimited as exc:
        wait = interval.on_rate_limit(exc.retry_after) if interval else exc.retry_after
        hint = f" (Retry-After={exc.retry_after}s)" if exc.retry_after is not None else ""
        log_line(logfile, f"RATE LIMITED (429){hint} — backing off to ~{round(wait or 0)}s")
        return prev, wait
    except urllib.error.URLError as exc:
        if interval:
            interval.on_error()
        log_line(logfile, f"ERROR fetching endpoint: {exc}")
        return prev, None
    except (json.JSONDecodeError, ValueError) as exc:
        if interval:
            interval.on_error()
        log_line(logfile, f"ERROR parsing response: {exc}")
        return prev, None

    if interval:
        interval.on_success()
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

    log_line(logfile, format_snapshot(snap, interval.current if interval else 0))

    if jsonfile:
        record = {"timestamp": _now(), "interval": round(interval.current, 1) if interval else None, **snap}
        log_json(jsonfile, record)

    return snap, None


def _handle_signal(signum, frame):
    global _running
    _running = False


def _sleep_responsive(seconds: float) -> None:
    """Sleep in 1s slices so signals interrupt promptly."""
    slept = 0.0
    while _running and slept < seconds:
        step = min(1.0, seconds - slept)
        time.sleep(step)
        slept += step


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Track EarthMC vote party progress (adaptive interval).")
    parser.add_argument("-u", "--url", default=DEFAULT_URL, help="server endpoint URL")
    parser.add_argument("-f", "--logfile", default=DEFAULT_LOGFILE, help="log file path")
    parser.add_argument(
        "-i", "--interval", type=float, default=DEFAULT_BASE_INTERVAL,
        help="base (fastest) seconds between polls (default 60)",
    )
    parser.add_argument(
        "--max-interval", type=float, default=DEFAULT_MAX_INTERVAL,
        help="maximum seconds between polls under throttling (default 3600 = 1 hr)",
    )
    parser.add_argument("--once", action="store_true", help="poll once then exit")
    parser.add_argument(
        "--duration", type=float, default=None,
        help="stop cleanly after this many seconds (default: run until interrupted)",
    )
    parser.add_argument(
        "--json", dest="jsonfile", nargs="?", const="voteparty.jsonl", default=None,
        help="also append machine-readable JSONL (default voteparty.jsonl)",
    )
    args = parser.parse_args(argv)

    if args.max_interval < args.interval:
        args.max_interval = args.interval

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    if args.once:
        log_line(args.logfile, f"=== single poll (url={args.url}) ===")
        poll_once(args.url, args.logfile, args.jsonfile, None, None)
        return 0

    interval = AdaptiveInterval(args.interval, args.max_interval)
    log_line(
        args.logfile,
        f"=== tracker started (adaptive {args.interval}s..{args.max_interval}s, url={args.url}) ===",
    )

    deadline = None if args.duration is None else time.monotonic() + args.duration

    prev = None
    while _running:
        prev, wait_override = poll_once(args.url, args.logfile, args.jsonfile, prev, interval)
        if deadline is not None and time.monotonic() >= deadline:
            break
        wait = wait_override if wait_override is not None else interval.current
        # Don't sleep past the deadline.
        if deadline is not None:
            wait = min(wait, max(0, deadline - time.monotonic()))
        _sleep_responsive(wait)

    reason = "duration reached" if (deadline is not None and _running) else "stopped"
    log_line(args.logfile, f"=== tracker {reason} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

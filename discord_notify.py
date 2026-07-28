#!/usr/bin/env python3
"""Post the current vote-party firing prediction to a Discord webhook.

Fetches the live vote count from the EarthMC API, runs the reported model
(`shape_analogue`, plain-analogue fallback) using the committed cycle history as
the library, and posts a Discord embed with the median firing time and its 80% /
90% margins. Designed to be run hourly from GitHub Actions.

The webhook URL is read from the DISCORD_WEBHOOK_URL environment variable (set it
as a repository secret) or passed with --webhook. Nothing is posted if it is
unset, so local/dry runs are safe.

Usage:
  python3 discord_notify.py                 # post (needs DISCORD_WEBHOOK_URL)
  python3 discord_notify.py --dry-run       # print the payload, don't post
  python3 discord_notify.py --webhook URL   # override the env var
"""
import argparse
import json
import os
import time
import urllib.request
import urllib.error

from predict import (load_points, split_cycles, shape_analogue_quantiles,
                     analogue_quantiles, fmt_ts, fmt_ts_rounded,
                     display_granularity_min)

API_URL = "https://api.earthmc.net/v4/"
DATA = "data/voteparty.jsonl"


def fetch_live():
    """Return (collected, target, remaining, players) from the live API."""
    req = urllib.request.Request(API_URL, headers={"User-Agent": "vp-tracker"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    vp = d["voteParty"]
    target = int(vp["target"])
    remaining = int(vp["numRemaining"])
    players = d.get("stats", {}).get("numOnlinePlayers")
    return target - remaining, target, remaining, players


def _fmt_delta(seconds):
    """Signed h/m offset from now, e.g. '+11h42m' or '-15m'."""
    sign = "+" if seconds >= 0 else "-"
    s = abs(int(seconds))
    h, m = s // 3600, (s % 3600) // 60
    return f"{sign}{h}h{m:02d}m" if h else f"{sign}{m}m"


def build_payload(now=None):
    """Compute the prediction and return a Discord webhook JSON payload (or None
    if there isn't enough history to predict)."""
    now = now if now is not None else time.time()
    pts = load_points(DATA)
    cycles = split_cycles(pts)
    try:
        collected, target, remaining, players = fetch_live()
    except Exception:
        # fall back to the last committed point if the API is unreachable
        last = pts[-1]
        collected, target = float(last["collected"]), float(last["target"])
        remaining, players = int(target - collected), last.get("players_online")

    lib = list(range(len(cycles) - 1))
    q = shape_analogue_quantiles(cycles, lib, target, now, float(collected),
                                 [0.05, 0.1, 0.5, 0.9, 0.95])
    model = "shape_analogue"
    if q is None:
        q = analogue_quantiles(cycles, lib, target, now, float(collected),
                               [0.05, 0.1, 0.5, 0.9, 0.95])
        model = "analogue"
    if q is None:
        return None

    p05, p10, p50, p90, p95 = (float(x) for x in q)
    gran = display_granularity_min((p90 - p10) / 120)
    pct = round(100 * collected / target, 1)

    med_line = f"**{fmt_ts_rounded(p50, gran)}**  ({fmt_ts(p50)})"
    w80 = (f"{fmt_ts(p10)} → {fmt_ts(p90)}\n"
           f"`{_fmt_delta(p10 - now)} … {_fmt_delta(p90 - now)}` from now "
           f"(median {_fmt_delta(p10 - p50)} / {_fmt_delta(p90 - p50)})")
    w90 = (f"{fmt_ts(p05)} → {fmt_ts(p95)}\n"
           f"`{_fmt_delta(p05 - now)} … {_fmt_delta(p95 - now)}` from now")

    color = 0xE74C3C if pct >= 90 else 0x3498DB   # red in the endgame, else blue
    embed = {
        "title": "🗳️ EarthMC Vote Party — firing prediction",
        "color": color,
        "fields": [
            {"name": "Progress", "value": f"{int(collected)} / {int(target)}  "
             f"(**{pct}%**){'' if players is None else f' · {players} online'}",
             "inline": False},
            {"name": "Median firing (ETA)", "value": med_line, "inline": False},
            {"name": "80% window", "value": w80, "inline": False},
            {"name": "90% window", "value": w90, "inline": False},
        ],
        "footer": {"text": f"model: {model} · {len(lib)} library cycles · "
                           "times UTC · updates hourly"},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
    }
    return {"embeds": [embed]}


def post(payload, webhook):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook, data=data, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "vp-tracker"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--webhook", default=os.environ.get("DISCORD_WEBHOOK_URL", ""))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    payload = build_payload()
    if payload is None:
        print("Not enough history to predict — nothing posted.")
        return 0

    if args.dry_run or not args.webhook:
        if not args.webhook and not args.dry_run:
            print("DISCORD_WEBHOOK_URL not set — printing payload instead of posting:")
        print(json.dumps(payload, indent=2))
        return 0

    for attempt in range(4):
        try:
            status = post(payload, args.webhook)
            print(f"Posted to Discord (HTTP {status}).")
            return 0
        except urllib.error.HTTPError as e:
            print(f"Discord HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:200]}")
            if e.code == 429:            # rate limited — back off and retry
                time.sleep(2 ** attempt * 2)
                continue
            return 1
        except Exception as e:
            print(f"Post failed ({e}); retry {attempt + 1}/4")
            time.sleep(2 ** attempt * 2)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

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
                     analogue_quantiles, fmt_ts)

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


def _fmt_dur(seconds):
    """Unsigned h/m duration, e.g. '1h42m' or '15m'."""
    s = abs(int(seconds))
    h, m = s // 3600, (s % 3600) // 60
    return f"{h}h{m:02d}m" if h else f"{m}m"


def dts(epoch, style="f"):
    """Discord dynamic timestamp. Discord renders it in EACH viewer's own local
    timezone automatically — 'F' full date+time, 'f' short, 't' time, 'R'
    relative ('in 11 hours')."""
    return f"<t:{int(epoch)}:{style}>"


def build_payload(now=None):
    """Compute the prediction and return a Discord webhook JSON payload (or None
    if there isn't enough history to predict)."""
    now = now if now is not None else time.time()
    pts = load_points(DATA)
    if not pts:
        return None
    cycles = split_cycles(pts)
    stale_note = None
    try:
        collected, target, remaining, players = fetch_live()
    except Exception:
        # Live API unreachable — fall back to the last committed point, but anchor
        # the prediction clock to THAT point's timestamp (not the current wall
        # clock) so hour-old progress isn't treated as current, and flag it.
        last = pts[-1]
        collected, target = float(last["collected"]), float(last["target"])
        remaining, players = int(target - collected), last.get("players_online")
        now = float(last["_t"])
        age_min = round((time.time() - now) / 60)
        stale_note = (f"⚠️ live API unavailable — using committed data from "
                      f"{fmt_ts(now)} ({age_min} min ago)")

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
    pct = 100 * collected / target
    margin80 = _fmt_dur((p90 - p10) / 2)              # symmetric ± of the 80% window
    players_txt = "" if players is None else f" · {int(players)} online"

    # Compact single-block layout. Every time is a Discord dynamic timestamp, so
    # it renders in each reader's own timezone (:f short date+time, :R relative,
    # :t time-only). Backticked lines stay literal — no timestamps inside them.
    bar_n = 18
    filled = max(0, min(bar_n, round(pct / 100 * bar_n)))
    bar = "█" * filled + "░" * (bar_n - filled)
    desc = (
        f"🗳️ **Vote party** — fires {dts(p50, 'f')}  ({dts(p50, 'R')})\n"
        f"`{bar}`  {pct:.1f}%\n"
        f"**Window** {dts(p10, 't')} → {dts(p90, 't')} · **±{margin80}** (80%)\n"
        f"`{int(collected):,} / {int(target):,}{players_txt} · {model}`"
    )
    if stale_note:
        desc = f"{stale_note}\n{desc}"

    color = (0xF1C40F if stale_note else            # amber when running on stale data
             0xE74C3C if pct >= 90 else 0x3498DB)    # red in the endgame, else blue
    embed = {
        "description": desc,
        "color": color,
        "footer": {"text": "times shown in your local timezone"},
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

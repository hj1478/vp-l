#!/usr/bin/env python3
"""Post the town snipe list to Discord.

Reads data/snipe_list.json (produced by town_candidates.py) and posts an embed of
the best targets: towns falling soon with zero active competitors (join & inherit),
ranked by bank gold, plus reclaimable ruined towns. Fall times are shown as
Discord dynamic timestamps so each reader sees their own local "in ~N days".

Webhook from DISCORD_WEBHOOK_URL (or --webhook). --dry-run prints instead of posts.
Usage: python3 discord_snipes.py
"""
import argparse
import json
import os
import time
import urllib.request
import urllib.error

SNIPES = "data/snipe_list.json"


def fmt_rows(rows, now):
    out = []
    for s in rows:
        d2f = s.get("days_to_fall_est")
        when = f"<t:{int(now + d2f*86400)}:R>" if d2f is not None else "reclaim now"
        out.append((s["town"], f"{int(s['balance'])}g", when, f"{s['num_residents']}r"))
    return out


def build_payload(path=SNIPES, now=None):
    now = now if now is not None else time.time()
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    towns = d.get("towns", [])
    soon = sorted([s for s in towns if s.get("status") == "falls_soon"
                   and s.get("active_competitors") == 0],
                  key=lambda s: -s["balance"])[:12]
    ruined = sorted([s for s in towns if s.get("status") == "ruined"],
                    key=lambda s: -s["balance"])[:6]
    if not soon and not ruined:
        return None

    def block(rows):
        lines = []
        for name, gold, when, res in fmt_rows(rows, now):
            lines.append(f"**{name}** — {gold} · {res} · falls {when}")
        return "\n".join(lines)

    parts = []
    if soon:
        parts.append("**⚔️ Join & inherit — falling soon, no competition**\n" + block(soon))
    if ruined:
        parts.append("**💰 Ruined — reclaim now** _(bank may be drained)_\n" + block(ruined))
    embed = {
        "title": "🏴 EarthMC Snipe List",
        "color": 0x2ECC71,
        "description": "\n\n".join(parts)[:4000],
        "footer": {"text": f"scanned {d.get('scanned', '?')} towns · est. falls assume no "
                           "premium · verify in-game"},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
    }
    return {"embeds": [embed]}


def post(payload, webhook):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(webhook, data=data, method="POST",
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "vp-tracker"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--webhook", default=os.environ.get("DISCORD_WEBHOOK_URL", ""))
    ap.add_argument("--input", default=SNIPES)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    payload = build_payload(args.input)
    if payload is None:
        print("No snipe list yet (run town_candidates.py first) — nothing posted.")
        return 0
    if args.dry_run or not args.webhook:
        if not args.webhook and not args.dry_run:
            print("DISCORD_WEBHOOK_URL not set — printing payload instead:")
        print(json.dumps(payload, indent=2))
        return 0
    for attempt in range(4):
        try:
            print(f"Posted snipe list to Discord (HTTP {post(payload, args.webhook)}).")
            return 0
        except urllib.error.HTTPError as e:
            print(f"Discord HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:200]}")
            if e.code == 429:
                time.sleep(2 ** attempt * 2)
                continue
            return 1
        except Exception as e:
            print(f"Post failed ({e}); retry {attempt + 1}/4")
            time.sleep(2 ** attempt * 2)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

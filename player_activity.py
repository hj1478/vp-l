#!/usr/bin/env python3
"""Reconstruct player sessions + playtime from data/players.jsonl and graph them.

A session is a contiguous online stretch. Login is approximated by the first poll
we saw the player online; logout is pinned to the API's `lastOnline` timestamp
(precise even if we missed the exact poll). Online stretches separated by a gap
larger than MAX_GAP_MIN are treated as separate sessions (we missed the logout).

Outputs data/player_activity.png (session timeline + daily playtime) and
data/player_activity.json (per-player summary). Usage:
  python3 player_activity.py [-i data/players.jsonl] [-o data] [--days 7]
"""
import argparse
import calendar
import json
import os
from datetime import datetime, timezone, timedelta

MAX_GAP_MIN = 20.0      # online polls farther apart than this => separate sessions


def parse_ts(s):
    return calendar.timegm(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timetuple())


def load(path):
    rows = []
    if not os.path.exists(path):
        return rows
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def sessions_for(recs, now):
    """recs: chronological list for one player. Returns list of
    (start_epoch, end_epoch, ongoing_bool)."""
    out = []
    start = last_online_poll = None
    for r in recs:
        t = parse_ts(r["timestamp"])
        if r.get("online"):
            if start is None:
                start = t
            elif t - last_online_poll > MAX_GAP_MIN * 60:
                out.append((start, last_online_poll, False))   # missed logout
                start = t
            last_online_poll = t
        else:
            if start is not None:
                lo = r.get("last_online")
                lo = lo / 1000.0 if lo else None
                end = lo if (lo and start <= lo <= t + 60) else last_online_poll
                out.append((start, end, False))
                start = None
    if start is not None:
        out.append((start, last_online_poll, True))            # still online
    return out


def summarize(rows, now):
    by = {}
    for r in rows:
        by.setdefault(r["name"], []).append(r)
    players = {}
    for name, recs in by.items():
        recs.sort(key=lambda r: r["timestamp"])
        sess = sessions_for(recs, now)
        total = sum(max(0, e - s) for s, e, _ in sess)
        ongoing = any(o for _, _, o in sess)
        last_rec = recs[-1]
        last_online_ms = last_rec.get("last_online")
        players[name] = {
            "sessions": sess,
            "num_sessions": len(sess),
            "total_playtime_min": round(total / 60, 1),
            "avg_session_min": round(total / 60 / len(sess), 1) if sess else 0.0,
            "currently_online": ongoing,
            "last_seen": (datetime.fromtimestamp(last_online_ms / 1000, tz=timezone.utc)
                          .strftime("%Y-%m-%dT%H:%M:%SZ") if last_online_ms else None),
            "town": last_rec.get("town"),
            "nation": last_rec.get("nation"),
        }
    return players


def daily_playtime(sess, days, now):
    """Minutes played per UTC day for the last `days` days (dict day->min)."""
    start_day = (datetime.fromtimestamp(now, tz=timezone.utc).date() - timedelta(days=days - 1))
    buckets = {}
    for s, e, _ in sess:
        a = s
        while a < e:
            d = datetime.fromtimestamp(a, tz=timezone.utc).date()
            day_end = calendar.timegm((datetime.combine(d, datetime.min.time())
                                       + timedelta(days=1)).timetuple())
            seg_end = min(e, day_end)
            if d >= start_day:
                buckets[d] = buckets.get(d, 0) + (seg_end - a) / 60.0
            a = seg_end
    return buckets


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/players.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--no-graph", action="store_true")
    args = ap.parse_args(argv)

    rows = load(args.input)
    if not rows:
        print("No player data yet (data/players.jsonl empty). Add names to "
              "players.txt and let the tracker run.")
        return 0
    now = parse_ts(max(r["timestamp"] for r in rows))
    players = summarize(rows, now)

    os.makedirs(args.outdir, exist_ok=True)
    out = {"generated_at": datetime.fromtimestamp(now, tz=timezone.utc)
           .strftime("%Y-%m-%dT%H:%M:%SZ"),
           "window_days": args.days,
           "players": {n: {k: v for k, v in p.items() if k != "sessions"}
                       for n, p in players.items()}}
    with open(os.path.join(args.outdir, "player_activity.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    for n, p in sorted(players.items()):
        state = "🟢 ONLINE" if p["currently_online"] else "offline"
        print(f"{n:16s} {state:10s} | {p['num_sessions']:3d} sessions | "
              f"{p['total_playtime_min']:7.0f} min total | avg {p['avg_session_min']:.0f} min "
              f"| last seen {p['last_seen']}")

    if not args.no_graph:
        make_graph(players, args.days, now, os.path.join(args.outdir, "player_activity.png"))
    return 0


def make_graph(players, days, now, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    names = sorted(players)
    if not names:
        return
    cmap = plt.cm.tab10(range(len(names)))
    color = {n: cmap[i % 10] for i, n in enumerate(names)}
    t_min = now - days * 86400

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 2.4 + 1.1 * len(names)),
                                   gridspec_kw={"height_ratios": [1.4, 1]})

    # Panel 1: session timeline (Gantt)
    for i, n in enumerate(names):
        bars = []
        for s, e, ongoing in players[n]["sessions"]:
            s2 = max(s, t_min)
            if e <= t_min:
                continue
            bars.append((mdates.date2num(datetime.fromtimestamp(s2, tz=timezone.utc)),
                         (e - s2) / 86400.0))
        ax1.broken_barh(bars, (i - 0.4, 0.8), facecolors=color[n],
                        edgecolor="black", linewidth=0.4, alpha=0.9)
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels([f"{n} (online)" if players[n]["currently_online"] else n
                         for n in names])
    ax1.set_ylim(-0.6, len(names) - 0.4)
    ax1.set_xlim(mdates.date2num(datetime.fromtimestamp(t_min, tz=timezone.utc)),
                 mdates.date2num(datetime.fromtimestamp(now + 3600, tz=timezone.utc)))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=timezone.utc))
    ax1.set_title(f"Player online sessions — last {days} days (UTC)", fontweight="bold")
    ax1.grid(axis="x", alpha=0.3)
    for lb in ax1.get_xticklabels():
        lb.set_rotation(15)

    # Panel 2: daily playtime (grouped bars)
    day_list = [(datetime.fromtimestamp(now, tz=timezone.utc).date() - timedelta(days=d))
                for d in range(days - 1, -1, -1)]
    w = 0.8 / max(1, len(names))
    for i, n in enumerate(names):
        daily = daily_playtime(players[n]["sessions"], days, now)
        vals = [daily.get(d, 0) / 60.0 for d in day_list]   # hours
        xs = [x + (i - len(names) / 2) * w + w / 2 for x in range(len(day_list))]
        ax2.bar(xs, vals, width=w, color=color[n], label=n, edgecolor="black", linewidth=0.3)
    ax2.set_xticks(range(len(day_list)))
    ax2.set_xticklabels([d.strftime("%m-%d") for d in day_list])
    ax2.set_ylabel("hours online")
    ax2.set_title("Daily playtime", fontweight="bold")
    ax2.legend(fontsize=8, ncol=min(len(names), 5))
    ax2.grid(axis="y", alpha=0.3)

    fig.suptitle("EarthMC player activity", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())

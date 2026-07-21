#!/usr/bin/env python3
"""Graph of all vote-party cycles: the full time series with cycles coloured and
firings marked, plus overlaid fill curves (progress vs hours since cycle start).

Usage: python3 cycles_graph.py [-i data/voteparty.jsonl] [-o data/cycles.png]
"""
import argparse
from datetime import datetime, timezone

import numpy as np

from predict import (load_points, split_cycles, cycle_arrays, cycle_fire_time,
                     label_sigma_min, TIGHT_LABEL_MIN)


def dt(e):
    return datetime.fromtimestamp(e, tz=timezone.utc)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--out", default="data/cycles.png")
    args = ap.parse_args(argv)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    pts = load_points(args.input)
    target = float(pts[-1]["target"])
    cycles = split_cycles(pts)
    ncyc = len(cycles)
    cmap = plt.cm.turbo(np.linspace(0.05, 0.95, ncyc))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9),
                                   gridspec_kw={"height_ratios": [1.5, 1], "hspace": 0.28})

    # --- Panel 1: full time series, coloured per cycle ---
    ax1.axhline(target, color="#333", ls="--", lw=1, label=f"target ({int(target)})")
    for i, (cyc, col) in enumerate(zip(cycles, cmap)):
        xs = [dt(p["_t"]) for p in cyc]
        ys = [p["collected"] for p in cyc]
        completed = i < ncyc - 1
        bracket = label_sigma_min(cycles, i, target)
        tight = bracket is not None and bracket <= TIGHT_LABEL_MIN
        lbl = f"cycle {i+1} ({len(cyc)}pts"
        lbl += ", current)" if not completed else (", tight)" if tight else f", ±{round(bracket)}m)")
        ax1.plot(xs, ys, "-o", color=col, ms=2.5, lw=1.4, label=lbl)
        # mark the firing (last point of a completed cycle)
        if completed:
            fire, _ = cycle_fire_time(cyc, target)
            if fire is not None:
                ax1.scatter([dt(fire)], [target], marker="*",
                            s=140 if tight else 70,
                            color=col, edgecolor="black", linewidth=0.6, zorder=6)
    ax1.set_title(f"All {ncyc} vote-party cycles — collected votes over time "
                  f"(★ = firing; large ★ = tightly-labeled)", fontweight="bold")
    ax1.set_ylabel("votes collected")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=timezone.utc))
    ax1.legend(fontsize=7, ncol=2, loc="upper left")
    ax1.grid(alpha=0.3)
    for lb in ax1.get_xticklabels():
        lb.set_rotation(20)

    # --- Panel 2: overlaid fill curves (progress% vs hours since cycle start) ---
    for i, (cyc, col) in enumerate(zip(cycles, cmap)):
        t, y = cycle_arrays(cyc)
        completed = i < ncyc - 1
        ax2.plot(t / 3600.0, 100 * y / target, "-", color=col,
                 lw=2.2 if not completed else 1.4,
                 alpha=1.0 if not completed else 0.7,
                 label=f"cycle {i+1}" + ("" if completed else " (current)"))
    ax2.axhline(100, color="#333", ls="--", lw=0.8)
    ax2.set_title("Fill curves aligned to cycle start — how each cycle filled",
                  fontweight="bold")
    ax2.set_xlabel("hours since cycle start")
    ax2.set_ylabel("% of target")
    ax2.legend(fontsize=7, ncol=3)
    ax2.grid(alpha=0.3)

    fig.savefig(args.out, dpi=110, bbox_inches="tight")
    plt.close(fig)

    # summary
    print(f"{ncyc} cycles:")
    for i, cyc in enumerate(cycles):
        b = label_sigma_min(cycles, i, target)
        dur = (cyc[-1]["_t"] - cyc[0]["_t"]) / 3600.0
        tag = "current" if i == ncyc - 1 else ("tight" if (b and b <= TIGHT_LABEL_MIN) else f"loose σ±{round(b)}m")
        print(f"  cycle {i+1}: {len(cyc):3d} pts, spans {dur:4.1f}h, last {cyc[-1]['percent']:.0f}%  [{tag}]")


if __name__ == "__main__":
    raise SystemExit(main())

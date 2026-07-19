#!/usr/bin/env python3
"""Replay the predictor over a completed vote-party cycle.

Picks a completed cycle, then steps through it and shows what the model would
have predicted at each stage (using leave-one-cycle-out weights, so it never
sees the cycle it is predicting). Visualises how the projected firing time
converges on the actual one as the cycle fills.

Outputs data/replay.png. Usage:
    python3 replay.py                # densest completed cycle
    python3 replay.py --cycle 2      # 1-indexed completed cycle
    python3 replay.py --stages 25,40,55,70,85,95
"""

import argparse
from datetime import datetime, timezone

import numpy as np

from predict import (
    MODELS, load_points, split_cycles, cycle_arrays, cycle_fire_time,
    make_ctx, backtest_staged, weights_for_progress,
)


def dt(epoch):
    return datetime.fromtimestamp(epoch, tz=timezone.utc)


def stage_prediction(cyc, others, target, up_to):
    """Ensemble + diurnal firing epoch using the first `up_to` points."""
    staged = backtest_staged(others or [cyc], target)
    ctx = make_ctx(cyc, others)
    t, y = cycle_arrays(cyc)
    t0 = cyc[0]["_t"]
    tf, yf = t[:up_to], y[:up_to]
    w = weights_for_progress(staged, float(yf[-1]) / target * 100.0)
    etas, ws = [], []
    diurnal = None
    for n in MODELS:
        tc = MODELS[n](tf, yf, target, ctx)
        if tc is None:
            continue
        if n == "diurnal":
            diurnal = t0 + tc
        etas.append(t0 + tc)
        ws.append(w.get(n, 0.0))
    if not etas:
        return None, None
    ws = np.array(ws)
    ws = ws / ws.sum() if ws.sum() > 0 else np.ones(len(ws)) / len(ws)
    return float(np.sum(np.array(etas) * ws)), diurnal


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--out", default="data/replay.png")
    ap.add_argument("--cycle", type=int, default=None, help="1-indexed completed cycle")
    ap.add_argument("--stages", default="25,40,55,70,85,95")
    args = ap.parse_args(argv)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    points = load_points(args.input)
    target = float(points[-1]["target"])
    completed = split_cycles(points)[:-1]
    if not completed:
        print("No completed cycles yet.")
        return 1

    ci = (args.cycle - 1) if args.cycle else max(range(len(completed)),
                                                 key=lambda k: len(completed[k]))
    cyc = completed[ci]
    others = [c for cj, c in enumerate(completed) if cj != ci]
    fire, _ = cycle_fire_time(cyc, target)
    t, y = cycle_arrays(cyc)
    t0 = cyc[0]["_t"]
    stage_pcts = [float(s) for s in args.stages.split(",")]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(15, 6))

    # --- Panel A: actual curve + a projection ray at each stage ---
    xs = [dt(p["_t"]) for p in cyc]
    axA.plot(xs, [p["collected"] for p in cyc], "-", color="#1f77b4", lw=2,
             label="actual collected", zorder=3)
    axA.axhline(target, color="#333", ls="--", lw=1, label=f"target ({int(target)})")
    axA.axvline(dt(fire), color="green", lw=2.2, label="ACTUAL firing", zorder=2)

    cmap = plt.cm.plasma(np.linspace(0, 0.85, len(stage_pcts)))
    conv = []
    for pct, col in zip(stage_pcts, cmap):
        up_to = int(np.searchsorted(y, target * pct / 100.0)) + 1
        up_to = max(3, min(up_to, len(y)))
        ens, diur = stage_prediction(cyc, others, target, up_to)
        if ens is None:
            continue
        sx, sy = dt(t0 + t[up_to - 1]), y[up_to - 1]
        axA.plot([sx, dt(ens)], [sy, target], "--", color=col, lw=1.6, alpha=0.9)
        axA.scatter([sx], [sy], color=col, s=45, zorder=5)
        axA.scatter([dt(ens)], [target], color=col, s=70, marker="v", zorder=5,
                    label=f"predict @ {pct:.0f}%")
        conv.append((y[up_to - 1] / target * 100.0, ens, diur))

    axA.set_title(f"Replay on completed cycle {ci+1} "
                  f"({len(cyc)} pts) — each ray = model projection at that stage",
                  fontweight="bold", fontsize=11)
    axA.set_ylabel("votes collected")
    axA.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=timezone.utc))
    axA.legend(fontsize=7, loc="upper left")
    axA.grid(alpha=0.3)

    # --- Panel B: convergence of predicted firing time vs stage ---
    if conv:
        pr = [c[0] for c in conv]
        ens_dt = [dt(c[1]) for c in conv]
        diu_dt = [dt(c[2]) for c in conv if c[2] is not None]
        diu_pr = [c[0] for c in conv if c[2] is not None]
        axB.plot(pr, ens_dt, "o-", color="crimson", lw=2, label="ensemble prediction")
        if diu_dt:
            axB.plot(diu_pr, diu_dt, "s--", color="darkorange", lw=1.6, label="diurnal")
        axB.axhline(dt(fire), color="green", lw=2, label="ACTUAL firing")
        axB.fill_between(pr, [dt(fire - 900) for _ in pr], [dt(fire + 900) for _ in pr],
                         color="green", alpha=0.08, label="±15 min")
        axB.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=timezone.utc))
        axB.set_xlabel("cycle progress at prediction time (%)")
        axB.set_ylabel("predicted firing time (UTC)")
        axB.set_title("Prediction converges on actual as the cycle fills",
                      fontweight="bold", fontsize=11)
        axB.legend(fontsize=8)
        axB.grid(alpha=0.3)

    fig.suptitle("Vote-party predictor — stage-by-stage replay", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(args.out, dpi=110, bbox_inches="tight")
    plt.close(fig)

    print(f"Replayed cycle {ci+1} ({len(cyc)} pts). Actual firing: {dt(fire):%H:%M}Z")
    for pr, ens, diur in conv:
        print(f"  @ {pr:4.0f}%  ensemble -> {dt(ens):%H:%M}Z  "
              f"(err {(ens-fire)/60:+.0f} min)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

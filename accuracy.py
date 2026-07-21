#!/usr/bin/env python3
"""Stage-wise accuracy backtest for the vote-party predictor.

For every *completed* cycle we replay it point by point. At each stage (each
successive observation) we fit each model — and the ensemble — using ONLY the
data available up to that stage, predict the firing time, and compare it to the
cycle's actual firing time.

Because the counter resets before we ever log a point at exactly `target`, the
true firing instant is not directly observed. We estimate each cycle's
reference firing time by extrapolating its final observed segment (last few
points) to the target. This is the best available ground truth; cycles whose
last observation is far below target have a looser reference (flagged in the
output).

Ensemble weights are computed **leave-one-cycle-out**: when scoring cycle c,
the backtest weights come only from the *other* completed cycles, so a cycle is
never evaluated using knowledge of itself.

Outputs (under data/):
    accuracy.png    — |ETA error| vs cycle progress, per cycle + per model
    accuracy.json   — raw stage-by-stage errors and stage-bucket summary

Usage:
    python3 accuracy.py                 # reads data/voteparty.jsonl
    python3 accuracy.py --no-graph
"""

import argparse
import json
import os

import numpy as np

from predict import (
    MODELS, load_points, split_cycles, cycle_arrays,
    backtest_staged, weights_for_progress, fmt_ts, make_ctx, cycle_fire_time,
)

MIN_FIT = 3  # need at least this many points before a stage is predictable


def model_eta_epoch(name, t, y, target, t0, ctx=None):
    """Predicted firing epoch for one model given partial (t, y). None if n/a."""
    t_cross = MODELS[name](t, y, target, ctx)
    return (t0 + t_cross) if t_cross is not None else None


def evaluate(points, target):
    cycles = split_cycles(points)
    # A cycle is "completed" if a later cycle exists after it (i.e. it reset).
    completed = cycles[:-1]
    if len(completed) < 1:
        return None

    # Reference firing time per completed cycle.
    fires = []
    for cyc in completed:
        epoch, quality = cycle_fire_time(cyc, target)
        fires.append({"epoch": epoch, "quality": quality})

    results = []  # per (cycle, stage)
    for ci, cyc in enumerate(completed):
        fire = fires[ci]["epoch"]
        if fire is None:
            continue
        # Leave-one-cycle-out weights and history context.
        others = [c for cj, c in enumerate(completed) if cj != ci]
        staged = backtest_staged(others if others else completed, target)
        ctx = make_ctx(cyc, others)

        t, y = cycle_arrays(cyc)
        t0 = cyc[0]["_t"]
        n = len(t)
        for i in range(MIN_FIT, n + 1):
            t_fit, y_fit = t[:i], y[:i]
            progress = float(y_fit[-1] / target * 100.0)
            weights = weights_for_progress(staged, progress)

            per_model = {}
            etas, ws = [], []
            for name in MODELS:
                eta = model_eta_epoch(name, t_fit, y_fit, target, t0, ctx)
                per_model[name] = ((eta - fire) / 60.0) if eta is not None else None
                if eta is not None and np.isfinite(eta):
                    etas.append(eta)
                    ws.append(weights.get(name, 0.0))
            if etas:
                ws = np.array(ws)
                ws = ws / ws.sum() if ws.sum() > 0 else np.ones(len(ws)) / len(ws)
                ens_eta = float(np.sum(np.array(etas) * ws))
                ens_err = (ens_eta - fire) / 60.0
            else:
                ens_err = None

            results.append({
                "cycle": ci,
                "stage_index": i,
                "progress_pct": round(progress, 1),
                "hours_elapsed": round(float(t_fit[-1] / 3600.0), 2),
                "ensemble_err_min": round(ens_err, 1) if ens_err is not None else None,
                "model_err_min": {k: (round(v, 1) if v is not None else None)
                                  for k, v in per_model.items()},
            })

    # Stage-bucket summary (mean absolute error).
    buckets = [(0, 25), (25, 50), (50, 75), (75, 101)]
    summary = {}
    names = ["ensemble"] + list(MODELS)
    for lo, hi in buckets:
        label = f"{lo}-{hi if hi <= 100 else 100}%"
        summary[label] = {}
        for name in names:
            vals = []
            for r in results:
                if lo <= r["progress_pct"] < hi:
                    v = (r["ensemble_err_min"] if name == "ensemble"
                         else r["model_err_min"][name])
                    if v is not None:
                        vals.append(abs(v))
            summary[label][name] = round(float(np.mean(vals)), 1) if vals else None

    return {
        "target": target,
        "num_completed_cycles": len(completed),
        "references": [
            {"cycle": ci, "fire_time": fmt_ts(f["epoch"]) if f["epoch"] else None,
             "last_observed_pct": round(f["quality"], 1)}
            for ci, f in enumerate(fires)
        ],
        "stage_results": results,
        "stage_bucket_mae_min": summary,
    }


def make_graph(ev, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    results = ev["stage_results"]
    cycles = sorted({r["cycle"] for r in results})

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # Left: ensemble |error| vs progress, one line per cycle + mean curve.
    cmap = plt.cm.viridis(np.linspace(0, 0.85, len(cycles)))
    for ci, col in zip(cycles, cmap):
        rows = [r for r in results if r["cycle"] == ci and r["ensemble_err_min"] is not None]
        rows.sort(key=lambda r: r["progress_pct"])
        xs = [r["progress_pct"] for r in rows]
        ys = [abs(r["ensemble_err_min"]) for r in rows]
        ax1.plot(xs, ys, "o-", color=col, alpha=0.8, label=f"cycle {ci+1}")

    # Mean |error| across cycles, binned by progress.
    bins = np.arange(0, 101, 10)
    centers, means = [], []
    for b0, b1 in zip(bins[:-1], bins[1:]):
        vals = [abs(r["ensemble_err_min"]) for r in results
                if r["ensemble_err_min"] is not None and b0 <= r["progress_pct"] < b1]
        if vals:
            centers.append((b0 + b1) / 2)
            means.append(np.mean(vals))
    if centers:
        ax1.plot(centers, means, "k--", lw=2.5, label="mean |error|", zorder=10)

    ax1.set_title("Ensemble ETA error vs cycle progress", fontweight="bold")
    ax1.set_xlabel("cycle progress (% of target collected)")
    ax1.set_ylabel("|predicted − actual firing| (minutes)")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    # Right: per-model mean |error| vs progress (averaged across cycles).
    for name in MODELS:
        centers, means = [], []
        for b0, b1 in zip(bins[:-1], bins[1:]):
            vals = [abs(r["model_err_min"][name]) for r in results
                    if r["model_err_min"][name] is not None and b0 <= r["progress_pct"] < b1]
            if vals:
                centers.append((b0 + b1) / 2)
                means.append(np.mean(vals))
        if centers:
            ax2.plot(centers, means, "o-", alpha=0.8, label=name)
    # Ensemble overlay in bold.
    centers, means = [], []
    for b0, b1 in zip(bins[:-1], bins[1:]):
        vals = [abs(r["ensemble_err_min"]) for r in results
                if r["ensemble_err_min"] is not None and b0 <= r["progress_pct"] < b1]
        if vals:
            centers.append((b0 + b1) / 2)
            means.append(np.mean(vals))
    if centers:
        ax2.plot(centers, means, "k--", lw=2.5, label="ensemble", zorder=10)

    ax2.set_title("Per-model mean ETA error vs progress", fontweight="bold")
    ax2.set_xlabel("cycle progress (% of target collected)")
    ax2.set_ylabel("mean |error| (minutes)")
    ax2.legend(fontsize=8, ncol=2)
    ax2.grid(alpha=0.3)

    fig.suptitle("Vote-party predictor — stage-wise accuracy backtest "
                 f"({ev['num_completed_cycles']} completed cycles)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage-wise accuracy backtest.")
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--no-graph", action="store_true")
    args = ap.parse_args(argv)

    points = load_points(args.input)
    target = float(points[-1]["target"])
    ev = evaluate(points, target)
    if ev is None:
        print("No completed cycles yet — need at least one full cycle to test accuracy.")
        return 1

    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "accuracy.json"), "w", encoding="utf-8") as fh:
        json.dump(ev, fh, indent=2)
    if not args.no_graph:
        make_graph(ev, os.path.join(args.outdir, "accuracy.png"))

    print(f"Completed cycles tested: {ev['num_completed_cycles']}")
    print("Reference firing times (from end-of-cycle extrapolation):")
    for r in ev["references"]:
        print(f"  cycle {r['cycle']+1}: {r['fire_time']}  (last obs {r['last_observed_pct']}% of target)")
    print("\nMean |ETA error| in minutes, by cycle-progress bucket:")
    hdr = ["stage"] + ["ensemble"] + list(MODELS)
    print("  " + "  ".join(f"{h:>9s}" for h in hdr))
    for stage, row in ev["stage_bucket_mae_min"].items():
        cells = [f"{stage:>9s}"] + [
            (f"{row[n]:>9.1f}" if row.get(n) is not None else f"{'—':>9s}")
            for n in (["ensemble"] + list(MODELS))
        ]
        print("  " + "  ".join(cells))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Detailed model-performance report for the vote-party predictor.

Runs the leave-one-cycle-out backtest across all completed cycles and, for each
model (plus the ensemble), computes error metrics overall and per cycle-stage.
Produces a detailed graph and machine/human-readable tables.

Metrics per model:
    n          — number of stage predictions it produced
    coverage   — % of stages where it returned a prediction
    MAE        — mean absolute ETA error (minutes)
    RMSE       — root-mean-square ETA error (minutes)
    median     — median absolute error (minutes)
    P90        — 90th-percentile absolute error (minutes)
    bias       — mean signed error (min); + = predicts too late, − = too early
    weight     — current ensemble weight (stage-blended, from live prediction)

Outputs (under data/):
    model_report.png   — heatmap + ranked MAE + bias + weights
    model_report.md    — overall metrics table + per-stage MAE table
    model_report.json  — all metrics

Usage:
    python3 model_report.py                 # reads data/voteparty.jsonl
    python3 model_report.py --no-graph
"""

import argparse
import json
import os

import numpy as np

from predict import (
    MODELS, load_points, split_cycles, cycle_arrays, cycle_fire_time,
    make_ctx, backtest_staged, weights_for_progress, predict,
)

MIN_FIT = 3
STAGES = [(0, 25), (25, 50), (50, 75), (75, 90), (90, 100)]


def _stage(progress):
    for lo, hi in STAGES:
        if lo <= progress < hi:
            return f"{lo}-{hi}%"
    return f"{STAGES[-1][0]}-{STAGES[-1][1]}%"


def collect_errors(points, target):
    """Leave-one-out signed ETA errors (minutes) per model and ensemble, tagged
    with the progress stage at prediction time."""
    cycles = split_cycles(points)
    completed = cycles[:-1]
    names = list(MODELS) + ["ensemble"]
    rows = []  # {model, stage, progress, signed_err_min}
    for ci, cyc in enumerate(completed):
        fire, _ = cycle_fire_time(cyc, target)
        if fire is None or len(cyc) < MIN_FIT + 1:
            continue
        others = [c for cj, c in enumerate(completed) if cj != ci]
        staged = backtest_staged(others if others else completed, target)
        ctx = make_ctx(cyc, others)
        t, y = cycle_arrays(cyc)
        t0 = cyc[0]["_t"]
        for i in range(MIN_FIT, len(t) + 1):
            t_fit, y_fit = t[:i], y[:i]
            progress = float(y_fit[-1]) / target * 100.0
            weights = weights_for_progress(staged, progress)
            etas, ws = [], []
            for name in MODELS:
                tc = MODELS[name](t_fit, y_fit, target, ctx)
                if tc is None:
                    continue
                eta = t0 + tc
                etas.append(eta)
                ws.append(weights.get(name, 0.0))
                rows.append({"model": name, "stage": _stage(progress),
                             "progress": progress, "err": (eta - fire) / 60.0})
            if etas:
                wsn = np.array(ws)
                wsn = wsn / wsn.sum() if wsn.sum() > 0 else np.ones(len(wsn)) / len(wsn)
                ens = float(np.sum(np.array(etas) * wsn))
                rows.append({"model": "ensemble", "stage": _stage(progress),
                             "progress": progress, "err": (ens - fire) / 60.0})
    return rows, completed, names


def summarize(rows, names, n_stage_origins):
    stats = {}
    stage_labels = [f"{lo}-{hi}%" for lo, hi in STAGES]
    for name in names:
        errs = np.array([r["err"] for r in rows if r["model"] == name])
        if len(errs) == 0:
            continue
        ae = np.abs(errs)
        per_stage = {}
        for sl in stage_labels:
            se = [abs(r["err"]) for r in rows if r["model"] == name and r["stage"] == sl]
            per_stage[sl] = round(float(np.mean(se)), 1) if se else None
        stats[name] = {
            "n": int(len(errs)),
            "coverage_pct": round(100 * len(errs) / max(n_stage_origins, 1), 0),
            "mae_min": round(float(np.mean(ae)), 1),
            "rmse_min": round(float(np.sqrt(np.mean(errs ** 2))), 1),
            "median_min": round(float(np.median(ae)), 1),
            "p90_min": round(float(np.percentile(ae, 90)), 1),
            "bias_min": round(float(np.mean(errs)), 1),
            "per_stage_mae": per_stage,
        }
    return stats, stage_labels


def make_graph(stats, stage_labels, weights, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Order models best→worst by MAE; keep ensemble tracked but sorted in too.
    order = sorted(stats.keys(), key=lambda n: stats[n]["mae_min"])
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1], hspace=0.32, wspace=0.28)

    # Panel 1: heatmap of per-stage MAE.
    ax1 = fig.add_subplot(gs[0, :])
    M = np.array([[stats[n]["per_stage_mae"][s] if stats[n]["per_stage_mae"][s] is not None
                   else np.nan for s in stage_labels] for n in order], dtype=float)
    im = ax1.imshow(M, aspect="auto", cmap="RdYlGn_r", vmin=0,
                    vmax=np.nanpercentile(M, 92) if np.isfinite(M).any() else 1)
    ax1.set_xticks(range(len(stage_labels)))
    ax1.set_xticklabels(stage_labels)
    ax1.set_yticks(range(len(order)))
    ax1.set_yticklabels([f"{n}  (w={weights.get(n, 0):.2f})" if n != "ensemble" else n
                         for n in order])
    for i in range(len(order)):
        for j in range(len(stage_labels)):
            v = M[i, j]
            if np.isfinite(v):
                ax1.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8,
                         color="black")
    ax1.set_title("Mean |ETA error| (minutes) by model × cycle stage — "
                  "greener is better", fontweight="bold")
    fig.colorbar(im, ax=ax1, fraction=0.025, pad=0.01, label="MAE (min)")

    # Panel 2: overall MAE ranked bar.
    ax2 = fig.add_subplot(gs[1, 0])
    maes = [stats[n]["mae_min"] for n in order]
    colors = ["crimson" if n == "ensemble" else "#4c72b0" for n in order]
    ax2.barh(range(len(order)), maes, color=colors)
    ax2.set_yticks(range(len(order)))
    ax2.set_yticklabels(order)
    ax2.invert_yaxis()
    for i, v in enumerate(maes):
        ax2.text(v, i, f" {v:.0f}", va="center", fontsize=8)
    ax2.set_title("Overall MAE (all stages)", fontweight="bold")
    ax2.set_xlabel("MAE (min)")
    ax2.grid(alpha=0.3, axis="x")

    # Panel 3: bias (signed error) — early vs late tendency.
    ax3 = fig.add_subplot(gs[1, 1])
    biases = [stats[n]["bias_min"] for n in order]
    bcolors = ["#d62728" if b > 0 else "#2ca02c" for b in biases]
    ax3.barh(range(len(order)), biases, color=bcolors)
    ax3.axvline(0, color="#333", lw=1)
    ax3.set_yticks(range(len(order)))
    ax3.set_yticklabels(order)
    ax3.invert_yaxis()
    for i, v in enumerate(biases):
        ax3.text(v, i, f" {v:+.0f}", va="center", fontsize=8)
    ax3.set_title("Bias: + predicts too LATE, − too EARLY", fontweight="bold")
    ax3.set_xlabel("mean signed error (min)")
    ax3.grid(alpha=0.3, axis="x")

    fig.suptitle("Vote-party predictor — model performance report", fontsize=14)
    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)


def write_markdown(stats, stage_labels, weights, path, n_cycles):
    order = sorted(stats.keys(), key=lambda n: stats[n]["mae_min"])
    L = [
        "# Model Performance Report",
        "",
        f"Leave-one-cycle-out backtest over **{n_cycles} completed cycles**. "
        "Error = |predicted firing time − actual firing time|, in minutes.",
        "",
        "## Overall metrics (ranked by MAE)",
        "",
        "| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |",
        "|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|",
    ]
    for n in order:
        s = stats[n]
        w = "—" if n == "ensemble" else f"{weights.get(n, 0):.3f}"
        L.append(f"| {'**'+n+'**' if n=='ensemble' else n} | {w} | {s['mae_min']} | "
                 f"{s['rmse_min']} | {s['median_min']} | {s['p90_min']} | "
                 f"{s['bias_min']:+} | {s['coverage_pct']:.0f}% | {s['n']} |")
    L += ["", "## Mean |ETA error| by cycle stage (minutes)", "",
          "| Model | " + " | ".join(stage_labels) + " |",
          "|-------|" + "|".join(["----:"] * len(stage_labels)) + "|"]
    for n in order:
        cells = [str(stats[n]["per_stage_mae"][s]) if stats[n]["per_stage_mae"][s] is not None
                 else "—" for s in stage_labels]
        L.append(f"| {n} | " + " | ".join(cells) + " |")
    L += ["",
          "**Bias** > 0 means the model tends to predict the party *later* than it "
          "actually fires; < 0 means *earlier*. **Coverage** is the share of "
          "stages where the model produced a prediction (some need ≥3 points or "
          "history). See `model_report.png`.", ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Detailed model-performance report.")
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--no-graph", action="store_true")
    args = ap.parse_args(argv)

    points = load_points(args.input)
    target = float(points[-1]["target"])
    rows, completed, names = collect_errors(points, target)
    if not rows:
        print("No completed cycles yet — need at least one full cycle.")
        return 1

    # number of distinct (cycle, stage-origin) points, for coverage.
    n_origins = len({(r["model"] == "ensemble", round(r["progress"], 3)) for r in rows
                     if r["model"] == "ensemble"})
    stats, stage_labels = summarize(rows, names, n_origins)

    # Current live weights.
    live = predict(split_cycles(points), target)
    weights = {n: live["models"][n]["weight"] for n in live["models"]}

    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "model_report.json"), "w", encoding="utf-8") as fh:
        json.dump({"n_completed_cycles": len(completed), "weights": weights,
                   "stats": stats}, fh, indent=2)
    write_markdown(stats, stage_labels, weights,
                   os.path.join(args.outdir, "model_report.md"), len(completed))
    if not args.no_graph:
        make_graph(stats, stage_labels, weights,
                   os.path.join(args.outdir, "model_report.png"))

    order = sorted(stats.keys(), key=lambda n: stats[n]["mae_min"])
    print(f"Completed cycles: {len(completed)}\n")
    hdr = f"{'model':11s} {'MAE':>6s} {'RMSE':>6s} {'median':>7s} {'P90':>6s} {'bias':>6s} {'wt':>6s}"
    print(hdr)
    print("-" * len(hdr))
    for n in order:
        s = stats[n]
        w = weights.get(n, 0.0) if n != "ensemble" else 0.0
        print(f"{n:11s} {s['mae_min']:6.1f} {s['rmse_min']:6.1f} {s['median_min']:7.1f} "
              f"{s['p90_min']:6.1f} {s['bias_min']:+6.1f} {w:6.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

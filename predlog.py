#!/usr/bin/env python3
"""Out-of-sample prediction log & track record.

For every cycle, this reconstructs — *causally* — what the deployed model would
have predicted at each stage, using only the cycles that had completed **before
that cycle started** (no hindsight). Once a cycle fires, its actual firing time
resolves the error for every prediction made during it.

This is the honest real-world scorecard: unlike the backtest (which uses
leave-one-out over all cycles), each entry here only ever saw the past — exactly
what the live system had available at the time.

The log is regenerated deterministically from the data each run, so it always
reflects the latest cycles and newly-resolved actuals.

Outputs (under data/):
    predictions_log.jsonl  — one row per (cycle, stage): predicted vs actual
    prediction_track.png   — error vs progress, stage MAE, learning curve
    PREDICTION_LOG.md       — compact per-cycle track record

Usage:
    python3 predlog.py                 # reads data/voteparty.jsonl
    python3 predlog.py --no-graph
"""

import argparse
import json
import os

import numpy as np

from predict import (
    MODELS, load_points, split_cycles, cycle_arrays, cycle_fire_time,
    make_ctx, backtest_staged, weights_for_progress, fmt_ts,
    label_sigma_min, TIGHT_LABEL_MIN,
    shape_analogue_forecast, analogue_forecast, wquantile,
)

MIN_FIT = 3
STAGES = [(0, 25), (25, 50), (50, 75), (75, 90), (90, 100)]


def _stage(p):
    for lo, hi in STAGES:
        if lo <= p < hi:
            return f"{lo}-{hi}%"
    return f"{STAGES[-1][0]}-{STAGES[-1][1]}%"


def build_log(points, target):
    """Causal reconstruction: predictions use only earlier cycles."""
    cycles = split_cycles(points)
    entries = []
    for ci, cyc in enumerate(cycles):
        prior = cycles[:ci]                      # only cycles that finished earlier
        completed = ci < len(cycles) - 1         # a later cycle exists → this one fired
        fire = cycle_fire_time(cyc, target)[0] if completed else None
        bracket = label_sigma_min(cycles, ci, target)  # extrapolation label sigma (min)
        tight = bool(bracket is not None and bracket <= TIGHT_LABEL_MIN)
        staged = backtest_staged(prior, target) if prior else None
        ctx = make_ctx(cyc, prior)
        t, y = cycle_arrays(cyc)
        t0 = cyc[0]["_t"]
        cyc_id = fmt_ts(t0)
        lib = list(range(ci))                    # library = prior cycle indices
        for i in range(MIN_FIT, len(t) + 1):
            t_fit, y_fit = t[:i], y[:i]
            prog = float(y_fit[-1]) / target * 100.0
            now, coll = t0 + t[i - 1], float(y_fit[-1])
            # REPORTED PRIMARY: shape-aware analogue median, plain-analogue fallback
            # before a diurnal profile is estimable. Same construction as predict().
            fc = shape_analogue_forecast(cycles, lib, target, now, coll)
            if fc is None:
                fc = analogue_forecast(cycles, lib, target, now, coll)
            primary = float(wquantile(fc["preds"], fc["w"], [0.5])[0]) if fc else None
            # ensemble kept as a diagnostic column only
            weights = (weights_for_progress(staged, prog) if staged
                       else {n: 1.0 / len(MODELS) for n in MODELS})
            etas, ws = [], []
            for n in MODELS:
                tc = MODELS[n](t_fit, y_fit, target, ctx)
                if tc is None:
                    continue
                etas.append(t0 + tc)
                ws.append(weights.get(n, 0.0))
            ens = None
            if etas:
                wn = np.array(ws)
                wn = wn / wn.sum() if wn.sum() > 0 else np.ones(len(wn)) / len(wn)
                ens = float(np.sum(np.array(etas) * wn))
            if primary is None:
                continue
            err = (primary - fire) / 60.0 if fire is not None else None
            entries.append({
                "cycle": ci + 1,
                "cycle_id": cyc_id,
                "data_ts": fmt_ts(t0 + t[i - 1]),
                "progress_pct": round(prog, 1),
                "stage": _stage(prog),
                "n_prior_cycles": len(prior),
                "primary_eta": fmt_ts(primary),
                "ensemble_eta": fmt_ts(ens) if ens is not None else None,
                "actual_fire": fmt_ts(fire) if fire is not None else None,
                "error_min": round(err, 1) if err is not None else None,
                "resolved": fire is not None,
                "label_bracket_min": int(round(bracket)) if bracket is not None else None,
                "label_tight": tight,
            })
    return entries, cycles


def _stage_mae(res):
    out = {}
    for lo, hi in STAGES:
        lbl = f"{lo}-{hi}%"
        v = [abs(e["error_min"]) for e in res if e["stage"] == lbl]
        out[lbl] = round(float(np.mean(v)), 1) if v else None
    return out


def summarize(entries):
    """Out-of-sample stats over resolved entries that had ≥1 prior cycle.

    The headline uses only **tightly-labeled** cycles (trustworthy firing time);
    the loose-label set is reported separately and flagged as contaminated.
    """
    res = [e for e in entries if e["resolved"] and e["n_prior_cycles"] >= 1
           and e["error_min"] is not None]
    tight = [e for e in res if e.get("label_tight")]
    n_tight_cycles = len({e["cycle"] for e in tight})
    stats = {"n_resolved": len(res), "n_tight_labeled": len(tight),
             "n_tight_cycles": n_tight_cycles}
    if tight:
        ae = np.abs([e["error_min"] for e in tight])
        stats["tight_overall_mae_min"] = round(float(np.mean(ae)), 1)
        stats["tight_stage_mae_min"] = _stage_mae(tight)
    if res:
        stats["all_overall_mae_min"] = round(float(np.mean(np.abs([e["error_min"] for e in res]))), 1)
        stats["all_stage_mae_min"] = _stage_mae(res)
    return stats, res, tight


def make_graph(entries, res, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    ax1, ax2, ax3 = axes

    cycles = sorted({e["cycle"] for e in res})
    cmap = plt.cm.viridis(np.linspace(0, 0.85, max(len(cycles), 1)))

    # Panel 1: signed error vs progress, per cycle.
    for cyc, col in zip(cycles, cmap):
        rows = sorted([e for e in res if e["cycle"] == cyc], key=lambda e: e["progress_pct"])
        ax1.plot([e["progress_pct"] for e in rows], [e["error_min"] for e in rows],
                 "o-", color=col, alpha=0.85, label=f"cycle {cyc}")
    ax1.axhline(0, color="green", lw=1.5)
    ax1.axhspan(-15, 15, color="green", alpha=0.08, label="±15 min")
    ax1.set_title("Out-of-sample error vs progress", fontweight="bold")
    ax1.set_xlabel("cycle progress (%)")
    ax1.set_ylabel("predicted − actual (min)  (+late / −early)")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    # Panel 2: out-of-sample MAE by stage.
    labels = [f"{lo}-{hi}%" for lo, hi in STAGES]
    maes = []
    for lbl in labels:
        v = [abs(e["error_min"]) for e in res if e["stage"] == lbl]
        maes.append(np.mean(v) if v else np.nan)
    colors = plt.cm.RdYlGn_r(np.clip(np.array([m if np.isfinite(m) else 0 for m in maes]) / 120, 0, 1))
    ax2.bar(range(len(labels)), [m if np.isfinite(m) else 0 for m in maes], color=colors)
    ax2.set_xticks(range(len(labels)))
    ax2.set_xticklabels(labels, rotation=20)
    for i, m in enumerate(maes):
        if np.isfinite(m):
            ax2.text(i, m, f"{m:.0f}", ha="center", va="bottom", fontsize=9)
    ax2.set_title("Out-of-sample MAE by stage", fontweight="bold")
    ax2.set_ylabel("mean |error| (min)")
    ax2.grid(alpha=0.3, axis="y")

    # Panel 3: learning curve — per-cycle MAE (stages ≥50%) as cycles accrue.
    xs, ys = [], []
    for cyc in cycles:
        v = [abs(e["error_min"]) for e in res if e["cycle"] == cyc and e["progress_pct"] >= 50]
        if v:
            xs.append(cyc)
            ys.append(np.mean(v))
    if xs:
        ax3.plot(xs, ys, "o-", color="crimson", lw=2)
        for x, yv in zip(xs, ys):
            ax3.text(x, yv, f" {yv:.0f}", fontsize=8, va="bottom")
    ax3.set_title("Learning curve — late-stage MAE per cycle\n(more prior data → better)",
                  fontweight="bold", fontsize=10)
    ax3.set_xlabel("cycle number")
    ax3.set_ylabel("mean |error| ≥50% (min)")
    ax3.grid(alpha=0.3)

    fig.suptitle("Vote-party predictor — out-of-sample track record", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)


def write_markdown(entries, res, tight, stats, path):
    L = ["# Prediction Track Record (out-of-sample)", "",
         "Causal reconstruction — each prediction used only cycles that finished "
         "*before* its cycle began. Predictions are the reported primary "
         "(**shape_analogue**, plain-analogue fallback before a diurnal profile "
         "is estimable) — the exact model shipped in predict.py.", "",
         f"⚠️ **Label caveat:** **{stats.get('n_tight_cycles', 0)} cycle(s)** have a "
         "firing time known (by extrapolation to target) to within "
         f"{int(__import__('predict').TIGHT_LABEL_MIN)} min. The **tight-label** "
         "row is the trustworthy one; looser cycles carry larger label error.", ""]
    if "tight_overall_mae_min" in stats:
        L += [f"**Tight-label OOS MAE:** {stats['tight_overall_mae_min']} min "
              f"(n={stats['n_tight_labeled']} predictions, "
              f"{stats['n_tight_cycles']} cycle(s))",
              "**Tight-label MAE by stage:** " + "  ·  ".join(
                  f"{k}={v}m" for k, v in stats["tight_stage_mae_min"].items()
                  if v is not None), ""]
    if "all_overall_mae_min" in stats:
        L += [f"_All-cycle (contaminated) MAE: {stats['all_overall_mae_min']} min "
              f"over {stats['n_resolved']} predictions — do not trust._", ""]
    # Per-cycle snapshot at ~50/75/90%.
    L += ["## Per-cycle snapshots", "",
          "| Cycle | Actual fire | Label | @~50% | @~75% | @~90% |",
          "|-------|-------------|-------|------:|------:|------:|"]
    for cyc in sorted({e["cycle"] for e in res}):
        rows = [e for e in res if e["cycle"] == cyc]
        fire = rows[0]["actual_fire"]
        lbl = "tight" if rows[0].get("label_tight") else f"±{rows[0].get('label_bracket_min','?')}m"

        def at(target_pct):
            cand = min(rows, key=lambda e: abs(e["progress_pct"] - target_pct))
            return f"{cand['error_min']:+.0f}m" if abs(cand["progress_pct"] - target_pct) < 15 else "—"
        L.append(f"| {cyc} | {fire} | {lbl} | {at(50)} | {at(75)} | {at(90)} |")
    L += ["", "Values are primary-model error (predicted − actual firing), minutes; "
          "+ = predicted too late. See `prediction_track.png`.", ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Out-of-sample prediction log.")
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--no-graph", action="store_true")
    args = ap.parse_args(argv)

    points = load_points(args.input)
    target = float(points[-1]["target"])
    entries, cycles = build_log(points, target)
    stats, res, tight = summarize(entries)

    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "predictions_log.jsonl"), "w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps(e) + "\n")
    write_markdown(entries, res, tight, stats,
                   os.path.join(args.outdir, "PREDICTION_LOG.md"))
    if not args.no_graph and res:
        make_graph(entries, res, os.path.join(args.outdir, "prediction_track.png"))

    print(f"Logged {len(entries)} predictions across {len(cycles)} cycles.")
    print(f"Resolved: {stats.get('n_resolved', 0)} | "
          f"tightly-labeled: {stats.get('n_tight_labeled', 0)} "
          f"({stats.get('n_tight_cycles', 0)} cycle(s))")
    if "tight_overall_mae_min" in stats:
        print(f"TIGHT-LABEL OOS MAE: {stats['tight_overall_mae_min']} min (trustworthy)")
        for k, v in stats["tight_stage_mae_min"].items():
            if v is not None:
                print(f"  {k:8s} {v} min")
    if "all_overall_mae_min" in stats:
        print(f"all-cycle MAE (contaminated): {stats['all_overall_mae_min']} min")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

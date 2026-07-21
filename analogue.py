#!/usr/bin/env python3
"""Conditional analogue / curve-library forecaster (nonparametric).

Rather than assume any functional form, this borrows the **actual remaining
trajectories** of past cycles. Given the current cycle's state (progress +
current UTC time-of-day), each library cycle contributes: "when I was at this
same progress, at this same time of day, I went on to fire T minutes later."

The forecast is the similarity-weighted distribution of those {now + T} — a
genuinely empirical predictive distribution, so its spread reflects real
historical variability (the thing the smooth NHPP couldn't represent).

CONDITIONING: analogues are weighted by how close their UTC time-of-day *at the
matching progress* is to the current UTC time-of-day — because the remaining
trajectory depends on the diurnal pattern still to come. Weights are partially
pooled toward uniform so the forecast never collapses onto one analogue at our
tiny sample size.

Outputs data/analogue.json + analogue.png. Usage: python3 analogue.py [-i ..] [-o data]
"""
import argparse
import json
import os
from datetime import datetime, timezone

import numpy as np

from predict import (load_points, split_cycles, cycle_arrays, cycle_fire_time,
                     tight_cycle_indices, fmt_ts, make_ctx, MODELS,
                     time_at_collected, analogue_forecast, wquantile)


def summarize(fc):
    p = fc["preds"]
    w = fc["w"]
    q = wquantile(p, w, [0.05, 0.1, 0.5, 0.9, 0.95])
    return {"p05": q[0], "p10": q[1], "p50": q[2], "p90": q[3], "p95": q[4],
            "n_eff": float(1.0 / np.sum(w ** 2))}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--no-graph", action="store_true")
    args = ap.parse_args(argv)

    pts = load_points(args.input)
    target = float(pts[-1]["target"])
    cycles = split_cycles(pts)
    cur = cycles[-1]
    _, y = cycle_arrays(cur)
    now, collected = cur[-1]["_t"], y[-1]
    prog = 100 * collected / target

    fc = analogue_forecast(cycles, list(range(len(cycles) - 1)), target, now, collected)
    if fc is None:
        print("No analogues.")
        return 1
    s = summarize(fc)

    # Causal OOS vs diurnal on tight cycles + interval coverage.
    tight = tight_cycle_indices(cycles)
    a_err, d_err, cov, ncov = [], [], 0, 0
    for ci in tight:
        prior = list(range(ci))
        if not prior:
            continue
        fire, _ = cycle_fire_time(cycles[ci], target)
        if fire is None:
            continue
        t, yy = cycle_arrays(cycles[ci])
        for i in range(3, len(t) + 1):
            f2 = analogue_forecast(cycles, prior, target,
                                   cycles[ci][i - 1]["_t"], yy[i - 1])
            if f2 is None:
                continue
            qq = wquantile(f2["preds"], f2["w"], [0.1, 0.5, 0.9])
            a_err.append(abs(qq[1] - fire) / 60)
            ncov += 1
            cov += int(qq[0] <= fire <= qq[2])
            tc = MODELS["diurnal"](t[:i], yy[:i], target, make_ctx(cycles[ci], [cycles[k] for k in prior]))
            if tc is not None:
                d_err.append(abs((cycles[ci][0]["_t"] + tc - fire) / 60))

    cov_pct = round(100 * cov / ncov) if ncov else None
    out = {
        "generated_at": fmt_ts(pts[-1]["_t"]),
        "progress_pct": round(prog, 1),
        "median_eta": fmt_ts(s["p50"]),
        "interval_80": [fmt_ts(s["p10"]), fmt_ts(s["p90"])],
        "interval_90": [fmt_ts(s["p05"]), fmt_ts(s["p95"])],
        "effective_analogues": round(s["n_eff"], 1),
        "n_library_cycles": len(cycles) - 1,
        "oos_verdict": {
            "analogue_median_mae_min": round(float(np.mean(a_err)), 1) if a_err else None,
            "diurnal_median_mae_min": round(float(np.mean(d_err)), 1) if d_err else None,
            "interval_80_measured_coverage_pct": cov_pct,
            "n_tight_stage_predictions": ncov,
        },
        "note": "Nonparametric: forecast is the similarity-weighted distribution "
                "of past cycles' actual remaining trajectories. Intervals reflect "
                "real historical spread; coverage measured on tight cycles above.",
    }
    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "analogue.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    print(f"Cycles {len(cycles)} | current {prog:.0f}% | library {len(cycles)-1} | "
          f"eff. analogues {s['n_eff']:.1f}")
    print(f"Analogue median ETA {out['median_eta']}  "
          f"80% [{out['interval_80'][0]} .. {out['interval_80'][1]}]")
    if a_err:
        print(f"OOS (tight): analogue median MAE {np.mean(a_err):.1f} min | "
              f"diurnal {np.mean(d_err):.1f} min | "
              f"80% coverage {cov}/{ncov} = {cov_pct}%")

    if not args.no_graph:
        make_graph(cycles, target, fc, s, os.path.join(args.outdir, "analogue.png"))
    return 0


def make_graph(cycles, target, fc, s, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    def dt(e):
        return datetime.fromtimestamp(e, tz=timezone.utc)

    cur = cycles[-1]
    _, yy = cycle_arrays(cur)
    now, collected = cur[-1]["_t"], yy[-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5),
                                   gridspec_kw={"width_ratios": [1.5, 1]})

    xs = [dt(p["_t"]) for p in cur]
    ax1.plot(xs, [p["collected"] for p in cur], "o-", color="black", ms=3, lw=2,
             label="current cycle", zorder=6)
    ax1.axhline(target, color="#333", ls="--", lw=1)

    # Overlay each analogue's remaining trajectory, shifted to start at "now".
    cmap = plt.cm.viridis(np.linspace(0, 0.85, len(cycles) - 1))
    for li, col in zip(range(len(cycles) - 1), cmap):
        L = cycles[li]
        fire, _ = cycle_fire_time(L, target)
        if fire is None:
            continue
        tc = time_at_collected(L, collected, target, fire)
        if tc is None:
            continue
        tL = np.array([p["_t"] for p in L])
        yL = np.array([p["collected"] for p in L])
        mask = tL >= tc
        if mask.sum() < 1:
            continue
        shifted = [dt(now + (tt - tc)) for tt in tL[mask]]
        # weight index in preds order isn't 1:1; use uniform-ish alpha for viz
        ax1.plot(shifted, yL[mask], "-", color=col, alpha=0.5, lw=1.2,
                 label=f"cycle {li+1} analogue")
    ax1.axvspan(dt(s["p10"]), dt(s["p90"]), color="crimson", alpha=0.12, label="80% interval")
    ax1.axvline(dt(s["p50"]), color="crimson", lw=2, label="median firing")
    ax1.set_title("Conditional analogue — current cycle + borrowed continuations",
                  fontweight="bold")
    ax1.set_ylabel("votes collected")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=timezone.utc))
    ax1.legend(fontsize=7, ncol=2)
    ax1.grid(alpha=0.3)
    for lb in ax1.get_xticklabels():
        lb.set_rotation(20)

    order = np.argsort(fc["preds"])
    ax2.bar([dt(p) for p in fc["preds"][order]], fc["w"][order] * 100,
            width=0.02, color="#4c72b0")
    ax2.axvline(dt(s["p50"]), color="crimson", lw=2, label="median")
    ax2.set_title("Weighted analogue firing times", fontweight="bold")
    ax2.set_xlabel("firing time (UTC)")
    ax2.set_ylabel("weight (%)")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=timezone.utc))
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)
    for lb in ax2.get_xticklabels():
        lb.set_rotation(20)

    fig.suptitle("Conditional analogue / curve-library forecaster (nonparametric)", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())

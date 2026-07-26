#!/usr/bin/env python3
"""Shape-aware analogue — prototype + paired causal evaluation.

HYPOTHESIS (from FINDINGS.md): the LOO shape oracle beats the constant-rate
oracle by ~10 min mid-cycle. The current `analogue` borrows each library cycle's
*absolute remaining duration* from the matching-progress point. If the library
cycles happened to traverse a different diurnal phase than the current cycle must
traverse to reach target, every borrowed duration is mis-timed by the shape error
the oracle identifies.

FIX UNDER TEST: decompose each library analogue into
  - LEVEL: a pace multiplier m = (its actual remaining duration) /
           (the diurnal-expected duration for the same remaining votes at the
            same start time-of-day) — how fast/slow that cycle ran net of the
            diurnal pattern; and
  - SHAPE: the pooled diurnal rate profile.
Then FORECAST by integrating the diurnal profile forward from *now* (the current
cycle's actual phase), scaled by the borrowed pace multiplier, until the (exactly
known) remaining votes accumulate. Same tod-similarity weights and same
label-sigma Monte-Carlo spread as the current analogue, so the ONLY thing that
changes is whether the borrowed duration is re-timed through the current phase.

This file does NOT touch the reported model. It runs the SAME causal OOS as
analogue.py and reports the PAIRED MAE difference (shape-aware − current) with a
cluster-bootstrap 95% CI, so we can decide per PREREGISTRATION.md §2 whether the
challenger beats the incumbent by more than noise. Ship only if it clears the bar.

Usage: python3 shape_analogue.py [-i data/voteparty.jsonl]
"""
import argparse
import numpy as np

from predict import (load_points, split_cycles, cycle_arrays, cycle_fire_time,
                     tight_cycle_indices, wquantile, analogue_quantiles,
                     shape_analogue_forecast, shape_analogue_quantiles as shape_quantiles)


def evaluate(cycles, target):
    """Paired causal OOS: shape-aware vs current analogue on identical points."""
    tight = tight_cycle_indices(cycles, target)
    per_cycle = {}   # ci -> {"a":[cur aerr], "s":[shape aerr], "covc":[], "covs":[]}
    for ci in tight:
        prior = list(range(ci))
        if len(prior) < 2:            # need >=2 library cycles for a diurnal profile
            continue
        fire, _ = cycle_fire_time(cycles[ci], target)
        if fire is None:
            continue
        t, yy = cycle_arrays(cycles[ci])
        rec = {"a": [], "s": [], "covc": [], "covs": []}
        for i in range(3, len(t) + 1):
            now, coll = cycles[ci][i - 1]["_t"], yy[i - 1]
            qc = analogue_quantiles(cycles, prior, target, now, coll, [0.1, 0.5, 0.9])
            qs = shape_quantiles(cycles, prior, target, now, coll, [0.1, 0.5, 0.9])
            if qc is None or qs is None:
                continue
            rec["a"].append(abs(qc[1] - fire) / 60)
            rec["s"].append(abs(qs[1] - fire) / 60)
            rec["covc"].append(int(qc[0] <= fire <= qc[2]))
            rec["covs"].append(int(qs[0] <= fire <= qs[2]))
        if rec["a"]:
            per_cycle[ci] = rec
    return per_cycle


def cluster_bootstrap_paired(per_cycle, nboot=4000):
    """95% CI on mean(shape_aerr) - mean(cur_aerr), resampling whole cycles."""
    keys = list(per_cycle)
    if len(keys) < 2:
        return None
    rng = np.random.default_rng(11)
    diffs = []
    for _ in range(nboot):
        samp = rng.choice(keys, size=len(keys), replace=True)
        a = [v for k in samp for v in per_cycle[k]["a"]]
        s = [v for k in samp for v in per_cycle[k]["s"]]
        if a and s:
            diffs.append(np.mean(s) - np.mean(a))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return round(float(np.mean(diffs)), 2), [round(float(lo), 2), round(float(hi), 2)]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    args = ap.parse_args(argv)
    pts = load_points(args.input)
    target = float(pts[-1]["target"])
    cycles = split_cycles(pts)

    per_cycle = evaluate(cycles, target)
    keys = list(per_cycle)
    if not keys:
        print("Not enough tight cycles with >=2 priors to evaluate.")
        return 1
    cur = [v for k in keys for v in per_cycle[k]["a"]]
    sha = [v for k in keys for v in per_cycle[k]["s"]]
    covc = [v for k in keys for v in per_cycle[k]["covc"]]
    covs = [v for k in keys for v in per_cycle[k]["covs"]]

    print(f"Evaluated {len(keys)} tight cycles, {len(cur)} paired stage-predictions.\n")
    def cb(metric, nboot=4000):
        if len(keys) < 2:
            return None
        rng = np.random.default_rng(3)
        vals = [np.mean([v for k in rng.choice(keys, len(keys), replace=True)
                         for v in per_cycle[k][metric]]) for _ in range(nboot)]
        lo, hi = np.percentile(vals, [2.5, 97.5])
        return [round(float(lo), 1), round(float(hi), 1)]
    print(f"  current analogue   MAE {np.mean(cur):6.1f} min (CI {cb('a')}) | "
          f"80% cov {100*np.mean(covc):4.0f}% (CI {[round(100*x) for x in cb('covc')]})")
    print(f"  shape-aware        MAE {np.mean(sha):6.1f} min (CI {cb('s')}) | "
          f"80% cov {100*np.mean(covs):4.0f}% (CI {[round(100*x) for x in cb('covs')]})")

    paired = cluster_bootstrap_paired(per_cycle)
    if paired:
        d, ci = paired
        print(f"\n  PAIRED  shape - current = {d:+.2f} min, 95% CI {ci}")
        verdict = ("SHIP: challenger better, CI excludes 0" if ci[1] < 0 else
                   "REJECT: challenger worse, CI excludes 0" if ci[0] > 0 else
                   "NO DECISION: CI straddles 0 — no more than noise (keep incumbent)")
        print(f"  VERDICT: {verdict}")

    # ---- adversarial checks ------------------------------------------------
    print("\n  Per-cycle paired mean diff (shape - current), min:")
    fragile = []
    for k in keys:
        dk = np.mean(per_cycle[k]["s"]) - np.mean(per_cycle[k]["a"])
        n = len(per_cycle[k]["a"])
        print(f"    cycle {k+1:2d}: {dk:+6.1f}  (n={n})")
        fragile.append((k, dk))
    # leave-one-cycle-out: does removing any single cycle flip the sign of the mean diff?
    print("\n  Leave-one-cycle-out on the pooled paired diff:")
    worst = None
    for drop in keys:
        rem = [kk for kk in keys if kk != drop]
        a = [v for kk in rem for v in per_cycle[kk]["a"]]
        s = [v for kk in rem for v in per_cycle[kk]["s"]]
        dd = np.mean(s) - np.mean(a)
        if worst is None or dd > worst[1]:
            worst = (drop, dd)
    print(f"    most adverse drop = cycle {worst[0]+1}: pooled diff still {worst[1]:+.1f} min")

    # pace-shrink sensitivity: does the win survive the hyperparameter, and is it
    # the pace-borrowing or just the diurnal re-timing that helps?  pace_shrink→inf
    # forces m=1 (pure current-phase diurnal re-timing, no per-analogue pace).
    print("\n  pace_shrink sensitivity (paired mean diff vs current, min):")
    for ps in [0.0, 200.0, 400.0, 800.0, 1e12]:
        pc = {}
        tight = tight_cycle_indices(cycles, target)
        for ci in tight:
            prior = list(range(ci))
            if len(prior) < 2:
                continue
            fire, _ = cycle_fire_time(cycles[ci], target)
            if fire is None:
                continue
            t, yy = cycle_arrays(cycles[ci])
            aa, ss = [], []
            for i in range(3, len(t) + 1):
                now, coll = cycles[ci][i - 1]["_t"], yy[i - 1]
                qc = analogue_quantiles(cycles, prior, target, now, coll, [0.5])
                fc = shape_analogue_forecast(cycles, prior, target, now, coll, pace_shrink=ps)
                if qc is None or fc is None:
                    continue
                med = wquantile(fc["preds"], fc["w"], [0.5])[0]
                aa.append(abs(qc[0] - fire) / 60)
                ss.append(abs(med - fire) / 60)
            if aa:
                pc[ci] = {"a": aa, "s": ss}
        a = [v for kk in pc for v in pc[kk]["a"]]
        s = [v for kk in pc for v in pc[kk]["s"]]
        tag = "(m=1: pure diurnal re-time)" if ps > 1e9 else ("(no shrink)" if ps == 0 else "")
        print(f"    pace_shrink={ps:>10.0f}: {np.mean(s)-np.mean(a):+6.1f}  {tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

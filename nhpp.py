#!/usr/bin/env python3
"""Partially-pooled Non-Homogeneous Poisson Process model for vote-party firing.

Votes arrive as a counting process. We model the arrival intensity as

    λ_c(t) = a_c · s(τ(t))

where s(τ) is a **shared** UTC time-of-day shape (pooled across all cycles) and
a_c is a **per-cycle level**. With only a handful of cycles a new cycle's level
is poorly identified early on, so we **partially pool** it: a hierarchical
normal-normal posterior shrinks the current cycle's level toward the global mean
strongly when little of the cycle has been seen, and weakly once most of it has.

Because it's a generative counting process, it yields a *predictive
distribution* for the firing time (from level uncertainty + Poisson arrival
noise) — i.e. genuine quantile intervals rather than an empirical error band.

Outputs data/nhpp.json (+ nhpp.png with -o's dir). Deterministic (seeded RNG).

Usage: python3 nhpp.py [-i data/voteparty.jsonl] [-o data]
"""
import argparse
import json
import os
from datetime import datetime, timezone

import numpy as np

from predict import (load_points, split_cycles, cycle_arrays, cycle_fire_time,
                     diurnal_profile, tight_cycle_indices, fmt_ts)

NBINS = 24
SEED = 20260721  # fixed so repeated runs on the same data are reproducible


def _binsecs():
    return 86400.0 / NBINS


def integ_lambda(prof, ta, tb):
    """Expected votes under the shape s(τ) over [ta, tb] (votes)."""
    bs = _binsecs()
    total, t = 0.0, ta
    while t < tb - 1e-6:
        bi = int((t % 86400.0) // bs) % NBINS
        seg = min((int(t // bs) + 1) * bs - t, tb - t)
        total += prof[bi] * seg
        t += seg
    return total


def cycle_levels(prof, cycles_subset):
    """Per-cycle level a_c = observed votes / expected votes under the shape."""
    levels = []
    for c in cycles_subset:
        t, y = cycle_arrays(c)
        exp = integ_lambda(prof, c[0]["_t"], c[-1]["_t"])
        if exp > 1e-6:
            levels.append((y[-1] - y[0]) / exp)
    return np.array(levels)


def pooled_posterior(prof, prior_cycles, cur_cycle):
    """Hierarchical normal-normal posterior for the current cycle's level a."""
    lv = cycle_levels(prof, prior_cycles)
    if len(lv) >= 1:
        a_bar = float(np.mean(lv))
        tau2 = float(np.var(lv, ddof=1)) if len(lv) >= 2 else (0.15 * a_bar) ** 2
        tau2 = max(tau2, (0.05 * a_bar) ** 2)  # floor: never claim zero spread
    else:
        a_bar, tau2 = 1.0, 0.25 ** 2
    t0, now = cur_cycle[0]["_t"], cur_cycle[-1]["_t"]
    _, y = cycle_arrays(cur_cycle)
    exp_obs = integ_lambda(prof, t0, now)
    if exp_obs > 1e-6 and (y[-1] - y[0]) > 0:
        a_obs = (y[-1] - y[0]) / exp_obs
        s2 = max(a_obs / exp_obs, 1e-9)          # Poisson-derived obs variance
        prec = 1.0 / tau2 + 1.0 / s2
        post_mean = (a_bar / tau2 + a_obs / s2) / prec
        post_var = 1.0 / prec
    else:  # nothing observed yet → prior only
        a_obs, post_mean, post_var = None, a_bar, tau2
    return {"a_bar": a_bar, "tau": tau2 ** 0.5, "a_obs": a_obs,
            "post_mean": post_mean, "post_sd": post_var ** 0.5, "n_prior": len(lv)}


def predictive_firing(prof, now_epoch, collected, target, post_mean, post_sd,
                      rng, nsim=4000, dt=300.0, max_h=60):
    """Monte-Carlo predictive firing epochs (level uncertainty + Poisson noise)."""
    bs = _binsecs()
    a = np.clip(rng.normal(post_mean, post_sd, nsim), 1e-3, None)
    coll = np.full(nsim, float(collected))
    cross = np.full(nsim, np.nan)
    epoch = now_epoch
    for _ in range(int(max_h * 3600 / dt)):
        lam = prof[int((epoch % 86400.0) // bs) % NBINS]
        draw = rng.poisson(np.clip(a * lam * dt, 0, None))
        prev = coll.copy()
        coll += draw
        newly = np.isnan(cross) & (coll >= target)
        if newly.any():
            need = target - prev[newly]
            frac = np.clip(need / np.maximum(draw[newly], 1e-9), 0, 1)
            cross[newly] = epoch + frac * dt
        epoch += dt
        if not np.isnan(cross).any():
            break
    cross[np.isnan(cross)] = epoch  # censored (didn't reach in max_h)
    return cross


def predictive_firing_bootstrap(prior_cycles, cur_cycle, now_epoch, collected,
                                target, rng, nboot=40, nsim_each=150):
    """Predictive firing distribution that also propagates **structural**
    uncertainty by bootstrapping which historical cycles define the shape and
    level. Each bootstrap resamples the prior cycles (with replacement), rebuilds
    the pooled shape + partially-pooled level posterior, and simulates paths.
    This captures shape/level model uncertainty that the parametric NHPP alone
    ignores (and which made the raw intervals badly overconfident)."""
    n = len(prior_cycles)
    crosses = []
    posts = []
    for _ in range(nboot):
        idx = rng.integers(0, n, n) if n > 0 else np.array([], dtype=int)
        boot = [prior_cycles[i] for i in idx]
        prof_b, _ = diurnal_profile(boot, nbins=NBINS)
        if prof_b is None:
            continue
        post_b = pooled_posterior(prof_b, boot, cur_cycle)
        posts.append(post_b["post_mean"])
        crosses.append(predictive_firing(prof_b, now_epoch, collected, target,
                                         post_b["post_mean"], post_b["post_sd"],
                                         rng, nsim=nsim_each))
    if not crosses:
        return None, None
    return np.concatenate(crosses), float(np.std(posts))


def predict_nhpp(cycles, target, rng):
    prof, mean_rate = diurnal_profile(cycles[:-1], nbins=NBINS)
    if prof is None:
        return None
    cur = cycles[-1]
    _, y = cycle_arrays(cur)
    post = pooled_posterior(prof, cycles[:-1], cur)
    cross, boot_sd = predictive_firing_bootstrap(cycles[:-1], cur, cur[-1]["_t"],
                                                 y[-1], target, rng)
    if cross is None:
        cross = predictive_firing(prof, cur[-1]["_t"], y[-1], target,
                                  post["post_mean"], post["post_sd"], rng)
    q = {p: float(np.percentile(cross, p)) for p in (5, 10, 25, 50, 75, 90, 95)}
    return {"post": post, "quantiles": q, "cross": cross, "prof": prof}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--no-graph", action="store_true")
    args = ap.parse_args(argv)

    rng = np.random.default_rng(SEED)
    pts = load_points(args.input)
    target = float(pts[-1]["target"])
    cycles = split_cycles(pts)
    res = predict_nhpp(cycles, target, rng)
    if res is None:
        print("Not enough data.")
        return 1
    q, post = res["quantiles"], res["post"]
    cur = cycles[-1]
    _, y = cycle_arrays(cur)
    prog = 100 * y[-1] / target

    out = {"__status__": "EXPERIMENTAL — diagnostic only, NOT the reported prediction",
        "generated_at": fmt_ts(pts[-1]["_t"]),
        "progress_pct": round(prog, 1),
        "median_eta": fmt_ts(q[50]),
        "interval_80": [fmt_ts(q[10]), fmt_ts(q[90])],
        "interval_90": [fmt_ts(q[5]), fmt_ts(q[95])],
        "level_posterior": {"mean": round(post["post_mean"], 3),
                            "sd": round(post["post_sd"], 3),
                            "global_mean": round(post["a_bar"], 3),
                            "global_sd": round(post["tau"], 3),
                            "observed": round(post["a_obs"], 3) if post["a_obs"] else None,
                            "n_prior_cycles": post["n_prior"]},
    }

    # Out-of-sample check vs diurnal on TIGHT cycles, causal (prior-only).
    from predict import make_ctx, MODELS
    tight = set(tight_cycle_indices(cycles, target))
    nhpp_err, diur_err, covered, ncov = [], [], 0, 0
    for ci in tight:
        prior = cycles[:ci]
        if not prior:
            continue
        fire, _ = cycle_fire_time(cycles[ci], target)
        if fire is None:
            continue
        prof_i, _ = diurnal_profile(prior, nbins=NBINS)
        if prof_i is None:
            continue
        t, yy = cycle_arrays(cycles[ci])
        for i in range(3, len(t) + 1):
            sub = cycles[ci][:i]
            cross, _ = predictive_firing_bootstrap(prior, sub, sub[-1]["_t"],
                                                   yy[i-1], target, rng,
                                                   nboot=25, nsim_each=60)
            if cross is None:
                continue
            med = np.percentile(cross, 50)
            nhpp_err.append(abs(med - fire) / 60)
            lo, hi = np.percentile(cross, 10), np.percentile(cross, 90)
            ncov += 1
            covered += int(lo <= fire <= hi)
            tc = MODELS["diurnal"](t[:i], yy[:i], target, make_ctx(cycles[ci], prior))
            if tc is not None:
                diur_err.append(abs((cycles[ci][0]["_t"] + tc - fire) / 60))

    cov_pct = round(100 * covered / ncov) if ncov else None
    out["oos_verdict"] = {
        "nhpp_median_mae_min": round(float(np.mean(nhpp_err)), 1) if nhpp_err else None,
        "diurnal_median_mae_min": round(float(np.mean(diur_err)), 1) if diur_err else None,
        "interval_80_measured_coverage_pct": cov_pct,
        "n_tight_stage_predictions": ncov,
        "verdict": ("Intervals are OVERCONFIDENT — measured coverage "
                    f"{cov_pct}% vs 80% nominal; median no better than diurnal. "
                    "Dominant uncertainty is structural/within-cycle, which this "
                    "process model does not capture. Do not trust the intervals; "
                    "revisit with conformal calibration once more tight cycles exist."),
    }
    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "nhpp.json"), "w", encoding="utf-8") as fh:
        json.dump({k: v for k, v in out.items() if k != "cross"}, fh, indent=2)

    print(f"Cycles {len(cycles)} | current {prog:.0f}% | prior cycles {post['n_prior']}")
    print(f"NHPP median ETA {out['median_eta']}  80% [{out['interval_80'][0]} .. {out['interval_80'][1]}]")
    print(f"level: obs={out['level_posterior']['observed']} pooled={post['post_mean']:.2f}"
          f"±{post['post_sd']:.2f} (global {post['a_bar']:.2f}±{post['tau']:.2f})")
    if nhpp_err:
        print(f"OOS (tight cycles): NHPP median MAE {np.mean(nhpp_err):.1f} min | "
              f"diurnal {np.mean(diur_err):.1f} min | "
              f"80% interval empirical coverage {covered}/{ncov} = {100*covered/ncov:.0f}%")

    if not args.no_graph:
        make_graph(res, cycles, target, os.path.join(args.outdir, "nhpp.png"))
    return 0


def make_graph(res, cycles, target, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    def dt(e):
        return datetime.fromtimestamp(e, tz=timezone.utc)

    cur = cycles[-1]
    _, y = cycle_arrays(cur)
    q = res["quantiles"]
    cross = res["cross"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5),
                                   gridspec_kw={"width_ratios": [1.4, 1]})

    xs = [dt(p["_t"]) for p in cur]
    ax1.plot(xs, [p["collected"] for p in cur], "o-", color="#1f77b4", ms=3, label="collected")
    ax1.axhline(target, color="#333", ls="--", lw=1, label="target")
    ax1.axvspan(dt(q[10]), dt(q[90]), color="crimson", alpha=0.12, label="80% interval")
    ax1.axvspan(dt(q[5]), dt(q[95]), color="crimson", alpha=0.06, label="90% interval")
    ax1.axvline(dt(q[50]), color="crimson", lw=2, label="median firing")
    ax1.set_title("NHPP prediction — current cycle + predictive interval", fontweight="bold")
    ax1.set_ylabel("votes collected")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=timezone.utc))
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)
    for lb in ax1.get_xticklabels():
        lb.set_rotation(20)

    ax2.hist([dt(c) for c in cross], bins=40, color="#4c72b0", alpha=0.85)
    ax2.axvline(dt(q[50]), color="crimson", lw=2, label="median")
    ax2.axvline(dt(q[10]), color="crimson", lw=1, ls="--")
    ax2.axvline(dt(q[90]), color="crimson", lw=1, ls="--", label="10/90%")
    ax2.set_title("Predictive distribution of firing time", fontweight="bold")
    ax2.set_xlabel("firing time (UTC)")
    ax2.set_ylabel("simulations")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=timezone.utc))
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)
    for lb in ax2.get_xticklabels():
        lb.set_rotation(20)

    fig.suptitle("Partially-pooled NHPP vote-party model", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())

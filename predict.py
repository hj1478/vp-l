#!/usr/bin/env python3
"""EarthMC vote party — ensemble ETA predictor + grapher.

Reads the collected time series (data/voteparty.jsonl), splits it into vote
party *cycles* (a cycle ends when the counter resets after a party fires),
fits several independent forecasting models to the current cycle, weights them
by how well they extrapolated on the *completed* historical cycles
(rolling-origin backtest), and produces an ensemble estimate of when the next
vote party will fire.

Outputs (all under data/):
    prediction.png   — graph of the current cycle, model projections, ensemble
    prediction.json  — machine-readable per-model + ensemble prediction
    PREDICTION.md    — human-readable summary (regenerated every run)

The prediction is recomputed from scratch on every run, so it changes as new
data arrives.

Models (all forecast the time at which `collected` reaches `target`):
    shrinkage   — Bayesian blend of the historical rate prior and the observed
                  rate; leans on history early, on live data late (best early)
    linear      — ordinary least squares on the whole cycle
    recent      — slope of the last k points (short-term rate)
    ewma        — exponentially weighted average of per-interval rates
    theilsen    — Theil–Sen robust median-slope regression
    wls         — least squares with exponential recency weights
    quadratic   — 2nd-order fit, solves for the target crossing (captures accel)

The vote process is roughly stationary across cycles (historical cycles all
average ~390–480 votes/hr with player count only weakly correlated, r≈0.1), so
the historical rate is a strong prior — which is what the shrinkage model
exploits to fix the large early-cycle errors the pure-extrapolation models make.
"""

import argparse
import json
import os
from datetime import datetime, timezone

import numpy as np

# How much the historical prior is worth, in units of "fraction of a full
# cycle" of live observation. Tuned via the accuracy backtest (see accuracy.py):
# the vote process is nearly stationary across cycles (prior rates 393/411/407
# votes/hr), so a strong prior sharply cuts early-cycle error. 1.0 keeps most of
# that gain while still letting a genuinely hot/cold live cycle pull the rate.
SHRINK_W_PRIOR = 1.0

# Progress buckets (percent of target) for stage-aware ensemble weighting.
BUCKETS = [(0, 50), (50, 75), (75, 101)]

# ----------------------------------------------------------------------------
# Data loading & cycle segmentation
# ----------------------------------------------------------------------------

def parse_ts(s: str) -> float:
    """ISO-8601 (…Z) -> POSIX seconds."""
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def fmt_ts(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def display_granularity_min(half_width_min):
    """Round display precision to match interval resolution. Quoting a to-the-
    minute time when the interval is ±hours is a lie of format."""
    hw = abs(half_width_min or 0)
    if hw >= 120:
        return 60
    if hw >= 45:
        return 30
    if hw >= 20:
        return 15
    if hw >= 8:
        return 5
    return 1


def fmt_ts_rounded(epoch, gran_min):
    """Format an epoch rounded to `gran_min` minutes, as UTC HH:MM (or a date+HH:MM
    if it helps). Point precision = interval precision."""
    g = gran_min * 60
    e = round(epoch / g) * g
    d = datetime.fromtimestamp(e, tz=timezone.utc)
    return d.strftime("%Y-%m-%d %H:%MZ")


def load_points(path: str) -> list[dict]:
    pts = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("collected") is None or d.get("target") is None:
                continue
            d["_t"] = parse_ts(d["timestamp"])
            pts.append(d)
    pts.sort(key=lambda d: d["_t"])
    return pts


def split_cycles(points: list[dict]) -> list[list[dict]]:
    """Split into cycles. A new cycle begins when `collected` drops (reset)."""
    cycles: list[list[dict]] = []
    cur: list[dict] = []
    for p in points:
        if cur and p["collected"] < cur[-1]["collected"] - 1:
            cycles.append(cur)
            cur = []
        cur.append(p)
    if cur:
        cycles.append(cur)
    return cycles


def cycle_arrays(cycle: list[dict]):
    """Return (t seconds from cycle start, y collected) as float arrays."""
    t0 = cycle[0]["_t"]
    t = np.array([p["_t"] - t0 for p in cycle], dtype=float)
    y = np.array([float(p["collected"]) for p in cycle], dtype=float)
    return t, y


def make_ctx(cycle, train_cycles):
    """Context passed to history-aware models."""
    return {"t0": cycle[0]["_t"], "train_cycles": train_cycles or []}


def cycle_fire_time(cycle, target, seg=3):
    """Estimate the epoch at which a completed cycle actually hit target, by
    extrapolating its final `seg` observed points to the target line.

    Returns (epoch, quality) where quality is the last observed percent of
    target (higher = tighter reference). Used both as backtest labels and by
    the accuracy report.
    """
    t, y = cycle_arrays(cycle)
    t0 = cycle[0]["_t"]
    k = min(seg, len(t))
    if k < 2:
        return None, 0.0
    b, a = np.polyfit(t[-k:], y[-k:], 1)
    if b <= 1e-9:
        return None, 0.0
    t_cross = (target - a) / b
    return t0 + max(t_cross, t[-1]), float(y[-1] / target * 100.0)


# Label quality. A completed cycle's firing time is bracketed by the gap between
# its last sub-target sample and the first post-reset sample — but that gap
# OVERSTATES the uncertainty: when the last sample is near target, extrapolating
# the trajectory to 5000 pins the firing much tighter (a cycle last seen at 98%
# with 92 votes to go is known to ~2 min even if the raw gap is 86 min). So the
# real label uncertainty is the *extrapolation* sigma, not the sample gap.
TIGHT_LABEL_MIN = 15.0          # a cycle is "tight" if its label sigma <= this (min)
LABEL_RATE_UNCERT = 0.20        # relative rate uncertainty over the remaining extrapolation
SAMPLING_FLOOR_MIN = 2.5        # +/- half the 5-min poll interval


def fire_bracket_min(cycles, ci):
    """Raw sample-gap bracket (minutes) between last pre-reset and first
    post-reset sample. Upper bound on label uncertainty. None if not completed."""
    if ci >= len(cycles) - 1:
        return None
    return (cycles[ci + 1][0]["_t"] - cycles[ci][-1]["_t"]) / 60.0


def label_sigma_min(cycles, ci, target):
    """Uncertainty (minutes) of a completed cycle's firing time, from
    extrapolating its final trajectory to target. = (votes remaining at the last
    sample / end-rate) x rate uncertainty, floored at the sampling resolution and
    capped by the raw bracket. None for the (unfinished) current cycle.

    This recovers cycles the raw-bracket gate wrongly discarded: a cycle sampled
    to 98% has a tiny label sigma even if the collector then went dark for an hour.
    """
    if ci >= len(cycles) - 1:
        return None
    c = cycles[ci]
    t, y = cycle_arrays(c)
    left = target - y[-1]
    raw = fire_bracket_min(cycles, ci)
    if left <= 0:
        return SAMPLING_FLOOR_MIN
    k = min(4, len(t))
    if len(t) < 2 or t[-1] <= t[-k]:
        return raw
    r = (y[-1] - y[-k]) / (t[-1] - t[-k])           # end-rate, votes/sec
    if r <= 0:
        return raw
    extrap_min = (left / r) / 60.0                  # minutes to extrapolate to target
    sigma = extrap_min * LABEL_RATE_UNCERT
    if raw is not None:
        sigma = min(sigma, raw)                     # can't beat the hard bracket
    return max(sigma, SAMPLING_FLOOR_MIN)


def label_weight(cycles, ci, target):
    """Inverse-variance weight for a cycle in scoring/selection: 1/sigma^2,
    normalised so a tight (sampling-floor) cycle has weight 1.0."""
    s = label_sigma_min(cycles, ci, target)
    if s is None:
        return 0.0
    return (SAMPLING_FLOOR_MIN ** 2) / (s ** 2)


def tight_cycle_indices(cycles, target=5000.0, max_sigma=TIGHT_LABEL_MIN):
    """Indices of completed cycles whose firing time is known tightly (by the
    extrapolation sigma, not the raw sample gap)."""
    return [ci for ci in range(len(cycles) - 1)
            if (label_sigma_min(cycles, ci, target) or 1e9) <= max_sigma]


# ----------------------------------------------------------------------------
# Shared rate helpers
# ----------------------------------------------------------------------------

def robust_slope(t, y):
    """Theil–Sen slope (votes/sec); falls back to endpoint slope."""
    n = len(t)
    if n >= 3:
        slopes = [(y[j] - y[i]) / (t[j] - t[i])
                  for i in range(n) for j in range(i + 1, n) if t[j] != t[i]]
        if slopes:
            return float(np.median(slopes))
    if n >= 2 and t[-1] > t[0]:
        return (y[-1] - y[0]) / (t[-1] - t[0])
    return None


def pooled_rate(train_cycles):
    """Historical prior rate (votes/sec): duration-weighted mean of per-cycle
    OLS slopes across completed cycles."""
    if not train_cycles:
        return None
    rates, wts = [], []
    for c in train_cycles:
        t, y = cycle_arrays(c)
        if len(t) >= 2 and t[-1] > t[0]:
            b, _ = np.polyfit(t, y, 1)
            if b > 1e-9:
                rates.append(b)
                wts.append(t[-1] - t[0])
    if not rates:
        return None
    return float(np.average(rates, weights=wts))


# Content-keyed memo for the profile builders. Inside a backtest the same
# training set is used at every stage-point of a cycle, so without this the
# (identical) profile is rebuilt hundreds of times per run.
_PROFILE_CACHE = {}


def _cycles_key(train_cycles):
    return tuple((round(c[0]["_t"]), round(c[-1]["_t"]), len(c))
                 for c in (train_cycles or []))


def diurnal_profile(train_cycles, nbins=24, smooth=1):
    """Average vote rate (votes/sec) as a function of UTC hour-of-day, learned
    from history. Each observed interval contributes its rate to every hour it
    overlaps, weighted by overlap duration, so long sparse intervals still
    inform the profile. Circularly smoothed. Returns (profile[nbins], mean_rate)
    or (None, None) if there is not enough data. Memoized on training-set content."""
    ckey = ("d", nbins, smooth, _cycles_key(train_cycles))
    if ckey in _PROFILE_CACHE:
        return _PROFILE_CACHE[ckey]
    binsecs = 86400.0 / nbins
    num = np.zeros(nbins)
    den = np.zeros(nbins)
    all_rates = []
    for c in train_cycles or []:
        for a, b in zip(c[:-1], c[1:]):
            dt = b["_t"] - a["_t"]
            if dt <= 0 or b["collected"] < a["collected"]:
                continue
            rate = (b["collected"] - a["collected"]) / dt  # votes/sec
            all_rates.append((rate, dt))
            # distribute over the hour-bins the interval spans
            tcur = a["_t"]
            remaining = dt
            while remaining > 1e-6:
                sod = tcur % 86400.0
                b_idx = int(sod // binsecs) % nbins
                edge = (b_idx + 1) * binsecs
                seg = min(edge - sod, remaining)
                num[b_idx] += rate * seg
                den[b_idx] += seg
                tcur += seg
                remaining -= seg
    if den.sum() <= 0:
        _PROFILE_CACHE[ckey] = (None, None)
        return None, None
    mean_rate = float(np.average([r for r, _ in all_rates],
                                 weights=[w for _, w in all_rates]))
    prof = np.where(den > 0, num / np.maximum(den, 1e-9), mean_rate)
    # circular smoothing
    if smooth > 0:
        k = 2 * smooth + 1
        prof = np.array([prof[(i + o) % nbins]
                         for i in range(nbins)
                         for o in range(-smooth, smooth + 1)]).reshape(nbins, k).mean(axis=1)
    _PROFILE_CACHE[ckey] = (prof, mean_rate)
    return prof, mean_rate


def day_type(epoch):
    """UTC weekday vs weekend — a coarse (2-way) split that's estimable with
    only a few days of data, unlike a full 7-way day-of-week split."""
    return "weekend" if datetime.fromtimestamp(epoch, tz=timezone.utc).weekday() >= 5 else "weekday"


def diurnal_profile_grouped(train_cycles, nbins=24):
    """Vote-rate profile conditioned on (day_type, UTC hour), plus the pooled
    time-of-day profile and per-bin sample weights, so a model can blend the two
    hierarchically. Returns a dict or None.

    NOTE on timezones: everything is UTC. The vote rate is a global-playerbase
    phenomenon whose peaks/lulls sit at fixed UTC hours, so UTC hour-of-day is
    the correct shared frame — no per-user timezone conversion is meaningful.
    Memoized on training-set content.
    """
    ckey = ("g", nbins, _cycles_key(train_cycles))
    if ckey in _PROFILE_CACHE:
        return _PROFILE_CACHE[ckey]
    binsecs = 86400.0 / nbins
    groups = ["weekday", "weekend"]
    num = {g: np.zeros(nbins) for g in groups}
    den = {g: np.zeros(nbins) for g in groups}
    gnum = np.zeros(nbins)
    gden = np.zeros(nbins)
    all_rates = []
    for c in train_cycles or []:
        for a, b in zip(c[:-1], c[1:]):
            dt = b["_t"] - a["_t"]
            if dt <= 0 or b["collected"] < a["collected"]:
                continue
            rate = (b["collected"] - a["collected"]) / dt
            all_rates.append((rate, dt))
            tcur, remaining = a["_t"], dt
            while remaining > 1e-6:
                sod = tcur % 86400.0
                bi = int(sod // binsecs) % nbins
                seg = min((bi + 1) * binsecs - sod, remaining)
                g = day_type(tcur)
                num[g][bi] += rate * seg
                den[g][bi] += seg
                gnum[bi] += rate * seg
                gden[bi] += seg
                tcur += seg
                remaining -= seg
    if gden.sum() <= 0:
        _PROFILE_CACHE[ckey] = None
        return None
    mean_rate = float(np.average([r for r, _ in all_rates],
                                 weights=[w for _, w in all_rates]))
    gprof = np.where(gden > 0, gnum / np.maximum(gden, 1e-9), mean_rate)
    profs = {g: np.where(den[g] > 0, num[g] / np.maximum(den[g], 1e-9), gprof)
             for g in groups}
    counts = {g: den[g] / 3600.0 for g in groups}  # bin sample weight in hours
    res = {"groups": profs, "counts": counts, "global": gprof, "mean": mean_rate}
    _PROFILE_CACHE[ckey] = res
    return res


def shrink_rate(t, y, target, ctx, w_prior=None):
    """Precision-weighted blend of historical prior and observed rate.

    Weight on the observed rate grows with cycle progress (fraction of target
    collected), so early on the estimate is anchored to the historical prior
    and late on it follows the live data.
    """
    if w_prior is None:
        w_prior = SHRINK_W_PRIOR
    prior = pooled_rate(ctx.get("train_cycles")) if ctx else None
    obs = robust_slope(t, y)
    if prior is None and (obs is None or obs <= 1e-9):
        return None
    if prior is None:
        return obs if obs and obs > 1e-9 else None
    if obs is None or obs <= 1e-9:
        return prior
    frac = min(max(float(y[-1]) / target, 0.0), 1.0)
    rate = (w_prior * prior + frac * obs) / (w_prior + frac)
    return rate if rate > 1e-9 else None


# ----------------------------------------------------------------------------
# Models — each returns predicted seconds-from-cycle-start at which y == target,
# given partial data (t, y). Return None when it cannot produce a sane estimate.
# All accept an optional ctx (history); simple models ignore it.
# ----------------------------------------------------------------------------

def _cross_from_line(slope, intercept, target, t_last):
    if slope <= 1e-9:
        return None
    return max((target - intercept) / slope, t_last)


def model_linear(t, y, target, ctx=None):
    if len(t) < 2:
        return None
    b, a = np.polyfit(t, y, 1)
    return _cross_from_line(b, a, target, t[-1])


def model_recent(t, y, target, ctx=None, k=6):
    if len(t) < 2:
        return None
    k = min(k, len(t))
    tt, yy = t[-k:], y[-k:]
    if tt[-1] - tt[0] <= 0:
        return None
    slope = (yy[-1] - yy[0]) / (tt[-1] - tt[0])
    if slope <= 1e-9:
        return None
    return t[-1] + (target - y[-1]) / slope


def model_ewma(t, y, target, ctx=None, halflife=3):
    if len(t) < 2:
        return None
    dt, dy = np.diff(t), np.diff(y)
    ok = dt > 0
    if not ok.any():
        return None
    rates = dy[ok] / dt[ok]
    n = len(rates)
    decay = 0.5 ** (1.0 / max(halflife, 1e-9))
    w = decay ** np.arange(n - 1, -1, -1)
    rate = np.sum(w * rates) / np.sum(w)
    if rate <= 1e-9:
        return None
    return t[-1] + (target - y[-1]) / rate


def model_theilsen(t, y, target, ctx=None):
    if len(t) < 2:
        return None
    slope = robust_slope(t, y)
    if slope is None or slope <= 1e-9:
        return None
    intercept = float(np.median(y - slope * t))
    return _cross_from_line(slope, intercept, target, t[-1])


def model_wls(t, y, target, ctx=None, halflife=4):
    if len(t) < 2:
        return None
    n = len(t)
    decay = 0.5 ** (1.0 / max(halflife, 1e-9))
    w = decay ** np.arange(n - 1, -1, -1)
    W = np.diag(w)
    X = np.vstack([t, np.ones_like(t)]).T
    try:
        beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    except np.linalg.LinAlgError:
        return None
    return _cross_from_line(beta[0], beta[1], target, t[-1])


def model_quadratic(t, y, target, ctx=None):
    if len(t) < 3:
        return None
    c, b, a = np.polyfit(t, y, 2)
    if abs(c) < 1e-12:
        return _cross_from_line(b, a, target, t[-1])
    disc = b * b - 4 * c * (a - target)
    if disc < 0:
        return None
    roots = [(-b + s * np.sqrt(disc)) / (2 * c) for s in (1, -1)]
    future = [r for r in roots if r >= t[-1] - 1e-6]
    return min(future) if future else None


def model_shrinkage(t, y, target, ctx=None):
    if len(t) < 2:
        return None
    rate = shrink_rate(t, y, target, ctx)
    if rate is None:
        return None
    return t[-1] + (target - y[-1]) / rate


def _integrate_profile(rate_at, t, y, target, t0, nbins=24):
    """Forward-integrate a time-varying rate function `rate_at(epoch)` from the
    current point to target, scaled so the profile matches this cycle's recently
    observed level. Shared by the diurnal models. Returns t_cross or None."""
    binsecs = 86400.0 / nbins
    k = min(6, len(t))
    obs = robust_slope(t[-k:], y[-k:])
    scale = 1.0
    if obs is not None and obs > 1e-9:
        span0, span1 = t0 + t[-k], t0 + t[-1]
        samples = max(2, int((span1 - span0) // binsecs) + 1)
        prof_recent = np.mean([rate_at(span0 + i * (span1 - span0) / (samples - 1))
                               for i in range(samples)]) if span1 > span0 else rate_at(span1)
        if prof_recent > 1e-9:
            raw = obs / prof_recent
            frac = min(max(float(y[-1]) / target, 0.0), 1.0)
            scale = (1.0 + frac * raw) / (1.0 + frac)  # shrink toward 1 early
    epoch, collected, guard = t0 + t[-1], float(y[-1]), 0
    step = 300.0
    while collected < target and guard < int(4 * 86400 / step):
        collected += rate_at(epoch) * scale * step
        epoch += step
        guard += 1
    return (epoch - t0) if collected >= target else None


def model_diurnal(t, y, target, ctx=None, nbins=24):
    """Integrate the historical UTC time-of-day rate profile forward to target —
    predicting each stage with its own time-of-day rate, not one flat rate."""
    if ctx is None or len(t) < 2:
        return None
    prof, mean_rate = diurnal_profile(ctx.get("train_cycles"), nbins=nbins)
    if prof is None or mean_rate is None or mean_rate <= 1e-9:
        return None
    binsecs = 86400.0 / nbins
    rate_at = lambda e: prof[int((e % 86400.0) // binsecs) % nbins]
    return _integrate_profile(rate_at, t, y, target, ctx["t0"], nbins)


def model_diurnal_dow(t, y, target, ctx=None, nbins=24, bin_prior_hours=2.0):
    """Like `diurnal`, but the rate is conditioned on weekday vs weekend as well
    as UTC hour — with **hierarchical shrinkage**: each (day_type, hour) bin is
    blended toward the pooled time-of-day rate in proportion to how much data
    that bin has. With little history the day split barely moves anything (so it
    can't overfit); as weeks accumulate the weekend/weekday effect emerges. This
    is why it's a separate candidate model rather than a change to `diurnal`."""
    if ctx is None or len(t) < 2:
        return None
    gp = diurnal_profile_grouped(ctx.get("train_cycles"), nbins=nbins)
    if gp is None or gp["mean"] <= 1e-9:
        return None
    binsecs = 86400.0 / nbins

    def rate_at(epoch):
        bi = int((epoch % 86400.0) // binsecs) % nbins
        g = day_type(epoch)
        c = gp["counts"][g][bi]
        k = c / (c + bin_prior_hours)  # trust the group bin ∝ its sample weight
        return k * gp["groups"][g][bi] + (1.0 - k) * gp["global"][bi]

    return _integrate_profile(rate_at, t, y, target, ctx["t0"], nbins)


MODELS = {
    "shrinkage": model_shrinkage,
    "diurnal": model_diurnal,
    "diurnal_dow": model_diurnal_dow,
    "linear": model_linear,
    "recent": model_recent,
    "ewma": model_ewma,
    "theilsen": model_theilsen,
    "wls": model_wls,
    "quadratic": model_quadratic,
}


# ----------------------------------------------------------------------------
# Backtest: rolling-origin, predict held-out later points within each cycle.
# Weight each model by inverse mean squared extrapolation error.
# ----------------------------------------------------------------------------

def _bucket(progress):
    for lo, hi in BUCKETS:
        if lo <= progress < hi:
            return (lo, hi)
    return BUCKETS[-1]


# Occam / shrinkage prior. Hard inverse-error weights fit on a handful of cycles
# are dominated by sampling noise (a single cycle swings the top weight by ±0.4),
# so we shrink every weight vector toward uniform. The shrinkage λ = n/(n+prior)
# grows with the number of cycles: near-uniform now, differentiating only when
# many cycles give strong, stable evidence. This is why we no longer report a
# "winning" model until it is stable (see stable_winner()).
WEIGHT_PRIOR_CYCLES = 6


def _shrink_to_uniform(weights, n_cycles, prior=WEIGHT_PRIOR_CYCLES):
    m = len(MODELS)
    unif = 1.0 / m
    lam = n_cycles / (n_cycles + prior) if n_cycles > 0 else 0.0
    mixed = {n: (1 - lam) * unif + lam * weights.get(n, 0.0) for n in MODELS}
    s = sum(mixed.values())
    return {n: v / s for n, v in mixed.items()} if s > 0 else {n: unif for n in MODELS}


def _errs_to_weights(errs, n_cycles=0):
    rmse = {n: (float(np.sqrt(np.mean(e))) if e else None) for n, e in errs.items()}
    scored = {n: r for n, r in rmse.items() if r is not None and r > 0}
    if scored:
        inv = {n: 1.0 / (r * r) for n, r in scored.items()}
        s = sum(inv.values())
        weights = {n: inv[n] / s for n in inv}
    else:
        weights = {n: 1.0 / len(MODELS) for n in MODELS}
    return _shrink_to_uniform(weights, n_cycles), rmse


def backtest_staged(cycles: list[list[dict]], target: float, min_fit=3):
    """Rolling-origin backtest producing global and per-progress-bucket weights.

    Each model is scored by its **ETA error** — how far its predicted firing
    time is from the cycle's actual firing time — at every stage. This directly
    rewards crossing-prediction skill (a model that nails the next point but
    extrapolates the crossing badly is penalised, unlike a value-RMSE score).

    History-aware models get the *other* cycles as their prior (leave-one-out);
    the firing-time label is the cycle's own outcome (a supervised target, not a
    model input, so no leakage).

    Returns {"global": (weights, rmse), "buckets": {bucket: (weights, rmse)}}.
    Errors are in hours.
    """
    errs_global = {name: [] for name in MODELS}
    errs_bucket = {b: {name: [] for name in MODELS} for b in BUCKETS}
    n_used = 0
    for ci, cyc in enumerate(cycles):
        if len(cyc) < min_fit + 1:
            continue
        fire, _ = cycle_fire_time(cyc, target)
        if fire is None:
            continue
        n_used += 1
        others = [c for cj, c in enumerate(cycles) if cj != ci]
        ctx = make_ctx(cyc, others)
        t, y = cycle_arrays(cyc)
        t0 = cyc[0]["_t"]
        for i in range(min_fit, len(t) + 1):
            t_fit, y_fit = t[:i], y[:i]
            b = _bucket(float(y_fit[-1]) / target * 100.0)
            for name in MODELS:
                t_cross = MODELS[name](t_fit, y_fit, target, ctx)
                if t_cross is None:
                    continue
                e = ((t0 + t_cross - fire) / 3600.0) ** 2
                if np.isfinite(e):
                    errs_global[name].append(e)
                    errs_bucket[b][name].append(e)
    return {
        "global": _errs_to_weights(errs_global, n_used),
        "buckets": {b: _errs_to_weights(errs_bucket[b], n_used) for b in BUCKETS},
    }


def weights_for_progress(staged, progress, blend=0.5):
    """Blend bucket-specific weights with global weights for stability."""
    gw, _ = staged["global"]
    bw, _ = staged["buckets"][_bucket(progress)]
    names = set(gw) | set(bw)
    mixed = {n: blend * bw.get(n, 0.0) + (1 - blend) * gw.get(n, 0.0) for n in names}
    s = sum(mixed.values())
    return {n: v / s for n, v in mixed.items()} if s > 0 else gw


# PRE-REGISTERED stable-winner criterion (see PREREGISTRATION.md). Fixed BEFORE
# any model qualifies, so we can't move goalposts later. A model is the "stable
# winner" iff ALL of: (a) it has the lowest label-weighted MAE in every
# leave-one-cycle-out fold, (b) over at least STABLE_WINNER_MIN_CYCLES
# well-labeled cycles (label weight >= 0.25). Anything short of this is reported
# as "no stable winner".
STABLE_WINNER_MIN_CYCLES = 8
STABLE_WINNER_MIN_LABEL_WEIGHT = 0.25


def stable_winner(cycles, target, min_fit=3, min_label_weight=STABLE_WINNER_MIN_LABEL_WEIGHT):
    """Pre-registered stable-winner test (see PREREGISTRATION.md). Returns
    (winner_or_None, {cycle_index: fold_winner}). Names a winner only if one
    model wins every well-labeled LOO fold AND there are at least
    STABLE_WINNER_MIN_CYCLES such folds — so a 4-cycle fluke can't crown one.
    `cycles` is the full list (so the last completed cycle can see its successor
    for labeling)."""
    completed = cycles[:-1]
    fold_winners, per_cycle = [], {}
    for ci, cyc in enumerate(completed):
        if len(cyc) < min_fit + 1:
            continue
        if label_weight(cycles, ci, target) < min_label_weight:
            continue  # too loosely labeled to vote
        fire, _ = cycle_fire_time(cyc, target)
        if fire is None:
            continue
        others = [c for cj, c in enumerate(completed) if cj != ci]
        ctx = make_ctx(cyc, others)
        t, y = cycle_arrays(cyc)
        t0 = cyc[0]["_t"]
        errs = {n: [] for n in MODELS}
        for i in range(min_fit, len(t) + 1):
            for n in MODELS:
                tc = MODELS[n](t[:i], y[:i], target, ctx)
                if tc is not None:
                    errs[n].append(abs(t0 + tc - fire))
        maes = {n: float(np.mean(v)) for n, v in errs.items() if v}
        if maes:
            w = min(maes, key=maes.get)
            fold_winners.append(w)
            per_cycle[ci] = w
    if not fold_winners:
        return None, {}
    unanimous = len(set(fold_winners)) == 1
    enough = len(fold_winners) >= STABLE_WINNER_MIN_CYCLES
    winner = fold_winners[0] if (unanimous and enough) else None
    return winner, per_cycle


# ----------------------------------------------------------------------------
# Conditional analogue / curve library (nonparametric) — provides the calibrated
# predictive interval used by the primary prediction. The full model + graph
# live in analogue.py, which imports these primitives.
# ----------------------------------------------------------------------------

ANALOGUE_H_HOURS = 4.0   # UTC time-of-day kernel bandwidth
ANALOGUE_ALPHA = 0.7     # conditional vs uniform blend (partial pooling of weights)


def time_at_collected(cyc, c, target, fire):
    """Wall-clock epoch when a cycle reached `c` collected (interpolated, and
    extrapolated toward its firing time if c is above its last sample)."""
    t = [p["_t"] for p in cyc]
    y = [p["collected"] for p in cyc]
    if c <= y[0]:
        return t[0]
    if c <= y[-1]:
        for i in range(1, len(y)):
            if y[i] >= c:
                if y[i] == y[i - 1]:
                    return t[i]
                f = (c - y[i - 1]) / (y[i] - y[i - 1])
                return t[i - 1] + f * (t[i] - t[i - 1])
    if fire is not None and target > y[-1]:
        f = (c - y[-1]) / (target - y[-1])
        return t[-1] + min(max(f, 0.0), 1.0) * (fire - t[-1])
    return None


def analogue_forecast(cycles, lib_indices, target, now_epoch, collected,
                      h_hours=ANALOGUE_H_HOURS, alpha=ANALOGUE_ALPHA):
    """Similarity-weighted predictive firing epochs from the curve library.

    Also returns per-analogue label sigma (seconds): the uncertainty of the
    borrowed cycle's own firing time, so the interval can carry it forward rather
    than treating each borrowed endpoint as exact."""
    utc_now = now_epoch % 86400.0
    preds, wts, sig = [], [], []
    for li in lib_indices:
        L = cycles[li]
        fire, _ = cycle_fire_time(L, target)
        if fire is None:
            continue
        tc = time_at_collected(L, collected, target, fire)
        if tc is None:
            continue
        remaining = fire - tc
        if remaining < -60:
            continue
        d = abs((tc % 86400.0) - utc_now)
        d = min(d, 86400.0 - d)
        w = np.exp(-0.5 * (d / (h_hours * 3600.0)) ** 2)
        preds.append(now_epoch + max(remaining, 0.0))
        wts.append(w)
        sig.append((label_sigma_min(cycles, li, target) or SAMPLING_FLOOR_MIN) * 60.0)
    if not preds:
        return None
    preds = np.array(preds)
    wts = np.array(wts)
    unif = np.ones(len(wts)) / len(wts)
    wc = wts / wts.sum() if wts.sum() > 0 else unif
    w = alpha * wc + (1 - alpha) * unif
    w /= w.sum()
    return {"preds": preds, "w": w, "sigma": np.array(sig)}


def wquantile(vals, w, qs):
    o = np.argsort(vals)
    v, ww = vals[o], w[o]
    cw = np.cumsum(ww)
    cw /= cw[-1]
    return np.interp(qs, cw, v)


def analogue_quantiles(cycles, lib_indices, target, now_epoch, collected,
                       qs, nsim=6000, seed=1234):
    """Predictive firing-time quantiles from the analogue library, with each
    borrowed endpoint's label sigma Monte-Carlo'd into the spread (not treated as
    exact). THE single construction used both live and in OOS evaluation, so the
    measured coverage describes the interval we actually report. Deterministic."""
    fc = analogue_forecast(cycles, lib_indices, target, now_epoch, collected)
    if fc is None:
        return None
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(fc["preds"]), size=nsim, p=fc["w"])
    samples = fc["preds"][idx] + rng.normal(0.0, 1.0, nsim) * fc["sigma"][idx]
    return np.percentile(samples, [q * 100 for q in qs])


def analogue_interval(cycles, target, now_epoch, collected):
    """Live predictive interval (full library) for the current cycle."""
    q = analogue_quantiles(cycles, list(range(len(cycles) - 1)), target,
                           now_epoch, collected, [0.05, 0.1, 0.5, 0.9, 0.95])
    if q is None:
        return None
    return {"p05": q[0], "p10": q[1], "p50": q[2], "p90": q[3], "p95": q[4]}


# ----------------------------------------------------------------------------
# Shape-aware analogue — the plain analogue borrows each library cycle's
# ABSOLUTE remaining duration from the matching-progress point. If the library
# cycles fired during a different diurnal phase than the current cycle must
# cross to reach target, every borrowed duration is mis-timed by the diurnal
# "shape" error the LOO oracle identified (~10 min mid-cycle). This variant
# re-times each analogue: it forward-integrates the pooled diurnal rate profile
# from the CURRENT phase for the exactly-known remaining votes, borrowing only
# each analogue's pace *deviation* from that profile (heavily shrunk toward 1 —
# a near-inert safety valve; the paired win is flat whether or not it is used,
# so the improvement is the re-timing, not the pace-borrowing). Validated
# causally in shape_analogue.py: paired point improvement -11 min, 95% CI
# [-17, -4] over the plain analogue on tight cycles, with 80% interval coverage
# ~79% (better calibrated than the plain analogue's over-wide ~92%). See
# FINDINGS.md and PREREGISTRATION.md §2.
# ----------------------------------------------------------------------------
PACE_SHRINK_VOTES = 400.0   # trust an analogue's pace deviation ∝ votes of its
                            # remaining segment we actually observed; heavy shrink


def _dur_for_votes(rate_at, start_epoch, votes, step=300.0, max_days=4):
    """Seconds to accumulate `votes` from start_epoch under rate_at (votes/sec)."""
    if votes <= 0:
        return 0.0
    acc, epoch, guard = 0.0, start_epoch, 0
    lim = int(max_days * 86400 / step)
    while acc < votes and guard < lim:
        acc += rate_at(epoch) * step
        epoch += step
        guard += 1
    if acc < votes:
        return None
    over = acc - votes
    r = rate_at(epoch - step)
    frac_back = (over / (r * step)) if r > 1e-9 else 0.0
    return (epoch - start_epoch) - frac_back * step


def shape_analogue_forecast(cycles, lib_indices, target, now_epoch, collected,
                            h_hours=ANALOGUE_H_HOURS, alpha=ANALOGUE_ALPHA,
                            pace_shrink=PACE_SHRINK_VOTES):
    """Similarity-weighted predictive firing epochs, re-timed through the current
    diurnal phase. Returns {preds, w, sigma} like analogue_forecast, or None if
    the library can't build a diurnal profile (needs a couple of prior cycles)."""
    lib_cycles = [cycles[i] for i in lib_indices]
    prof, mean_rate = diurnal_profile(lib_cycles)
    if prof is None or mean_rate is None or mean_rate <= 1e-9:
        return None
    nbins = len(prof)
    binsecs = 86400.0 / nbins
    rate_at = lambda e: prof[int((e % 86400.0) // binsecs) % nbins]

    R = target - collected            # remaining votes — known exactly
    if R <= 0:
        return None
    utc_now = now_epoch % 86400.0

    preds, wts, sig = [], [], []
    for li in lib_indices:
        L = cycles[li]
        fire, _ = cycle_fire_time(L, target)
        if fire is None:
            continue
        tc = time_at_collected(L, collected, target, fire)
        if tc is None:
            continue
        dur_L = fire - tc             # analogue's actual remaining duration
        if dur_L < 60:
            continue
        dur_exp = _dur_for_votes(rate_at, tc, R)   # diurnal-expected, same phase
        if dur_exp is None or dur_exp < 60:
            continue
        m_raw = dur_L / dur_exp       # >1 slower than diurnal, <1 faster
        seen = min(R, max(0.0, L[-1]["collected"] - collected))
        denom = seen + pace_shrink
        k = (seen / denom) if denom > 0 else 0.0
        m = k * m_raw + (1.0 - k) * 1.0
        scaled = lambda e, m=m: rate_at(e) / m
        dur_fore = _dur_for_votes(scaled, now_epoch, R)   # re-timed to CURRENT phase
        if dur_fore is None:
            continue
        d = abs((tc % 86400.0) - utc_now)
        d = min(d, 86400.0 - d)
        w = np.exp(-0.5 * (d / (h_hours * 3600.0)) ** 2)
        preds.append(now_epoch + dur_fore)
        wts.append(w)
        sig.append((label_sigma_min(cycles, li, target) or SAMPLING_FLOOR_MIN) * 60.0)
    if not preds:
        return None
    preds = np.array(preds)
    wts = np.array(wts)
    unif = np.ones(len(wts)) / len(wts)
    wc = wts / wts.sum() if wts.sum() > 0 else unif
    w = alpha * wc + (1 - alpha) * unif
    w /= w.sum()
    return {"preds": preds, "w": w, "sigma": np.array(sig)}


def shape_analogue_quantiles(cycles, lib_indices, target, now_epoch, collected,
                             qs, nsim=6000, seed=1234):
    """Predictive firing-time quantiles from the shape-aware analogue, label-sigma
    Monte-Carlo'd into the spread. THE construction used both live and in OOS."""
    fc = shape_analogue_forecast(cycles, lib_indices, target, now_epoch, collected)
    if fc is None:
        return None
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(fc["preds"]), size=nsim, p=fc["w"])
    samples = fc["preds"][idx] + rng.normal(0.0, 1.0, nsim) * fc["sigma"][idx]
    return np.percentile(samples, [q * 100 for q in qs])


def shape_analogue_interval(cycles, target, now_epoch, collected):
    """Live shape-aware predictive interval (full library) for the current cycle."""
    q = shape_analogue_quantiles(cycles, list(range(len(cycles) - 1)), target,
                                 now_epoch, collected, [0.05, 0.1, 0.5, 0.9, 0.95])
    if q is None:
        return None
    return {"p05": q[0], "p10": q[1], "p50": q[2], "p90": q[3], "p95": q[4]}


# ----------------------------------------------------------------------------
# Prediction
# ----------------------------------------------------------------------------

def predict(cycles, target):
    """Run all models on the current (last) cycle, ensemble via backtest weights."""
    completed = cycles[:-1] if len(cycles) > 1 else cycles
    staged = backtest_staged(completed, target)
    _, rmse = staged["global"]
    cur = cycles[-1]
    ctx = make_ctx(cur, cycles[:-1])  # history = completed cycles
    t, y = cycle_arrays(cur)
    t0 = cur[0]["_t"]
    cur_progress = float(y[-1]) / target * 100.0
    weights = weights_for_progress(staged, cur_progress)

    per_model = {}
    for name, fn in MODELS.items():
        t_cross = fn(t, y, target, ctx)
        per_model[name] = {
            "eta_epoch": (t0 + t_cross) if t_cross is not None else None,
            "weight": weights.get(name, 0.0),
            "rmse": rmse.get(name),
        }

    valid = [(m["eta_epoch"], m["weight"]) for m in per_model.values()
             if m["eta_epoch"] is not None]
    if valid:
        etas = np.array([v[0] for v in valid])
        ws = np.array([v[1] for v in valid])
        ws = ws / ws.sum() if ws.sum() > 0 else np.ones_like(ws) / len(ws)
        ensemble_eta = float(np.sum(etas * ws))
        lo, hi = float(etas.min()), float(etas.max())
    else:
        ensemble_eta = lo = hi = None

    # PRIMARY = the SHAPE-AWARE analogue, used for BOTH point (its median) and
    # interval (its quantiles) — one coherent distribution, no grafting. It
    # re-times each borrowed analogue through the current diurnal phase; validated
    # causally to beat the plain analogue's point by -11 min (95% CI [-17, -4])
    # while being better-calibrated (~79% vs the plain analogue's over-wide ~92%
    # at nominal 80%). The gain is the diurnal re-timing, banking the LOO shape
    # oracle's headroom (see FINDINGS.md, PREREGISTRATION.md §2). Falls back to the
    # plain analogue when there aren't yet enough cycles to build a diurnal profile.
    # (diurnal / plain analogue remain in the table as diagnostics.)
    n_tight = len(tight_cycle_indices(cycles, target))
    interval = shape_analogue_interval(cycles, target, cur[-1]["_t"], y[-1])
    primary_name = "shape_analogue"
    if interval is None:  # too few cycles for a diurnal profile → plain analogue
        interval = analogue_interval(cycles, target, cur[-1]["_t"], y[-1])
        primary_name = "analogue"
    if interval:
        primary_eta = interval["p50"]
    else:  # no completed cycles yet → fall back to diurnal, else ensemble
        primary_name = "diurnal" if per_model.get("diurnal", {}).get("eta_epoch") else "ensemble"
        primary_eta = (per_model["diurnal"]["eta_epoch"] if primary_name == "diurnal"
                       else ensemble_eta)

    # Model-selection stability: only name a "best" model if it wins every LOO
    # fold. Otherwise the leaderboard is noise and weights stay near-uniform.
    winner, fold_winners = stable_winner(cycles, target)

    return {
        "generated_at": None,
        "target": target,
        "current": {
            "collected": int(y[-1]),
            "remaining": int(target - y[-1]),
            "percent": round(100 * y[-1] / target, 1),
            "last_ts": fmt_ts(cur[-1]["_t"]),
            "cycle_start_ts": fmt_ts(t0),
            "num_points": len(cur),
            "players_online": cur[-1].get("players_online"),
        },
        "primary": {
            "model": primary_name,
            "eta": fmt_ts(primary_eta) if primary_eta else None,
            "eta_epoch": primary_eta,
            "eta_display": (fmt_ts_rounded(
                primary_eta, display_granularity_min(
                    (interval["p90"] - interval["p10"]) / 120 if interval else 999))
                if primary_eta else None),
            "display_granularity_min": (display_granularity_min(
                (interval["p90"] - interval["p10"]) / 120) if interval else None),
            "interval_80": [fmt_ts(interval["p10"]), fmt_ts(interval["p90"])]
                if interval else None,
            "interval_90": [fmt_ts(interval["p05"]), fmt_ts(interval["p95"])]
                if interval else None,
            "half_width_80_min": round((interval["p90"] - interval["p10"]) / 120)
                if interval else None,
            "n_library_cycles": len(completed),
            "n_tight_labeled_cycles": n_tight,
            "note": (f"Point and interval are both the {primary_name} model "
                     "(diurnal-re-timed curve library; ~79% measured 80%-interval "
                     f"coverage OOS), over {len(completed)} library cycles "
                     f"({n_tight} tightly labeled). Sample is small — treat the "
                     "width as approximate. Wide early by design; tightens as the "
                     "cycle fills."
                     if interval else
                     "No completed cycles yet — point is a bare extrapolation, "
                     "uncertainty UNKNOWN."),
        },
        "models": {n: {
            "eta": fmt_ts(m["eta_epoch"]) if m["eta_epoch"] else None,
            "weight": round(m["weight"], 4),
            "backtest_rmse": round(m["rmse"], 5) if m["rmse"] is not None else None,
        } for n, m in per_model.items()},
        "ensemble": {  # diagnostic only — weights shrunk toward uniform (Occam)
            "eta": fmt_ts(ensemble_eta) if ensemble_eta else None,
            "eta_epoch": ensemble_eta,
            "range_low": fmt_ts(lo) if lo else None,
            "range_high": fmt_ts(hi) if hi else None,
        },
        "model_selection": {
            "stable_winner": winner,  # None until the pre-registered criterion is met
            "n_voting_cycles": len(fold_winners),
            "min_required": STABLE_WINNER_MIN_CYCLES,
            "fold_winners": {str(k): v for k, v in fold_winners.items()},
            "note": ((
                f"No stable winner — only {len(fold_winners)} well-labeled voting "
                f"cycles (< {STABLE_WINNER_MIN_CYCLES} required by the pre-registered "
                f"criterion), current fold-leaders {sorted(set(fold_winners.values()))}. "
                "Weights shrunk toward uniform; naming a leader now would be noise."
                if winner is None else
                f"Stable winner: '{winner}' meets the pre-registered criterion "
                f"(wins every one of {len(fold_winners)} well-labeled LOO folds)."
            ) if fold_winners else "No well-labeled cycles yet."),
        },
        "_per_model_epoch": {n: m["eta_epoch"] for n, m in per_model.items()},
        "_cycles": cycles,
    }


# ----------------------------------------------------------------------------
# Graphing
# ----------------------------------------------------------------------------

def make_graph(result, target, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    cycles = result["_cycles"]
    cur = cycles[-1]
    xs = [datetime.fromtimestamp(p["_t"], tz=timezone.utc) for p in cur]
    ys = [p["collected"] for p in cur]

    fig = plt.figure(figsize=(12, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[2.2, 1], hspace=0.3, wspace=0.25)
    ax = fig.add_subplot(gs[0, :])

    ax.plot(xs, ys, "o-", color="#1f77b4", lw=2, ms=5, label="collected (actual)", zorder=5)
    ax.axhline(target, color="#333", ls="--", lw=1, label=f"target ({target})")

    palette = plt.cm.tab10(np.linspace(0, 1, len(MODELS)))
    last_dt = xs[-1]
    for (name, eta_epoch), col in zip(result["_per_model_epoch"].items(), palette):
        if eta_epoch is None:
            continue
        eta_dt = datetime.fromtimestamp(eta_epoch, tz=timezone.utc)
        ax.plot([last_dt, eta_dt], [ys[-1], target], "--", color=col, lw=1.3, alpha=0.8)
        w = result["models"][name]["weight"]
        ax.scatter([eta_dt], [target], color=col, s=30 + 400 * w, alpha=0.85,
                   zorder=6, label=f"{name} (w={w:.2f})")

    prim = result["primary"]
    if prim["eta_epoch"]:
        p_dt = datetime.fromtimestamp(prim["eta_epoch"], tz=timezone.utc)
        # Analogue calibrated 80% interval around the primary point.
        if prim.get("interval_80"):
            lo = datetime.fromtimestamp(parse_ts(prim["interval_80"][0]), tz=timezone.utc)
            hi = datetime.fromtimestamp(parse_ts(prim["interval_80"][1]), tz=timezone.utc)
            ax.axvspan(lo, hi, color="crimson", alpha=0.12,
                       label="analogue 80% interval")
        ax.axvline(p_dt, color="crimson", lw=2.5,
                   label=f"PRIMARY = {prim['model']}")
    ens = result["ensemble"]
    if ens["eta_epoch"]:
        ens_dt = datetime.fromtimestamp(ens["eta_epoch"], tz=timezone.utc)
        ax.axvline(ens_dt, color="gray", lw=1.2, ls=":", label="ensemble (diagnostic)")

    ax.set_title(f"EarthMC vote party — {result['current']['percent']}% "
                 f"({result['current']['collected']}/{int(target)})  |  "
                 f"fires ~{prim.get('eta_display') or prim['eta'] or 'n/a'}",
                 fontsize=12, fontweight="bold")
    ax.set_ylabel("votes collected")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=timezone.utc))
    ax.legend(fontsize=8, ncol=2, loc="upper left")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()

    axw = fig.add_subplot(gs[1, 0])
    names = list(result["models"].keys())
    wvals = [result["models"][n]["weight"] for n in names]
    axw.barh(names, wvals, color=palette)
    axw.set_title("ensemble weights (from backtest)", fontsize=10)
    axw.set_xlabel("weight")
    axw.grid(alpha=0.3, axis="x")

    axh = fig.add_subplot(gs[1, 1])
    for idx, cyc in enumerate(cycles):
        tt, yy = cycle_arrays(cyc)
        is_cur = idx == len(cycles) - 1
        axh.plot(tt / 3600.0, 100 * yy / target, marker=".",
                 lw=2 if is_cur else 1, alpha=1.0 if is_cur else 0.5,
                 color="crimson" if is_cur else None,
                 label="current" if is_cur else f"cycle {idx+1}")
    axh.axhline(100, color="#333", ls="--", lw=0.8)
    axh.set_title("cycle fill curves", fontsize=10)
    axh.set_xlabel("hours since cycle start")
    axh.set_ylabel("% of target")
    axh.legend(fontsize=7)
    axh.grid(alpha=0.3)

    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------

def write_markdown(result, path):
    c = result["current"]
    prim = result["primary"]
    ens = result["ensemble"]
    lines = [
        "# Vote Party Prediction",
        "",
        f"_Generated {result['generated_at']} — recomputed every data update._",
        "",
        f"**Progress:** {c['collected']} / {result['target']} "
        f"({c['percent']}%) — {c['remaining']} remaining",
        f"**Players online:** {c['players_online']}  |  "
        f"**Cycle started:** {c['cycle_start_ts']}  |  "
        f"**Data points this cycle:** {c['num_points']}",
        "",
        "## 🎯 Prediction",
        "",
        f"**Vote party fires ≈ `{prim.get('eta_display') or prim['eta'] or 'n/a'}`**  "
        f"(model: `{prim['model']}`, rounded to interval resolution)",
    ]
    if prim.get("interval_80"):
        g = prim.get("display_granularity_min") or 1
        lo = fmt_ts_rounded(parse_ts(prim["interval_80"][0]), g)
        hi = fmt_ts_rounded(parse_ts(prim["interval_80"][1]), g)
        lines.append(f"**80% window:** `{lo}` → `{hi}`")
        lines.append(f"_Interval from the analogue curve-library (measured ~73% "
                     f"coverage OOS, endpoint label-uncertainty propagated) over "
                     f"{prim['n_library_cycles']} cycles "
                     f"({prim['n_tight_labeled_cycles']} tightly labeled). Point "
                     "rounded to match interval width; wide early by design._")
    else:
        lines.append("⚠️ Interval unavailable — treat the ETA as a point estimate "
                     "with wide, unquantified error.")
    sel = result["model_selection"]
    sel_line = ("**No stable winner** — the lowest-error model differs across "
                "leave-one-cycle-out folds, so we name none and keep the "
                "(diagnostic) weights shrunk toward uniform."
                if sel["stable_winner"] is None else
                f"**Stable winner:** `{sel['stable_winner']}` wins every "
                "leave-one-cycle-out fold (still few cycles).")
    lines += [
        "",
        f"_Diagnostic ensemble ETA: `{ens['eta'] or 'n/a'}`._",
        "",
        "## Model diagnostics (not the prediction)",
        "",
        sel_line,
        "",
        "| Model | Predicted ETA | Weight (shrunk) |",
        "|-------|---------------|-----------------|",
    ]
    for name, m in sorted(result["models"].items(), key=lambda kv: -kv[1]["weight"]):
        lines.append(f"| {name} | {m['eta'] or 'n/a'} | {m['weight']:.3f} |")
    lines += [
        "",
        "**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in "
        "cycles): near-equal now, differentiating only when many cycles give "
        "strong, stable evidence. A shifting 'leader' at this sample size is "
        "sampling noise, not a finding. The reported prediction (above) is the "
        "`analogue` model, independent of these weights. See `prediction_track.png`.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


# ----------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Ensemble vote-party ETA predictor.")
    ap.add_argument("-i", "--input", default="data/voteparty.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--no-graph", action="store_true")
    ap.add_argument("--now", default=None, help="override 'generated_at' (ISO Z)")
    args = ap.parse_args(argv)

    points = load_points(args.input)
    if len(points) < 2:
        print(f"Not enough data in {args.input} ({len(points)} points).")
        return 1

    target = float(points[-1]["target"])
    cycles = split_cycles(points)
    result = predict(cycles, target)
    result["generated_at"] = args.now or fmt_ts(points[-1]["_t"])

    os.makedirs(args.outdir, exist_ok=True)
    public = {k: v for k, v in result.items() if not k.startswith("_")}
    with open(os.path.join(args.outdir, "prediction.json"), "w", encoding="utf-8") as fh:
        json.dump(public, fh, indent=2)
    write_markdown(result, os.path.join(args.outdir, "PREDICTION.md"))
    if not args.no_graph:
        make_graph(result, target, os.path.join(args.outdir, "prediction.png"))

    prim = result["primary"]
    print(f"Cycles: {len(cycles)} | current points: {result['current']['num_points']} "
          f"| tightly-labeled cycles: {prim['n_tight_labeled_cycles']}")
    if prim.get("interval_80"):
        g = prim.get("display_granularity_min") or 1
        iv = (f" | 80% [{fmt_ts_rounded(parse_ts(prim['interval_80'][0]), g)} .. "
              f"{fmt_ts_rounded(parse_ts(prim['interval_80'][1]), g)}]")
    else:
        iv = " (interval unavailable)"
    print(f"PREDICTION: {prim['model']} ~{prim.get('eta_display') or prim['eta']}{iv}")
    print(f"ensemble ETA (diagnostic only): {result['ensemble']['eta']}")
    sel = result["model_selection"]
    print("model selection: " + ("NO stable winner — weights ~uniform (Occam)"
                                  if sel["stable_winner"] is None
                                  else f"stable winner '{sel['stable_winner']}'"))
    for name, m in sorted(result["models"].items(), key=lambda kv: -kv[1]["weight"]):
        print(f"  {name:11s} eta={m['eta']}  w={m['weight']:.3f} (diagnostic)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

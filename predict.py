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


# Label quality: a completed cycle's firing time is only known to within the
# gap between its last sub-target sample and the first sample after reset. Only
# cycles bracketed tighter than this (minutes) have a trustworthy label.
TIGHT_BRACKET_MIN = 15.0


def fire_bracket_min(cycles, ci):
    """Minutes between the last pre-reset sample and the first post-reset sample
    — the window the true firing time is known to lie in. None if not completed."""
    if ci >= len(cycles) - 1:
        return None
    return (cycles[ci + 1][0]["_t"] - cycles[ci][-1]["_t"]) / 60.0


def tight_cycle_indices(cycles, max_bracket=TIGHT_BRACKET_MIN):
    """Indices of completed cycles whose firing was tightly bracketed."""
    return [ci for ci in range(len(cycles) - 1)
            if (fire_bracket_min(cycles, ci) or 1e9) <= max_bracket]


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


def diurnal_profile(train_cycles, nbins=24, smooth=1):
    """Average vote rate (votes/sec) as a function of UTC hour-of-day, learned
    from history. Each observed interval contributes its rate to every hour it
    overlaps, weighted by overlap duration, so long sparse intervals still
    inform the profile. Circularly smoothed. Returns (profile[nbins], mean_rate)
    or (None, None) if there is not enough data."""
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
    """
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
        return None
    mean_rate = float(np.average([r for r, _ in all_rates],
                                 weights=[w for _, w in all_rates]))
    gprof = np.where(gden > 0, gnum / np.maximum(gden, 1e-9), mean_rate)
    profs = {g: np.where(den[g] > 0, num[g] / np.maximum(den[g], 1e-9), gprof)
             for g in groups}
    counts = {g: den[g] / 3600.0 for g in groups}  # bin sample weight in hours
    return {"groups": profs, "counts": counts, "global": gprof, "mean": mean_rate}


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

def _predict_y_at(name, t_fit, y_fit, t_query, target, ctx):
    """Predict collected at a future time using a model's underlying fit."""
    if len(t_fit) < 2:
        return None
    if name == "shrinkage":
        rate = shrink_rate(t_fit, y_fit, target, ctx)
        return None if rate is None else y_fit[-1] + rate * (t_query - t_fit[-1])
    if name == "quadratic" and len(t_fit) >= 3:
        c, b, a = np.polyfit(t_fit, y_fit, 2)
        return c * t_query ** 2 + b * t_query + a
    if name == "recent":
        k = min(6, len(t_fit))
        tt, yy = t_fit[-k:], y_fit[-k:]
        if tt[-1] - tt[0] <= 0:
            return None
        slope = (yy[-1] - yy[0]) / (tt[-1] - tt[0])
        return yy[-1] + slope * (t_query - tt[-1])
    if name == "ewma":
        dt, dy = np.diff(t_fit), np.diff(y_fit)
        ok = dt > 0
        if not ok.any():
            return None
        rates = dy[ok] / dt[ok]
        n = len(rates)
        decay = 0.5 ** (1.0 / 3)
        w = decay ** np.arange(n - 1, -1, -1)
        rate = np.sum(w * rates) / np.sum(w)
        return y_fit[-1] + rate * (t_query - t_fit[-1])
    if name == "theilsen":
        slope = robust_slope(t_fit, y_fit)
        if slope is None:
            return None
        intercept = float(np.median(y_fit - slope * t_fit))
        return slope * t_query + intercept
    if name == "wls":
        n = len(t_fit)
        decay = 0.5 ** (1.0 / 4)
        w = decay ** np.arange(n - 1, -1, -1)
        W = np.diag(w)
        X = np.vstack([t_fit, np.ones_like(t_fit)]).T
        try:
            beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y_fit)
        except np.linalg.LinAlgError:
            return None
        return beta[0] * t_query + beta[1]
    b, a = np.polyfit(t_fit, y_fit, 1)  # default: linear
    return b * t_query + a


def _bucket(progress):
    for lo, hi in BUCKETS:
        if lo <= progress < hi:
            return (lo, hi)
    return BUCKETS[-1]


def _errs_to_weights(errs):
    rmse = {n: (float(np.sqrt(np.mean(e))) if e else None) for n, e in errs.items()}
    scored = {n: r for n, r in rmse.items() if r is not None and r > 0}
    if scored:
        inv = {n: 1.0 / (r * r) for n, r in scored.items()}
        s = sum(inv.values())
        weights = {n: inv[n] / s for n in inv}
    else:
        weights = {n: 1.0 / len(MODELS) for n in MODELS}
    return weights, rmse


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
    for ci, cyc in enumerate(cycles):
        if len(cyc) < min_fit + 1:
            continue
        fire, _ = cycle_fire_time(cyc, target)
        if fire is None:
            continue
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
        "global": _errs_to_weights(errs_global),
        "buckets": {b: _errs_to_weights(errs_bucket[b]) for b in BUCKETS},
    }


def weights_for_progress(staged, progress, blend=0.5):
    """Blend bucket-specific weights with global weights for stability."""
    gw, _ = staged["global"]
    bw, _ = staged["buckets"][_bucket(progress)]
    names = set(gw) | set(bw)
    mixed = {n: blend * bw.get(n, 0.0) + (1 - blend) * gw.get(n, 0.0) for n in names}
    s = sum(mixed.values())
    return {n: v / s for n, v in mixed.items()} if s > 0 else gw


def backtest_weights(cycles: list[list[dict]], target: float, min_fit=3):
    """Backward-compatible global weights (weights dict, rmse dict)."""
    return backtest_staged(cycles, target, min_fit)["global"]


def ensemble_eta_at(cycle, ctx, staged, target, up_to):
    """Ensemble firing epoch using the first `up_to` points of a cycle."""
    t, y = cycle_arrays(cycle)
    t0 = cycle[0]["_t"]
    t_fit, y_fit = t[:up_to], y[:up_to]
    weights = weights_for_progress(staged, float(y_fit[-1]) / target * 100.0)
    etas, ws = [], []
    for name in MODELS:
        tc = MODELS[name](t_fit, y_fit, target, ctx)
        if tc is None:
            continue
        etas.append(t0 + tc)
        ws.append(weights.get(name, 0.0))
    if not etas:
        return None
    ws = np.array(ws)
    ws = ws / ws.sum() if ws.sum() > 0 else np.ones(len(ws)) / len(ws)
    return float(np.sum(np.array(etas) * ws))


def empirical_stage_error(completed, target, predictor="diurnal", min_fit=3,
                          tight_indices=None):
    """Measured |ETA error| (seconds) per progress bucket for a given predictor,
    via leave-one-cycle-out over completed cycles.

    NOT a calibrated interval — it is a raw empirical error estimate from a tiny
    sample. When ``tight_indices`` is given, only those (tightly-bracketed)
    cycles contribute; loosely-bracketed cycles are excluded because their label
    error (tens to hundreds of minutes) would swamp the estimate.

    Returns {bucket: {"mae": sec|None, "std": sec|None, "n": int}}.
    """
    tight = set(tight_indices) if tight_indices is not None else set(range(len(completed)))
    buckets = {b: [] for b in BUCKETS}
    for ci, cyc in enumerate(completed):
        if ci not in tight:
            continue
        fire, _ = cycle_fire_time(cyc, target)
        if fire is None or len(cyc) < min_fit + 1:
            continue
        others = [c for cj, c in enumerate(completed) if cj != ci]
        staged = backtest_staged(others if others else completed, target)
        ctx = make_ctx(cyc, others)
        t, y = cycle_arrays(cyc)
        t0 = cyc[0]["_t"]
        for i in range(min_fit, len(t) + 1):
            if predictor == "ensemble":
                pred = ensemble_eta_at(cyc, ctx, staged, target, i)
            else:
                tc = MODELS[predictor](t[:i], y[:i], target, ctx)
                pred = (t0 + tc) if tc is not None else None
            if pred is None:
                continue
            buckets[_bucket(float(y[i - 1]) / target * 100.0)].append(abs(pred - fire))
    out = {}
    for b, v in buckets.items():
        out[b] = {"mae": float(np.mean(v)) if v else None,
                  "std": float(np.std(v)) if len(v) > 1 else None,
                  "n": len(v)}
    return out


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

    # PRIMARY predictor = diurnal (it beats the ensemble out-of-sample). Fall
    # back to the ensemble only when diurnal cannot produce an estimate.
    primary_name = "diurnal" if per_model.get("diurnal", {}).get("eta_epoch") else "ensemble"
    primary_eta = per_model["diurnal"]["eta_epoch"] if primary_name == "diurnal" else ensemble_eta

    # Empirical error estimate (NOT a calibrated interval): measured error of the
    # primary predictor at this stage, from tightly-bracketed cycles only.
    # Tightness is computed from the FULL cycle list so the last completed cycle
    # can see the current cycle as its successor.
    tight_idx = tight_cycle_indices(cycles)
    n_tight = len(tight_idx)
    emp = empirical_stage_error(completed, target, predictor=primary_name,
                                tight_indices=tight_idx)
    bucket_err = emp.get(_bucket(cur_progress), {"mae": None, "std": None, "n": 0})
    band = bucket_err["mae"]

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
            "empirical_error_min": round(band / 60) if band is not None else None,
            "empirical_error_std_min": round(bucket_err["std"] / 60)
                if bucket_err["std"] is not None else None,
            "error_estimate_n": bucket_err["n"],
            "n_tight_labeled_cycles": n_tight,
            "note": ("empirical error from tightly-labeled cycles; "
                     f"n={bucket_err['n']} at this stage — treat as a rough "
                     "spread, NOT a calibrated interval"
                     if bucket_err["n"] else
                     "no tightly-labeled cycles at this stage yet — "
                     "uncertainty is UNKNOWN (likely wide)"),
        },
        "models": {n: {
            "eta": fmt_ts(m["eta_epoch"]) if m["eta_epoch"] else None,
            "weight": round(m["weight"], 4),
            "backtest_rmse": round(m["rmse"], 5) if m["rmse"] is not None else None,
        } for n, m in per_model.items()},
        "ensemble": {  # kept as a diagnostic only — does NOT beat diurnal OOS
            "eta": fmt_ts(ensemble_eta) if ensemble_eta else None,
            "eta_epoch": ensemble_eta,
            "range_low": fmt_ts(lo) if lo else None,
            "range_high": fmt_ts(hi) if hi else None,
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
        ax.axvline(p_dt, color="crimson", lw=2.5,
                   label=f"PRIMARY = {prim['model']}")
        band = prim.get("empirical_error_min")
        if band and prim["error_estimate_n"]:
            lo = datetime.fromtimestamp(prim["eta_epoch"] - band * 60, tz=timezone.utc)
            hi = datetime.fromtimestamp(prim["eta_epoch"] + band * 60, tz=timezone.utc)
            ax.axvspan(lo, hi, color="crimson", alpha=0.12,
                       label=f"empirical ±{band}m (n={prim['error_estimate_n']})")
    ens = result["ensemble"]
    if ens["eta_epoch"]:
        ens_dt = datetime.fromtimestamp(ens["eta_epoch"], tz=timezone.utc)
        ax.axvline(ens_dt, color="gray", lw=1.2, ls=":", label="ensemble (diagnostic)")

    ax.set_title(f"EarthMC vote party — {result['current']['percent']}% "
                 f"({result['current']['collected']}/{int(target)})  |  "
                 f"PRIMARY ({prim['model']}) ETA {prim['eta'] or 'n/a'}",
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
        f"## 🎯 Prediction (primary model: `{prim['model']}`)",
        "",
        f"**Vote party fires ≈ `{prim['eta'] or 'n/a'}`**",
    ]
    band = prim.get("empirical_error_min")
    if band is not None and prim["error_estimate_n"]:
        lines.append(f"Empirical error at this stage: **±{band} min** "
                     f"(n={prim['error_estimate_n']} tightly-labeled predictions"
                     + (f", spread ±{prim['empirical_error_std_min']}m" if prim.get('empirical_error_std_min') else "")
                     + "). This is a raw error estimate from a tiny sample, "
                     "**not a calibrated interval** — real uncertainty is likely wider.")
    else:
        lines.append(f"⚠️ Uncertainty **unknown** at this stage: only "
                     f"{prim['n_tight_labeled_cycles']} tightly-labeled cycle(s) "
                     "so far. Treat the ETA as a point estimate with wide, "
                     "unquantified error.")
    lines += [
        "",
        f"_Diagnostic — ensemble ETA (does **not** beat `{prim['model']}` "
        f"out-of-sample): `{ens['eta'] or 'n/a'}`._",
        "",
        "## Individual models",
        "",
        "| Model | Predicted ETA | Weight | Backtest RMSE |",
        "|-------|---------------|--------|---------------|",
    ]
    for name, m in sorted(result["models"].items(), key=lambda kv: -kv[1]["weight"]):
        lines.append(f"| {name} | {m['eta'] or 'n/a'} | {m['weight']:.3f} | "
                     f"{m['backtest_rmse'] if m['backtest_rmse'] is not None else 'n/a'} |")
    lines += [
        "",
        "**Caveats:** weights are unstable at this sample size (dropping one "
        "cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic "
        "only — the reported prediction is the single best model (`diurnal`), "
        "which beats the ensemble out-of-sample. Firing-time labels for "
        "loosely-sampled cycles are uncertain by tens of minutes and are excluded "
        "from the error estimate. See `prediction_track.png` for the honest "
        "out-of-sample record.",
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
    band = prim.get("empirical_error_min")
    band_s = (f" ±{band}m (n={prim['error_estimate_n']}, empirical not calibrated)"
              if band is not None and prim["error_estimate_n"] else " (uncertainty unknown)")
    print(f"PRIMARY ({prim['model']}) ETA: {prim['eta']}{band_s}")
    print(f"ensemble ETA (diagnostic only): {result['ensemble']['eta']}")
    for name, m in sorted(result["models"].items(), key=lambda kv: -kv[1]["weight"]):
        print(f"  {name:10s} eta={m['eta']}  w={m['weight']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

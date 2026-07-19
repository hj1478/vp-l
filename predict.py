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


MODELS = {
    "shrinkage": model_shrinkage,
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


def calibrated_stage_mae(completed, target, min_fit=3):
    """Measured ensemble |ETA error| (seconds) per progress bucket, via
    leave-one-cycle-out over the completed cycles. Used to attach an honest,
    stage-appropriate confidence band to the live prediction."""
    buckets = {b: [] for b in BUCKETS}
    for ci, cyc in enumerate(completed):
        fire, _ = cycle_fire_time(cyc, target)
        if fire is None or len(cyc) < min_fit + 1:
            continue
        others = [c for cj, c in enumerate(completed) if cj != ci]
        staged = backtest_staged(others if others else completed, target)
        ctx = make_ctx(cyc, others)
        t, y = cycle_arrays(cyc)
        for i in range(min_fit, len(t) + 1):
            ens = ensemble_eta_at(cyc, ctx, staged, target, i)
            if ens is None:
                continue
            buckets[_bucket(float(y[i - 1]) / target * 100.0)].append(abs(ens - fire))
    return {b: (float(np.mean(v)) if v else None) for b, v in buckets.items()}


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
        spread = float(np.sqrt(np.sum(ws * (etas - ensemble_eta) ** 2)))
        lo, hi = float(etas.min()), float(etas.max())
    else:
        ensemble_eta = spread = lo = hi = None

    # Calibrated band: measured ensemble error at the current cycle stage.
    band = None
    if ensemble_eta is not None and len(completed) >= 1:
        mae = calibrated_stage_mae(completed, target)
        band = mae.get(_bucket(cur_progress))

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
        "models": {n: {
            "eta": fmt_ts(m["eta_epoch"]) if m["eta_epoch"] else None,
            "weight": round(m["weight"], 4),
            "backtest_rmse": round(m["rmse"], 5) if m["rmse"] is not None else None,
        } for n, m in per_model.items()},
        "ensemble": {
            "eta": fmt_ts(ensemble_eta) if ensemble_eta else None,
            "eta_epoch": ensemble_eta,
            "spread_seconds": round(spread) if spread is not None else None,
            "range_low": fmt_ts(lo) if lo else None,
            "range_high": fmt_ts(hi) if hi else None,
            "calibrated_band_min": round(band / 60) if band is not None else None,
            "calibrated_low": fmt_ts(ensemble_eta - band) if band is not None else None,
            "calibrated_high": fmt_ts(ensemble_eta + band) if band is not None else None,
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

    ens = result["ensemble"]
    if ens["eta_epoch"]:
        ens_dt = datetime.fromtimestamp(ens["eta_epoch"], tz=timezone.utc)
        ax.axvline(ens_dt, color="crimson", lw=2.5, label="ENSEMBLE ETA")
        if ens.get("calibrated_low") and ens.get("calibrated_high"):
            lo = datetime.fromtimestamp(parse_ts(ens["calibrated_low"]), tz=timezone.utc)
            hi = datetime.fromtimestamp(parse_ts(ens["calibrated_high"]), tz=timezone.utc)
            ax.axvspan(lo, hi, color="crimson", alpha=0.12,
                       label=f"calibrated ±{ens['calibrated_band_min']} min")
        elif ens["range_low"] and ens["range_high"]:
            lo = datetime.fromtimestamp(parse_ts(ens["range_low"]), tz=timezone.utc)
            hi = datetime.fromtimestamp(parse_ts(ens["range_high"]), tz=timezone.utc)
            ax.axvspan(lo, hi, color="crimson", alpha=0.08, label="model spread")

    ax.set_title(f"EarthMC vote party — current cycle & ensemble prediction\n"
                 f"{result['current']['percent']}% ({result['current']['collected']}/{target}), "
                 f"ETA {ens['eta'] or 'n/a'}", fontsize=13, fontweight="bold")
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
        "## 🎯 Ensemble prediction",
        "",
        f"**Vote party fires ≈ `{ens['eta'] or 'n/a'}`**",
    ]
    if ens.get("calibrated_band_min") is not None:
        lines.append(f"Calibrated confidence: **±{ens['calibrated_band_min']} min** "
                     f"(`{ens['calibrated_low']}` → `{ens['calibrated_high']}`) — "
                     f"the ensemble's measured error at this cycle stage.")
    if ens["range_low"]:
        lines.append(f"Model spread: `{ens['range_low']}` → `{ens['range_high']}`")
    lines += [
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
        "Weights come from a rolling-origin backtest on completed cycles "
        "(leave-one-out for history-aware models): each model's inverse "
        "mean-squared extrapolation error, normalised. See `prediction.png`.",
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

    ens = result["ensemble"]
    print(f"Cycles found: {len(cycles)} | current cycle points: {result['current']['num_points']}")
    band = ens.get("calibrated_band_min")
    print(f"Ensemble ETA: {ens['eta']}" + (f" (calibrated ±{band} min)" if band is not None else ""))
    for name, m in sorted(result["models"].items(), key=lambda kv: -kv[1]["weight"]):
        print(f"  {name:10s} eta={m['eta']}  w={m['weight']:.3f}  rmse={m['backtest_rmse']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

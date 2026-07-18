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
    linear      — ordinary least squares on the whole cycle
    recent      — slope of the last k points (short-term rate)
    ewma        — exponentially weighted average of per-interval rates
    theilsen    — Theil–Sen robust median-slope regression
    wls         — least squares with exponential recency weights
    quadratic   — 2nd-order fit, solves for the target crossing (captures accel)

Usage:
    python3 predict.py                       # read data/voteparty.jsonl
    python3 predict.py -i path/to.jsonl -o out_dir
    python3 predict.py --no-graph            # skip the PNG (text/JSON only)
"""

import argparse
import json
import os
from datetime import datetime, timezone

import numpy as np

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


# ----------------------------------------------------------------------------
# Models — each returns predicted seconds-from-cycle-start at which y == target,
# given partial data (t, y). Return None when it cannot produce a sane estimate.
# ----------------------------------------------------------------------------

def _cross_from_line(slope, intercept, target, t_last):
    if slope <= 1e-9:
        return None
    t_cross = (target - intercept) / slope
    # Must be at/after the last observation.
    return max(t_cross, t_last)


def model_linear(t, y, target):
    if len(t) < 2:
        return None
    b, a = np.polyfit(t, y, 1)
    return _cross_from_line(b, a, target, t[-1])


def model_recent(t, y, target, k=6):
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


def model_ewma(t, y, target, halflife=3):
    if len(t) < 2:
        return None
    dt = np.diff(t)
    dy = np.diff(y)
    ok = dt > 0
    if not ok.any():
        return None
    rates = dy[ok] / dt[ok]
    # Exponential weights, most recent heaviest.
    n = len(rates)
    decay = 0.5 ** (1.0 / max(halflife, 1e-9))
    w = decay ** np.arange(n - 1, -1, -1)
    rate = np.sum(w * rates) / np.sum(w)
    if rate <= 1e-9:
        return None
    return t[-1] + (target - y[-1]) / rate


def model_theilsen(t, y, target):
    if len(t) < 2:
        return None
    slopes = []
    n = len(t)
    for i in range(n):
        for j in range(i + 1, n):
            if t[j] != t[i]:
                slopes.append((y[j] - y[i]) / (t[j] - t[i]))
    if not slopes:
        return None
    slope = float(np.median(slopes))
    if slope <= 1e-9:
        return None
    intercept = float(np.median(y - slope * t))
    return _cross_from_line(slope, intercept, target, t[-1])


def model_wls(t, y, target, halflife=4):
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
    slope, intercept = beta[0], beta[1]
    return _cross_from_line(slope, intercept, target, t[-1])


def model_quadratic(t, y, target):
    if len(t) < 3:
        return None
    c, b, a = np.polyfit(t, y, 2)  # y = c t^2 + b t + a
    if abs(c) < 1e-12:
        return _cross_from_line(b, a, target, t[-1])
    disc = b * b - 4 * c * (a - target)
    if disc < 0:
        return None
    roots = [(-b + s * np.sqrt(disc)) / (2 * c) for s in (1, -1)]
    future = [r for r in roots if r >= t[-1] - 1e-6]
    if not future:
        return None
    return min(future)


MODELS = {
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

def _predict_y_at(name, t_fit, y_fit, t_query):
    """Use a model's underlying fit to predict y at a future time (for backtest)."""
    if len(t_fit) < 2:
        return None
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
        slopes = [(y_fit[j] - y_fit[i]) / (t_fit[j] - t_fit[i])
                  for i in range(len(t_fit)) for j in range(i + 1, len(t_fit))
                  if t_fit[j] != t_fit[i]]
        if not slopes:
            return None
        slope = float(np.median(slopes))
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
    # default: linear
    b, a = np.polyfit(t_fit, y_fit, 1)
    return b * t_query + a


def backtest_weights(cycles: list[list[dict]], target: float, min_fit=3):
    """Return (weights dict, per-model rmse dict) from rolling-origin backtest."""
    errs = {name: [] for name in MODELS}
    for cyc in cycles:
        if len(cyc) < min_fit + 1:
            continue
        t, y = cycle_arrays(cyc)
        for i in range(min_fit, len(t)):
            t_fit, y_fit = t[:i], y[:i]
            for j in range(i, len(t)):  # held-out later points
                for name in MODELS:
                    pred = _predict_y_at(name, t_fit, y_fit, t[j])
                    if pred is not None and np.isfinite(pred):
                        # Normalise error by target so it is scale-free.
                        errs[name].append(((pred - y[j]) / target) ** 2)
    rmse = {}
    for name, e in errs.items():
        rmse[name] = float(np.sqrt(np.mean(e))) if e else None
    # Inverse-MSE weights (only over models that produced a score).
    scored = {n: r for n, r in rmse.items() if r is not None and r > 0}
    if scored:
        inv = {n: 1.0 / (r * r) for n, r in scored.items()}
        s = sum(inv.values())
        weights = {n: inv[n] / s for n in inv}
    else:
        weights = {n: 1.0 / len(MODELS) for n in MODELS}
    return weights, rmse


# ----------------------------------------------------------------------------
# Prediction
# ----------------------------------------------------------------------------

def predict(cycles, target):
    """Run all models on the current (last) cycle, ensemble via backtest weights."""
    weights, rmse = backtest_weights(cycles[:-1] if len(cycles) > 1 else cycles, target)
    cur = cycles[-1]
    t, y = cycle_arrays(cur)
    t0 = cur[0]["_t"]

    per_model = {}
    for name, fn in MODELS.items():
        t_cross = fn(t, y, target)
        per_model[name] = {
            "eta_epoch": (t0 + t_cross) if t_cross is not None else None,
            "weight": weights.get(name, 0.0),
            "rmse": rmse.get(name),
        }

    # Weighted ensemble over models that produced a finite ETA.
    valid = [(m["eta_epoch"], m["weight"]) for m in per_model.values()
             if m["eta_epoch"] is not None]
    if valid:
        etas = np.array([v[0] for v in valid])
        ws = np.array([v[1] for v in valid])
        ws = ws / ws.sum() if ws.sum() > 0 else np.ones_like(ws) / len(ws)
        ensemble_eta = float(np.sum(etas * ws))
        # Uncertainty band: weighted std, plus the raw min/max spread.
        var = float(np.sum(ws * (etas - ensemble_eta) ** 2))
        spread = float(np.sqrt(var))
        lo, hi = float(etas.min()), float(etas.max())
    else:
        ensemble_eta = spread = lo = hi = None

    return {
        "generated_at": None,  # stamped by caller
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
    t0 = cur[0]["_t"]
    xs = [datetime.fromtimestamp(p["_t"], tz=timezone.utc) for p in cur]
    ys = [p["collected"] for p in cur]

    fig = plt.figure(figsize=(12, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[2.2, 1], hspace=0.3, wspace=0.25)
    ax = fig.add_subplot(gs[0, :])

    # Actual data.
    ax.plot(xs, ys, "o-", color="#1f77b4", lw=2, ms=5, label="collected (actual)", zorder=5)
    ax.axhline(target, color="#333", ls="--", lw=1, label=f"target ({target})")

    # Model projection lines + ETA markers.
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
        if ens["range_low"] and ens["range_high"]:
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

    # Bottom-left: model weights.
    axw = fig.add_subplot(gs[1, 0])
    names = list(result["models"].keys())
    wvals = [result["models"][n]["weight"] for n in names]
    axw.barh(names, wvals, color=palette)
    axw.set_title("ensemble weights (from backtest)", fontsize=10)
    axw.set_xlabel("weight")
    axw.grid(alpha=0.3, axis="x")

    # Bottom-right: historical cycle fill curves (percent vs hours since start).
    axh = fig.add_subplot(gs[1, 1])
    for idx, cyc in enumerate(cycles):
        tt, yy = cycle_arrays(cyc)
        hrs = tt / 3600.0
        pct = 100 * yy / target
        is_cur = idx == len(cycles) - 1
        axh.plot(hrs, pct, marker=".", lw=2 if is_cur else 1,
                 alpha=1.0 if is_cur else 0.5,
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
    if ens["range_low"]:
        lines.append(f"Model spread: `{ens['range_low']}` → `{ens['range_high']}` "
                     f"(±{round((ens['spread_seconds'] or 0)/60)} min)")
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
        "Weights come from a rolling-origin backtest on completed cycles: each "
        "model's inverse mean-squared extrapolation error, normalised. Lower RMSE "
        "→ higher weight. See `prediction.png` for the graph.",
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

    # JSON (drop private helper keys).
    public = {k: v for k, v in result.items() if not k.startswith("_")}
    with open(os.path.join(args.outdir, "prediction.json"), "w", encoding="utf-8") as fh:
        json.dump(public, fh, indent=2)

    write_markdown(result, os.path.join(args.outdir, "PREDICTION.md"))

    if not args.no_graph:
        make_graph(result, target, os.path.join(args.outdir, "prediction.png"))

    ens = result["ensemble"]
    print(f"Cycles found: {len(cycles)} | current cycle points: {result['current']['num_points']}")
    print(f"Ensemble ETA: {ens['eta']} (spread ±{round((ens['spread_seconds'] or 0)/60)} min)")
    for name, m in sorted(result["models"].items(), key=lambda kv: -kv[1]["weight"]):
        print(f"  {name:10s} eta={m['eta']}  w={m['weight']:.3f}  rmse={m['backtest_rmse']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

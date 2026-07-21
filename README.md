# EarthMC Vote Party Tracker

A dependency-free Python script that polls the [EarthMC API](https://earthmc.net/docs/api)
and logs vote party progress (plus a snapshot of server stats) to a file.

The vote party data lives on the root server endpoint
(`GET https://api.earthmc.net/v4/`) as:

```json
"voteParty": { "target": 5000, "numRemaining": 1646 }
```

`collected = target - numRemaining`, so the tracker derives the count and percentage
each poll.

## Usage

```bash
python3 voteparty_tracker.py            # adaptive, as fast as every 60s
python3 voteparty_tracker.py -i 30      # base 30 seconds
python3 voteparty_tracker.py --max-interval 1800
python3 voteparty_tracker.py -f my.log  # custom log file
python3 voteparty_tracker.py --once     # single poll then exit
python3 voteparty_tracker.py --json     # also write machine-readable JSONL
```

Stop a running tracker with `Ctrl+C` (or `SIGTERM`); it logs a clean shutdown line.

## Adaptive polling

The interval is not fixed — it uses **AIMD** (additive-increase / multiplicative-decrease)
control so it collects as fast as the API tolerates without hammering it:

- Starts at the **base** interval (`-i`, default 60s) for fast collection.
- On an HTTP **429 (rate limited)** it **doubles** the interval and honours the
  server's `Retry-After` header when present, up to `--max-interval`.
- On each successful poll it **eases back down** toward the base interval.
- Transient network errors trigger a mild (×1.5) back-off.

The current "next poll" spacing is shown on every log line and stored in the JSONL
`interval` field, so you can see the controller reacting.

> Note: the root endpoint is served through Cloudflare and may be briefly cached,
> so polling faster than the cache TTL can return identical data for a few seconds.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-u`, `--url` | `https://api.earthmc.net/v4/` | Server endpoint to poll |
| `-f`, `--logfile` | `voteparty.log` | Human-readable log file |
| `-i`, `--interval` | `60` | Base (fastest) seconds between polls |
| `--max-interval` | `3600` | Slowest interval under throttling (1 hr) |
| `--once` | off | Poll once and exit |
| `--json [FILE]` | off (`voteparty.jsonl`) | Also append one JSON object per poll |

## What gets logged

Each poll appends a timestamped (UTC) line:

```
[2026-07-17T06:35:41Z] vote party 3398/5000 (68.0%) | 1602 remaining | players 406/800 | moon WAXING_CRESCENT
```

When the vote party fires (the remaining counter resets upward), it records a distinct event:

```
[...] *** VOTE PARTY FIRED! remaining reset 12 -> 4998 (+4986) ***
```

Network or parse errors are logged and the tracker keeps running.

The optional JSONL file captures the full snapshot per poll (target, remaining,
collected, percent, players, towns, nations, residents) for later analysis.

## Prediction model (`predict.py`)

`predict.py` reads the collected time series, splits it into vote-party
**cycles** (a cycle ends when the counter resets after a party fires), and
forecasts when the *next* party will fire. It is recomputed on every data
update, so the prediction constantly changes as new points arrive.

It runs **eight independent models** and **ensembles** them:

| Model | Idea |
|-------|------|
| `diurnal` | **Predict each stage separately** — learns the vote rate as a function of UTC time-of-day and integrates that profile forward to target (budgets for the overnight lull and evening peak instead of assuming one flat rate) |
| `diurnal_dow` | Same, but conditioned on **weekday vs weekend** as well as UTC hour, with per-bin hierarchical shrinkage toward the pooled profile so it can't overfit thin data. A candidate model — earns weight as multi-week data accumulates. **Timezones:** everything is UTC hour-of-day, the correct frame for a global playerbase whose peaks sit at fixed UTC hours. |
| `shrinkage` | Bayesian blend of the historical rate prior and the observed rate — leans on history early, on live data late |
| `linear` | OLS regression over the whole cycle |
| `recent` | slope of the last k points (short-term rate) |
| `ewma` | exponentially-weighted average of per-interval rates |
| `theilsen` | Theil–Sen robust median-slope regression |
| `wls` | least squares with exponential recency weights |
| `quadratic` | 2nd-order fit, solves for the target crossing (accel/decel) |

**Why these two lead:** the vote process is nearly stationary across cycles
(historical cycles average ~390–410 votes/hr, player count only weakly predicts
rate, r≈0.1), so the historical rate is a strong prior — which `shrinkage`
exploits. But the rate is *not* flat within a cycle: it rises and falls with the
time of day. `diurnal` captures that shape and, once a few cycles have
accumulated, becomes the most accurate model at every stage — it predicts each
remaining portion of the cycle with its own time-of-day rate instead of
extrapolating one rate across the overnight lull it hasn't reached yet.

**Weighting:** each model's ETA is weighted by a **rolling-origin backtest** on
the completed historical cycles, scored by **inverse mean-squared ETA error**
(how far its predicted *firing time* lands from the actual firing time) — not
just next-point accuracy. Weights are **stage-aware**: computed per
cycle-progress bucket, so the ensemble trusts shrinkage early and the reactive
models late.

### ⚠️ Honest status of the modeling (read this)

Out-of-sample testing at the current sample size (a handful of cycles) exposed
real limits, and the system is deliberately conservative as a result:

- **The reported prediction is the `analogue` curve-library, for both the point
  (its median) and the interval (its quantiles).** We checked whether `diurnal`'s
  point beats the analogue median: it does *not* by more than noise (paired
  |error| difference 14 min but sd 57 min; diurnal wins only 54% of stage-points,
  driven by one cycle), and the diurnal-vs-analogue offset is large and unstable
  (+38 min, sd 74 min). Grafting a diurnal point inside an analogue interval would
  mis-centre a calibrated width around a wrong centre, so we use **one coherent
  distribution** instead. `diurnal`, `diurnal_dow`, the ensemble, `nhpp`, etc.
  remain as diagnostics.
- **The interval is measured to be ~calibrated** (~75% coverage at 80% nominal
  on tight cycles), because its spread is the *real* historical spread of past
  cycles' remaining trajectories — not a process assumption (the NHPP's
  parametric interval was overconfident at ~19% and is shelved).
- **Ensemble weights are shrunk toward uniform (Occam prior).** Hard
  inverse-error weights fit on a few cycles swing the top weight by ±0.4 —
  sampling noise, not skill. Weights are pulled toward equal by λ = n/(n+6)
  (in cycles), so they only differentiate once many cycles give strong, stable
  evidence. We **do not name a "winning" model** until it wins *every*
  leave-one-cycle-out fold (`stable_winner`); right now there is none, and the
  weights are a diagnostic, not the prediction.
- **Firing-time labels are uncertain.** A cycle's true firing time is only known
  to within the gap between its last pre-reset sample and first post-reset
  sample — tens to hundreds of minutes for loosely-sampled cycles. Only
  tightly-bracketed cycles are used for error/coverage measurement; the rest are
  flagged. Tightening these labels (endgame fast-polling, self-chaining
  collection) is the current top priority.

```bash
pip install -r requirements.txt
python3 predict.py                 # reads data/voteparty.jsonl
python3 predict.py --no-graph      # text/JSON only, skip the PNG
```

Outputs (under `data/`):
- **`prediction.png`** — current cycle, each model's projection, the ensemble
  ETA with its spread band, weight bars, and historical cycle fill curves.
- **`prediction.json`** — machine-readable per-model + ensemble prediction.
- **`PREDICTION.md`** — human-readable summary, regenerated every run.

The scheduled workflow runs this after each polling window, so the committed
prediction always reflects the latest data.

## Accuracy backtest (`accuracy.py`)

`accuracy.py` measures how good the predictor is **at each stage of a cycle**.
For every completed cycle it replays the cycle point by point and, at each
stage, predicts the firing time using only the data available up to that
point — then compares to when the party actually fired.

- **Ground truth:** the exact 5,000 crossing is never logged (the counter
  resets first), so each cycle's reference firing time is estimated by
  extrapolating its final observed segment to target. Cycles whose last
  observation is well below target have a looser reference (reported).
- **No leakage:** ensemble weights are computed **leave-one-cycle-out** — a
  cycle is never scored using knowledge of itself.

```bash
python3 accuracy.py                 # reads data/voteparty.jsonl
```

Outputs `data/accuracy.png` (|ETA error| vs cycle progress, per cycle and per
model) and `data/accuracy.json` (raw stage errors + a stage-bucket summary).

Measured mean |ETA error| by stage (current data, 4 completed cycles):

| Stage | Ensemble | Diurnal (best) | Shrinkage |
|-------|----------|----------------|-----------|
| 0–25% | ~208 min | **~131 min** | ~184 min |
| 25–50% | ~94 min | **~63 min** | ~140 min |
| 50–75% | ~44 min | **~36 min** | ~85 min |
| 75–100% | ~15 min | **~15 min** | ~45 min |

Error shrinks as the cycle fills. The `diurnal` model is now the standout at
every stage, which is why the backtest gives it the top weight (~0.4). These
numbers move as cycles accumulate — the ensemble re-weights automatically.

## Model performance report (`model_report.py`)

`model_report.py` produces a detailed per-model scorecard from the same
leave-one-out backtest: overall MAE / RMSE / median / P90, **bias** (does the
model predict too early or too late?), coverage, current weight, and a per-stage
MAE breakdown.

```bash
python3 model_report.py                 # reads data/voteparty.jsonl
```

Outputs `data/model_report.png` (MAE heatmap by model × stage, ranked MAE, and
bias chart) plus `data/model_report.md` / `.json` with the full tables. A
current finding: every model has a **negative bias** — they all tend to predict
the party a bit *earlier* than it actually fires — which is a candidate for a
future bias-correction term.

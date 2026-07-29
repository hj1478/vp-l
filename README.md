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

The **reported point + interval are one coherent model, `shape_analogue`** (see
"Honest status" below). It also runs **nine independent candidate models** and
ensembles them, but only as **diagnostics**:

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

**Why shape matters:** the vote process is nearly stationary across cycles
(historical cycles average ~390–410 votes/hr, player count only weakly predicts
rate, r≈0.1), so the historical rate is a strong prior — which `shrinkage`
exploits. But the rate is *not* flat within a cycle: it rises and falls with the
time of day. The **shipped `shape_analogue`** model banks that shape (see below);
`diurnal` is the candidate-pool member that captures it.

**Weighting (diagnostic ensemble):** each model's ETA is weighted by a **rolling-origin backtest** on
the completed historical cycles, scored by **inverse mean-squared ETA error**
(how far its predicted *firing time* lands from the actual firing time) — not
just next-point accuracy. Weights are **stage-aware**: computed per
cycle-progress bucket, so the ensemble trusts shrinkage early and the reactive
models late.

### ⚠️ Honest status of the modeling (read this)

Out-of-sample testing at the current sample size (a handful of cycles) exposed
real limits, and the system is deliberately conservative as a result:

- **The reported prediction is the `shape_analogue` model, for both the point
  (its median) and the interval (its quantiles)** — one coherent distribution, no
  grafting. It borrows past cycles' remaining trajectories like the plain
  `analogue`, but **re-times each one through the current diurnal phase** instead
  of copying its absolute remaining duration. Validated causally (paired
  cluster-bootstrap): it beats the plain analogue's point by **~11 min, 95% CI
  [−17, −4]** (excludes zero), banking the shape-oracle headroom, while being
  better-calibrated. It falls back to the plain `analogue` before a diurnal
  profile is estimable. `diurnal`, `diurnal_dow`, the ensemble, `nhpp`, etc.
  remain as diagnostics.
- **The interval is measured to be ~calibrated** (~79% coverage at 80% nominal
  on tight cycles, better than the plain analogue's over-wide ~92%), because its
  spread is the *real* historical spread of past cycles' remaining trajectories —
  not a process assumption (the NHPP's parametric interval was overconfident at
  ~19% and is shelved).
- **Ensemble weights are shrunk toward uniform (Occam prior).** Hard
  inverse-error weights fit on a few cycles swing the top weight by ±0.4 —
  sampling noise, not skill. Weights are pulled toward equal by λ = n/(n+6)
  (in cycles), so they only differentiate once many cycles give strong, stable
  evidence. We **do not name a "winning" model** until it wins *every*
  leave-one-cycle-out fold (`stable_winner`); right now there is none, and the
  weights are a diagnostic, not the prediction.
- **Firing-time labels: recovered, not binarized.** A cycle's firing time is
  *not* as uncertain as the raw sample gap suggests — when the last sample is
  near target, extrapolating the trajectory to 5000 pins it tightly (a cycle
  last seen at 98% is known to ~2 min even if the collector then went dark for an
  hour). Each cycle gets a continuous **label σ** (extrapolation uncertainty),
  used to (a) recover cycles the raw-gap gate wrongly discarded,
  (b) inverse-variance weight cycles in model selection, and (c) carry each
  borrowed analogue endpoint's uncertainty into the interval. The one genuinely
  loose cycle (last seen at 81%, ~1000 votes out) stays down-weighted.
- **Display precision = interval resolution.** The point is rounded to match the
  interval width (±2h interval → "~17:00", never a false "17:30").
- **Every OOS metric carries a cluster-bootstrap 95% CI** over cycles, and it is
  deliberately wide (shape_analogue MAE ~20 min, CI ~[13, 29]; 80% coverage ~79%,
  CI ~[70, 90] on tight cycles) — a point-metric from ~12 cycles is not precise,
  and we show that rather than hide it.

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

A separate hourly **analysis** workflow regenerates this (and the diagnostics)
from the committed data, so the prediction tracks the latest data without
holding up collection. A **Discord** workflow (`discord_notify.py`) can post the
current prediction and its margins to a webhook every hour (set the
`DISCORD_WEBHOOK_URL` repo secret).

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

> This is a **candidate-model diagnostic** — it profiles the nine candidate
> models and their ensemble, *not* the shipped `shape_analogue` model. For the
> shipped model's out-of-sample accuracy (MAE by stage, causal), see
> **`data/PREDICTION_LOG.md`** (produced by `predlog.py`). As a rule, error
> shrinks sharply as the cycle fills — tens of minutes early, ~10 min in the
> final decile — for every model; the live numbers move as cycles accumulate.

## Model performance report (`model_report.py`)

`model_report.py` produces a detailed per-model scorecard from the same
leave-one-out backtest: overall MAE / RMSE / median / P90, **bias** (does the
model predict too early or too late?), coverage, current weight, and a per-stage
MAE breakdown.

```bash
python3 model_report.py                 # reads data/voteparty.jsonl
```

Outputs `data/model_report.png` (MAE heatmap by model × stage, ranked MAE, and
bias chart) plus `data/model_report.md` / `.json` with the full tables. Like the
accuracy backtest, this scores the **candidate models** (a diagnostic), not the
shipped `shape_analogue`. Bias varies by model and shifts as data accrues (most
candidates currently run slightly *late*, i.e. positive bias) — see the live
`model_report.md` for current figures.

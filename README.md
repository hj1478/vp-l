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

It runs **six independent models** and **ensembles** them:

| Model | Idea |
|-------|------|
| `linear` | OLS regression over the whole cycle |
| `recent` | slope of the last k points (short-term rate) |
| `ewma` | exponentially-weighted average of per-interval rates |
| `theilsen` | Theil–Sen robust median-slope regression |
| `wls` | least squares with exponential recency weights |
| `quadratic` | 2nd-order fit, solves for the target crossing (accel/decel) |

Each model's ETA is weighted by a **rolling-origin backtest** on the *completed*
historical cycles: models are scored by inverse mean-squared extrapolation
error, so consistently-accurate models dominate and outliers are down-weighted
automatically.

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
The headline finding: error shrinks as the cycle fills — roughly a couple of
hours off at ~30% complete, down to ~15–20 minutes past 75%.

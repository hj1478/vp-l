# Vote Party Prediction

_Generated 2026-07-19T11:14:26Z — recomputed every data update._

**Progress:** 4039 / 5000.0 (80.8%) — 961 remaining
**Players online:** 510  |  **Cycle started:** 2026-07-19T01:50:55Z  |  **Data points this cycle:** 36

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-19T13:14:30Z`**
Calibrated confidence: **±15 min** (`2026-07-19T12:59:48Z` → `2026-07-19T13:29:11Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-19T12:51:43Z` → `2026-07-19T13:51:49Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| quadratic | 2026-07-19T12:51:43Z | 0.381 | 4.44793 |
| diurnal | 2026-07-19T13:24:26Z | 0.236 | 1.23859 |
| wls | 2026-07-19T13:25:03Z | 0.085 | 2.39243 |
| shrinkage | 2026-07-19T13:41:48Z | 0.075 | 2.12742 |
| ewma | 2026-07-19T13:12:56Z | 0.075 | 2.78818 |
| linear | 2026-07-19T13:51:49Z | 0.056 | 2.53637 |
| theilsen | 2026-07-19T13:47:29Z | 0.051 | 2.64368 |
| recent | 2026-07-19T13:08:13Z | 0.041 | 3.63121 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

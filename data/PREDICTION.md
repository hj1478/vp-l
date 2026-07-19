# Vote Party Prediction

_Generated 2026-07-18T22:46:27Z — recomputed every data update._

**Progress:** 4038 / 5000.0 (80.8%) — 962 remaining
**Players online:** 546  |  **Cycle started:** 2026-07-18T11:51:06Z  |  **Data points this cycle:** 108

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-19T01:57:45Z`**
Calibrated confidence: **±15 min** (`2026-07-19T01:43:07Z` → `2026-07-19T02:12:23Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-19T01:21:03Z` → `2026-07-19T02:31:03Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| quadratic | 2026-07-19T02:09:11Z | 0.262 | 1.05846 |
| shrinkage | 2026-07-19T01:21:42Z | 0.210 | 0.77396 |
| ewma | 2026-07-19T02:23:39Z | 0.168 | 1.15774 |
| recent | 2026-07-19T02:31:03Z | 0.140 | 1.23207 |
| wls | 2026-07-19T02:04:05Z | 0.081 | 1.31572 |
| linear | 2026-07-19T01:23:33Z | 0.070 | 1.33777 |
| theilsen | 2026-07-19T01:21:03Z | 0.069 | 1.31598 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

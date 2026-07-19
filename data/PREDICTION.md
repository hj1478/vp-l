# Vote Party Prediction

_Generated 2026-07-18T12:46:06Z — recomputed every data update._

**Progress:** 748 / 5000.0 (15.0%) — 4252 remaining
**Players online:** 601  |  **Cycle started:** 2026-07-18T11:51:06Z  |  **Data points this cycle:** 12

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-18T21:30:35Z`**
Calibrated confidence: **±120 min** (`2026-07-18T19:30:52Z` → `2026-07-18T23:30:18Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-18T17:30:32Z` → `2026-07-18T23:02:49Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| shrinkage | 2026-07-18T23:02:49Z | 0.361 | 0.77396 |
| ewma | 2026-07-18T21:41:56Z | 0.120 | 1.15774 |
| quadratic | 2026-07-18T17:30:32Z | 0.117 | 1.05846 |
| recent | 2026-07-18T21:02:10Z | 0.107 | 1.23207 |
| theilsen | 2026-07-18T21:23:51Z | 0.100 | 1.31598 |
| wls | 2026-07-18T21:12:11Z | 0.098 | 1.31572 |
| linear | 2026-07-18T21:19:24Z | 0.097 | 1.33777 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

# Vote Party Prediction

_Generated 2026-07-19T19:48:09Z — recomputed every data update._

**Progress:** 2507 / 5000.0 (50.1%) — 2493 remaining
**Players online:** 524  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 68

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T03:52:07Z`**
Calibrated confidence: **±40 min** (`2026-07-20T03:12:00Z` → `2026-07-20T04:32:15Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T02:18:40Z` → `2026-07-20T05:40:55Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T04:18:09Z | 0.394 | 1.06707 |
| wls | 2026-07-20T03:47:04Z | 0.117 | 2.93923 |
| ewma | 2026-07-20T04:36:00Z | 0.113 | 3.16131 |
| shrinkage | 2026-07-20T02:20:15Z | 0.105 | 1.98583 |
| linear | 2026-07-20T02:18:40Z | 0.091 | 3.05697 |
| recent | 2026-07-20T05:40:55Z | 0.081 | 3.69949 |
| theilsen | 2026-07-20T02:24:04Z | 0.060 | 3.25194 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

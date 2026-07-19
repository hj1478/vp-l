# Vote Party Prediction

_Generated 2026-07-19T23:37:05Z — recomputed every data update._

**Progress:** 3391 / 5000.0 (67.8%) — 1609 remaining
**Players online:** 533  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 104

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T05:40:27Z`**
Calibrated confidence: **±40 min** (`2026-07-20T05:00:20Z` → `2026-07-20T06:20:35Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T04:06:40Z` → `2026-07-20T08:25:39Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T05:22:05Z | 0.394 | 1.06707 |
| wls | 2026-07-20T06:16:08Z | 0.117 | 2.93923 |
| ewma | 2026-07-20T07:37:27Z | 0.113 | 3.16131 |
| shrinkage | 2026-07-20T04:06:40Z | 0.105 | 1.98583 |
| linear | 2026-07-20T04:10:50Z | 0.091 | 3.05697 |
| recent | 2026-07-20T08:25:39Z | 0.081 | 3.69949 |
| theilsen | 2026-07-20T04:07:39Z | 0.060 | 3.25194 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

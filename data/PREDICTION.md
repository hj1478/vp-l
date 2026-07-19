# Vote Party Prediction

_Generated 2026-07-19T20:58:28Z — recomputed every data update._

**Progress:** 2762 / 5000.0 (55.2%) — 2238 remaining
**Players online:** 520  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 80

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T04:46:39Z`**
Calibrated confidence: **±40 min** (`2026-07-20T04:06:31Z` → `2026-07-20T05:26:46Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T02:50:37Z` → `2026-07-20T06:31:43Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T04:43:28Z | 0.394 | 1.06707 |
| wls | 2026-07-20T06:31:43Z | 0.117 | 2.93923 |
| ewma | 2026-07-20T06:10:25Z | 0.113 | 3.16131 |
| shrinkage | 2026-07-20T02:56:06Z | 0.105 | 1.98583 |
| linear | 2026-07-20T02:54:48Z | 0.091 | 3.05697 |
| recent | 2026-07-20T06:28:37Z | 0.081 | 3.69949 |
| theilsen | 2026-07-20T02:50:37Z | 0.060 | 3.25194 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

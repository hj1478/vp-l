# Vote Party Prediction

_Generated 2026-07-19T22:37:28Z — recomputed every data update._

**Progress:** 3174 / 5000.0 (63.5%) — 1826 remaining
**Players online:** 522  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 92

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T04:38:25Z`**
Calibrated confidence: **±40 min** (`2026-07-20T03:58:17Z` → `2026-07-20T05:18:32Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T03:25:56Z` → `2026-07-20T06:03:17Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T04:32:28Z | 0.394 | 1.06707 |
| wls | 2026-07-20T06:03:17Z | 0.117 | 2.93923 |
| ewma | 2026-07-20T05:18:08Z | 0.113 | 3.16131 |
| shrinkage | 2026-07-20T03:36:07Z | 0.105 | 1.98583 |
| linear | 2026-07-20T03:41:06Z | 0.091 | 3.05697 |
| recent | 2026-07-20T05:28:27Z | 0.081 | 3.69949 |
| theilsen | 2026-07-20T03:25:56Z | 0.060 | 3.25194 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

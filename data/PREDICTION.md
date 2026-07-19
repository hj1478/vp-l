# Vote Party Prediction

_Generated 2026-07-19T17:41:28Z — recomputed every data update._

**Progress:** 1850 / 5000.0 (37.0%) — 3150 remaining
**Players online:** 577  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 44

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T03:07:43Z`**
Calibrated confidence: **±117 min** (`2026-07-20T01:10:42Z` → `2026-07-20T05:04:45Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T01:32:09Z` → `2026-07-20T04:00:43Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T03:56:28Z | 0.527 | 1.06707 |
| shrinkage | 2026-07-20T01:46:01Z | 0.156 | 1.98583 |
| wls | 2026-07-20T01:59:32Z | 0.066 | 2.93923 |
| linear | 2026-07-20T01:32:09Z | 0.061 | 3.05697 |
| ewma | 2026-07-20T03:05:01Z | 0.057 | 3.16131 |
| theilsen | 2026-07-20T01:42:51Z | 0.055 | 3.25194 |
| recent | 2026-07-20T04:00:43Z | 0.042 | 3.69949 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

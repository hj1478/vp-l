# Vote Party Prediction

_Generated 2026-07-19T15:17:36Z — recomputed every data update._

**Progress:** 979 / 5000.0 (19.6%) — 4021 remaining
**Players online:** 545  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 20

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T02:11:16Z`**
Calibrated confidence: **±117 min** (`2026-07-20T00:14:14Z` → `2026-07-20T04:08:17Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T00:00:54Z` → `2026-07-20T03:17:36Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T03:17:36Z | 0.527 | 1.06707 |
| shrinkage | 2026-07-20T01:19:39Z | 0.156 | 1.98583 |
| wls | 2026-07-20T00:22:51Z | 0.066 | 2.93923 |
| linear | 2026-07-20T00:00:54Z | 0.061 | 3.05697 |
| ewma | 2026-07-20T01:22:23Z | 0.057 | 3.16131 |
| theilsen | 2026-07-20T00:06:05Z | 0.055 | 3.25194 |
| recent | 2026-07-20T01:19:08Z | 0.042 | 3.69949 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

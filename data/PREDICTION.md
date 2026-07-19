# Vote Party Prediction

_Generated 2026-07-19T16:43:52Z — recomputed every data update._

**Progress:** 1510 / 5000.0 (30.2%) — 3490 remaining
**Players online:** 579  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 32

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T02:14:24Z`**
Calibrated confidence: **±117 min** (`2026-07-20T00:17:23Z` → `2026-07-20T04:11:26Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T00:56:28Z` → `2026-07-20T02:53:52Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T02:53:52Z | 0.527 | 1.06707 |
| shrinkage | 2026-07-20T01:36:28Z | 0.156 | 1.98583 |
| wls | 2026-07-20T01:59:23Z | 0.066 | 2.93923 |
| linear | 2026-07-20T01:17:27Z | 0.061 | 3.05697 |
| ewma | 2026-07-20T00:57:29Z | 0.057 | 3.16131 |
| theilsen | 2026-07-20T01:23:18Z | 0.055 | 3.25194 |
| recent | 2026-07-20T00:56:28Z | 0.042 | 3.69949 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

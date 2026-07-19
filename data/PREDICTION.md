# Vote Party Prediction

_Generated 2026-07-19T13:52:00Z — recomputed every data update._

**Progress:** 355 / 5000.0 (7.1%) — 4645 remaining
**Players online:** 589  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 8

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T01:54:43Z`**
Calibrated confidence: **±117 min** (`2026-07-19T23:57:41Z` → `2026-07-20T03:51:44Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-19T22:30:15Z` → `2026-07-20T03:37:00Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T03:37:00Z | 0.527 | 1.06707 |
| shrinkage | 2026-07-20T01:28:51Z | 0.156 | 1.98583 |
| wls | 2026-07-19T22:49:21Z | 0.066 | 2.93923 |
| linear | 2026-07-19T22:34:25Z | 0.061 | 3.05697 |
| ewma | 2026-07-19T23:22:12Z | 0.057 | 3.16131 |
| theilsen | 2026-07-19T22:30:15Z | 0.055 | 3.25194 |
| recent | 2026-07-19T23:41:04Z | 0.042 | 3.69949 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

# Vote Party Prediction

_Generated 2026-07-19T18:45:52Z — recomputed every data update._

**Progress:** 2204 / 5000.0 (44.1%) — 2796 remaining
**Players online:** 594  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 56

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T03:21:35Z`**
Calibrated confidence: **±117 min** (`2026-07-20T01:24:33Z` → `2026-07-20T05:18:37Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T01:53:59Z` → `2026-07-20T04:18:26Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T04:00:52Z | 0.527 | 1.06707 |
| shrinkage | 2026-07-20T02:01:23Z | 0.156 | 1.98583 |
| wls | 2026-07-20T02:54:37Z | 0.066 | 2.93923 |
| linear | 2026-07-20T01:53:59Z | 0.061 | 3.05697 |
| ewma | 2026-07-20T03:33:11Z | 0.057 | 3.16131 |
| theilsen | 2026-07-20T02:07:17Z | 0.055 | 3.25194 |
| recent | 2026-07-20T04:18:26Z | 0.042 | 3.69949 |
| quadratic | n/a | 0.037 | 3.68622 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

# Vote Party Prediction

_Generated 2026-07-20T00:44:34Z — recomputed every data update._

**Progress:** 3888 / 5000.0 (77.8%) — 1112 remaining
**Players online:** 514  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 116

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-20T03:47:24Z`**
Calibrated confidence: **±9 min** (`2026-07-20T03:38:54Z` → `2026-07-20T03:55:55Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-20T03:16:22Z` → `2026-07-20T04:24:47Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T03:54:34Z | 0.355 | 1.06707 |
| quadratic | n/a | 0.146 | 3.68622 |
| ewma | 2026-07-20T03:16:54Z | 0.123 | 3.16131 |
| wls | 2026-07-20T03:45:50Z | 0.122 | 2.93923 |
| shrinkage | 2026-07-20T03:53:52Z | 0.092 | 1.98583 |
| recent | 2026-07-20T03:16:22Z | 0.075 | 3.69949 |
| linear | 2026-07-20T04:23:06Z | 0.047 | 3.05697 |
| theilsen | 2026-07-20T04:24:47Z | 0.040 | 3.25194 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

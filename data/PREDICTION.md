# Vote Party Prediction

_Generated 2026-07-19T12:44:02Z — recomputed every data update._

**Progress:** 4688 / 5000.0 (93.8%) — 312 remaining
**Players online:** 639  |  **Cycle started:** 2026-07-19T01:50:55Z  |  **Data points this cycle:** 48

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-19T13:21:28Z`**
Calibrated confidence: **±15 min** (`2026-07-19T13:06:47Z` → `2026-07-19T13:36:10Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-19T13:08:35Z` → `2026-07-19T13:38:10Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| quadratic | 2026-07-19T13:08:35Z | 0.381 | 4.44793 |
| diurnal | 2026-07-19T13:29:02Z | 0.236 | 1.23859 |
| wls | 2026-07-19T13:25:50Z | 0.085 | 2.39243 |
| shrinkage | 2026-07-19T13:30:59Z | 0.075 | 2.12742 |
| ewma | 2026-07-19T13:26:27Z | 0.075 | 2.78818 |
| linear | 2026-07-19T13:38:10Z | 0.056 | 2.53637 |
| theilsen | 2026-07-19T13:31:58Z | 0.051 | 2.64368 |
| recent | 2026-07-19T13:26:22Z | 0.041 | 3.63121 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

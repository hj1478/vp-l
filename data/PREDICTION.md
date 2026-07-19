# Vote Party Prediction

_Generated 2026-07-19T06:09:08Z — recomputed every data update._

**Progress:** 1670 / 5000.0 (33.4%) — 3330 remaining
**Players online:** 431  |  **Cycle started:** 2026-07-19T01:50:55Z  |  **Data points this cycle:** 24

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-19T15:25:15Z`**
Calibrated confidence: **±162 min** (`2026-07-19T12:43:17Z` → `2026-07-19T18:07:14Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-19T11:57:03Z` → `2026-07-19T16:33:39Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| shrinkage | 2026-07-19T15:14:39Z | 0.248 | 2.12742 |
| wls | 2026-07-19T16:08:08Z | 0.182 | 2.39243 |
| linear | 2026-07-19T16:33:16Z | 0.163 | 2.53637 |
| theilsen | 2026-07-19T16:33:39Z | 0.150 | 2.64368 |
| ewma | 2026-07-19T14:20:59Z | 0.133 | 2.78818 |
| recent | 2026-07-19T13:31:39Z | 0.078 | 3.63121 |
| quadratic | 2026-07-19T11:57:03Z | 0.044 | 4.44793 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

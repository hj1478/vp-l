# Vote Party Prediction

_Generated 2026-07-19T02:45:55Z — recomputed every data update._

**Progress:** 496 / 5000.0 (9.9%) — 4504 remaining
**Players online:** 517  |  **Cycle started:** 2026-07-19T01:50:55Z  |  **Data points this cycle:** 12

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-19T18:53:12Z`**
Calibrated confidence: **±162 min** (`2026-07-19T16:11:14Z` → `2026-07-19T21:35:11Z`) — the ensemble's measured error at this cycle stage.
Model spread: `2026-07-19T11:31:20Z` → `2026-07-19T21:00:27Z`

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| shrinkage | 2026-07-19T14:59:49Z | 0.248 | 2.12742 |
| wls | 2026-07-19T20:39:22Z | 0.182 | 2.39243 |
| linear | 2026-07-19T21:00:27Z | 0.163 | 2.53637 |
| theilsen | 2026-07-19T20:56:28Z | 0.150 | 2.64368 |
| ewma | 2026-07-19T20:50:58Z | 0.133 | 2.78818 |
| recent | 2026-07-19T19:29:56Z | 0.078 | 3.63121 |
| quadratic | 2026-07-19T11:31:20Z | 0.044 | 4.44793 |

Weights come from a rolling-origin backtest on completed cycles (leave-one-out for history-aware models): each model's inverse mean-squared extrapolation error, normalised. See `prediction.png`.

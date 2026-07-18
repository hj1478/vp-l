# Vote Party Prediction

_Generated 2026-07-18T22:46:27Z — recomputed every data update._

**Progress:** 4038 / 5000.0 (80.8%) — 962 remaining
**Players online:** 546  |  **Cycle started:** 2026-07-18T11:51:06Z  |  **Data points this cycle:** 108

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-19T01:59:23Z`**
Model spread: `2026-07-19T01:21:03Z` → `2026-07-19T02:31:03Z` (±28 min)

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| ewma | 2026-07-19T02:23:39Z | 0.215 | 0.06557 |
| recent | 2026-07-19T02:31:03Z | 0.196 | 0.06861 |
| theilsen | 2026-07-19T01:21:03Z | 0.177 | 0.07219 |
| wls | 2026-07-19T02:04:05Z | 0.176 | 0.07251 |
| linear | 2026-07-19T01:23:33Z | 0.170 | 0.0736 |
| quadratic | 2026-07-19T02:09:11Z | 0.066 | 0.11829 |

Weights come from a rolling-origin backtest on completed cycles: each model's inverse mean-squared extrapolation error, normalised. Lower RMSE → higher weight. See `prediction.png` for the graph.

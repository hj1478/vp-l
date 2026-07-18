# Vote Party Prediction

_Generated 2026-07-18T19:44:51Z — recomputed every data update._

**Progress:** 3131 / 5000.0 (62.6%) — 1869 remaining
**Players online:** 596  |  **Cycle started:** 2026-07-18T11:51:06Z  |  **Data points this cycle:** 84

## 🎯 Ensemble prediction

**Vote party fires ≈ `2026-07-19T01:55:18Z`**
Model spread: `2026-07-19T01:05:52Z` → `2026-07-19T03:50:30Z` (±57 min)

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| ewma | 2026-07-19T02:01:22Z | 0.215 | 0.06557 |
| recent | 2026-07-19T03:13:49Z | 0.196 | 0.06861 |
| theilsen | 2026-07-19T01:05:52Z | 0.177 | 0.07219 |
| wls | 2026-07-19T01:09:34Z | 0.176 | 0.07251 |
| linear | 2026-07-19T01:11:13Z | 0.170 | 0.0736 |
| quadratic | 2026-07-19T03:50:30Z | 0.066 | 0.11829 |

Weights come from a rolling-origin backtest on completed cycles: each model's inverse mean-squared extrapolation error, normalised. Lower RMSE → higher weight. See `prediction.png` for the graph.

# Model Performance Report

Leave-one-cycle-out backtest over **28 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

> ⚠️ **Diagnostic only.** These are the nine candidate models and their ensemble — NONE is the shipped reported model (`shape_analogue`). For the shipped model's out-of-sample accuracy see `PREDICTION_LOG.md`.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.291 | 28.7 | 37.2 | 22.5 | 63.0 | +11.7 | 100% | 2815 |
| diurnal | 0.251 | 29.9 | 39.3 | 22.6 | 69.1 | +12.8 | 100% | 2815 |
| ensemble _(diag)_ | — | 40.1 | 54.0 | 29.5 | 89.4 | +14.6 | 100% | 2815 |
| shrinkage | 0.134 | 54.1 | 68.5 | 43.9 | 114.9 | +7.1 | 100% | 2815 |
| quadratic | 0.042 | 88.1 | 165.5 | 30.7 | 270.1 | -9.4 | 68% | 1928 |
| wls | 0.081 | 88.8 | 142.8 | 47.4 | 232.8 | +22.8 | 100% | 2815 |
| linear | 0.060 | 100.0 | 140.1 | 67.0 | 225.1 | +18.0 | 100% | 2815 |
| theilsen | 0.057 | 105.0 | 151.3 | 69.3 | 230.4 | +21.8 | 100% | 2815 |
| ewma | 0.051 | 105.7 | 183.3 | 52.2 | 269.4 | +37.7 | 100% | 2815 |
| recent | 0.033 | 113.9 | 218.3 | 54.5 | 290.2 | +45.6 | 100% | 2815 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 31.7 | 39.2 | 33.2 | 25.5 | 12.2 |
| diurnal | 32.3 | 40.7 | 35.1 | 27.7 | 12.4 |
| ensemble | 65.0 | 50.3 | 38.5 | 30.2 | 13.6 |
| shrinkage | 73.6 | 83.4 | 55.3 | 37.6 | 14.3 |
| quadratic | 377.1 | 143.3 | 58.1 | 50.4 | 22.4 |
| wls | 215.3 | 110.5 | 56.9 | 35.3 | 12.4 |
| linear | 206.0 | 128.0 | 73.3 | 51.8 | 27.8 |
| theilsen | 214.2 | 138.5 | 78.9 | 52.7 | 26.2 |
| ewma | 247.8 | 136.4 | 71.3 | 39.0 | 15.6 |
| recent | 262.6 | 142.2 | 82.3 | 38.0 | 22.3 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

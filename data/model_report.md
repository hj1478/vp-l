# Model Performance Report

Leave-one-cycle-out backtest over **24 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

> ⚠️ **Diagnostic only.** These are the nine candidate models and their ensemble — NONE is the shipped reported model (`shape_analogue`). For the shipped model's out-of-sample accuracy see `PREDICTION_LOG.md`.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.338 | 30.5 | 38.8 | 24.9 | 65.0 | +9.5 | 100% | 1986 |
| diurnal | 0.322 | 31.0 | 40.0 | 25.2 | 69.9 | +9.8 | 100% | 1986 |
| ensemble _(diag)_ | — | 44.0 | 58.2 | 33.2 | 96.8 | +11.4 | 100% | 1986 |
| shrinkage | 0.109 | 58.1 | 72.5 | 48.0 | 118.7 | +3.1 | 100% | 1986 |
| quadratic | 0.035 | 78.9 | 164.2 | 26.5 | 232.2 | -6.3 | 68% | 1343 |
| wls | 0.043 | 93.0 | 142.5 | 53.0 | 235.8 | +16.4 | 100% | 1986 |
| ewma | 0.037 | 105.5 | 169.8 | 57.7 | 271.5 | +29.2 | 100% | 1986 |
| linear | 0.043 | 106.4 | 144.5 | 75.9 | 224.5 | +11.5 | 100% | 1986 |
| theilsen | 0.040 | 112.3 | 155.3 | 82.8 | 227.1 | +15.2 | 100% | 1986 |
| recent | 0.034 | 113.5 | 192.3 | 57.7 | 291.5 | +38.1 | 100% | 1986 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 35.1 | 42.0 | 33.3 | 23.7 | 13.5 |
| diurnal | 34.4 | 43.3 | 34.0 | 24.0 | 14.0 |
| ensemble | 69.6 | 59.6 | 40.0 | 26.2 | 15.4 |
| shrinkage | 69.7 | 86.8 | 64.7 | 39.4 | 17.3 |
| quadratic | 423.3 | 131.8 | 50.4 | 24.9 | 18.9 |
| wls | 205.6 | 129.2 | 59.5 | 28.4 | 16.2 |
| ewma | 223.1 | 152.8 | 70.5 | 29.0 | 20.4 |
| linear | 198.0 | 134.8 | 87.1 | 59.8 | 31.3 |
| theilsen | 202.0 | 148.1 | 95.7 | 61.0 | 30.8 |
| recent | 234.9 | 158.5 | 81.2 | 28.9 | 29.5 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

# Model Performance Report

Leave-one-cycle-out backtest over **23 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

> ⚠️ **Diagnostic only.** These are the nine candidate models and their ensemble — NONE is the shipped reported model (`shape_analogue`). For the shipped model's out-of-sample accuracy see `PREDICTION_LOG.md`.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.292 | 30.9 | 39.6 | 24.9 | 66.6 | +8.5 | 100% | 1813 |
| diurnal | 0.277 | 31.4 | 40.8 | 25.0 | 71.6 | +8.8 | 100% | 1813 |
| ensemble _(diag)_ | — | 45.0 | 59.6 | 33.6 | 99.0 | +9.5 | 100% | 1813 |
| shrinkage | 0.106 | 57.7 | 72.3 | 46.1 | 118.8 | -1.0 | 100% | 1813 |
| quadratic | 0.057 | 84.5 | 171.6 | 30.0 | 244.8 | -7.4 | 67% | 1221 |
| wls | 0.070 | 95.2 | 145.0 | 55.0 | 235.5 | +12.8 | 100% | 1813 |
| ewma | 0.053 | 107.2 | 171.6 | 61.1 | 267.9 | +25.7 | 100% | 1813 |
| linear | 0.053 | 109.1 | 148.5 | 78.2 | 228.0 | +6.0 | 100% | 1813 |
| theilsen | 0.048 | 114.8 | 158.9 | 87.4 | 229.0 | +9.3 | 100% | 1813 |
| recent | 0.043 | 115.1 | 195.1 | 59.9 | 288.1 | +34.8 | 100% | 1813 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 35.5 | 42.4 | 33.4 | 24.1 | 13.7 |
| diurnal | 35.1 | 43.0 | 34.3 | 24.4 | 14.4 |
| ensemble | 71.9 | 59.8 | 40.3 | 26.4 | 15.8 |
| shrinkage | 68.5 | 84.1 | 64.6 | 39.2 | 17.5 |
| quadratic | 423.3 | 136.4 | 53.5 | 25.8 | 20.2 |
| wls | 212.8 | 125.1 | 61.2 | 28.6 | 17.5 |
| ewma | 225.4 | 149.2 | 72.8 | 29.8 | 22.3 |
| linear | 206.4 | 133.0 | 88.6 | 60.4 | 31.2 |
| theilsen | 210.5 | 143.4 | 98.4 | 61.8 | 31.0 |
| recent | 237.4 | 152.6 | 83.5 | 30.2 | 32.7 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

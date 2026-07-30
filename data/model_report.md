# Model Performance Report

Leave-one-cycle-out backtest over **25 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

> ⚠️ **Diagnostic only.** These are the nine candidate models and their ensemble — NONE is the shipped reported model (`shape_analogue`). For the shipped model's out-of-sample accuracy see `PREDICTION_LOG.md`.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.344 | 30.3 | 39.1 | 24.5 | 65.9 | +10.9 | 100% | 2197 |
| diurnal | 0.317 | 31.7 | 41.2 | 25.3 | 72.7 | +11.9 | 100% | 2197 |
| ensemble _(diag)_ | — | 43.4 | 57.9 | 32.9 | 94.4 | +12.6 | 100% | 2197 |
| shrinkage | 0.115 | 55.4 | 69.9 | 44.8 | 116.0 | +2.8 | 100% | 2197 |
| quadratic | 0.034 | 92.0 | 173.7 | 32.1 | 281.0 | -8.0 | 68% | 1501 |
| wls | 0.042 | 92.1 | 143.7 | 53.0 | 231.6 | +17.1 | 100% | 2197 |
| linear | 0.043 | 102.3 | 141.1 | 72.6 | 219.2 | +9.4 | 100% | 2197 |
| ewma | 0.034 | 107.4 | 183.8 | 58.8 | 267.6 | +32.5 | 100% | 2197 |
| theilsen | 0.040 | 108.5 | 154.0 | 76.3 | 224.8 | +13.6 | 100% | 2197 |
| recent | 0.030 | 117.2 | 226.6 | 58.8 | 288.3 | +41.7 | 100% | 2197 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 33.2 | 41.5 | 34.9 | 25.4 | 12.5 |
| diurnal | 34.1 | 43.1 | 36.4 | 27.4 | 13.3 |
| ensemble | 66.5 | 56.7 | 41.3 | 31.2 | 15.0 |
| shrinkage | 65.6 | 84.6 | 59.8 | 40.2 | 16.6 |
| quadratic | 417.2 | 146.8 | 58.6 | 45.0 | 24.9 |
| wls | 204.6 | 126.2 | 59.2 | 36.2 | 14.6 |
| linear | 193.9 | 131.7 | 81.4 | 56.3 | 30.7 |
| ewma | 231.6 | 148.3 | 74.3 | 38.6 | 18.9 |
| theilsen | 201.3 | 144.2 | 88.7 | 57.9 | 30.1 |
| recent | 253.4 | 154.5 | 84.9 | 37.3 | 27.2 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

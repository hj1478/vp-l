# Model Performance Report

Leave-one-cycle-out backtest over **11 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.282 | 34.2 | 43.8 | 27.5 | 75.5 | -2.2 | 105% | 669 |
| diurnal | 0.257 | 36.8 | 46.1 | 31.9 | 83.6 | -0.8 | 105% | 669 |
| **ensemble** | — | 56.7 | 74.3 | 40.8 | 129.5 | -4.2 | 105% | 669 |
| shrinkage | 0.103 | 65.7 | 83.1 | 48.4 | 155.9 | -23.4 | 105% | 669 |
| quadratic | 0.055 | 78.8 | 149.8 | 29.0 | 227.2 | -11.0 | 54% | 342 |
| wls | 0.064 | 94.8 | 134.7 | 58.4 | 225.7 | -3.0 | 105% | 669 |
| linear | 0.063 | 99.4 | 137.0 | 65.1 | 224.8 | -22.3 | 105% | 669 |
| theilsen | 0.062 | 106.5 | 143.4 | 76.0 | 233.9 | -17.7 | 105% | 669 |
| ewma | 0.058 | 107.5 | 158.4 | 69.0 | 268.1 | +12.9 | 105% | 669 |
| recent | 0.056 | 113.2 | 173.7 | 66.1 | 290.6 | +19.1 | 105% | 669 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 45.9 | 44.4 | 30.9 | 30.2 | 12.6 |
| diurnal | 52.9 | 46.4 | 31.4 | 33.4 | 14.5 |
| ensemble | 107.0 | 75.8 | 39.9 | 34.7 | 14.9 |
| shrinkage | 98.2 | 91.8 | 55.4 | 42.4 | 20.4 |
| quadratic | 401.8 | 105.1 | 74.7 | 41.8 | 16.7 |
| wls | 210.5 | 123.4 | 59.7 | 40.0 | 22.3 |
| linear | 216.6 | 124.0 | 67.7 | 46.4 | 24.4 |
| theilsen | 216.8 | 135.5 | 79.6 | 47.1 | 26.9 |
| ewma | 214.0 | 152.6 | 80.0 | 39.1 | 12.3 |
| recent | 213.3 | 161.8 | 87.3 | 43.4 | 17.0 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

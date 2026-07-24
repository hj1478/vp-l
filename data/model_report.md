# Model Performance Report

Leave-one-cycle-out backtest over **13 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.270 | 31.4 | 40.7 | 24.8 | 71.4 | -2.3 | 107% | 841 |
| diurnal | 0.245 | 34.1 | 43.3 | 29.5 | 77.7 | +0.2 | 107% | 841 |
| **ensemble** | — | 53.4 | 69.5 | 39.3 | 118.3 | +0.2 | 107% | 841 |
| shrinkage | 0.114 | 59.9 | 76.5 | 45.1 | 140.6 | -14.8 | 107% | 841 |
| wls | 0.076 | 98.2 | 141.9 | 56.2 | 237.5 | +6.1 | 107% | 841 |
| quadratic | 0.056 | 99.0 | 186.4 | 38.6 | 335.4 | -8.8 | 61% | 477 |
| linear | 0.068 | 105.4 | 145.4 | 69.5 | 228.9 | -6.6 | 107% | 841 |
| ewma | 0.059 | 109.9 | 164.2 | 69.0 | 268.7 | +18.5 | 107% | 841 |
| theilsen | 0.061 | 112.2 | 151.5 | 81.3 | 227.8 | -2.7 | 107% | 841 |
| recent | 0.052 | 117.8 | 179.8 | 68.9 | 286.3 | +25.8 | 107% | 841 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 35.6 | 40.9 | 30.7 | 25.4 | 11.8 |
| diurnal | 41.3 | 43.0 | 32.2 | 27.2 | 14.3 |
| ensemble | 89.1 | 68.2 | 39.5 | 31.2 | 14.5 |
| shrinkage | 76.2 | 81.2 | 53.8 | 39.6 | 20.4 |
| wls | 203.3 | 121.5 | 58.0 | 36.6 | 22.3 |
| quadratic | 434.6 | 141.3 | 65.2 | 38.4 | 16.7 |
| linear | 207.4 | 123.9 | 71.1 | 50.9 | 24.4 |
| ewma | 201.2 | 150.2 | 79.4 | 34.6 | 12.3 |
| theilsen | 207.6 | 133.5 | 84.5 | 52.9 | 26.9 |
| recent | 207.3 | 159.3 | 91.6 | 36.8 | 17.0 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

# Model Performance Report

Leave-one-cycle-out backtest over **9 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.284 | 30.2 | 39.3 | 23.7 | 65.6 | -3.5 | 104% | 531 |
| diurnal | 0.258 | 33.3 | 42.1 | 26.8 | 75.1 | -3.3 | 104% | 531 |
| **ensemble** | — | 54.0 | 73.9 | 34.0 | 133.9 | -9.5 | 104% | 531 |
| shrinkage | 0.089 | 72.9 | 90.6 | 53.8 | 163.3 | -34.8 | 104% | 531 |
| quadratic | 0.058 | 77.9 | 156.6 | 22.3 | 269.7 | -13.1 | 52% | 268 |
| wls | 0.065 | 94.7 | 138.3 | 52.6 | 233.7 | -9.1 | 104% | 531 |
| ewma | 0.063 | 98.8 | 150.0 | 59.4 | 249.8 | -0.8 | 104% | 531 |
| linear | 0.064 | 99.9 | 143.1 | 59.2 | 249.3 | -32.3 | 104% | 531 |
| theilsen | 0.062 | 108.3 | 150.3 | 70.7 | 256.4 | -28.0 | 104% | 531 |
| recent | 0.059 | 109.1 | 173.3 | 62.3 | 281.4 | +10.3 | 104% | 531 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 42.7 | 41.5 | 26.7 | 20.7 | 14.2 |
| diurnal | 50.2 | 43.0 | 29.9 | 25.9 | 14.8 |
| ensemble | 124.7 | 72.3 | 35.0 | 20.8 | 15.3 |
| shrinkage | 131.5 | 107.3 | 57.4 | 32.6 | 20.5 |
| quadratic | 415.6 | 97.1 | 82.9 | 31.7 | 16.7 |
| wls | 249.9 | 116.8 | 62.1 | 19.3 | 22.3 |
| ewma | 239.4 | 127.5 | 78.6 | 22.0 | 12.3 |
| linear | 257.9 | 128.3 | 59.5 | 31.2 | 24.4 |
| theilsen | 260.4 | 140.4 | 74.1 | 33.5 | 26.9 |
| recent | 240.0 | 148.4 | 90.2 | 26.7 | 17.0 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

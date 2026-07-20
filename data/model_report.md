# Model Performance Report

Leave-one-cycle-out backtest over **6 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal | 0.558 | 35.2 | 43.9 | 31.3 | 70.6 | -15.1 | 102% | 325 |
| **ensemble** | — | 60.3 | 79.0 | 37.6 | 143.8 | -26.5 | 102% | 325 |
| shrinkage | 0.109 | 94.0 | 109.6 | 87.8 | 172.1 | -68.0 | 102% | 325 |
| quadratic | 0.036 | 100.3 | 190.8 | 23.8 | 400.9 | -54.6 | 46% | 147 |
| wls | 0.068 | 114.6 | 159.6 | 66.0 | 277.4 | -32.2 | 102% | 325 |
| ewma | 0.044 | 114.9 | 169.9 | 73.9 | 272.6 | -21.2 | 102% | 325 |
| linear | 0.090 | 122.3 | 168.2 | 69.5 | 282.7 | -67.9 | 102% | 325 |
| recent | 0.029 | 127.4 | 196.3 | 73.7 | 303.8 | -7.7 | 102% | 325 |
| theilsen | 0.067 | 128.9 | 174.1 | 89.7 | 282.0 | -68.6 | 102% | 325 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal | 55.8 | 43.4 | 28.7 | 20.4 | 20.7 |
| ensemble | 146.4 | 76.6 | 32.9 | 21.6 | 16.5 |
| shrinkage | 161.1 | 140.6 | 65.7 | 35.6 | 29.5 |
| quadratic | 415.6 | 75.6 | 75.2 | 37.1 | 17.1 |
| wls | 315.1 | 124.2 | 72.4 | 18.6 | 31.5 |
| ewma | 300.8 | 127.1 | 83.4 | 23.7 | 20.0 |
| linear | 322.1 | 162.8 | 58.2 | 33.2 | 16.3 |
| recent | 296.9 | 146.8 | 103.5 | 29.5 | 28.1 |
| theilsen | 320.4 | 174.3 | 69.0 | 35.9 | 17.9 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

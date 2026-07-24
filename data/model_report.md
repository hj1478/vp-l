# Model Performance Report

Leave-one-cycle-out backtest over **14 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.261 | 30.4 | 39.2 | 24.8 | 67.1 | +1.0 | 108% | 950 |
| diurnal | 0.229 | 32.7 | 41.6 | 27.4 | 75.2 | +3.6 | 108% | 950 |
| **ensemble** | — | 54.1 | 69.6 | 40.3 | 115.8 | +8.5 | 108% | 950 |
| shrinkage | 0.112 | 59.8 | 75.3 | 47.5 | 130.4 | -5.6 | 108% | 950 |
| wls | 0.079 | 107.4 | 157.0 | 59.0 | 260.6 | +23.1 | 108% | 950 |
| quadratic | 0.064 | 107.9 | 214.5 | 38.8 | 363.4 | -1.0 | 63% | 554 |
| ewma | 0.073 | 116.5 | 175.2 | 74.7 | 289.5 | +31.8 | 108% | 950 |
| linear | 0.060 | 118.8 | 161.9 | 81.8 | 261.7 | +17.0 | 108% | 950 |
| theilsen | 0.056 | 126.5 | 169.1 | 93.7 | 267.9 | +21.9 | 108% | 950 |
| recent | 0.067 | 126.6 | 194.3 | 70.9 | 316.0 | +41.2 | 108% | 950 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 33.5 | 39.1 | 31.5 | 24.2 | 10.7 |
| diurnal | 38.3 | 39.8 | 33.5 | 26.2 | 12.8 |
| ensemble | 90.5 | 64.7 | 42.0 | 30.9 | 14.3 |
| shrinkage | 70.9 | 82.1 | 57.0 | 41.2 | 18.7 |
| wls | 233.0 | 117.6 | 63.1 | 35.6 | 19.9 |
| quadratic | 509.0 | 127.9 | 62.3 | 37.1 | 15.9 |
| ewma | 221.6 | 147.5 | 84.5 | 32.5 | 11.1 |
| linear | 228.8 | 134.3 | 78.2 | 58.3 | 31.0 |
| theilsen | 225.4 | 149.5 | 91.1 | 61.8 | 36.7 |
| recent | 242.1 | 151.8 | 97.2 | 34.8 | 15.0 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

# Model Performance Report

Leave-one-cycle-out backtest over **20 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.325 | 31.4 | 40.2 | 24.9 | 67.9 | +8.1 | 117% | 1553 |
| diurnal | 0.317 | 31.6 | 40.8 | 24.9 | 72.1 | +8.6 | 117% | 1553 |
| **ensemble** | — | 46.8 | 62.4 | 33.7 | 104.9 | +11.1 | 117% | 1553 |
| shrinkage | 0.112 | 57.8 | 73.3 | 44.6 | 122.5 | -0.3 | 117% | 1553 |
| quadratic | 0.037 | 85.6 | 178.6 | 28.2 | 272.6 | -2.2 | 77% | 1025 |
| wls | 0.045 | 96.6 | 149.2 | 54.3 | 243.6 | +18.3 | 117% | 1553 |
| ewma | 0.040 | 107.9 | 175.8 | 58.8 | 273.6 | +31.8 | 117% | 1553 |
| linear | 0.045 | 111.3 | 153.1 | 76.2 | 235.7 | +12.3 | 117% | 1553 |
| recent | 0.037 | 116.0 | 200.5 | 58.5 | 290.7 | +39.9 | 117% | 1553 |
| theilsen | 0.042 | 117.8 | 164.8 | 86.1 | 246.1 | +17.7 | 117% | 1553 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 36.0 | 43.3 | 34.2 | 24.8 | 11.9 |
| diurnal | 36.3 | 43.5 | 34.7 | 24.9 | 11.8 |
| ensemble | 77.9 | 61.7 | 41.6 | 26.9 | 13.3 |
| shrinkage | 70.1 | 84.6 | 62.9 | 39.2 | 16.4 |
| quadratic | 444.8 | 120.1 | 55.5 | 28.3 | 16.3 |
| wls | 222.7 | 122.1 | 61.0 | 28.8 | 14.4 |
| ewma | 232.8 | 146.5 | 75.2 | 28.9 | 14.1 |
| linear | 216.7 | 133.7 | 85.7 | 59.2 | 32.7 |
| recent | 245.2 | 150.5 | 84.1 | 30.3 | 26.0 |
| theilsen | 221.7 | 145.3 | 96.1 | 61.9 | 32.1 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

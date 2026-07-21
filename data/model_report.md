# Model Performance Report

Leave-one-cycle-out backtest over **7 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal | 0.410 | 35.0 | 43.8 | 29.6 | 71.5 | -9.7 | 102% | 376 |
| **ensemble** | — | 58.8 | 78.3 | 37.2 | 141.5 | -20.7 | 102% | 376 |
| quadratic | 0.038 | 86.1 | 169.9 | 24.4 | 323.8 | -43.2 | 51% | 188 |
| shrinkage | 0.107 | 90.2 | 107.1 | 85.2 | 177.4 | -56.6 | 102% | 376 |
| wls | 0.100 | 105.3 | 150.7 | 58.2 | 261.5 | -21.9 | 102% | 376 |
| ewma | 0.101 | 106.5 | 160.4 | 66.5 | 264.6 | -11.4 | 102% | 376 |
| linear | 0.101 | 112.2 | 158.3 | 60.7 | 275.8 | -52.7 | 102% | 376 |
| recent | 0.064 | 116.3 | 184.7 | 66.5 | 290.9 | -0.9 | 102% | 376 |
| theilsen | 0.079 | 121.1 | 166.0 | 78.1 | 275.2 | -50.0 | 102% | 376 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal | 58.4 | 42.4 | 30.0 | 23.6 | 18.5 |
| ensemble | 144.4 | 78.3 | 34.4 | 22.8 | 16.0 |
| quadratic | 415.6 | 75.6 | 65.4 | 37.5 | 16.3 |
| shrinkage | 157.2 | 142.9 | 66.2 | 36.6 | 25.4 |
| wls | 293.6 | 125.9 | 63.9 | 20.0 | 26.6 |
| ewma | 278.6 | 128.8 | 78.2 | 24.6 | 16.4 |
| linear | 298.1 | 163.0 | 52.7 | 33.2 | 17.6 |
| recent | 276.7 | 148.0 | 90.1 | 29.9 | 22.6 |
| theilsen | 304.3 | 174.9 | 67.1 | 35.9 | 19.8 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

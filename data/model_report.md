# Model Performance Report

Leave-one-cycle-out backtest over **4 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal | 0.236 | 59.9 | 74.3 | 56.3 | 126.2 | -51.7 | 102% | 117 |
| **ensemble** | — | 87.3 | 112.0 | 63.8 | 205.4 | -78.5 | 102% | 117 |
| wls | 0.085 | 108.7 | 143.5 | 62.3 | 276.9 | -78.1 | 102% | 117 |
| ewma | 0.075 | 115.0 | 167.3 | 71.1 | 269.6 | -63.1 | 102% | 117 |
| shrinkage | 0.075 | 116.6 | 127.6 | 107.7 | 195.9 | -113.4 | 102% | 117 |
| linear | 0.056 | 122.7 | 152.2 | 67.7 | 280.8 | -117.4 | 102% | 117 |
| theilsen | 0.051 | 132.2 | 158.6 | 83.2 | 276.7 | -127.2 | 102% | 117 |
| recent | 0.041 | 136.3 | 217.9 | 79.0 | 303.3 | -46.9 | 102% | 117 |
| quadratic | 0.381 | 171.3 | 266.9 | 48.5 | 532.5 | -108.4 | 51% | 59 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal | 130.9 | 62.8 | 36.1 | 15.7 | 1.0 |
| ensemble | 208.3 | 93.5 | 43.8 | 15.2 | 6.7 |
| wls | 266.7 | 112.6 | 54.0 | 18.6 | 19.6 |
| ewma | 259.9 | 143.9 | 46.8 | 16.6 | 6.2 |
| shrinkage | 183.8 | 140.2 | 85.4 | 47.0 | 7.7 |
| linear | 265.0 | 140.9 | 57.9 | 45.6 | 27.0 |
| theilsen | 260.7 | 165.3 | 63.1 | 48.4 | 31.3 |
| recent | 257.7 | 196.3 | 55.8 | 25.8 | 5.7 |
| quadratic | 435.0 | 164.7 | 85.7 | 3.6 | 2.9 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

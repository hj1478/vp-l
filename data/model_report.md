# Model Performance Report

Leave-one-cycle-out backtest over **19 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.261 | 31.5 | 40.4 | 25.1 | 68.6 | +6.5 | 115% | 1451 |
| diurnal | 0.247 | 32.3 | 41.6 | 25.4 | 72.8 | +7.9 | 115% | 1451 |
| **ensemble** | — | 47.9 | 63.4 | 35.2 | 108.1 | +9.3 | 115% | 1451 |
| shrinkage | 0.115 | 58.0 | 73.7 | 44.7 | 124.8 | -2.2 | 115% | 1451 |
| quadratic | 0.071 | 86.4 | 180.4 | 30.1 | 265.0 | -2.4 | 75% | 944 |
| wls | 0.091 | 98.1 | 146.0 | 55.6 | 247.3 | +14.6 | 115% | 1451 |
| ewma | 0.071 | 108.3 | 172.2 | 61.3 | 271.5 | +27.0 | 115% | 1451 |
| linear | 0.055 | 113.3 | 152.1 | 79.3 | 238.8 | +7.6 | 115% | 1451 |
| recent | 0.038 | 118.3 | 201.9 | 61.4 | 292.3 | +37.3 | 115% | 1451 |
| theilsen | 0.052 | 118.9 | 158.0 | 90.4 | 249.5 | +11.8 | 115% | 1451 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 36.3 | 42.2 | 34.6 | 24.8 | 11.9 |
| diurnal | 36.8 | 43.4 | 35.6 | 24.8 | 12.2 |
| ensemble | 80.1 | 61.2 | 42.3 | 27.1 | 13.6 |
| shrinkage | 69.5 | 83.0 | 63.2 | 39.1 | 16.6 |
| quadratic | 471.1 | 108.0 | 57.3 | 29.5 | 17.6 |
| wls | 223.2 | 120.3 | 62.7 | 29.5 | 15.0 |
| ewma | 226.7 | 144.2 | 77.9 | 29.2 | 15.5 |
| linear | 218.2 | 135.7 | 85.9 | 59.4 | 32.8 |
| recent | 248.1 | 146.9 | 87.3 | 30.3 | 29.0 |
| theilsen | 216.9 | 147.6 | 96.4 | 62.6 | 33.4 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

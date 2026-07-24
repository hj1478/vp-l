# Model Performance Report

Leave-one-cycle-out backtest over **15 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.320 | 30.1 | 39.2 | 23.0 | 67.4 | +3.4 | 110% | 1046 |
| diurnal | 0.288 | 32.5 | 41.7 | 26.4 | 75.1 | +5.5 | 110% | 1046 |
| **ensemble** | — | 51.0 | 66.8 | 37.6 | 114.0 | +7.9 | 110% | 1046 |
| shrinkage | 0.112 | 55.8 | 71.9 | 42.9 | 126.9 | -6.6 | 110% | 1046 |
| quadratic | 0.041 | 99.7 | 202.6 | 34.0 | 323.3 | -4.6 | 67% | 637 |
| wls | 0.050 | 101.5 | 150.6 | 57.8 | 244.7 | +17.5 | 110% | 1046 |
| ewma | 0.047 | 109.6 | 168.0 | 66.6 | 273.8 | +27.6 | 110% | 1046 |
| linear | 0.049 | 112.8 | 155.5 | 73.6 | 242.9 | +10.5 | 110% | 1046 |
| recent | 0.044 | 119.9 | 186.6 | 67.9 | 301.6 | +36.4 | 110% | 1046 |
| theilsen | 0.048 | 119.9 | 162.3 | 84.7 | 254.6 | +14.8 | 110% | 1046 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 31.6 | 39.7 | 31.7 | 25.1 | 10.8 |
| diurnal | 36.2 | 41.3 | 33.7 | 26.7 | 12.6 |
| ensemble | 84.9 | 61.8 | 40.4 | 29.6 | 13.4 |
| shrinkage | 66.0 | 77.3 | 54.9 | 37.5 | 16.5 |
| quadratic | 486.5 | 111.2 | 58.2 | 35.0 | 15.9 |
| wls | 221.6 | 112.9 | 61.0 | 32.9 | 18.1 |
| ewma | 210.3 | 140.2 | 80.4 | 31.0 | 10.7 |
| linear | 218.2 | 128.7 | 76.5 | 55.3 | 28.0 |
| recent | 230.5 | 145.9 | 93.0 | 34.3 | 14.5 |
| theilsen | 215.2 | 142.6 | 88.5 | 58.7 | 33.0 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

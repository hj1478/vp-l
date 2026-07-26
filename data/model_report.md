# Model Performance Report

Leave-one-cycle-out backtest over **18 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.345 | 29.9 | 38.5 | 24.3 | 65.0 | +6.5 | 114% | 1341 |
| diurnal | 0.296 | 32.3 | 41.6 | 25.5 | 72.4 | +7.6 | 114% | 1341 |
| **ensemble** | — | 49.6 | 64.3 | 37.4 | 106.5 | +10.7 | 114% | 1341 |
| shrinkage | 0.104 | 60.6 | 76.2 | 47.2 | 127.8 | -0.9 | 114% | 1341 |
| quadratic | 0.038 | 87.3 | 181.7 | 31.0 | 236.3 | -4.2 | 73% | 864 |
| wls | 0.046 | 101.6 | 149.6 | 57.9 | 250.3 | +19.9 | 114% | 1341 |
| ewma | 0.041 | 112.8 | 177.3 | 66.6 | 276.3 | +32.3 | 114% | 1341 |
| linear | 0.045 | 116.7 | 155.5 | 82.9 | 244.6 | +14.1 | 114% | 1341 |
| theilsen | 0.044 | 122.8 | 161.8 | 94.0 | 253.4 | +18.7 | 114% | 1341 |
| recent | 0.038 | 123.5 | 208.4 | 66.1 | 300.7 | +42.9 | 114% | 1341 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 32.9 | 38.2 | 33.5 | 24.2 | 12.9 |
| diurnal | 37.0 | 41.7 | 35.6 | 25.5 | 12.8 |
| ensemble | 81.7 | 62.1 | 42.9 | 29.3 | 14.6 |
| shrinkage | 71.4 | 85.8 | 64.3 | 42.0 | 18.3 |
| quadratic | 465.3 | 100.1 | 55.6 | 32.0 | 18.5 |
| wls | 224.3 | 124.0 | 63.7 | 32.9 | 16.0 |
| ewma | 229.1 | 150.0 | 80.3 | 29.8 | 16.8 |
| linear | 218.4 | 139.1 | 87.1 | 62.4 | 35.6 |
| theilsen | 217.1 | 151.8 | 98.3 | 65.7 | 36.3 |
| recent | 252.6 | 151.8 | 89.4 | 31.8 | 31.7 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

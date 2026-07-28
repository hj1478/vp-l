# Model Performance Report

Leave-one-cycle-out backtest over **22 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.267 | 30.7 | 39.4 | 24.5 | 66.6 | +8.1 | 118% | 1707 |
| diurnal | 0.257 | 30.9 | 40.1 | 24.5 | 69.9 | +8.1 | 118% | 1707 |
| **ensemble** | — | 45.9 | 60.7 | 33.9 | 101.2 | +9.8 | 118% | 1707 |
| shrinkage | 0.108 | 59.3 | 74.1 | 48.7 | 120.3 | -1.0 | 118% | 1707 |
| quadratic | 0.073 | 84.2 | 174.7 | 27.7 | 255.5 | -5.0 | 78% | 1129 |
| wls | 0.090 | 97.6 | 148.4 | 55.0 | 241.9 | +14.9 | 118% | 1707 |
| ewma | 0.071 | 107.9 | 174.2 | 59.0 | 273.3 | +27.0 | 118% | 1707 |
| linear | 0.050 | 112.8 | 152.3 | 81.7 | 229.8 | +9.2 | 118% | 1707 |
| recent | 0.035 | 116.5 | 198.5 | 59.8 | 291.4 | +36.1 | 118% | 1707 |
| theilsen | 0.048 | 118.5 | 162.9 | 91.0 | 235.6 | +13.1 | 118% | 1707 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 35.2 | 42.6 | 33.2 | 24.3 | 11.4 |
| diurnal | 34.7 | 43.3 | 33.8 | 24.8 | 11.3 |
| ensemble | 73.4 | 61.5 | 41.2 | 27.2 | 12.9 |
| shrinkage | 70.0 | 86.9 | 65.5 | 41.0 | 16.5 |
| quadratic | 433.1 | 129.2 | 53.7 | 26.5 | 15.6 |
| wls | 215.3 | 128.1 | 61.9 | 29.3 | 13.8 |
| ewma | 228.3 | 149.9 | 73.2 | 28.0 | 13.6 |
| linear | 208.7 | 137.3 | 89.5 | 62.3 | 33.4 |
| recent | 240.4 | 155.3 | 82.9 | 29.7 | 25.1 |
| theilsen | 212.9 | 147.1 | 99.5 | 64.0 | 32.7 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

# Model Performance Report

Leave-one-cycle-out backtest over **17 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.346 | 28.7 | 36.8 | 23.8 | 62.0 | +5.4 | 113% | 1272 |
| diurnal | 0.296 | 31.0 | 39.7 | 25.1 | 69.9 | +5.6 | 113% | 1272 |
| **ensemble** | — | 48.2 | 63.1 | 35.8 | 104.2 | +8.3 | 113% | 1272 |
| shrinkage | 0.104 | 57.8 | 73.0 | 45.0 | 121.9 | -5.4 | 113% | 1272 |
| quadratic | 0.039 | 86.3 | 180.9 | 31.7 | 223.5 | -2.0 | 73% | 822 |
| wls | 0.046 | 100.1 | 148.8 | 57.1 | 244.8 | +16.3 | 113% | 1272 |
| ewma | 0.042 | 111.2 | 176.8 | 65.6 | 271.3 | +28.3 | 113% | 1272 |
| linear | 0.045 | 115.8 | 155.8 | 79.7 | 249.3 | +9.9 | 113% | 1272 |
| recent | 0.039 | 121.7 | 208.6 | 64.0 | 293.5 | +38.8 | 113% | 1272 |
| theilsen | 0.044 | 122.0 | 162.2 | 92.2 | 258.9 | +13.8 | 113% | 1272 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 31.1 | 36.8 | 32.1 | 23.4 | 13.5 |
| diurnal | 36.1 | 39.9 | 33.8 | 24.9 | 12.9 |
| ensemble | 82.8 | 59.5 | 40.7 | 28.5 | 14.8 |
| shrinkage | 68.0 | 82.7 | 60.9 | 40.7 | 18.3 |
| quadratic | 465.8 | 100.1 | 56.7 | 32.9 | 18.5 |
| wls | 228.3 | 118.1 | 64.1 | 32.8 | 16.0 |
| ewma | 234.2 | 143.3 | 79.7 | 30.2 | 16.8 |
| linear | 224.5 | 137.6 | 84.2 | 60.7 | 35.6 |
| recent | 254.4 | 144.7 | 91.4 | 32.4 | 31.7 |
| theilsen | 223.3 | 150.3 | 95.7 | 64.4 | 36.3 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

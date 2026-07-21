# Model Performance Report

Leave-one-cycle-out backtest over **8 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.403 | 31.1 | 40.8 | 24.0 | 67.6 | -4.8 | 103% | 479 |
| diurnal | 0.379 | 33.9 | 42.6 | 27.1 | 72.1 | -5.2 | 103% | 479 |
| **ensemble** | — | 42.9 | 55.3 | 31.8 | 98.3 | -7.8 | 103% | 479 |
| shrinkage | 0.074 | 75.2 | 92.1 | 58.4 | 159.4 | -38.6 | 103% | 479 |
| quadratic | 0.017 | 86.2 | 166.3 | 24.9 | 313.1 | -18.7 | 50% | 232 |
| wls | 0.030 | 100.9 | 143.6 | 59.0 | 240.1 | -9.5 | 103% | 479 |
| ewma | 0.026 | 104.8 | 155.8 | 66.4 | 259.1 | -0.1 | 103% | 479 |
| linear | 0.027 | 106.2 | 148.5 | 66.5 | 261.7 | -35.1 | 103% | 479 |
| recent | 0.020 | 115.8 | 180.4 | 68.8 | 290.6 | +11.9 | 103% | 479 |
| theilsen | 0.025 | 115.8 | 156.4 | 79.7 | 261.8 | -30.7 | 103% | 479 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 40.9 | 45.1 | 26.6 | 19.0 | 15.6 |
| diurnal | 49.0 | 45.1 | 29.7 | 25.2 | 15.8 |
| ensemble | 80.2 | 59.4 | 30.6 | 21.3 | 16.2 |
| shrinkage | 132.1 | 109.5 | 58.2 | 35.6 | 22.1 |
| quadratic | 415.6 | 75.6 | 95.2 | 37.6 | 17.6 |
| wls | 254.7 | 125.6 | 65.7 | 20.3 | 23.9 |
| ewma | 244.5 | 137.2 | 79.8 | 26.1 | 13.5 |
| linear | 261.8 | 138.6 | 62.6 | 35.2 | 25.7 |
| recent | 244.2 | 159.1 | 93.0 | 30.9 | 18.5 |
| theilsen | 266.3 | 152.0 | 78.1 | 38.1 | 28.4 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

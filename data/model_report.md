# Model Performance Report

Leave-one-cycle-out backtest over **21 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.266 | 30.8 | 39.6 | 24.2 | 67.5 | +6.7 | 117% | 1615 |
| diurnal | 0.255 | 31.2 | 40.3 | 24.6 | 70.7 | +7.0 | 117% | 1615 |
| **ensemble** | — | 46.5 | 61.5 | 34.0 | 102.9 | +8.3 | 117% | 1615 |
| shrinkage | 0.111 | 58.9 | 74.0 | 46.9 | 121.2 | -3.9 | 117% | 1615 |
| quadratic | 0.072 | 85.8 | 176.2 | 29.4 | 262.4 | -5.0 | 78% | 1076 |
| wls | 0.090 | 97.6 | 149.2 | 55.2 | 241.9 | +12.8 | 117% | 1615 |
| ewma | 0.070 | 108.5 | 175.5 | 59.4 | 273.5 | +26.1 | 117% | 1615 |
| linear | 0.052 | 112.7 | 153.5 | 79.9 | 233.9 | +6.1 | 117% | 1615 |
| recent | 0.036 | 116.1 | 199.0 | 59.8 | 288.8 | +34.6 | 117% | 1615 |
| theilsen | 0.049 | 119.3 | 165.0 | 90.7 | 242.8 | +11.1 | 117% | 1615 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 35.5 | 42.5 | 33.2 | 24.0 | 11.8 |
| diurnal | 35.7 | 42.7 | 33.9 | 24.8 | 11.8 |
| ensemble | 76.5 | 61.3 | 41.1 | 26.9 | 13.2 |
| shrinkage | 70.3 | 85.4 | 64.8 | 40.3 | 16.4 |
| quadratic | 436.2 | 124.9 | 55.1 | 28.3 | 16.3 |
| wls | 222.1 | 123.6 | 62.6 | 29.4 | 14.4 |
| ewma | 234.8 | 147.2 | 74.0 | 28.8 | 14.1 |
| linear | 216.4 | 134.9 | 88.1 | 60.8 | 32.7 |
| recent | 244.6 | 150.6 | 83.5 | 30.4 | 26.0 |
| theilsen | 222.0 | 146.2 | 98.3 | 63.2 | 32.1 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

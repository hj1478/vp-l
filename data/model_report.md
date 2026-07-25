# Model Performance Report

Leave-one-cycle-out backtest over **16 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.286 | 29.7 | 38.3 | 24.3 | 65.7 | +5.8 | 111% | 1154 |
| diurnal | 0.260 | 31.7 | 40.5 | 25.5 | 72.7 | +7.4 | 111% | 1154 |
| **ensemble** | — | 50.0 | 65.8 | 36.7 | 109.1 | +12.0 | 111% | 1154 |
| shrinkage | 0.114 | 56.3 | 71.9 | 43.4 | 118.2 | -1.0 | 111% | 1154 |
| quadratic | 0.056 | 91.2 | 190.6 | 28.7 | 276.3 | -5.3 | 70% | 725 |
| wls | 0.069 | 101.9 | 151.6 | 57.6 | 246.8 | +25.6 | 111% | 1154 |
| ewma | 0.054 | 113.0 | 181.2 | 65.4 | 279.5 | +37.8 | 111% | 1154 |
| linear | 0.059 | 115.7 | 157.6 | 76.8 | 253.3 | +22.8 | 111% | 1154 |
| theilsen | 0.054 | 122.5 | 164.3 | 89.5 | 261.0 | +27.2 | 111% | 1154 |
| recent | 0.046 | 122.8 | 206.4 | 64.3 | 302.7 | +46.1 | 111% | 1154 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 32.6 | 38.5 | 31.7 | 24.4 | 12.0 |
| diurnal | 35.9 | 39.9 | 33.5 | 26.5 | 13.5 |
| ensemble | 85.0 | 60.2 | 39.7 | 29.3 | 14.6 |
| shrinkage | 66.7 | 79.4 | 56.4 | 38.1 | 17.8 |
| quadratic | 464.8 | 102.8 | 55.0 | 33.3 | 14.8 |
| wls | 226.7 | 114.2 | 61.2 | 32.6 | 17.3 |
| ewma | 233.0 | 140.6 | 78.6 | 30.4 | 11.2 |
| linear | 222.6 | 134.3 | 79.6 | 56.9 | 32.1 |
| theilsen | 221.3 | 147.2 | 91.4 | 60.6 | 35.4 |
| recent | 254.0 | 143.7 | 91.7 | 33.4 | 14.8 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

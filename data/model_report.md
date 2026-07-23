# Model Performance Report

Leave-one-cycle-out backtest over **12 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.237 | 32.4 | 41.9 | 25.3 | 74.6 | -1.3 | 107% | 761 |
| diurnal | 0.210 | 35.5 | 44.7 | 30.4 | 80.6 | +0.8 | 107% | 761 |
| **ensemble** | — | 56.5 | 72.9 | 42.3 | 123.6 | +3.0 | 107% | 761 |
| shrinkage | 0.115 | 63.3 | 79.2 | 49.7 | 143.4 | -13.0 | 107% | 761 |
| quadratic | 0.068 | 93.9 | 178.0 | 31.0 | 325.2 | +11.9 | 57% | 405 |
| wls | 0.083 | 101.3 | 141.3 | 62.0 | 242.0 | +10.6 | 107% | 761 |
| linear | 0.074 | 109.0 | 144.6 | 79.5 | 230.2 | -3.5 | 107% | 761 |
| ewma | 0.074 | 113.8 | 165.9 | 75.5 | 281.9 | +23.7 | 107% | 761 |
| theilsen | 0.071 | 115.8 | 150.7 | 91.8 | 230.0 | +1.2 | 107% | 761 |
| recent | 0.069 | 120.9 | 181.1 | 71.8 | 294.4 | +30.7 | 107% | 761 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 38.0 | 43.0 | 30.3 | 27.4 | 11.8 |
| diurnal | 44.8 | 45.9 | 31.6 | 29.8 | 14.3 |
| ensemble | 96.4 | 75.0 | 40.5 | 33.1 | 14.5 |
| shrinkage | 79.5 | 89.9 | 56.6 | 41.8 | 20.3 |
| quadratic | 426.3 | 191.0 | 66.9 | 37.8 | 16.7 |
| wls | 211.7 | 130.8 | 58.5 | 37.8 | 22.3 |
| linear | 215.8 | 133.1 | 73.7 | 51.9 | 24.4 |
| ewma | 208.2 | 161.7 | 82.2 | 36.2 | 12.3 |
| theilsen | 212.6 | 143.7 | 88.4 | 53.8 | 26.9 |
| recent | 213.1 | 171.1 | 91.7 | 39.2 | 17.0 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

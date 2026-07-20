# Model Performance Report

Leave-one-cycle-out backtest over **5 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal | 0.355 | 47.6 | 64.0 | 38.0 | 123.5 | -30.3 | 101% | 167 |
| **ensemble** | — | 71.0 | 94.5 | 52.3 | 161.7 | -20.7 | 101% | 167 |
| shrinkage | 0.092 | 104.3 | 119.1 | 101.2 | 194.5 | -63.2 | 101% | 167 |
| ewma | 0.123 | 120.8 | 189.7 | 66.4 | 316.7 | -4.4 | 101% | 167 |
| wls | 0.122 | 121.3 | 176.4 | 58.8 | 287.6 | -9.5 | 101% | 167 |
| quadratic | 0.146 | 127.3 | 221.2 | 30.2 | 467.7 | -91.3 | 62% | 103 |
| recent | 0.075 | 135.1 | 222.0 | 67.2 | 321.8 | +6.1 | 101% | 167 |
| linear | 0.047 | 137.0 | 183.4 | 68.6 | 287.0 | -31.2 | 101% | 167 |
| theilsen | 0.040 | 149.5 | 195.1 | 89.7 | 283.8 | -32.2 | 101% | 167 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal | 93.5 | 57.7 | 34.5 | 11.4 | 12.5 |
| ensemble | 171.6 | 82.8 | 40.1 | 9.2 | 6.8 |
| shrinkage | 161.1 | 141.3 | 84.9 | 38.5 | 14.3 |
| ewma | 326.9 | 143.6 | 42.7 | 12.4 | 11.6 |
| wls | 329.7 | 134.5 | 51.2 | 15.2 | 11.2 |
| quadratic | 415.6 | 75.6 | 75.2 | 11.6 | 6.8 |
| recent | 327.0 | 180.0 | 50.7 | 18.1 | 12.3 |
| linear | 328.6 | 160.2 | 61.1 | 42.4 | 24.1 |
| theilsen | 326.0 | 188.8 | 76.3 | 45.6 | 18.8 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

# Model Performance Report

Leave-one-cycle-out backtest over **10 completed cycles**. Error = |predicted firing time − actual firing time|, in minutes.

## Overall metrics (ranked by MAE)

| Model | Weight | MAE | RMSE | Median | P90 | Bias | Coverage | n |
|-------|-------:|----:|-----:|-------:|----:|-----:|---------:|--:|
| diurnal_dow | 0.258 | 33.8 | 44.0 | 25.9 | 76.4 | +1.7 | 104% | 611 |
| diurnal | 0.230 | 37.7 | 47.5 | 32.3 | 85.6 | +2.4 | 104% | 611 |
| **ensemble** | — | 58.3 | 77.4 | 39.5 | 138.8 | +0.6 | 104% | 611 |
| shrinkage | 0.106 | 69.3 | 85.3 | 58.4 | 154.3 | -19.5 | 104% | 611 |
| quadratic | 0.062 | 76.4 | 150.2 | 24.8 | 226.8 | -4.1 | 52% | 303 |
| wls | 0.079 | 96.8 | 138.6 | 55.8 | 241.8 | +3.8 | 104% | 611 |
| linear | 0.075 | 101.4 | 140.8 | 67.7 | 233.6 | -16.9 | 104% | 611 |
| theilsen | 0.068 | 108.9 | 147.5 | 81.3 | 246.4 | -11.7 | 104% | 611 |
| ewma | 0.064 | 110.7 | 163.5 | 70.4 | 281.9 | +21.1 | 104% | 611 |
| recent | 0.058 | 117.2 | 179.9 | 68.8 | 297.3 | +27.2 | 104% | 611 |

## Mean |ETA error| by cycle stage (minutes)

| Model | 0-25% | 25-50% | 50-75% | 75-90% | 90-100% |
|-------|----:|----:|----:|----:|----:|
| diurnal_dow | 46.3 | 45.9 | 29.0 | 29.1 | 12.6 |
| diurnal | 54.9 | 49.6 | 31.2 | 34.0 | 14.5 |
| ensemble | 111.7 | 81.5 | 39.1 | 33.2 | 14.8 |
| shrinkage | 104.3 | 99.8 | 58.5 | 42.1 | 20.3 |
| quadratic | 415.6 | 97.1 | 78.7 | 38.3 | 16.7 |
| wls | 215.6 | 130.1 | 59.7 | 37.1 | 22.3 |
| linear | 222.0 | 129.3 | 68.9 | 44.1 | 24.4 |
| theilsen | 222.1 | 141.2 | 82.2 | 44.8 | 26.9 |
| ewma | 220.3 | 162.2 | 80.5 | 39.0 | 12.3 |
| recent | 220.1 | 173.2 | 88.6 | 44.1 | 17.0 |

**Bias** > 0 means the model tends to predict the party *later* than it actually fires; < 0 means *earlier*. **Coverage** is the share of stages where the model produced a prediction (some need ≥3 points or history). See `model_report.png`.

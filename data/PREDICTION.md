# Vote Party Prediction

_Generated 2026-07-20T15:58:17Z — recomputed every data update._

**Progress:** 310 / 5000.0 (6.2%) — 4690 remaining
**Players online:** 594  |  **Cycle started:** 2026-07-20T15:20:20Z  |  **Data points this cycle:** 9

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-21T05:48:17Z`**
Empirical error at this stage: **±30 min** (n=32 tightly-labeled predictions, spread ±19m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-21T04:58:11Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-21T05:48:17Z | 0.657 | 0.72923 |
| shrinkage | 2026-07-21T04:11:09Z | 0.101 | 1.7846 |
| wls | 2026-07-21T02:27:16Z | 0.049 | 2.51128 |
| ewma | 2026-07-21T02:49:29Z | 0.044 | 2.67264 |
| linear | 2026-07-21T02:15:32Z | 0.044 | 2.63868 |
| theilsen | 2026-07-21T02:34:45Z | 0.040 | 2.76609 |
| recent | 2026-07-21T03:55:51Z | 0.034 | 3.07848 |
| quadratic | n/a | 0.030 | 2.83173 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

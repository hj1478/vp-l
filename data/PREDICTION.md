# Vote Party Prediction

_Generated 2026-07-21T02:45:45Z — recomputed every data update._

**Progress:** 3803 / 5000.0 (76.1%) — 1197 remaining
**Players online:** 478  |  **Cycle started:** 2026-07-20T15:20:20Z  |  **Data points this cycle:** 81

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-21T05:55:45Z`**
Empirical error at this stage: **±14 min** (n=43 tightly-labeled predictions, spread ±11m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-21T06:14:11Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-21T05:55:45Z | 0.410 | 0.72923 |
| shrinkage | 2026-07-21T06:10:04Z | 0.107 | 1.7846 |
| linear | 2026-07-21T06:51:30Z | 0.101 | 2.63868 |
| ewma | 2026-07-21T06:25:34Z | 0.101 | 2.67264 |
| wls | 2026-07-21T06:04:00Z | 0.100 | 2.51128 |
| theilsen | 2026-07-21T06:56:15Z | 0.079 | 2.76609 |
| recent | 2026-07-21T06:25:29Z | 0.064 | 3.07848 |
| quadratic | 2026-07-21T06:15:40Z | 0.038 | 2.83173 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

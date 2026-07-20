# Vote Party Prediction

_Generated 2026-07-20T23:44:05Z — recomputed every data update._

**Progress:** 2643 / 5000.0 (52.9%) — 2357 remaining
**Players online:** 467  |  **Cycle started:** 2026-07-20T15:20:20Z  |  **Data points this cycle:** 57

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-21T06:19:05Z`**
Empirical error at this stage: **±33 min** (n=26 tightly-labeled predictions, spread ±14m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-21T06:49:04Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-21T06:19:05Z | 0.526 | 0.72923 |
| shrinkage | 2026-07-21T06:30:41Z | 0.106 | 1.7846 |
| linear | 2026-07-21T07:27:13Z | 0.099 | 2.63868 |
| wls | 2026-07-21T08:00:10Z | 0.076 | 2.51128 |
| theilsen | 2026-07-21T07:56:48Z | 0.066 | 2.76609 |
| ewma | 2026-07-21T07:56:45Z | 0.048 | 2.67264 |
| quadratic | n/a | 0.048 | 2.83173 |
| recent | 2026-07-21T07:16:44Z | 0.032 | 3.07848 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

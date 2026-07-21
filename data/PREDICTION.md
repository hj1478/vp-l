# Vote Party Prediction

_Generated 2026-07-21T00:44:07Z — recomputed every data update._

**Progress:** 3125 / 5000.0 (62.5%) — 1875 remaining
**Players online:** 451  |  **Cycle started:** 2026-07-20T15:20:20Z  |  **Data points this cycle:** 69

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-21T05:09:07Z`**
Empirical error at this stage: **±33 min** (n=26 tightly-labeled predictions, spread ±14m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-21T05:45:32Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-21T05:09:07Z | 0.526 | 0.72923 |
| shrinkage | 2026-07-21T06:06:46Z | 0.106 | 1.7846 |
| linear | 2026-07-21T07:18:10Z | 0.099 | 2.63868 |
| wls | 2026-07-21T05:31:47Z | 0.076 | 2.51128 |
| theilsen | 2026-07-21T07:29:42Z | 0.066 | 2.76609 |
| ewma | 2026-07-21T04:39:03Z | 0.048 | 2.67264 |
| quadratic | 2026-07-21T08:27:55Z | 0.048 | 2.83173 |
| recent | 2026-07-21T04:21:59Z | 0.032 | 3.07848 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

# Vote Party Prediction

_Generated 2026-07-21T09:29:19Z — recomputed every data update._

**Progress:** 1632 / 5000.0 (32.6%) — 3368 remaining
**Players online:** 411  |  **Cycle started:** 2026-07-21T05:37:06Z  |  **Data points this cycle:** 20

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-21T17:49:19Z`**
Empirical error at this stage: **±34 min** (n=81 tightly-labeled predictions, spread ±20m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-21T18:02:53Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-21T17:49:19Z | 0.635 | 0.70926 |
| shrinkage | 2026-07-21T18:19:52Z | 0.125 | 1.53546 |
| wls | 2026-07-21T17:46:19Z | 0.050 | 2.39366 |
| linear | 2026-07-21T17:42:25Z | 0.046 | 2.47523 |
| ewma | 2026-07-21T18:20:39Z | 0.043 | 2.59645 |
| theilsen | 2026-07-21T17:46:09Z | 0.042 | 2.60587 |
| recent | 2026-07-21T18:57:28Z | 0.033 | 3.00585 |
| quadratic | 2026-07-21T21:54:59Z | 0.028 | 2.77109 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

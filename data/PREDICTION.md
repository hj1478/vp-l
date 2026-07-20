# Vote Party Prediction

_Generated 2026-07-20T07:02:23Z — recomputed every data update._

**Progress:** 1310 / 5000.0 (26.2%) — 3690 remaining
**Players online:** 393  |  **Cycle started:** 2026-07-20T06:07:23Z  |  **Data points this cycle:** 12

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-20T15:52:23Z`**
Empirical error at this stage: **±29 min** (n=22 tightly-labeled predictions, spread ±22m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-20T16:33:35Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T15:52:23Z | 0.675 | 0.73149 |
| shrinkage | 2026-07-20T17:15:02Z | 0.101 | 1.82635 |
| wls | 2026-07-20T18:29:25Z | 0.046 | 2.66042 |
| ewma | 2026-07-20T18:43:19Z | 0.042 | 2.8319 |
| linear | 2026-07-20T18:17:30Z | 0.041 | 2.80416 |
| theilsen | 2026-07-20T18:40:18Z | 0.038 | 2.90236 |
| recent | 2026-07-20T18:35:04Z | 0.032 | 3.27184 |
| quadratic | n/a | 0.026 | 3.18017 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

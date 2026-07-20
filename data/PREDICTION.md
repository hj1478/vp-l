# Vote Party Prediction

_Generated 2026-07-20T13:04:42Z — recomputed every data update._

**Progress:** 3843 / 5000.0 (76.9%) — 1157 remaining
**Players online:** 502  |  **Cycle started:** 2026-07-20T06:07:23Z  |  **Data points this cycle:** 36

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-20T16:04:42Z`**
Empirical error at this stage: **±9 min** (n=23 tightly-labeled predictions, spread ±6m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-20T15:58:51Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T16:04:42Z | 0.429 | 0.73149 |
| shrinkage | 2026-07-20T16:03:35Z | 0.106 | 1.82635 |
| linear | 2026-07-20T15:53:35Z | 0.102 | 2.80416 |
| wls | 2026-07-20T15:56:38Z | 0.095 | 2.66042 |
| ewma | 2026-07-20T15:43:22Z | 0.095 | 2.8319 |
| theilsen | 2026-07-20T15:55:49Z | 0.080 | 2.90236 |
| recent | 2026-07-20T15:47:54Z | 0.059 | 3.27184 |
| quadratic | 2026-07-20T16:01:46Z | 0.033 | 3.18017 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

# Vote Party Prediction

_Generated 2026-07-20T10:45:42Z — recomputed every data update._

**Progress:** 2907 / 5000.0 (58.1%) — 2093 remaining
**Players online:** 464  |  **Cycle started:** 2026-07-20T06:07:23Z  |  **Data points this cycle:** 24

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-20T15:45:42Z`**
Empirical error at this stage: **±17 min** (n=5 tightly-labeled predictions, spread ±5m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-20T15:47:01Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T15:45:42Z | 0.558 | 0.73149 |
| shrinkage | 2026-07-20T16:09:41Z | 0.109 | 1.82635 |
| linear | 2026-07-20T15:48:17Z | 0.090 | 2.80416 |
| wls | 2026-07-20T15:44:50Z | 0.068 | 2.66042 |
| theilsen | 2026-07-20T15:50:33Z | 0.067 | 2.90236 |
| ewma | 2026-07-20T15:52:20Z | 0.044 | 2.8319 |
| quadratic | 2026-07-20T14:49:23Z | 0.036 | 3.18017 |
| recent | 2026-07-20T15:44:30Z | 0.029 | 3.27184 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

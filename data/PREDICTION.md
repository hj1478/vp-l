# Vote Party Prediction

_Generated 2026-07-20T00:44:34Z — recomputed every data update._

**Progress:** 3888 / 5000.0 (77.8%) — 1112 remaining
**Players online:** 514  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 116

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-20T03:54:34Z`**
Empirical error at this stage: **±10 min** (n=23 tightly-labeled predictions, spread ±6m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-20T03:47:24Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T03:54:34Z | 0.355 | 1.06707 |
| quadratic | n/a | 0.146 | 3.68622 |
| ewma | 2026-07-20T03:16:54Z | 0.123 | 3.16131 |
| wls | 2026-07-20T03:45:50Z | 0.122 | 2.93923 |
| shrinkage | 2026-07-20T03:53:52Z | 0.092 | 1.98583 |
| recent | 2026-07-20T03:16:22Z | 0.075 | 3.69949 |
| linear | 2026-07-20T04:23:06Z | 0.047 | 3.05697 |
| theilsen | 2026-07-20T04:24:47Z | 0.040 | 3.25194 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

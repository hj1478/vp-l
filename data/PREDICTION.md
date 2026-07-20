# Vote Party Prediction

_Generated 2026-07-20T03:03:28Z — recomputed every data update._

**Progress:** 4710 / 5000.0 (94.2%) — 290 remaining
**Players online:** 485  |  **Cycle started:** 2026-07-19T13:17:01Z  |  **Data points this cycle:** 160

## 🎯 Prediction (primary model: `diurnal`)

**Vote party fires ≈ `2026-07-20T03:53:28Z`**
Empirical error at this stage: **±10 min** (n=23 tightly-labeled predictions, spread ±6m). This is a raw error estimate from a tiny sample, **not a calibrated interval** — real uncertainty is likely wider.

_Diagnostic — ensemble ETA (does **not** beat `diurnal` out-of-sample): `2026-07-20T03:58:49Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal | 2026-07-20T03:53:28Z | 0.355 | 1.06707 |
| quadratic | 2026-07-20T04:11:13Z | 0.146 | 3.68622 |
| ewma | 2026-07-20T04:05:16Z | 0.123 | 3.16131 |
| wls | 2026-07-20T03:58:26Z | 0.122 | 2.93923 |
| shrinkage | 2026-07-20T03:52:46Z | 0.092 | 1.98583 |
| recent | 2026-07-20T03:54:13Z | 0.075 | 3.69949 |
| linear | 2026-07-20T04:03:48Z | 0.047 | 3.05697 |
| theilsen | 2026-07-20T03:59:04Z | 0.040 | 3.25194 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

# Vote Party Prediction

_Generated 2026-07-21T12:19:18Z — recomputed every data update._

**Progress:** 2873 / 5000.0 (57.5%) — 2127 remaining
**Players online:** 494  |  **Cycle started:** 2026-07-21T05:37:06Z  |  **Data points this cycle:** 32

## 🎯 Prediction

**Vote party fires ≈ `2026-07-21T16:56:15Z`**  (model: `analogue`)
**80% window:** `2026-07-21T14:48:00Z` → `2026-07-21T19:04:10Z`  (90%: `2026-07-21T14:48:00Z` → `2026-07-21T19:19:02Z`)
_Interval from the analogue curve-library (measured ~75% coverage OOS) over 8 cycles (3 tightly labeled). Wide early by design; tightens as the cycle fills._

_Diagnostic — ensemble ETA (does **not** beat `analogue` out-of-sample): `2026-07-21T17:00:45Z`._

## Individual models

| Model | Predicted ETA | Weight | Backtest RMSE |
|-------|---------------|--------|---------------|
| diurnal_dow | 2026-07-21T16:44:18Z | 0.378 | 0.68005 |
| diurnal | 2026-07-21T16:59:18Z | 0.328 | 0.70926 |
| shrinkage | 2026-07-21T17:48:05Z | 0.087 | 1.53546 |
| linear | 2026-07-21T17:32:14Z | 0.053 | 2.47523 |
| wls | 2026-07-21T17:23:35Z | 0.046 | 2.39366 |
| theilsen | 2026-07-21T17:33:07Z | 0.037 | 2.60587 |
| ewma | 2026-07-21T16:45:06Z | 0.030 | 2.59645 |
| quadratic | 2026-07-21T17:12:43Z | 0.021 | 2.77109 |
| recent | 2026-07-21T16:03:22Z | 0.020 | 3.00585 |

**Caveats:** weights are unstable at this sample size (dropping one cycle can swing the top weight by ±0.4), so the ensemble is a diagnostic only — the reported prediction is the single best model (`diurnal`), which beats the ensemble out-of-sample. Firing-time labels for loosely-sampled cycles are uncertain by tens of minutes and are excluded from the error estimate. See `prediction_track.png` for the honest out-of-sample record.

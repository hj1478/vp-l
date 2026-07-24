# Vote Party Prediction

_Generated 2026-07-24T01:24:21Z — recomputed every data update._

**Progress:** 2034 / 5000.0 (40.7%) — 2966 remaining
**Players online:** 465  |  **Cycle started:** 2026-07-23T19:26:42Z  |  **Data points this cycle:** 58

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 08:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 07:30Z` → `2026-07-24 09:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 13 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T09:31:48Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T09:04:21Z | 0.305 |
| diurnal | 2026-07-24T08:44:21Z | 0.275 |
| shrinkage | 2026-07-24T10:05:13Z | 0.108 |
| wls | 2026-07-24T09:17:21Z | 0.056 |
| linear | 2026-07-24T12:26:26Z | 0.055 |
| theilsen | 2026-07-24T14:34:33Z | 0.054 |
| ewma | 2026-07-24T09:50:46Z | 0.052 |
| recent | 2026-07-24T09:10:04Z | 0.049 |
| quadratic | 2026-07-24T06:50:25Z | 0.046 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-23T23:28:57Z — recomputed every data update._

**Progress:** 1222 / 5000.0 (24.4%) — 3778 remaining
**Players online:** 467  |  **Cycle started:** 2026-07-23T19:26:42Z  |  **Data points this cycle:** 46

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 09:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 07:30Z` → `2026-07-24 10:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 13 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T11:18:33Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T09:13:57Z | 0.305 |
| diurnal | 2026-07-24T09:38:57Z | 0.275 |
| shrinkage | 2026-07-24T10:13:35Z | 0.108 |
| wls | 2026-07-24T16:14:38Z | 0.056 |
| linear | 2026-07-24T15:27:47Z | 0.055 |
| theilsen | 2026-07-24T15:28:06Z | 0.054 |
| ewma | 2026-07-24T15:36:43Z | 0.052 |
| recent | 2026-07-24T16:23:51Z | 0.049 |
| quadratic | n/a | 0.046 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

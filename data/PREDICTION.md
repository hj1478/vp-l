# Vote Party Prediction

_Generated 2026-07-23T17:41:33Z — recomputed every data update._

**Progress:** 4484 / 5000.0 (89.7%) — 516 remaining
**Players online:** 627  |  **Cycle started:** 2026-07-23T07:36:43Z  |  **Data points this cycle:** 82

## 🎯 Prediction

**Vote party fires ≈ `2026-07-23 18:45Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-23 18:30Z` → `2026-07-23 19:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 12 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-23T19:01:58Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-23T19:11:33Z | 0.237 |
| diurnal | 2026-07-23T19:11:33Z | 0.210 |
| shrinkage | 2026-07-23T18:58:16Z | 0.115 |
| wls | 2026-07-23T19:01:51Z | 0.083 |
| ewma | 2026-07-23T19:05:16Z | 0.074 |
| linear | 2026-07-23T18:41:42Z | 0.074 |
| theilsen | 2026-07-23T18:37:45Z | 0.071 |
| recent | 2026-07-23T19:00:06Z | 0.069 |
| quadratic | 2026-07-23T18:51:01Z | 0.068 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-24T17:52:37Z — recomputed every data update._

**Progress:** 3896 / 5000.0 (77.9%) — 1104 remaining
**Players online:** 606  |  **Cycle started:** 2026-07-24T08:28:39Z  |  **Data points this cycle:** 68

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 21:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 20:00Z` → `2026-07-24 21:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 14 cycles (8 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T20:51:30Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T21:07:37Z | 0.261 |
| diurnal | 2026-07-24T21:02:37Z | 0.229 |
| shrinkage | 2026-07-24T20:41:50Z | 0.112 |
| wls | 2026-07-24T20:51:57Z | 0.079 |
| ewma | 2026-07-24T20:23:57Z | 0.073 |
| recent | 2026-07-24T20:16:16Z | 0.067 |
| quadratic | 2026-07-24T21:15:30Z | 0.064 |
| linear | 2026-07-24T20:27:06Z | 0.060 |
| theilsen | 2026-07-24T20:26:20Z | 0.056 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

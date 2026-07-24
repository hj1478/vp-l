# Vote Party Prediction

_Generated 2026-07-24T19:49:34Z — recomputed every data update._

**Progress:** 4528 / 5000.0 (90.6%) — 472 remaining
**Players online:** 644  |  **Cycle started:** 2026-07-24T08:28:39Z  |  **Data points this cycle:** 84

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 21:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 20:45Z` → `2026-07-24 21:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 14 cycles (8 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T21:37:23Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T21:54:34Z | 0.261 |
| diurnal | 2026-07-24T21:59:34Z | 0.229 |
| shrinkage | 2026-07-24T21:03:13Z | 0.112 |
| wls | 2026-07-24T21:10:21Z | 0.079 |
| ewma | 2026-07-24T21:35:00Z | 0.073 |
| recent | 2026-07-24T22:25:51Z | 0.067 |
| quadratic | 2026-07-24T21:23:05Z | 0.064 |
| linear | 2026-07-24T20:48:21Z | 0.060 |
| theilsen | 2026-07-24T20:46:40Z | 0.056 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-24T15:55:05Z — recomputed every data update._

**Progress:** 3149 / 5000.0 (63.0%) — 1851 remaining
**Players online:** 599  |  **Cycle started:** 2026-07-24T08:28:39Z  |  **Data points this cycle:** 56

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 21:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 20:00Z` → `2026-07-24 22:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 14 cycles (8 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T21:42:50Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T22:35:05Z | 0.283 |
| diurnal | 2026-07-24T22:25:05Z | 0.255 |
| shrinkage | 2026-07-24T20:36:30Z | 0.113 |
| wls | 2026-07-24T20:25:39Z | 0.070 |
| linear | 2026-07-24T20:08:25Z | 0.062 |
| theilsen | 2026-07-24T20:11:05Z | 0.056 |
| ewma | 2026-07-24T21:51:16Z | 0.056 |
| quadratic | 2026-07-24T20:43:18Z | 0.055 |
| recent | 2026-07-24T22:08:01Z | 0.049 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

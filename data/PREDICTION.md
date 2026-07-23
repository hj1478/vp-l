# Vote Party Prediction

_Generated 2026-07-23T12:53:43Z — recomputed every data update._

**Progress:** 2522 / 5000.0 (50.4%) — 2478 remaining
**Players online:** 512  |  **Cycle started:** 2026-07-23T07:36:43Z  |  **Data points this cycle:** 47

## 🎯 Prediction

**Vote party fires ≈ `2026-07-23 18:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-23 18:00Z` → `2026-07-23 21:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 12 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-23T18:37:06Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-23T18:33:43Z | 0.266 |
| diurnal | 2026-07-23T18:43:43Z | 0.244 |
| shrinkage | 2026-07-23T19:10:11Z | 0.111 |
| wls | 2026-07-23T18:39:31Z | 0.077 |
| linear | 2026-07-23T18:41:48Z | 0.069 |
| theilsen | 2026-07-23T18:40:32Z | 0.062 |
| ewma | 2026-07-23T17:45:11Z | 0.060 |
| quadratic | 2026-07-23T19:01:29Z | 0.057 |
| recent | 2026-07-23T17:33:39Z | 0.054 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-25T15:33:38Z — recomputed every data update._

**Progress:** 2596 / 5000.0 (51.9%) — 2404 remaining
**Players online:** 559  |  **Cycle started:** 2026-07-25T10:40:38Z  |  **Data points this cycle:** 36

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 22:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 21:00Z` → `2026-07-25 23:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 16 cycles (10 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T22:27:46Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T23:03:38Z | 0.286 |
| diurnal | 2026-07-25T23:23:38Z | 0.260 |
| shrinkage | 2026-07-25T21:32:37Z | 0.114 |
| wls | 2026-07-25T21:04:34Z | 0.069 |
| linear | 2026-07-25T20:52:44Z | 0.059 |
| quadratic | 2026-07-25T22:10:54Z | 0.056 |
| theilsen | 2026-07-25T20:53:42Z | 0.054 |
| ewma | 2026-07-25T21:52:30Z | 0.054 |
| recent | 2026-07-25T22:45:25Z | 0.046 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-26T13:43:20Z — recomputed every data update._

**Progress:** 1439 / 5000.0 (28.8%) — 3561 remaining
**Players online:** 588  |  **Cycle started:** 2026-07-26T10:47:48Z  |  **Data points this cycle:** 24

## 🎯 Prediction

**Vote party fires ≈ `2026-07-27 00:00Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-26 23:30Z` → `2026-07-27 01:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 18 cycles (12 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-27T00:01:27Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T01:03:20Z | 0.345 |
| diurnal | 2026-07-27T00:43:20Z | 0.296 |
| shrinkage | 2026-07-26T22:45:03Z | 0.104 |
| wls | 2026-07-26T21:46:00Z | 0.046 |
| linear | 2026-07-26T21:35:24Z | 0.045 |
| theilsen | 2026-07-26T21:39:02Z | 0.044 |
| ewma | 2026-07-26T22:39:05Z | 0.041 |
| quadratic | n/a | 0.038 |
| recent | 2026-07-26T22:38:54Z | 0.038 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-23T10:58:33Z — recomputed every data update._

**Progress:** 1679 / 5000.0 (33.6%) — 3321 remaining
**Players online:** 458  |  **Cycle started:** 2026-07-23T07:36:43Z  |  **Data points this cycle:** 35

## 🎯 Prediction

**Vote party fires ≈ `2026-07-23 19:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-23 14:00Z` → `2026-07-23 22:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 12 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-23T19:22:12Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-23T19:38:33Z | 0.298 |
| diurnal | 2026-07-23T19:43:33Z | 0.266 |
| shrinkage | 2026-07-23T19:27:46Z | 0.107 |
| wls | 2026-07-23T18:31:44Z | 0.059 |
| linear | 2026-07-23T18:32:34Z | 0.058 |
| theilsen | 2026-07-23T18:34:16Z | 0.057 |
| ewma | 2026-07-23T18:51:59Z | 0.054 |
| recent | 2026-07-23T20:30:22Z | 0.052 |
| quadratic | 2026-07-23T17:51:21Z | 0.049 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

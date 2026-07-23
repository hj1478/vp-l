# Vote Party Prediction

_Generated 2026-07-23T09:02:53Z — recomputed every data update._

**Progress:** 820 / 5000.0 (16.4%) — 4180 remaining
**Players online:** 443  |  **Cycle started:** 2026-07-23T07:36:43Z  |  **Data points this cycle:** 23

## 🎯 Prediction

**Vote party fires ≈ `2026-07-23 19:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-23 12:00Z` → `2026-07-23 22:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 12 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-23T19:11:07Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-23T19:17:53Z | 0.298 |
| diurnal | 2026-07-23T19:22:53Z | 0.266 |
| shrinkage | 2026-07-23T19:56:13Z | 0.107 |
| wls | 2026-07-23T18:48:28Z | 0.059 |
| linear | 2026-07-23T18:49:11Z | 0.058 |
| theilsen | 2026-07-23T18:41:17Z | 0.057 |
| ewma | 2026-07-23T19:22:25Z | 0.054 |
| recent | 2026-07-23T18:12:09Z | 0.052 |
| quadratic | 2026-07-23T18:05:22Z | 0.049 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

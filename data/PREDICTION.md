# Vote Party Prediction

_Generated 2026-07-29T23:07:15Z — recomputed every data update._

**Progress:** 3959 / 5000.0 (79.2%) — 1041 remaining
**Players online:** 504  |  **Cycle started:** 2026-07-29T11:43:48Z  |  **Data points this cycle:** 150

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 01:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 01:30Z` → `2026-07-30 02:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 24 cycles (17 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T02:55:26Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T02:27:15Z | 0.272 |
| diurnal | 2026-07-30T02:47:15Z | 0.250 |
| shrinkage | 2026-07-30T01:56:53Z | 0.116 |
| wls | 2026-07-30T03:29:28Z | 0.091 |
| quadratic | 2026-07-30T05:28:13Z | 0.076 |
| ewma | 2026-07-30T04:39:18Z | 0.055 |
| linear | 2026-07-30T01:20:14Z | 0.054 |
| theilsen | 2026-07-30T01:25:43Z | 0.051 |
| recent | 2026-07-30T05:40:46Z | 0.035 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-29T10:14:22Z — recomputed every data update._

**Progress:** 4139 / 5000.0 (82.8%) — 861 remaining
**Players online:** 447  |  **Cycle started:** 2026-07-29T00:12:31Z  |  **Data points this cycle:** 117

## 🎯 Prediction

**Vote party fires ≈ `2026-07-29 11:55Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-29 11:50Z` → `2026-07-29 12:20Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 23 cycles (16 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-29T12:06:00Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-29T11:59:22Z | 0.270 |
| diurnal | 2026-07-29T11:59:22Z | 0.248 |
| shrinkage | 2026-07-29T12:25:11Z | 0.119 |
| wls | 2026-07-29T12:04:39Z | 0.091 |
| quadratic | 2026-07-29T11:57:16Z | 0.075 |
| ewma | 2026-07-29T11:59:07Z | 0.055 |
| linear | 2026-07-29T12:34:25Z | 0.054 |
| theilsen | 2026-07-29T12:33:17Z | 0.052 |
| recent | 2026-07-29T11:47:49Z | 0.035 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

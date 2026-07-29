# Vote Party Prediction

_Generated 2026-07-29T03:47:49Z — recomputed every data update._

**Progress:** 1287 / 5000.0 (25.7%) — 3713 remaining
**Players online:** 442  |  **Cycle started:** 2026-07-29T00:12:31Z  |  **Data points this cycle:** 33

## 🎯 Prediction

**Vote party fires ≈ `2026-07-29 11:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-29 11:15Z` → `2026-07-29 12:30Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 23 cycles (16 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-29T13:28:17Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-29T12:32:49Z | 0.334 |
| diurnal | 2026-07-29T12:42:49Z | 0.319 |
| shrinkage | 2026-07-29T13:42:16Z | 0.112 |
| wls | 2026-07-29T16:07:12Z | 0.043 |
| linear | 2026-07-29T14:01:01Z | 0.043 |
| theilsen | 2026-07-29T14:25:33Z | 0.041 |
| ewma | 2026-07-29T17:26:02Z | 0.038 |
| recent | 2026-07-29T19:05:39Z | 0.035 |
| quadratic | n/a | 0.035 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

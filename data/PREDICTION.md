# Vote Party Prediction

_Generated 2026-07-29T07:28:46Z — recomputed every data update._

**Progress:** 2910 / 5000.0 (58.2%) — 2090 remaining
**Players online:** 398  |  **Cycle started:** 2026-07-29T00:12:31Z  |  **Data points this cycle:** 81

## 🎯 Prediction

**Vote party fires ≈ `2026-07-29 11:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-29 11:15Z` → `2026-07-29 12:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 23 cycles (16 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-29T12:22:58Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-29T12:18:46Z | 0.292 |
| diurnal | 2026-07-29T12:13:46Z | 0.277 |
| shrinkage | 2026-07-29T12:52:59Z | 0.106 |
| wls | 2026-07-29T12:34:34Z | 0.070 |
| quadratic | 2026-07-29T11:10:33Z | 0.057 |
| linear | 2026-07-29T12:57:05Z | 0.053 |
| ewma | 2026-07-29T12:39:45Z | 0.053 |
| theilsen | 2026-07-29T12:49:33Z | 0.048 |
| recent | 2026-07-29T12:21:43Z | 0.043 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

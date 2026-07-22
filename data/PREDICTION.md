# Vote Party Prediction

_Generated 2026-07-22T19:39:14Z — recomputed every data update._

**Progress:** 520 / 5000.0 (10.4%) — 4480 remaining
**Players online:** 580  |  **Cycle started:** 2026-07-22T18:12:39Z  |  **Data points this cycle:** 23

## 🎯 Prediction

**Vote party fires ≈ `2026-07-23 07:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-23 06:00Z` → `2026-07-23 10:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 11 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-23T09:13:36Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-23T08:04:14Z | 0.282 |
| diurnal | 2026-07-23T08:19:14Z | 0.257 |
| shrinkage | 2026-07-23T07:42:40Z | 0.103 |
| wls | 2026-07-23T11:13:54Z | 0.064 |
| linear | 2026-07-23T10:50:17Z | 0.063 |
| theilsen | 2026-07-23T10:40:35Z | 0.062 |
| ewma | 2026-07-23T12:22:17Z | 0.058 |
| recent | 2026-07-23T13:03:52Z | 0.056 |
| quadratic | n/a | 0.055 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

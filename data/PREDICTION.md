# Vote Party Prediction

_Generated 2026-07-28T05:25:29Z — recomputed every data update._

**Progress:** 2111 / 5000.0 (42.2%) — 2889 remaining
**Players online:** 435  |  **Cycle started:** 2026-07-28T00:05:45Z  |  **Data points this cycle:** 47

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 11:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-28 10:45Z` → `2026-07-28 12:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 21 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-28T11:44:33Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-28T11:10:29Z | 0.330 |
| diurnal | 2026-07-28T10:45:29Z | 0.321 |
| shrinkage | 2026-07-28T13:15:21Z | 0.110 |
| wls | 2026-07-28T13:50:28Z | 0.044 |
| linear | 2026-07-28T14:39:57Z | 0.043 |
| theilsen | 2026-07-28T14:12:16Z | 0.041 |
| ewma | 2026-07-28T10:12:01Z | 0.039 |
| recent | 2026-07-28T08:43:05Z | 0.036 |
| quadratic | 2026-07-28T16:55:01Z | 0.036 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-23T04:14:55Z — recomputed every data update._

**Progress:** 3314 / 5000.0 (66.3%) — 1686 remaining
**Players online:** 464  |  **Cycle started:** 2026-07-22T18:12:39Z  |  **Data points this cycle:** 82

## 🎯 Prediction

**Vote party fires ≈ `2026-07-23 08:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-23 06:30Z` → `2026-07-23 09:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 11 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-23T09:09:04Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-23T08:34:55Z | 0.250 |
| diurnal | 2026-07-23T08:49:55Z | 0.239 |
| shrinkage | 2026-07-23T08:58:49Z | 0.109 |
| wls | 2026-07-23T09:37:56Z | 0.079 |
| linear | 2026-07-23T09:25:16Z | 0.075 |
| theilsen | 2026-07-23T09:30:02Z | 0.068 |
| ewma | 2026-07-23T10:42:16Z | 0.063 |
| quadratic | 2026-07-23T07:58:44Z | 0.061 |
| recent | 2026-07-23T11:24:26Z | 0.057 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

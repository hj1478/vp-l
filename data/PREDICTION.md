# Vote Party Prediction

_Generated 2026-07-24T05:15:22Z — recomputed every data update._

**Progress:** 3362 / 5000.0 (67.2%) — 1638 remaining
**Players online:** 407  |  **Cycle started:** 2026-07-23T19:26:42Z  |  **Data points this cycle:** 82

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 09:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 08:00Z` → `2026-07-24 10:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 13 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T08:57:58Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T08:15:22Z | 0.270 |
| diurnal | 2026-07-24T08:10:22Z | 0.245 |
| shrinkage | 2026-07-24T09:56:05Z | 0.114 |
| wls | 2026-07-24T10:26:11Z | 0.076 |
| linear | 2026-07-24T11:01:31Z | 0.068 |
| theilsen | 2026-07-24T11:06:32Z | 0.061 |
| ewma | 2026-07-24T08:04:04Z | 0.059 |
| quadratic | 2026-07-24T09:15:54Z | 0.056 |
| recent | 2026-07-24T07:36:58Z | 0.052 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

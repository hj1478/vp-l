# Vote Party Prediction

_Generated 2026-07-24T07:11:17Z — recomputed every data update._

**Progress:** 4259 / 5000.0 (85.2%) — 741 remaining
**Players online:** 431  |  **Cycle started:** 2026-07-23T19:26:42Z  |  **Data points this cycle:** 94

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 08:45Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 08:15Z` → `2026-07-24 09:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 13 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T09:10:04Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T08:56:17Z | 0.242 |
| diurnal | 2026-07-24T09:01:17Z | 0.216 |
| shrinkage | 2026-07-24T09:16:23Z | 0.115 |
| wls | 2026-07-24T08:48:28Z | 0.081 |
| ewma | 2026-07-24T08:56:34Z | 0.073 |
| linear | 2026-07-24T10:10:48Z | 0.071 |
| theilsen | 2026-07-24T10:25:31Z | 0.068 |
| recent | 2026-07-24T08:57:40Z | 0.068 |
| quadratic | 2026-07-24T08:48:45Z | 0.065 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

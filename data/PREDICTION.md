# Vote Party Prediction

_Generated 2026-07-24T13:57:31Z — recomputed every data update._

**Progress:** 2362 / 5000.0 (47.2%) — 2638 remaining
**Players online:** 568  |  **Cycle started:** 2026-07-24T08:28:39Z  |  **Data points this cycle:** 44

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 20:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 19:30Z` → `2026-07-24 23:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 14 cycles (8 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T21:15:43Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T21:37:31Z | 0.320 |
| diurnal | 2026-07-24T21:47:31Z | 0.291 |
| shrinkage | 2026-07-24T20:39:16Z | 0.107 |
| wls | 2026-07-24T20:40:13Z | 0.050 |
| linear | 2026-07-24T20:01:28Z | 0.050 |
| theilsen | 2026-07-24T20:01:58Z | 0.049 |
| ewma | 2026-07-24T20:40:37Z | 0.047 |
| recent | 2026-07-24T20:39:06Z | 0.045 |
| quadratic | 2026-07-24T21:17:00Z | 0.042 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

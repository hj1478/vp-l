# Vote Party Prediction

_Generated 2026-07-27T06:10:37Z — recomputed every data update._

**Progress:** 2479 / 5000.0 (49.6%) — 2521 remaining
**Players online:** 388  |  **Cycle started:** 2026-07-26T23:31:47Z  |  **Data points this cycle:** 42

## 🎯 Prediction

**Vote party fires ≈ `2026-07-27 11:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-27 10:30Z` → `2026-07-27 12:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 19 cycles (13 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-27T12:37:33Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T12:30:37Z | 0.324 |
| diurnal | 2026-07-27T12:05:37Z | 0.308 |
| shrinkage | 2026-07-27T12:55:51Z | 0.113 |
| wls | 2026-07-27T12:56:24Z | 0.047 |
| linear | 2026-07-27T13:11:09Z | 0.046 |
| theilsen | 2026-07-27T13:11:02Z | 0.045 |
| ewma | 2026-07-27T12:36:03Z | 0.042 |
| recent | 2026-07-27T12:49:14Z | 0.038 |
| quadratic | 2026-07-27T15:08:16Z | 0.038 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

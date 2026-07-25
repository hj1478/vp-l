# Vote Party Prediction

_Generated 2026-07-25T13:34:36Z — recomputed every data update._

**Progress:** 1781 / 5000.0 (35.6%) — 3219 remaining
**Players online:** 584  |  **Cycle started:** 2026-07-25T10:40:38Z  |  **Data points this cycle:** 24

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 22:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 20:30Z` → `2026-07-26 00:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 16 cycles (10 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T22:15:04Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T23:19:36Z | 0.328 |
| diurnal | 2026-07-25T22:39:36Z | 0.298 |
| shrinkage | 2026-07-25T21:36:17Z | 0.110 |
| wls | 2026-07-25T20:47:07Z | 0.048 |
| linear | 2026-07-25T20:37:42Z | 0.047 |
| theilsen | 2026-07-25T20:34:49Z | 0.046 |
| ewma | 2026-07-25T19:53:29Z | 0.043 |
| recent | 2026-07-25T20:16:42Z | 0.041 |
| quadratic | n/a | 0.040 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

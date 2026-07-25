# Vote Party Prediction

_Generated 2026-07-25T11:35:38Z — recomputed every data update._

**Progress:** 889 / 5000.0 (17.8%) — 4111 remaining
**Players online:** 546  |  **Cycle started:** 2026-07-25T10:40:38Z  |  **Data points this cycle:** 12

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 22:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 21:00Z` → `2026-07-26 01:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 16 cycles (10 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T21:52:36Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T22:50:38Z | 0.328 |
| diurnal | 2026-07-25T22:35:38Z | 0.298 |
| shrinkage | 2026-07-25T21:49:37Z | 0.110 |
| wls | 2026-07-25T19:32:30Z | 0.048 |
| linear | 2026-07-25T19:24:33Z | 0.047 |
| theilsen | 2026-07-25T19:25:15Z | 0.046 |
| ewma | 2026-07-25T19:40:13Z | 0.043 |
| recent | 2026-07-25T19:37:30Z | 0.041 |
| quadratic | n/a | 0.040 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

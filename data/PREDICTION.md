# Vote Party Prediction

_Generated 2026-07-22T14:52:26Z — recomputed every data update._

**Progress:** 3671 / 5000.0 (73.4%) — 1329 remaining
**Players online:** 569  |  **Cycle started:** 2026-07-22T08:14:51Z  |  **Data points this cycle:** 48

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 18:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 17:30Z` → `2026-07-22 19:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 10 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T18:07:29Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T18:12:26Z | 0.258 |
| diurnal | 2026-07-22T18:27:26Z | 0.230 |
| shrinkage | 2026-07-22T18:08:55Z | 0.106 |
| wls | 2026-07-22T17:49:04Z | 0.079 |
| linear | 2026-07-22T17:49:37Z | 0.075 |
| theilsen | 2026-07-22T17:49:12Z | 0.068 |
| ewma | 2026-07-22T17:58:33Z | 0.064 |
| quadratic | 2026-07-22T17:45:47Z | 0.062 |
| recent | 2026-07-22T18:06:28Z | 0.058 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

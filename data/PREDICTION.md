# Vote Party Prediction

_Generated 2026-07-22T09:09:51Z — recomputed every data update._

**Progress:** 1135 / 5000.0 (22.7%) — 3865 remaining
**Players online:** 439  |  **Cycle started:** 2026-07-22T08:14:51Z  |  **Data points this cycle:** 12

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 18:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 12:00Z` → `2026-07-22 22:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 10 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T17:51:56Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T18:09:51Z | 0.280 |
| diurnal | 2026-07-22T18:19:51Z | 0.247 |
| shrinkage | 2026-07-22T18:46:42Z | 0.104 |
| wls | 2026-07-22T16:44:20Z | 0.066 |
| linear | 2026-07-22T16:33:54Z | 0.065 |
| theilsen | 2026-07-22T16:29:30Z | 0.064 |
| ewma | 2026-07-22T17:10:40Z | 0.060 |
| recent | 2026-07-22T17:45:52Z | 0.058 |
| quadratic | n/a | 0.057 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

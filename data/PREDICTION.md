# Vote Party Prediction

_Generated 2026-07-26T00:34:25Z — recomputed every data update._

**Progress:** 500 / 5000.0 (10.0%) — 4500 remaining
**Players online:** 494  |  **Cycle started:** 2026-07-25T23:40:26Z  |  **Data points this cycle:** 12

## 🎯 Prediction

**Vote party fires ≈ `2026-07-26 11:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-26 10:00Z` → `2026-07-26 13:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 17 cycles (11 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-26T11:02:50Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-26T11:34:25Z | 0.346 |
| diurnal | 2026-07-26T11:29:25Z | 0.296 |
| shrinkage | 2026-07-26T11:57:16Z | 0.104 |
| wls | 2026-07-26T08:03:07Z | 0.046 |
| linear | 2026-07-26T07:38:18Z | 0.045 |
| theilsen | 2026-07-26T08:20:23Z | 0.044 |
| ewma | 2026-07-26T09:49:47Z | 0.042 |
| quadratic | n/a | 0.039 |
| recent | 2026-07-26T12:28:39Z | 0.039 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

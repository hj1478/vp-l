# Vote Party Prediction

_Generated 2026-07-26T07:40:06Z — recomputed every data update._

**Progress:** 3342 / 5000.0 (66.8%) — 1658 remaining
**Players online:** 430  |  **Cycle started:** 2026-07-25T23:40:26Z  |  **Data points this cycle:** 59

## 🎯 Prediction

**Vote party fires ≈ `2026-07-26 11:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-26 10:00Z` → `2026-07-26 12:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 17 cycles (11 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-26T11:16:55Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-26T11:05:06Z | 0.296 |
| diurnal | 2026-07-26T11:10:06Z | 0.264 |
| shrinkage | 2026-07-26T11:57:08Z | 0.106 |
| wls | 2026-07-26T11:13:18Z | 0.068 |
| quadratic | 2026-07-26T10:46:54Z | 0.057 |
| linear | 2026-07-26T12:07:53Z | 0.057 |
| ewma | 2026-07-26T10:52:47Z | 0.053 |
| theilsen | 2026-07-26T12:01:43Z | 0.052 |
| recent | 2026-07-26T10:55:29Z | 0.046 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-26T09:40:44Z — recomputed every data update._

**Progress:** 4428 / 5000.0 (88.6%) — 572 remaining
**Players online:** 493  |  **Cycle started:** 2026-07-25T23:40:26Z  |  **Data points this cycle:** 71

## 🎯 Prediction

**Vote party fires ≈ `2026-07-26 10:45Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-26 10:30Z` → `2026-07-26 11:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 17 cycles (11 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-26T10:51:13Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-26T10:40:44Z | 0.272 |
| diurnal | 2026-07-26T10:45:44Z | 0.243 |
| shrinkage | 2026-07-26T11:06:43Z | 0.112 |
| wls | 2026-07-26T10:50:58Z | 0.087 |
| ewma | 2026-07-26T10:33:40Z | 0.070 |
| quadratic | 2026-07-26T10:46:23Z | 0.069 |
| linear | 2026-07-26T11:37:44Z | 0.055 |
| theilsen | 2026-07-26T11:35:16Z | 0.052 |
| recent | 2026-07-26T10:29:40Z | 0.039 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-22T16:47:00Z — recomputed every data update._

**Progress:** 4445 / 5000.0 (88.9%) — 555 remaining
**Players online:** 564  |  **Cycle started:** 2026-07-22T08:14:51Z  |  **Data points this cycle:** 60

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 18:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 17:45Z` → `2026-07-22 18:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 10 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T18:13:54Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T18:22:00Z | 0.222 |
| diurnal | 2026-07-22T18:27:00Z | 0.193 |
| shrinkage | 2026-07-22T18:08:39Z | 0.113 |
| wls | 2026-07-22T18:02:20Z | 0.086 |
| linear | 2026-07-22T17:53:00Z | 0.084 |
| theilsen | 2026-07-22T17:51:49Z | 0.081 |
| ewma | 2026-07-22T18:26:56Z | 0.076 |
| quadratic | 2026-07-22T17:56:45Z | 0.073 |
| recent | 2026-07-22T18:28:53Z | 0.071 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-26T21:55:08Z — recomputed every data update._

**Progress:** 4434 / 5000.0 (88.7%) — 566 remaining
**Players online:** 530  |  **Cycle started:** 2026-07-26T10:47:48Z  |  **Data points this cycle:** 82

## 🎯 Prediction

**Vote party fires ≈ `2026-07-26 23:40Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-26 23:30Z` → `2026-07-27 00:05Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 18 cycles (12 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-26T23:43:47Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T00:00:08Z | 0.274 |
| diurnal | 2026-07-26T23:50:08Z | 0.243 |
| shrinkage | 2026-07-26T23:24:12Z | 0.110 |
| wls | 2026-07-26T23:34:14Z | 0.088 |
| ewma | 2026-07-26T23:56:21Z | 0.071 |
| quadratic | 2026-07-26T23:43:46Z | 0.070 |
| linear | 2026-07-26T23:04:23Z | 0.054 |
| theilsen | 2026-07-26T23:02:38Z | 0.052 |
| recent | 2026-07-26T23:53:52Z | 0.038 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

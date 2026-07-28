# Vote Party Prediction

_Generated 2026-07-28T16:04:57Z — recomputed every data update._

**Progress:** 2085 / 5000.0 (41.7%) — 2915 remaining
**Players online:** 576  |  **Cycle started:** 2026-07-28T11:56:59Z  |  **Data points this cycle:** 35

## 🎯 Prediction

**Vote party fires ≈ `2026-07-29 00:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-29 00:15Z` → `2026-07-29 01:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 22 cycles (15 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-29T00:19:56Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-29T01:04:57Z | 0.333 |
| diurnal | 2026-07-29T01:09:57Z | 0.323 |
| shrinkage | 2026-07-28T23:20:03Z | 0.109 |
| wls | 2026-07-28T22:19:48Z | 0.043 |
| linear | 2026-07-28T22:43:10Z | 0.043 |
| theilsen | 2026-07-28T22:32:40Z | 0.041 |
| ewma | 2026-07-28T23:33:07Z | 0.038 |
| recent | 2026-07-28T23:45:52Z | 0.035 |
| quadratic | 2026-07-28T20:35:50Z | 0.035 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-26T16:48:06Z — recomputed every data update._

**Progress:** 2656 / 5000.0 (53.1%) — 2344 remaining
**Players online:** 508  |  **Cycle started:** 2026-07-26T10:47:48Z  |  **Data points this cycle:** 47

## 🎯 Prediction

**Vote party fires ≈ `2026-07-27 00:00Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-26 23:45Z` → `2026-07-27 00:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 18 cycles (12 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-26T23:39:34Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T00:13:06Z | 0.295 |
| diurnal | 2026-07-26T23:58:06Z | 0.260 |
| shrinkage | 2026-07-26T22:49:01Z | 0.104 |
| wls | 2026-07-26T22:49:04Z | 0.071 |
| quadratic | 2026-07-27T02:40:12Z | 0.059 |
| linear | 2026-07-26T22:24:13Z | 0.057 |
| ewma | 2026-07-26T22:18:21Z | 0.054 |
| theilsen | 2026-07-26T22:29:57Z | 0.052 |
| recent | 2026-07-26T22:07:53Z | 0.046 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

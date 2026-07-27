# Vote Party Prediction

_Generated 2026-07-27T09:17:39Z — recomputed every data update._

**Progress:** 4002 / 5000.0 (80.0%) — 998 remaining
**Players online:** 445  |  **Cycle started:** 2026-07-26T23:31:47Z  |  **Data points this cycle:** 65

## 🎯 Prediction

**Vote party fires ≈ `2026-07-27 11:20Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-27 11:10Z` → `2026-07-27 11:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 19 cycles (13 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-27T11:40:29Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T11:42:39Z | 0.261 |
| diurnal | 2026-07-27T11:37:39Z | 0.247 |
| shrinkage | 2026-07-27T11:50:21Z | 0.115 |
| wls | 2026-07-27T11:25:18Z | 0.091 |
| quadratic | 2026-07-27T11:10:10Z | 0.071 |
| ewma | 2026-07-27T11:42:22Z | 0.071 |
| linear | 2026-07-27T11:58:04Z | 0.055 |
| theilsen | 2026-07-27T11:51:37Z | 0.052 |
| recent | 2026-07-27T12:03:52Z | 0.038 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

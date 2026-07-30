# Vote Party Prediction

_Generated 2026-07-30T09:14:33Z — recomputed every data update._

**Progress:** 3285 / 5000.0 (65.7%) — 1715 remaining
**Players online:** 404  |  **Cycle started:** 2026-07-30T01:00:58Z  |  **Data points this cycle:** 108

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 12:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 12:15Z` → `2026-07-30 13:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 25 cycles (18 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T13:06:40Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T12:59:33Z | 0.292 |
| diurnal | 2026-07-30T12:59:33Z | 0.267 |
| shrinkage | 2026-07-30T13:38:05Z | 0.115 |
| wls | 2026-07-30T13:03:29Z | 0.074 |
| linear | 2026-07-30T13:46:26Z | 0.057 |
| quadratic | 2026-07-30T12:01:15Z | 0.052 |
| theilsen | 2026-07-30T13:41:36Z | 0.051 |
| ewma | 2026-07-30T13:14:13Z | 0.050 |
| recent | 2026-07-30T12:55:24Z | 0.041 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

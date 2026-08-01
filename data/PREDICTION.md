# Vote Party Prediction

_Generated 2026-08-01T03:34:54Z — recomputed every data update._

**Progress:** 4617 / 5000.0 (92.3%) — 383 remaining
**Players online:** 489  |  **Cycle started:** 2026-07-31T14:15:45Z  |  **Data points this cycle:** 191

## 🎯 Prediction

**Vote party fires ≈ `2026-08-01 04:40Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-08-01 04:20Z` → `2026-08-01 04:50Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 28 cycles (21 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-08-01T04:47:18Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-08-01T04:49:54Z | 0.291 |
| diurnal | 2026-08-01T04:44:54Z | 0.251 |
| shrinkage | 2026-08-01T04:38:54Z | 0.134 |
| wls | 2026-08-01T04:44:00Z | 0.081 |
| linear | 2026-08-01T04:49:13Z | 0.060 |
| theilsen | 2026-08-01T04:44:56Z | 0.057 |
| ewma | 2026-08-01T04:58:55Z | 0.051 |
| quadratic | 2026-08-01T04:49:49Z | 0.042 |
| recent | 2026-08-01T05:04:34Z | 0.033 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

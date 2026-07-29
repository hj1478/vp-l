# Vote Party Prediction

_Generated 2026-07-29T00:48:19Z — recomputed every data update._

**Progress:** 286 / 5000.0 (5.7%) — 4714 remaining
**Players online:** 471  |  **Cycle started:** 2026-07-29T00:12:31Z  |  **Data points this cycle:** 9

## 🎯 Prediction

**Vote party fires ≈ `2026-07-29 11:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-29 11:00Z` → `2026-07-29 12:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 23 cycles (16 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-29T11:58:55Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-29T12:13:19Z | 0.334 |
| diurnal | 2026-07-29T11:58:19Z | 0.319 |
| shrinkage | 2026-07-29T12:59:22Z | 0.112 |
| wls | 2026-07-29T11:09:52Z | 0.043 |
| linear | 2026-07-29T10:50:59Z | 0.043 |
| theilsen | 2026-07-29T10:53:50Z | 0.041 |
| ewma | 2026-07-29T11:18:07Z | 0.038 |
| recent | 2026-07-29T10:56:50Z | 0.035 |
| quadratic | n/a | 0.035 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

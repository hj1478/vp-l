# Vote Party Prediction

_Generated 2026-07-28T23:31:37Z — recomputed every data update._

**Progress:** 4524 / 5000.0 (90.5%) — 476 remaining
**Players online:** 505  |  **Cycle started:** 2026-07-28T11:56:59Z  |  **Data points this cycle:** 89

## 🎯 Prediction

**Vote party fires ≈ `2026-07-29 00:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-29 00:35Z` → `2026-07-29 01:10Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 22 cycles (15 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-29T01:39:16Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-29T01:21:37Z | 0.267 |
| diurnal | 2026-07-29T01:41:37Z | 0.257 |
| shrinkage | 2026-07-29T00:47:33Z | 0.108 |
| wls | 2026-07-29T01:25:14Z | 0.090 |
| quadratic | 2026-07-29T01:22:32Z | 0.073 |
| ewma | 2026-07-29T04:25:28Z | 0.071 |
| linear | 2026-07-29T00:11:41Z | 0.050 |
| theilsen | 2026-07-29T00:05:31Z | 0.048 |
| recent | 2026-07-29T06:01:40Z | 0.035 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-29T19:26:25Z — recomputed every data update._

**Progress:** 2930 / 5000.0 (58.6%) — 2070 remaining
**Players online:** 575  |  **Cycle started:** 2026-07-29T11:43:48Z  |  **Data points this cycle:** 102

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 01:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 01:15Z` → `2026-07-30 02:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 24 cycles (17 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T01:19:43Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T01:21:25Z | 0.293 |
| diurnal | 2026-07-30T01:31:25Z | 0.278 |
| shrinkage | 2026-07-30T00:46:40Z | 0.103 |
| wls | 2026-07-30T02:11:17Z | 0.070 |
| quadratic | n/a | 0.059 |
| linear | 2026-07-30T00:18:53Z | 0.053 |
| ewma | 2026-07-30T02:04:28Z | 0.053 |
| theilsen | 2026-07-30T00:19:49Z | 0.048 |
| recent | 2026-07-30T01:15:36Z | 0.043 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

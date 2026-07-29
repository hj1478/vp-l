# Vote Party Prediction

_Generated 2026-07-29T22:12:06Z — recomputed every data update._

**Progress:** 3747 / 5000.0 (74.9%) — 1253 remaining
**Players online:** 495  |  **Cycle started:** 2026-07-29T11:43:48Z  |  **Data points this cycle:** 138

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 01:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 01:30Z` → `2026-07-30 02:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 24 cycles (17 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T02:52:32Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T02:37:06Z | 0.293 |
| diurnal | 2026-07-30T02:47:06Z | 0.278 |
| shrinkage | 2026-07-30T01:32:59Z | 0.103 |
| wls | 2026-07-30T02:41:30Z | 0.070 |
| quadratic | 2026-07-30T05:32:31Z | 0.059 |
| linear | 2026-07-30T01:03:55Z | 0.053 |
| ewma | 2026-07-30T04:51:24Z | 0.053 |
| theilsen | 2026-07-30T01:10:28Z | 0.048 |
| recent | 2026-07-30T06:45:16Z | 0.043 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

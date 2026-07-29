# Vote Party Prediction

_Generated 2026-07-29T20:21:34Z — recomputed every data update._

**Progress:** 3240 / 5000.0 (64.8%) — 1760 remaining
**Players online:** 540  |  **Cycle started:** 2026-07-29T11:43:48Z  |  **Data points this cycle:** 114

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 01:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 01:15Z` → `2026-07-30 02:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 24 cycles (17 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T01:56:33Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T02:06:34Z | 0.293 |
| diurnal | 2026-07-30T02:16:34Z | 0.278 |
| shrinkage | 2026-07-30T00:56:59Z | 0.103 |
| wls | 2026-07-30T01:31:32Z | 0.070 |
| quadratic | n/a | 0.059 |
| linear | 2026-07-30T00:34:03Z | 0.053 |
| ewma | 2026-07-30T03:08:43Z | 0.053 |
| theilsen | 2026-07-30T00:41:39Z | 0.048 |
| recent | 2026-07-30T03:20:03Z | 0.043 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

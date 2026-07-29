# Vote Party Prediction

_Generated 2026-07-29T12:59:53Z — recomputed every data update._

**Progress:** 479 / 5000.0 (9.6%) — 4521 remaining
**Players online:** 502  |  **Cycle started:** 2026-07-29T11:43:48Z  |  **Data points this cycle:** 18

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 01:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 01:00Z` → `2026-07-30 02:30Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 24 cycles (17 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T00:55:19Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T00:59:53Z | 0.338 |
| diurnal | 2026-07-30T01:14:53Z | 0.322 |
| shrinkage | 2026-07-30T00:58:58Z | 0.109 |
| linear | 2026-07-30T04:09:48Z | 0.043 |
| wls | 2026-07-30T02:03:21Z | 0.043 |
| theilsen | 2026-07-30T04:12:35Z | 0.040 |
| ewma | 2026-07-29T23:31:34Z | 0.037 |
| quadratic | 2026-07-29T18:00:40Z | 0.035 |
| recent | 2026-07-29T20:07:43Z | 0.034 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

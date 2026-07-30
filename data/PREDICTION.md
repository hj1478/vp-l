# Vote Party Prediction

_Generated 2026-07-30T12:00:05Z — recomputed every data update._

**Progress:** 4583 / 5000.0 (91.7%) — 417 remaining
**Players online:** 526  |  **Cycle started:** 2026-07-30T01:00:58Z  |  **Data points this cycle:** 148

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 12:50Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 12:45Z` → `2026-07-30 13:05Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 25 cycles (18 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T13:02:51Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T13:05:05Z | 0.289 |
| diurnal | 2026-07-30T13:05:05Z | 0.249 |
| shrinkage | 2026-07-30T13:01:43Z | 0.132 |
| wls | 2026-07-30T12:49:33Z | 0.081 |
| linear | 2026-07-30T13:18:45Z | 0.060 |
| theilsen | 2026-07-30T13:12:16Z | 0.057 |
| ewma | 2026-07-30T12:52:09Z | 0.052 |
| quadratic | 2026-07-30T12:45:22Z | 0.047 |
| recent | 2026-07-30T13:00:35Z | 0.034 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

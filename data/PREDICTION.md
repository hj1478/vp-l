# Vote Party Prediction

_Generated 2026-07-30T06:28:59Z — recomputed every data update._

**Progress:** 2086 / 5000.0 (41.7%) — 2914 remaining
**Players online:** 380  |  **Cycle started:** 2026-07-30T01:00:58Z  |  **Data points this cycle:** 72

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 12:45Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 11:45Z` → `2026-07-30 13:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 25 cycles (18 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T13:10:21Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T12:48:59Z | 0.344 |
| diurnal | 2026-07-30T12:53:59Z | 0.317 |
| shrinkage | 2026-07-30T14:22:07Z | 0.115 |
| linear | 2026-07-30T15:13:22Z | 0.043 |
| wls | 2026-07-30T12:07:56Z | 0.042 |
| theilsen | 2026-07-30T15:45:46Z | 0.040 |
| ewma | 2026-07-30T13:01:00Z | 0.034 |
| quadratic | 2026-07-30T10:57:54Z | 0.034 |
| recent | 2026-07-30T13:15:09Z | 0.030 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

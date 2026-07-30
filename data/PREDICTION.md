# Vote Party Prediction

_Generated 2026-07-30T02:48:09Z — recomputed every data update._

**Progress:** 657 / 5000.0 (13.1%) — 4343 remaining
**Players online:** 490  |  **Cycle started:** 2026-07-30T01:00:58Z  |  **Data points this cycle:** 24

## 🎯 Prediction

**Vote party fires ≈ `2026-07-30 12:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-30 12:00Z` → `2026-07-30 13:15Z`
_Interval from the `shape_analogue` model (~79% measured 80%-interval coverage OOS, endpoint label-uncertainty propagated) over 25 cycles (18 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-30T13:21:38Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-30T12:38:09Z | 0.344 |
| diurnal | 2026-07-30T12:38:09Z | 0.317 |
| shrinkage | 2026-07-30T14:17:38Z | 0.115 |
| linear | 2026-07-30T15:37:27Z | 0.043 |
| wls | 2026-07-30T16:00:23Z | 0.042 |
| theilsen | 2026-07-30T15:42:24Z | 0.040 |
| ewma | 2026-07-30T14:13:35Z | 0.034 |
| quadratic | n/a | 0.034 |
| recent | 2026-07-30T14:41:30Z | 0.030 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `shape_analogue` model, independent of these weights. See `prediction_track.png`.

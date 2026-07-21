# Vote Party Prediction

_Generated 2026-07-21T12:19:18Z — recomputed every data update._

**Progress:** 2873 / 5000.0 (57.5%) — 2127 remaining
**Players online:** 494  |  **Cycle started:** 2026-07-21T05:37:06Z  |  **Data points this cycle:** 32

## 🎯 Prediction

**Vote party fires ≈ `2026-07-21 17:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-21 15:00Z` → `2026-07-21 19:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 8 cycles (5 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-21T17:03:34Z`._

## Model diagnostics (not the prediction)

**Stable winner:** `diurnal_dow` wins every leave-one-cycle-out fold (still few cycles).

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-21T16:44:18Z | 0.255 |
| diurnal | 2026-07-21T16:59:18Z | 0.228 |
| shrinkage | 2026-07-21T17:48:05Z | 0.098 |
| linear | 2026-07-21T17:32:14Z | 0.080 |
| wls | 2026-07-21T17:23:35Z | 0.076 |
| theilsen | 2026-07-21T17:33:07Z | 0.071 |
| ewma | 2026-07-21T16:45:06Z | 0.068 |
| quadratic | 2026-07-21T17:12:43Z | 0.062 |
| recent | 2026-07-21T16:03:22Z | 0.062 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

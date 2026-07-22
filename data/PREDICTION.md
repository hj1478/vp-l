# Vote Party Prediction

_Generated 2026-07-22T05:21:16Z — recomputed every data update._

**Progress:** 4268 / 5000.0 (85.4%) — 732 remaining
**Players online:** 454  |  **Cycle started:** 2026-07-21T17:14:23Z  |  **Data points this cycle:** 82

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 07:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 06:45Z` → `2026-07-22 08:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 9 cycles (6 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T06:55:50Z`._

## Model diagnostics (not the prediction)

**Stable winner:** `diurnal_dow` wins every leave-one-cycle-out fold (still few cycles).

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T06:26:16Z | 0.218 |
| diurnal | 2026-07-22T06:26:16Z | 0.194 |
| shrinkage | 2026-07-22T07:23:39Z | 0.099 |
| ewma | 2026-07-22T06:26:15Z | 0.097 |
| wls | 2026-07-22T07:37:54Z | 0.095 |
| linear | 2026-07-22T08:02:04Z | 0.080 |
| recent | 2026-07-22T06:05:52Z | 0.079 |
| theilsen | 2026-07-22T07:57:11Z | 0.074 |
| quadratic | 2026-07-22T07:33:09Z | 0.065 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

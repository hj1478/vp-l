# Vote Party Prediction

_Generated 2026-07-22T01:34:14Z — recomputed every data update._

**Progress:** 2893 / 5000.0 (57.9%) — 2107 remaining
**Players online:** 490  |  **Cycle started:** 2026-07-21T17:14:23Z  |  **Data points this cycle:** 58

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 07:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 04:00Z` → `2026-07-22 09:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 9 cycles (6 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T07:03:09Z`._

## Model diagnostics (not the prediction)

**Stable winner:** `diurnal_dow` wins every leave-one-cycle-out fold (still few cycles).

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T06:39:14Z | 0.266 |
| diurnal | 2026-07-22T06:44:14Z | 0.228 |
| shrinkage | 2026-07-22T07:26:36Z | 0.097 |
| linear | 2026-07-22T08:29:08Z | 0.079 |
| wls | 2026-07-22T06:44:27Z | 0.075 |
| theilsen | 2026-07-22T08:24:52Z | 0.070 |
| ewma | 2026-07-22T06:51:06Z | 0.065 |
| quadratic | 2026-07-22T06:56:58Z | 0.061 |
| recent | 2026-07-22T06:36:45Z | 0.059 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

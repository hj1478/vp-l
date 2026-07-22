# Vote Party Prediction

_Generated 2026-07-22T03:27:25Z — recomputed every data update._

**Progress:** 3501 / 5000.0 (70.0%) — 1499 remaining
**Players online:** 481  |  **Cycle started:** 2026-07-21T17:14:23Z  |  **Data points this cycle:** 70

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 07:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 06:00Z` → `2026-07-22 08:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 9 cycles (6 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T07:48:55Z`._

## Model diagnostics (not the prediction)

**Stable winner:** `diurnal_dow` wins every leave-one-cycle-out fold (still few cycles).

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T07:37:25Z | 0.266 |
| diurnal | 2026-07-22T07:42:25Z | 0.228 |
| shrinkage | 2026-07-22T07:36:29Z | 0.097 |
| linear | 2026-07-22T08:03:22Z | 0.079 |
| wls | 2026-07-22T07:33:55Z | 0.075 |
| theilsen | 2026-07-22T07:56:32Z | 0.070 |
| ewma | 2026-07-22T08:59:32Z | 0.065 |
| quadratic | 2026-07-22T06:56:00Z | 0.061 |
| recent | 2026-07-22T08:52:51Z | 0.059 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-21T19:53:10Z — recomputed every data update._

**Progress:** 938 / 5000.0 (18.8%) — 4062 remaining
**Players online:** 564  |  **Cycle started:** 2026-07-21T17:14:23Z  |  **Data points this cycle:** 22

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 08:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 05:00Z` → `2026-07-22 09:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 9 cycles (6 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T08:14:54Z`._

## Model diagnostics (not the prediction)

**Stable winner:** `diurnal_dow` wins every leave-one-cycle-out fold (still few cycles).

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T07:43:10Z | 0.284 |
| diurnal | 2026-07-22T07:58:10Z | 0.258 |
| shrinkage | 2026-07-22T06:45:35Z | 0.089 |
| wls | 2026-07-22T08:02:34Z | 0.065 |
| linear | 2026-07-22T07:23:22Z | 0.064 |
| ewma | 2026-07-22T12:28:09Z | 0.063 |
| theilsen | 2026-07-22T07:31:49Z | 0.062 |
| recent | 2026-07-22T11:40:58Z | 0.059 |
| quadratic | n/a | 0.058 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-21T16:06:28Z — recomputed every data update._

**Progress:** 4445 / 5000.0 (88.9%) — 555 remaining
**Players online:** 553  |  **Cycle started:** 2026-07-21T05:37:06Z  |  **Data points this cycle:** 44

## 🎯 Prediction

**Vote party fires ≈ `2026-07-21 17:15Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-21 17:00Z` → `2026-07-21 18:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 8 cycles (5 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-21T17:30:16Z`._

## Model diagnostics (not the prediction)

**Stable winner:** `diurnal_dow` wins every leave-one-cycle-out fold (still few cycles).

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-21T17:36:28Z | 0.213 |
| diurnal | 2026-07-21T17:36:28Z | 0.195 |
| shrinkage | 2026-07-21T17:31:03Z | 0.100 |
| ewma | 2026-07-21T17:17:57Z | 0.095 |
| wls | 2026-07-21T17:27:40Z | 0.095 |
| linear | 2026-07-21T17:29:48Z | 0.081 |
| recent | 2026-07-21T17:19:46Z | 0.080 |
| theilsen | 2026-07-21T17:29:19Z | 0.075 |
| quadratic | 2026-07-21T17:26:49Z | 0.067 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

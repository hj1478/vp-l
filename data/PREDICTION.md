# Vote Party Prediction

_Generated 2026-07-22T11:04:06Z — recomputed every data update._

**Progress:** 1958 / 5000.0 (39.2%) — 3042 remaining
**Players online:** 461  |  **Cycle started:** 2026-07-22T08:14:51Z  |  **Data points this cycle:** 24

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 18:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 14:00Z` → `2026-07-22 21:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 10 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T18:09:37Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T18:04:06Z | 0.280 |
| diurnal | 2026-07-22T18:19:06Z | 0.247 |
| shrinkage | 2026-07-22T18:45:58Z | 0.104 |
| wls | 2026-07-22T18:02:14Z | 0.066 |
| linear | 2026-07-22T17:48:28Z | 0.065 |
| theilsen | 2026-07-22T17:48:42Z | 0.064 |
| ewma | 2026-07-22T18:01:03Z | 0.060 |
| recent | 2026-07-22T17:54:54Z | 0.058 |
| quadratic | n/a | 0.057 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

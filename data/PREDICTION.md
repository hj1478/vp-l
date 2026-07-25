# Vote Party Prediction

_Generated 2026-07-25T20:34:06Z — recomputed every data update._

**Progress:** 4214 / 5000.0 (84.3%) — 786 remaining
**Players online:** 581  |  **Cycle started:** 2026-07-25T10:40:38Z  |  **Data points this cycle:** 71

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 22:45Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 22:00Z` → `2026-07-25 23:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 16 cycles (10 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T23:07:13Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T23:19:06Z | 0.259 |
| diurnal | 2026-07-25T23:19:06Z | 0.230 |
| shrinkage | 2026-07-25T22:37:48Z | 0.115 |
| wls | 2026-07-25T23:11:37Z | 0.082 |
| ewma | 2026-07-25T23:07:36Z | 0.073 |
| quadratic | 2026-07-26T00:08:06Z | 0.066 |
| recent | 2026-07-25T23:02:45Z | 0.066 |
| linear | 2026-07-25T22:10:11Z | 0.057 |
| theilsen | 2026-07-25T22:05:31Z | 0.053 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

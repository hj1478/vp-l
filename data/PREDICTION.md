# Vote Party Prediction

_Generated 2026-07-22T12:58:25Z — recomputed every data update._

**Progress:** 2841 / 5000.0 (56.8%) — 2159 remaining
**Players online:** 558  |  **Cycle started:** 2026-07-22T08:14:51Z  |  **Data points this cycle:** 36

## 🎯 Prediction

**Vote party fires ≈ `2026-07-22 18:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-22 17:30Z` → `2026-07-22 20:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 10 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-22T17:46:58Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-22T17:38:25Z | 0.258 |
| diurnal | 2026-07-22T17:53:25Z | 0.230 |
| shrinkage | 2026-07-22T18:21:38Z | 0.106 |
| wls | 2026-07-22T17:42:02Z | 0.079 |
| linear | 2026-07-22T17:52:31Z | 0.075 |
| theilsen | 2026-07-22T17:51:19Z | 0.068 |
| ewma | 2026-07-22T17:18:05Z | 0.064 |
| quadratic | 2026-07-22T17:58:21Z | 0.062 |
| recent | 2026-07-22T17:10:18Z | 0.058 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

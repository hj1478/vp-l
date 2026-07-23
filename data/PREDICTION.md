# Vote Party Prediction

_Generated 2026-07-23T06:09:48Z — recomputed every data update._

**Progress:** 4332 / 5000.0 (86.6%) — 668 remaining
**Players online:** 430  |  **Cycle started:** 2026-07-22T18:12:39Z  |  **Data points this cycle:** 94

## 🎯 Prediction

**Vote party fires ≈ `2026-07-23 07:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-23 07:15Z` → `2026-07-23 08:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 11 cycles (7 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-23T07:55:52Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-23T07:49:48Z | 0.222 |
| diurnal | 2026-07-23T07:39:48Z | 0.201 |
| shrinkage | 2026-07-23T08:01:32Z | 0.113 |
| wls | 2026-07-23T07:40:50Z | 0.085 |
| linear | 2026-07-23T08:49:27Z | 0.082 |
| theilsen | 2026-07-23T09:03:37Z | 0.079 |
| ewma | 2026-07-23T07:30:25Z | 0.076 |
| quadratic | 2026-07-23T07:44:46Z | 0.072 |
| recent | 2026-07-23T07:30:02Z | 0.070 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

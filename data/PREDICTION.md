# Vote Party Prediction

_Generated 2026-07-25T07:37:36Z — recomputed every data update._

**Progress:** 3859 / 5000.0 (77.2%) — 1141 remaining
**Players online:** 413  |  **Cycle started:** 2026-07-24T21:05:32Z  |  **Data points this cycle:** 70

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 10:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 09:30Z` → `2026-07-25 11:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 15 cycles (9 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T10:19:14Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T10:07:36Z | 0.254 |
| diurnal | 2026-07-25T10:07:36Z | 0.225 |
| shrinkage | 2026-07-25T10:41:45Z | 0.118 |
| wls | 2026-07-25T10:14:37Z | 0.081 |
| ewma | 2026-07-25T10:12:47Z | 0.074 |
| recent | 2026-07-25T09:59:19Z | 0.067 |
| quadratic | 2026-07-25T09:54:01Z | 0.064 |
| linear | 2026-07-25T11:12:46Z | 0.060 |
| theilsen | 2026-07-25T11:21:59Z | 0.056 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

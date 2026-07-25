# Vote Party Prediction

_Generated 2026-07-25T09:36:23Z — recomputed every data update._

**Progress:** 4830 / 5000.0 (96.6%) — 170 remaining
**Players online:** 527  |  **Cycle started:** 2026-07-24T21:05:32Z  |  **Data points this cycle:** 110

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 09:55Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 09:45Z` → `2026-07-25 10:20Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 15 cycles (9 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T09:58:49Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T09:56:23Z | 0.254 |
| diurnal | 2026-07-25T09:56:23Z | 0.225 |
| shrinkage | 2026-07-25T10:02:07Z | 0.118 |
| wls | 2026-07-25T09:57:26Z | 0.081 |
| ewma | 2026-07-25T09:51:09Z | 0.074 |
| recent | 2026-07-25T09:50:27Z | 0.067 |
| quadratic | 2026-07-25T09:58:11Z | 0.064 |
| linear | 2026-07-25T10:23:22Z | 0.060 |
| theilsen | 2026-07-25T10:09:23Z | 0.056 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

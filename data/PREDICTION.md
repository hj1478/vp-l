# Vote Party Prediction

_Generated 2026-07-25T18:34:31Z — recomputed every data update._

**Progress:** 3639 / 5000.0 (72.8%) — 1361 remaining
**Players online:** 596  |  **Cycle started:** 2026-07-25T10:40:38Z  |  **Data points this cycle:** 59

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 22:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 21:30Z` → `2026-07-25 23:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 16 cycles (10 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T22:42:47Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T22:59:31Z | 0.286 |
| diurnal | 2026-07-25T22:59:31Z | 0.260 |
| shrinkage | 2026-07-25T22:04:13Z | 0.114 |
| wls | 2026-07-25T22:22:36Z | 0.069 |
| linear | 2026-07-25T21:43:21Z | 0.059 |
| quadratic | 2026-07-26T00:12:59Z | 0.056 |
| theilsen | 2026-07-25T21:46:54Z | 0.054 |
| ewma | 2026-07-25T22:41:55Z | 0.054 |
| recent | 2026-07-25T22:02:58Z | 0.046 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

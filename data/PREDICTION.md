# Vote Party Prediction

_Generated 2026-07-25T05:38:39Z — recomputed every data update._

**Progress:** 2989 / 5000.0 (59.8%) — 2011 remaining
**Players online:** 456  |  **Cycle started:** 2026-07-24T21:05:32Z  |  **Data points this cycle:** 58

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 10:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 08:00Z` → `2026-07-25 11:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 15 cycles (9 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T10:43:56Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T10:38:39Z | 0.280 |
| diurnal | 2026-07-25T10:23:39Z | 0.253 |
| shrinkage | 2026-07-25T11:09:06Z | 0.118 |
| wls | 2026-07-25T10:35:05Z | 0.071 |
| linear | 2026-07-25T11:54:09Z | 0.062 |
| theilsen | 2026-07-25T12:01:15Z | 0.056 |
| quadratic | 2026-07-25T09:57:34Z | 0.056 |
| ewma | 2026-07-25T09:55:39Z | 0.056 |
| recent | 2026-07-25T11:00:42Z | 0.049 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

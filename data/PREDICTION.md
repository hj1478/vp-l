# Vote Party Prediction

_Generated 2026-07-26T11:42:48Z — recomputed every data update._

**Progress:** 567 / 5000.0 (11.3%) — 4433 remaining
**Players online:** 548  |  **Cycle started:** 2026-07-26T10:47:48Z  |  **Data points this cycle:** 12

## 🎯 Prediction

**Vote party fires ≈ `2026-07-26 23:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-26 21:00Z` → `2026-07-27 02:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 18 cycles (12 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-26T23:33:12Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T00:32:48Z | 0.345 |
| diurnal | 2026-07-27T00:17:48Z | 0.296 |
| shrinkage | 2026-07-26T22:58:52Z | 0.104 |
| wls | 2026-07-26T20:53:15Z | 0.046 |
| linear | 2026-07-26T20:11:55Z | 0.045 |
| theilsen | 2026-07-26T20:16:35Z | 0.044 |
| ewma | 2026-07-26T21:27:19Z | 0.041 |
| quadratic | n/a | 0.038 |
| recent | 2026-07-26T23:41:29Z | 0.038 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

# Vote Party Prediction

_Generated 2026-07-27T22:03:08Z — recomputed every data update._

**Progress:** 4327 / 5000.0 (86.5%) — 673 remaining
**Players online:** 515  |  **Cycle started:** 2026-07-27T11:06:55Z  |  **Data points this cycle:** 64

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 00:05Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-27 23:50Z` → `2026-07-28 00:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 20 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-28T00:16:35Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-28T00:28:08Z | 0.259 |
| diurnal | 2026-07-28T00:23:08Z | 0.252 |
| shrinkage | 2026-07-27T23:48:18Z | 0.114 |
| wls | 2026-07-28T00:03:48Z | 0.091 |
| quadratic | 2026-07-28T00:52:05Z | 0.072 |
| ewma | 2026-07-28T00:38:40Z | 0.071 |
| linear | 2026-07-27T23:18:31Z | 0.053 |
| theilsen | 2026-07-27T23:23:42Z | 0.050 |
| recent | 2026-07-28T00:54:42Z | 0.037 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

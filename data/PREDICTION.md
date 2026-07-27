# Vote Party Prediction

_Generated 2026-07-27T15:35:04Z — recomputed every data update._

**Progress:** 2143 / 5000.0 (42.9%) — 2857 remaining
**Players online:** 570  |  **Cycle started:** 2026-07-27T11:06:55Z  |  **Data points this cycle:** 29

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 00:15Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-27 23:45Z` → `2026-07-28 01:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 20 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-27T23:06:48Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T23:55:04Z | 0.325 |
| diurnal | 2026-07-27T23:40:04Z | 0.317 |
| shrinkage | 2026-07-27T22:36:36Z | 0.112 |
| wls | 2026-07-27T21:46:13Z | 0.045 |
| linear | 2026-07-27T21:45:29Z | 0.045 |
| theilsen | 2026-07-27T21:45:10Z | 0.042 |
| ewma | 2026-07-27T21:20:54Z | 0.040 |
| recent | 2026-07-27T20:54:55Z | 0.037 |
| quadratic | 2026-07-27T21:46:07Z | 0.037 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

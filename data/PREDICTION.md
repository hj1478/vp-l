# Vote Party Prediction

_Generated 2026-07-27T11:22:50Z — recomputed every data update._

**Progress:** 216 / 5000.0 (4.3%) — 4784 remaining
**Players online:** 535  |  **Cycle started:** 2026-07-27T11:06:55Z  |  **Data points this cycle:** 5

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 00:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-27 22:30Z` → `2026-07-28 01:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 20 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-27T22:39:57Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-28T00:07:50Z | 0.325 |
| diurnal | 2026-07-28T00:12:50Z | 0.317 |
| shrinkage | 2026-07-27T23:23:56Z | 0.112 |
| wls | 2026-07-27T17:54:15Z | 0.045 |
| linear | 2026-07-27T17:50:45Z | 0.045 |
| theilsen | 2026-07-27T17:31:57Z | 0.042 |
| ewma | 2026-07-27T17:24:47Z | 0.040 |
| recent | 2026-07-27T17:30:41Z | 0.037 |
| quadratic | n/a | 0.037 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

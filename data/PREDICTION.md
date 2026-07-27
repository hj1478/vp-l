# Vote Party Prediction

_Generated 2026-07-27T19:55:34Z — recomputed every data update._

**Progress:** 3642 / 5000.0 (72.8%) — 1358 remaining
**Players online:** 610  |  **Cycle started:** 2026-07-27T11:06:55Z  |  **Data points this cycle:** 52

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 00:15Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-28 00:00Z` → `2026-07-28 00:45Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 20 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-28T00:05:03Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-28T00:15:34Z | 0.283 |
| diurnal | 2026-07-28T00:15:34Z | 0.274 |
| shrinkage | 2026-07-27T23:23:11Z | 0.108 |
| wls | 2026-07-27T23:54:55Z | 0.071 |
| quadratic | 2026-07-28T01:47:23Z | 0.057 |
| linear | 2026-07-27T22:53:13Z | 0.056 |
| ewma | 2026-07-28T00:24:55Z | 0.054 |
| theilsen | 2026-07-27T22:54:35Z | 0.051 |
| recent | 2026-07-28T00:08:35Z | 0.046 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

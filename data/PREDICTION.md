# Vote Party Prediction

_Generated 2026-07-28T21:27:00Z — recomputed every data update._

**Progress:** 4040 / 5000.0 (80.8%) — 960 remaining
**Players online:** 534  |  **Cycle started:** 2026-07-28T11:56:59Z  |  **Data points this cycle:** 69

## 🎯 Prediction

**Vote party fires ≈ `2026-07-29 00:15Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-29 00:00Z` → `2026-07-29 01:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 22 cycles (15 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-29T00:15:12Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-29T00:22:00Z | 0.267 |
| diurnal | 2026-07-29T00:17:00Z | 0.257 |
| shrinkage | 2026-07-28T23:54:11Z | 0.108 |
| wls | 2026-07-29T00:12:08Z | 0.090 |
| quadratic | 2026-07-29T00:25:57Z | 0.073 |
| ewma | 2026-07-29T00:56:15Z | 0.071 |
| linear | 2026-07-28T23:31:18Z | 0.050 |
| theilsen | 2026-07-28T23:36:35Z | 0.048 |
| recent | 2026-07-29T00:32:47Z | 0.035 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

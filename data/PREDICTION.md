# Vote Party Prediction

_Generated 2026-07-28T10:43:27Z — recomputed every data update._

**Progress:** 4639 / 5000.0 (92.8%) — 361 remaining
**Players online:** 466  |  **Cycle started:** 2026-07-28T00:05:45Z  |  **Data points this cycle:** 94

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 11:25Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-28 11:20Z` → `2026-07-28 11:40Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 21 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-28T11:37:27Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-28T11:38:27Z | 0.266 |
| diurnal | 2026-07-28T11:38:27Z | 0.255 |
| shrinkage | 2026-07-28T11:37:49Z | 0.111 |
| wls | 2026-07-28T11:23:32Z | 0.090 |
| quadratic | 2026-07-28T11:24:15Z | 0.072 |
| ewma | 2026-07-28T11:29:00Z | 0.070 |
| linear | 2026-07-28T12:00:27Z | 0.052 |
| theilsen | 2026-07-28T11:56:01Z | 0.049 |
| recent | 2026-07-28T11:41:17Z | 0.036 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

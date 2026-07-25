# Vote Party Prediction

_Generated 2026-07-25T03:39:50Z — recomputed every data update._

**Progress:** 2124 / 5000.0 (42.5%) — 2876 remaining
**Players online:** 468  |  **Cycle started:** 2026-07-24T21:05:32Z  |  **Data points this cycle:** 46

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 10:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 09:30Z` → `2026-07-25 11:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 15 cycles (9 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T11:17:52Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-25T10:39:50Z | 0.320 |
| diurnal | 2026-07-25T10:44:50Z | 0.288 |
| shrinkage | 2026-07-25T11:34:42Z | 0.112 |
| wls | 2026-07-25T11:53:52Z | 0.050 |
| linear | 2026-07-25T12:34:12Z | 0.049 |
| theilsen | 2026-07-25T12:30:17Z | 0.048 |
| ewma | 2026-07-25T13:03:36Z | 0.047 |
| recent | 2026-07-25T14:57:40Z | 0.044 |
| quadratic | 2026-07-25T09:42:02Z | 0.041 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

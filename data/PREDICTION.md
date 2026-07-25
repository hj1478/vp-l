# Vote Party Prediction

_Generated 2026-07-25T22:34:03Z — recomputed every data update._

**Progress:** 4665 / 5000.0 (93.3%) — 335 remaining
**Players online:** 577  |  **Cycle started:** 2026-07-25T10:40:38Z  |  **Data points this cycle:** 119

## 🎯 Prediction

**Vote party fires ≈ `2026-07-25 23:30Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-25 23:00Z` → `2026-07-26 00:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 16 cycles (10 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-25T23:57:35Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-26T00:09:03Z | 0.259 |
| diurnal | 2026-07-25T23:54:03Z | 0.230 |
| shrinkage | 2026-07-25T23:31:54Z | 0.115 |
| wls | 2026-07-26T00:11:09Z | 0.082 |
| ewma | 2026-07-26T00:22:25Z | 0.073 |
| quadratic | 2026-07-26T00:15:01Z | 0.066 |
| recent | 2026-07-26T00:16:59Z | 0.066 |
| linear | 2026-07-25T23:07:22Z | 0.057 |
| theilsen | 2026-07-25T23:25:38Z | 0.053 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

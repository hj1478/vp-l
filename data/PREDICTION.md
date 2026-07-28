# Vote Party Prediction

_Generated 2026-07-28T07:33:43Z — recomputed every data update._

**Progress:** 3043 / 5000.0 (60.9%) — 1957 remaining
**Players online:** 299  |  **Cycle started:** 2026-07-28T00:05:45Z  |  **Data points this cycle:** 59

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 11:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-28 11:00Z` → `2026-07-28 12:15Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 21 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-28T12:19:22Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-28T12:13:43Z | 0.290 |
| diurnal | 2026-07-28T12:08:43Z | 0.280 |
| shrinkage | 2026-07-28T12:44:53Z | 0.104 |
| wls | 2026-07-28T12:00:41Z | 0.069 |
| quadratic | 2026-07-28T11:10:49Z | 0.057 |
| linear | 2026-07-28T13:14:28Z | 0.054 |
| ewma | 2026-07-28T12:29:42Z | 0.053 |
| theilsen | 2026-07-28T13:01:41Z | 0.049 |
| recent | 2026-07-28T12:53:03Z | 0.045 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

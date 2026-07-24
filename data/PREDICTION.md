# Vote Party Prediction

_Generated 2026-07-24T11:02:45Z — recomputed every data update._

**Progress:** 1137 / 5000.0 (22.7%) — 3863 remaining
**Players online:** 468  |  **Cycle started:** 2026-07-24T08:28:39Z  |  **Data points this cycle:** 21

## 🎯 Prediction

**Vote party fires ≈ `2026-07-24 21:00Z`**  (model: `analogue`, rounded to interval resolution)
**80% window:** `2026-07-24 19:00Z` → `2026-07-25 00:00Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 14 cycles (8 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-24T21:09:45Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-24T21:22:45Z | 0.320 |
| diurnal | 2026-07-24T21:32:45Z | 0.291 |
| shrinkage | 2026-07-24T20:59:59Z | 0.107 |
| wls | 2026-07-24T20:08:16Z | 0.050 |
| linear | 2026-07-24T19:54:19Z | 0.050 |
| theilsen | 2026-07-24T19:56:10Z | 0.049 |
| ewma | 2026-07-24T21:22:58Z | 0.047 |
| recent | 2026-07-24T21:09:19Z | 0.045 |
| quadratic | n/a | 0.042 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

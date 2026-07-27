# Vote Party Prediction

_Generated 2026-07-27T13:29:15Z — recomputed every data update._

**Progress:** 1186 / 5000.0 (23.7%) — 3814 remaining
**Players online:** 572  |  **Cycle started:** 2026-07-27T11:06:55Z  |  **Data points this cycle:** 17

## 🎯 Prediction

**Vote party fires ≈ `2026-07-28 00:30Z`**  (model: `shape_analogue`, rounded to interval resolution)
**80% window:** `2026-07-27 23:30Z` → `2026-07-28 01:30Z`
_Interval from the analogue curve-library (measured ~73% coverage OOS, endpoint label-uncertainty propagated) over 20 cycles (14 tightly labeled). Point rounded to match interval width; wide early by design._

_Diagnostic ensemble ETA: `2026-07-27T23:05:49Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-27T23:54:15Z | 0.325 |
| diurnal | 2026-07-27T23:59:15Z | 0.317 |
| shrinkage | 2026-07-27T23:01:56Z | 0.112 |
| wls | 2026-07-27T21:35:37Z | 0.045 |
| linear | 2026-07-27T21:44:36Z | 0.045 |
| theilsen | 2026-07-27T21:33:31Z | 0.042 |
| ewma | 2026-07-27T20:31:18Z | 0.040 |
| recent | 2026-07-27T19:53:12Z | 0.037 |
| quadratic | 2026-07-27T19:48:51Z | 0.037 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

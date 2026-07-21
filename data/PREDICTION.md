# Vote Party Prediction

_Generated 2026-07-21T12:19:18Z — recomputed every data update._

**Progress:** 2873 / 5000.0 (57.5%) — 2127 remaining
**Players online:** 494  |  **Cycle started:** 2026-07-21T05:37:06Z  |  **Data points this cycle:** 32

## 🎯 Prediction

**Vote party fires ≈ `2026-07-21T16:56:15Z`**  (model: `analogue`)
**80% window:** `2026-07-21T14:48:00Z` → `2026-07-21T19:04:10Z`  (90%: `2026-07-21T14:48:00Z` → `2026-07-21T19:19:02Z`)
_Interval from the analogue curve-library (measured ~75% coverage OOS) over 8 cycles (3 tightly labeled). Wide early by design; tightens as the cycle fills._

_Diagnostic ensemble ETA: `2026-07-21T17:03:34Z`._

## Model diagnostics (not the prediction)

**No stable winner** — the lowest-error model differs across leave-one-cycle-out folds, so we name none and keep the (diagnostic) weights shrunk toward uniform.

| Model | Predicted ETA | Weight (shrunk) |
|-------|---------------|-----------------|
| diurnal_dow | 2026-07-21T16:44:18Z | 0.255 |
| diurnal | 2026-07-21T16:59:18Z | 0.228 |
| shrinkage | 2026-07-21T17:48:05Z | 0.098 |
| linear | 2026-07-21T17:32:14Z | 0.080 |
| wls | 2026-07-21T17:23:35Z | 0.076 |
| theilsen | 2026-07-21T17:33:07Z | 0.071 |
| ewma | 2026-07-21T16:45:06Z | 0.068 |
| quadratic | 2026-07-21T17:12:43Z | 0.062 |
| recent | 2026-07-21T16:03:22Z | 0.062 |

**Weights are shrunk toward uniform** by an Occam prior (λ = n/(n+6) in cycles): near-equal now, differentiating only when many cycles give strong, stable evidence. A shifting 'leader' at this sample size is sampling noise, not a finding. The reported prediction (above) is the `analogue` model, independent of these weights. See `prediction_track.png`.

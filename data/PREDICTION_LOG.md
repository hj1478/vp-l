# Prediction Track Record (out-of-sample)

Causal reconstruction — each prediction used only cycles that finished *before* its cycle began. Predictions are the **primary model (`diurnal`)**, not the ensemble.

⚠️ **Label caveat:** only **3 cycle(s)** have a firing time known to within 15 min. Numbers over loosely-sampled cycles are contaminated by label error of tens of minutes, so the **tight-label** row is the trustworthy one.

**Tight-label OOS MAE:** 39.0 min (n=204 predictions, 3 cycle(s))
**Tight-label MAE by stage:** 0-25%=59.5m  ·  25-50%=63.0m  ·  50-75%=38.7m  ·  75-90%=12.7m  ·  90-100%=12.8m

_All-cycle (contaminated) MAE: 53.4 min over 479 predictions — do not trust._

## Per-cycle snapshots

| Cycle | Actual fire | Label | @~50% | @~75% | @~90% |
|-------|-------------|-------|------:|------:|------:|
| 2 | 2026-07-17T22:48:53Z | ±69m | -81m | -66m | -20m |
| 3 | 2026-07-18T11:33:30Z | ±117m | +3m | +7m | -4m |
| 4 | 2026-07-19T02:06:40Z | ±184m | -52m | -39m | -5m |
| 5 | 2026-07-19T13:14:36Z | tight | — | +30m | +6m |
| 6 | 2026-07-20T04:22:31Z | ±184m | -19m | -45m | -10m |
| 7 | 2026-07-20T15:20:21Z | tight | +52m | +43m | +23m |
| 8 | 2026-07-21T05:36:45Z | tight | +46m | +30m | +30m |

Values are primary-model error (predicted − actual firing), minutes; + = predicted too late. See `prediction_track.png`.

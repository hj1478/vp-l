# Prediction Track Record (out-of-sample)

Causal reconstruction — each prediction used only cycles that finished *before* its cycle began. Predictions are the **primary model (`diurnal`)**, not the ensemble.

⚠️ **Label caveat:** only **3 cycle(s)** have a firing time known to within 15 min. Numbers over loosely-sampled cycles are contaminated by label error of tens of minutes, so the **tight-label** row is the trustworthy one.

**Tight-label OOS MAE:** 48.1 min (n=204 predictions, 3 cycle(s))
**Tight-label MAE by stage:** 0-25%=84.5m  ·  25-50%=75.6m  ·  50-75%=45.0m  ·  75-90%=12.9m  ·  90-100%=14.0m

_All-cycle (contaminated) MAE: 62.1 min over 479 predictions — do not trust._

## Per-cycle snapshots

| Cycle | Actual fire | Label | @~50% | @~75% | @~90% |
|-------|-------------|-------|------:|------:|------:|
| 2 | 2026-07-17T22:48:53Z | ±69m | -79m | -64m | -20m |
| 3 | 2026-07-18T11:33:30Z | ±117m | +4m | +7m | -4m |
| 4 | 2026-07-19T02:06:40Z | ±184m | -61m | -36m | -6m |
| 5 | 2026-07-19T13:14:36Z | tight | — | +37m | +6m |
| 6 | 2026-07-20T04:22:31Z | ±184m | -30m | -46m | -6m |
| 7 | 2026-07-20T15:20:21Z | tight | +56m | +43m | +22m |
| 8 | 2026-07-21T05:36:45Z | tight | +66m | +38m | +34m |

Values are primary-model error (predicted − actual firing), minutes; + = predicted too late. See `prediction_track.png`.

# Prediction Track Record (out-of-sample)

Causal reconstruction — each prediction used only cycles that finished *before* its cycle began. Predictions are the **primary model (`diurnal`)**, not the ensemble.

⚠️ **Label caveat:** only **1 cycle(s)** have a firing time known to within 15 min. Numbers over loosely-sampled cycles are contaminated by label error of tens of minutes, so the **tight-label** row is the trustworthy one.

**Tight-label OOS MAE:** 77.2 min (n=50 predictions, 1 cycle(s))
**Tight-label MAE by stage:** 0-25%=209.0m  ·  25-50%=120.5m  ·  50-75%=45.6m  ·  75-90%=2.1m  ·  90-100%=6.6m

_All-cycle (contaminated) MAE: 85.1 min over 167 predictions — do not trust._

## Per-cycle snapshots

| Cycle | Actual fire | Label | @~50% | @~75% | @~90% |
|-------|-------------|-------|------:|------:|------:|
| 2 | 2026-07-17T22:48:53Z | ±69m | -79m | -64m | -20m |
| 3 | 2026-07-18T11:33:30Z | ±117m | +4m | +7m | -4m |
| 4 | 2026-07-19T02:06:40Z | ±184m | -61m | -36m | -6m |
| 5 | 2026-07-19T13:14:36Z | tight | — | +37m | +6m |

Values are primary-model error (predicted − actual firing), minutes; + = predicted too late. See `prediction_track.png`.

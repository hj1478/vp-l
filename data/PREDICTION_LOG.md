# Prediction Track Record (out-of-sample)

Causal reconstruction — each prediction used only cycles that finished *before* its cycle began. Predictions are the **analogue** model.

⚠️ **Label caveat:** **6 cycle(s)** have a firing time known (by extrapolation to target) to within 15 min. The **tight-label** row is the trustworthy one; looser cycles carry larger label error.

**Tight-label OOS MAE:** 56.1 min (n=343 predictions, 6 cycle(s))
**Tight-label MAE by stage:** 0-25%=81.9m  ·  25-50%=87.3m  ·  50-75%=48.7m  ·  75-90%=36.9m  ·  90-100%=13.4m

_All-cycle (contaminated) MAE: 63.9 min over 669 predictions — do not trust._

## Per-cycle snapshots

| Cycle | Actual fire | Label | @~50% | @~75% | @~90% |
|-------|-------------|-------|------:|------:|------:|
| 2 | 2026-07-17T22:48:53Z | tight | -81m | -66m | -20m |
| 3 | 2026-07-18T11:33:30Z | ±18m | +16m | +12m | +3m |
| 4 | 2026-07-19T02:06:40Z | ±45m | -56m | -40m | -9m |
| 5 | 2026-07-19T13:14:36Z | tight | — | +33m | +12m |
| 6 | 2026-07-20T04:22:31Z | ±15m | -30m | -42m | -9m |
| 7 | 2026-07-20T15:20:21Z | tight | +50m | +41m | +22m |
| 8 | 2026-07-21T05:36:45Z | tight | +74m | +38m | +34m |
| 9 | 2026-07-21T17:13:57Z | tight | +18m | +20m | +16m |
| 10 | 2026-07-22T06:24:38Z | tight | +90m | +103m | +31m |
| 11 | 2026-07-22T18:49:31Z | ±19m | -25m | -42m | -36m |

Values are primary-model error (predicted − actual firing), minutes; + = predicted too late. See `prediction_track.png`.

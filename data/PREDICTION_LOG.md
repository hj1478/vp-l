# Prediction Track Record (out-of-sample)

Causal reconstruction — each prediction used only cycles that finished *before* its cycle began. Predictions are the **analogue** model.

⚠️ **Label caveat:** **13 cycle(s)** have a firing time known (by extrapolation to target) to within 15 min. The **tight-label** row is the trustworthy one; looser cycles carry larger label error.

**Tight-label OOS MAE:** 49.7 min (n=1055 predictions, 13 cycle(s))
**Tight-label MAE by stage:** 0-25%=85.2m  ·  25-50%=71.6m  ·  50-75%=47.7m  ·  75-90%=28.4m  ·  90-100%=13.4m

_All-cycle (contaminated) MAE: 55.0 min over 1553 predictions — do not trust._

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
| 12 | 2026-07-23T07:37:32Z | ±17m | +37m | +52m | +18m |
| 13 | 2026-07-23T19:22:02Z | ±17m | -38m | -35m | -20m |
| 14 | 2026-07-24T08:28:45Z | tight | +82m | +35m | +41m |
| 15 | 2026-07-24T21:04:43Z | tight | +11m | +11m | -6m |
| 16 | 2026-07-25T09:47:42Z | tight | +96m | +34m | +24m |
| 17 | 2026-07-25T23:39:48Z | tight | -85m | -57m | -8m |
| 18 | 2026-07-26T10:26:52Z | tight | +119m | +48m | +24m |
| 19 | 2026-07-26T23:31:16Z | tight | +37m | +11m | +12m |
| 20 | 2026-07-27T11:07:21Z | tight | +90m | +23m | +24m |

Values are primary-model error (predicted − actual firing), minutes; + = predicted too late. See `prediction_track.png`.

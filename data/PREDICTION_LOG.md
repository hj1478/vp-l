# Prediction Track Record (out-of-sample)

Causal reconstruction — each prediction used only cycles that finished *before* its cycle began. Predictions are the reported primary (**shape_analogue**, plain-analogue fallback before a diurnal profile is estimable) — the exact model shipped in predict.py.

⚠️ **Label caveat:** **16 cycle(s)** have a firing time known (by extrapolation to target) to within 15 min. The **tight-label** row is the trustworthy one; looser cycles carry larger label error.

**Tight-label OOS MAE:** 21.5 min (n=1426 predictions, 16 cycle(s))
**Tight-label MAE by stage:** 0-25%=25.0m  ·  25-50%=29.8m  ·  50-75%=21.8m  ·  75-90%=20.9m  ·  90-100%=11.6m

_All-cycle (contaminated) MAE: 32.4 min over 1986 predictions — do not trust._

## Per-cycle snapshots

| Cycle | Actual fire | Label | @~50% | @~75% | @~90% |
|-------|-------------|-------|------:|------:|------:|
| 2 | 2026-07-17T22:48:53Z | tight | -240m | -102m | -29m |
| 3 | 2026-07-18T11:33:30Z | ±18m | -162m | -39m | -8m |
| 4 | 2026-07-19T02:06:40Z | ±45m | -161m | -43m | -27m |
| 5 | 2026-07-19T13:14:36Z | tight | — | +17m | +9m |
| 6 | 2026-07-20T04:22:31Z | ±15m | -34m | -2m | -28m |
| 7 | 2026-07-20T15:20:21Z | tight | -21m | +26m | +19m |
| 8 | 2026-07-21T05:36:45Z | tight | +47m | +20m | +18m |
| 9 | 2026-07-21T17:13:57Z | tight | -6m | +25m | +16m |
| 10 | 2026-07-22T06:24:38Z | tight | +18m | +43m | +31m |
| 11 | 2026-07-22T18:49:31Z | ±19m | -39m | -52m | -41m |
| 12 | 2026-07-23T07:37:32Z | ±17m | -6m | +4m | -2m |
| 13 | 2026-07-23T19:22:02Z | ±17m | -23m | -33m | -18m |
| 14 | 2026-07-24T08:28:45Z | tight | +8m | +15m | +22m |
| 15 | 2026-07-24T21:04:43Z | tight | +5m | +15m | +21m |
| 16 | 2026-07-25T09:47:42Z | tight | +25m | +9m | +14m |
| 17 | 2026-07-25T23:39:48Z | tight | -63m | -46m | -16m |
| 18 | 2026-07-26T10:26:52Z | tight | +46m | +41m | +26m |
| 19 | 2026-07-26T23:31:16Z | tight | +36m | +22m | +16m |
| 20 | 2026-07-27T11:07:21Z | tight | +22m | +5m | +17m |
| 21 | 2026-07-28T00:35:05Z | ±33m | -23m | -26m | -31m |
| 22 | 2026-07-28T11:22:21Z | tight | +5m | +20m | +7m |
| 23 | 2026-07-29T00:13:12Z | tight | +23m | +8m | +28m |
| 24 | 2026-07-29T11:43:09Z | tight | -6m | +17m | +12m |

Values are primary-model error (predicted − actual firing), minutes; + = predicted too late. See `prediction_track.png`.

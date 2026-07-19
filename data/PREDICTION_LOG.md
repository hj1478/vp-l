# Prediction Track Record (out-of-sample)

Causal reconstruction — each prediction used only cycles that finished *before* its cycle began. This is the honest real-world scorecard.

**Resolved predictions:** 117  |  **Overall MAE:** 88.5 min  |  **Bias:** -79.7 min

**MAE by stage:** 0-25% = 208.3min  ·  25-50% = 95.9min  ·  50-75% = 44.1min  ·  75-90% = 17.2min  ·  90-100% = 13.0min

## Per-cycle snapshots

| Cycle | Actual fire | @~50% | @~75% | @~90% |
|-------|-------------|------:|------:|------:|
| 2 | 2026-07-17T22:48:53Z | -79m | -64m | -20m |
| 3 | 2026-07-18T11:33:30Z | +4m | +7m | -4m |
| 4 | 2026-07-19T02:06:40Z | -61m | -36m | -6m |

Values are ensemble error (predicted − actual firing), minutes; + = predicted too late. See `prediction_track.png`.

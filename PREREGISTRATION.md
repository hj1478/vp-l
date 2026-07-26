# Pre-registered analysis criteria

Fixed **before** any model or claim qualifies, so the bar can't be moved after
seeing which way the data breaks. If we ever change a threshold here, that is a
methodology change to be recorded and dated — not a result.

## 1. Stable-winner criterion (model selection)

We will **not** report any model as the "best" / "winner" unless ALL of:

1. **Unanimous:** it has the lowest label-weighted MAE in **every**
   leave-one-cycle-out fold.
2. **Enough clean folds:** computed over at least **8 well-labeled cycles**
   (label weight ≥ 0.25, i.e. firing time known to ≈ ±5 min).
3. Ties and near-ties (difference inside the metric's bootstrap CI) do **not**
   count as a win.

Until then the output says **"no stable winner"** and diagnostic weights stay
shrunk toward uniform (Occam prior, λ = n/(n+6) cycles). Enforced in
`predict.stable_winner` (`STABLE_WINNER_MIN_CYCLES = 8`).

**Status (as of writing):** NOT met — fewer than 8 well-labeled cycles. Even
though one model currently wins all clean folds, we do not name it. This is
deliberate: the criterion was set to forbid exactly that premature call.

## 2. Reported prediction

- The reported **point and interval are one coherent model** (`shape_analogue`;
  falls back to plain `analogue` before a diurnal profile is estimable).
- We switch the reported model only if a challenger's point beats it by **more
  than the bootstrap CI** of the paired difference, AND the point-to-point offset
  is stable (so a calibrated interval isn't grafted around a mis-located point).
- Interval **coverage is measured causally** (only-prior cycles) on the **exact
  same interval construction** that is reported, and always shown with its
  cluster-bootstrap 95% CI.

**Status (2026-07-26): criterion MET — switched `analogue` → `shape_analogue`.**
The challenger's point beat the incumbent by −11.1 min, paired 95% CI [−17.2, −4.0]
(excludes zero), measured causally in `shape_analogue.py`. No grafting risk: point
and interval are the same distribution. Its 80% coverage is 79% [70, 90] (nominal),
vs the incumbent's over-wide 92%. The switch banks the LOO shape-oracle headroom
(FINDINGS.md, "Shape-aware analogue banks the oracle headroom").

## 3. "Wait for more data" is only a valid plan if data helps

We will treat "accuracy improves as cycles accumulate" as **true only if** the
per-cycle OOS error shows a **downward trend whose slope CI excludes zero**
(see the duration/learning-curve test). If the trend is flat, "wait for data"
is not a plan and we say so.

## 4. Label quality

- A cycle's firing time uses the **extrapolation σ** (votes remaining / end-rate
  × rate uncertainty), not the raw sample gap.
- Cycles are **inverse-variance weighted** by 1/σ² everywhere they are scored;
  none are silently discarded, none treated as exact.

# Diagnostic findings log

Dated, one-off analyses. Recorded so we don't re-litigate settled questions.
(Numbers move as data grows; the *conclusions* are what matter.)

## NHPP overconfidence: genuine overdispersion, not a bug
Tested the Poisson assumption on 478 five-minute intervals. The **mean** observed
increment (30.2 votes) matches the fitted Poisson expectation (30.6) — so the
intensity/mean is correct, ruling out a coding bug. But the **variance is ~7×
larger than Poisson allows** (Pearson dispersion 7.1; Var/mean 8.5). Votes arrive
in bursts, not as independent Poisson events. So the NHPP's counting noise was
~7× too small → intervals too narrow → ~19% coverage. **Verdict:** real mechanism
limitation. A negative-binomial / Cox process with dispersion ≈7 would be needed;
the analogue's *empirical* spread already captures this, which is why it calibrates.

## "Wait for data" is currently UNPROVEN
Per-tight-cycle OOS MAE vs number of prior cycles: pattern looks like improvement
(1 prior → 144 min, 8 prior → 6.5 min; slope −17 min/cycle) BUT the bootstrap
**slope 95% CI [−30.7, +8.8] includes zero**. Per pre-registration §3, we do NOT
claim data helps until the slope CI excludes zero. Suggestive, not established;
one outlier cycle (43 min at 7 priors) breaks monotonicity.

## Update at 11 tight cycles (2026-07-26)
- **Learning trend still unproven, effect shrank.** Per-cycle OOS MAE vs n_prior:
  slope −3.35 min/cycle, CI [−9.2, +3.2] (was −17 on 5 cycles — inflated by one
  outlier). Doubling the data flattened it toward zero. "Wait for data" is **not**
  the lever for point accuracy; the analogue plateaus after a few cycles.
- **Frontrunner but no stable winner.** Over 8 well-labeled folds `diurnal_dow`
  wins 6/8 (shrinkage 1, diurnal 1) — a real frontrunner, but not unanimous, so
  the pre-registered criterion correctly withholds the title.
- **Shape modeling is the lever, nearly proven.** LOO shape oracle 20.3 min
  [15,28] vs constant-rate oracle 30.4 min [21,38]; paired improvement +9.9 min,
  CI [−1.5, +19.7] — just barely crosses zero. ~10 min of mid-cycle headroom from
  modeling the rate's diurnal shape, on the threshold of significance. This is
  where to invest (not more data, not model-picking).

## Shape-aware analogue banks the oracle headroom (SHIPPED 2026-07-26)
The LOO shape oracle (~10 min mid-cycle headroom) is now **realized out-of-sample**,
not just an upper bound. The reported primary switched from the plain analogue to a
**shape-aware analogue** that re-times each borrowed cycle through the *current*
diurnal phase instead of copying its absolute remaining duration.
- **Paired causal OOS (9 tight cycles, 765 stage-predictions), `shape_analogue.py`:**
  plain analogue MAE 31.6 min → shape-aware **20.3 min**; paired difference
  **−11.1 min, 95% CI [−17.2, −4.0]** (excludes zero). 80%-interval coverage
  **79% [70, 90]** — better calibrated than the plain analogue's over-wide 92%.
  Robust: leave-one-cycle-out never flips the sign (most adverse drop still −8.7).
- **The gain is the re-timing, not the pace-borrowing.** Sweeping the pace-shrink
  from 0 to ∞ (∞ = no per-analogue pace, pure current-phase diurnal re-time) moves
  the paired win only −9.1 → −9.7 min. So per-analogue pace deviation is inert for
  the point (kept only as a heavily-shrunk safety valve); Occam-simplest form wins.
- **Why plain `model_diurnal` didn't already get this:** its `_integrate_profile`
  rescales the pooled profile to the current cycle's *recent observed rate*, which
  double-counts the current phase and injects lull/peak noise. Same 9 cycles:
  obs-rescaled diurnal 30.6 min vs pooled-level-no-rescale **21.9 min**. Trusting
  the historical level and letting the diurnal *shape* carry the time-variation is
  the whole trick. `model_diurnal`/plain analogue stay in the table as diagnostics.

## Re-validation at 51 tight cycles (2026-08-18): shape_analogue win HOLDS
Re-ran the paired causal test with ~5x more data (51 tight cycles vs the original
9, 802 stage-predictions). shape_analogue still beats the plain analogue:
- plain analogue MAE **21.7 min** [18.1, 25.8]; shape-aware **15.8 min** [13.5, 18.5]
- paired **−5.9 min, 95% CI [−8.9, −2.9]** — excludes zero, more precisely than the
  original [−17, −4]. The point effect settled from the small-sample −11 min down
  to ~−6 min but is now far more robustly significant.
- **Caveat:** at scale the 80% interval coverage is **74% [70, 80]** — slightly
  under nominal (the plain analogue over-covers at 94%). The interval may be a
  touch narrow now; worth widening the label-σ floor if it keeps drifting low.
- Model selection: still **NO stable winner** (weights ~uniform); 53 tight cycles.

Perf: `backtest_staged`/`stable_winner` and the shape_analogue harness were
O(points·cycles); they now subsample to ~16–24 evenly-spaced stages per cycle
(predict.py 120s→~23s, harness →14s). Diagnostic weights only — the reported
shape_analogue prediction is unchanged.

## Label extrapolation is minimal; tight-threshold is not fragile
- **Extrapolation fraction:** median cycle is sampled to ~98–99.8% of target, so
  the firing label rests on ≈**1.8%** extrapolation (σ = sampling floor). Only
  cycles 3 (13.6%) and 4 (19.2%) lean on extrapolation meaningfully. Self-chaining
  now samples cycles to ~99.8%, so recent labels are essentially observed.
- **Tight-threshold sensitivity:** coverage is flat at **93–94%** for any label-σ
  threshold from 8 to 40 min (MAE 27→45 as looser cycles enter); only including
  the genuinely loose cycles ("all") drops coverage to 74%. The 15-min threshold
  sits in a stable plateau — the calibration conclusion is robust, not cherry-picked.

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

## Label extrapolation is minimal; tight-threshold is not fragile
- **Extrapolation fraction:** median cycle is sampled to ~98–99.8% of target, so
  the firing label rests on ≈**1.8%** extrapolation (σ = sampling floor). Only
  cycles 3 (13.6%) and 4 (19.2%) lean on extrapolation meaningfully. Self-chaining
  now samples cycles to ~99.8%, so recent labels are essentially observed.
- **Tight-threshold sensitivity:** coverage is flat at **93–94%** for any label-σ
  threshold from 8 to 40 min (MAE 27→45 as looser cycles enter); only including
  the genuinely loose cycles ("all") drops coverage to 74%. The 15-min threshold
  sits in a stable plateau — the calibration conclusion is robust, not cherry-picked.

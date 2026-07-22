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

## Label extrapolation is minimal; tight-threshold is not fragile
- **Extrapolation fraction:** median cycle is sampled to ~98–99.8% of target, so
  the firing label rests on ≈**1.8%** extrapolation (σ = sampling floor). Only
  cycles 3 (13.6%) and 4 (19.2%) lean on extrapolation meaningfully. Self-chaining
  now samples cycles to ~99.8%, so recent labels are essentially observed.
- **Tight-threshold sensitivity:** coverage is flat at **93–94%** for any label-σ
  threshold from 8 to 40 min (MAE 27→45 as looser cycles enter); only including
  the genuinely loose cycles ("all") drops coverage to 74%. The 15-min threshold
  sits in a stable plateau — the calibration conclusion is robust, not cherry-picked.

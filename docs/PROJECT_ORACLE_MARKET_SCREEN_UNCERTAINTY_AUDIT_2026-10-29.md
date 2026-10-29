# Project Oracle — Market Screen Uncertainty Audit

**Source:** Run #168 aggregate chronological league walk-forward metrics and readiness table.  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only; no H2H paired holdout loaded; no provider/API calls; no production changes.

## What this audit adds

The previous screen identified league-market pairs with positive Brier skill versus the league-prevalence comparator in all three chronological folds, subject to the existing per-fold sample gate. This audit adds fold-level Expected Calibration Error (ECE), worst-fold Brier skill, minimum fold sample sizes, and accuracy 95% interval widths.

These are descriptive diagnostics, not new release gates. ECE thresholds are not universal pass/fail thresholds; interpret ECE alongside Brier score, log loss, reliability plots and sample sizes.

## Results

| Market | Pairs passing 3-fold sample gate | Positive Brier skill in all 3 folds | Candidates with max-fold ECE ≥ 0.10 | Candidates with max-fold ECE 0.05–<0.10 | Candidates with max-fold ECE <0.05 |
|---|---:|---:|---:|---:|---:|
| BTTS | 30 | 3 | 1 | 1 | 1 |
| Double Chance Away | 30 | 19 | 6 | 13 | 0 |
| Double Chance Home | 30 | 17 | 6 | 11 | 0 |

The ECE bands above are descriptive only. “Positive Brier skill in all folds” means better Brier score than the league-prevalence comparator in those observed folds; it does not establish profitability or prove the difference is statistically significant.

## Highest-priority retest candidates — not betting selections

| Market | League | Worst-fold Brier skill | Median fold ECE | Maximum fold ECE | Minimum test n | Interpretation |
|---|---|---:|---:|---:|---:|---|
| BTTS | Spain — Segunda División | +0.01603 | 0.04622 | 0.10039 | 164 | Positive skill, but one fold has ECE above 0.10; calibration review needed |
| BTTS | Spain — La Liga | +0.00563 | 0.03127 | 0.04056 | 133 | Lower observed ECE, but very small worst-fold skill |
| BTTS | Netherlands — Eredivisie | +0.00485 | 0.06836 | 0.07851 | 116 | Positive skill, calibration stability needs review |
| Double Chance Home | Saudi Arabia — Professional League | +0.07053 | 0.09061 | 0.13492 | 100 | Stronger skill signal, substantial fold calibration error |
| Double Chance Home | Italy — Serie A | +0.06568 | 0.05931 | 0.10997 | 115 | Positive skill, one fold's ECE above 0.10 |
| Double Chance Home | Spain — La Liga | +0.06097 | 0.05722 | 0.07220 | 133 | Positive skill; still uncalibrated |
| Double Chance Away | Ukraine — Ukrainian Premier League | +0.16747 | 0.09756 | 0.12544 | 101 | Strong skill signal but high observed calibration error |
| Double Chance Away | Russia — Russian Premier League | +0.11963 | 0.09014 | 0.13030 | 104 | Strong skill signal but high observed calibration error |
| Double Chance Away | Saudi Arabia — Professional League | +0.09733 | 0.09731 | 0.11864 | 100 | Positive skill, calibration review needed |

The complete 150-row audit is emitted as `oracle_selected50_market_screen_uncertainty_audit.csv`; the reproducible script emits the machine-readable summary as well.

## Interpretation and limitations

- 150 league-market hypotheses were screened (50 league groups × 3 markets). Candidate counts are exploratory and susceptible to selection bias.
- The source artifact contains no confidence intervals for fold-level Brier skill and no multiplicity-adjusted inference. Do not call these statistically confirmed edges.
- Accuracy 95% interval widths are often broad; accuracy alone should not rank markets.
- Provider competition identifiers are season surrogates in this archive. Canonical competition/team/fixture joins and official settlement truth remain unverified.
- No individual teams are ranked. The locked H2H paired holdout was not loaded or used.
- Combo remains excluded because its authoritative settlement definition is unresolved.

## Next action

1. Retain these as a retest queue only.
2. Prioritize an untouched chronological validation period and reliability diagnostics, especially for candidates with high fold ECE.
3. Obtain team-attributed out-of-sample predictions and verify canonical joins and settlement truth before building team-market performance profiles.
4. Keep production logic, frozen probabilities, calibration and governance unchanged.

**Decision: continue research; production and betting eligibility remain unapproved.**

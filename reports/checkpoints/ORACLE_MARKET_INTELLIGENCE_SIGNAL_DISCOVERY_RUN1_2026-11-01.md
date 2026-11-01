# Oracle Market Intelligence Signal Discovery — Run 1

Date: 1 November 2026, 21:04 SAST
Research branch: research/oracle-50-league-readiness-audit
Parent commit inspected: 9c144f5b4230f502c90c84971c0a78a42e5fccb5

## Work completed
- Re-inspected the live repository, branch and current workflow/artifact provenance.
- Analysed successful Market Intelligence repair artifact from run 41332548789 (artifact 13093888572; SHA-256 recorded in the detailed research note).
- Exact-joined 215 settled provider-score actuals to evidence trace and goal research; excluded four schedule-review rows and seven under-five-history rows.
- Built a reproducible research-only diagnostic script and eight unit tests. All eight tests pass locally.
- Produced 204 fixture-level diagnostics, feature/outcome association tables, interaction tests and probability-score tables with bootstrap intervals and Benjamini–Hochberg correction.

## Findings
- Strict sample: 204 fixtures, 36 leagues; 122 also have at least five home-at-home and away-away observations.
- Home-versus-away last-five PPG differential associates with home wins (rho +0.274, 95% CI +0.139 to +0.393; BH q 0.0082).
- Venue PPG differential and venue goals-for advantage are promising in the 122-match venue-qualified subset (rho +0.283 and +0.287 respectively; BH q about 0.021).
- Candidate interaction: (home PPG minus away PPG) multiplied by away goals-conceded average; home-win rho +0.249, 95% CI +0.118 to +0.382, BH q 0.0074. This is a hypothesis, not a validated model.
- No feature survived multiple-testing correction for BTTS or goal totals in this cohort.
- Oracle Home 1X showed small positive mean Brier improvement, but its paired 95% interval crosses zero; BTTS did not discriminate. Experimental Over 1.5 underperformed the constant-prevalence comparator.

## Blockers and safeguards
- All current league-table statuses are provisional; league-position features are quarantined.
- xG remains excluded because point-in-time capture timestamps are unverified.
- The existing goal-market research engine uses a three-observed-match team minimum and venue threshold of three; this is not compliant with the five-match evidence rule. No change was made to that engine.
- Twenty-four blocked fixture-side records have five archived matches but missing runtime feature fields; one side genuinely lacks five. Repair feature completeness; do not lower the minimum.
- Current source artifact expires 15 November 2026.
- No provider API credits used, no workflow dispatched, and no Oracle V1.6 logic/probabilities changed.

## Next steps
Carry the two candidate interactions into the existing 18-month historical feature-edge experiment as prespecified ablations. Use chronological folds, exact IDs, five observed matches for both teams and five for each venue split, and compare against league-only and frozen Oracle V1.6 baselines. Require consistent fold-level Brier/log-loss/AUC/ECE results and confidence intervals before any promotion.

Full analysis and all machine-readable outputs are in the companion research bundle. Production and betting eligibility remain false.

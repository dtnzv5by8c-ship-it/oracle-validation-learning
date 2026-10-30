# Oracle Selected-50 — League DNA & Market Feature Intelligence
**Date:** 30 October 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** Research-only; no production model changes.

## Purpose
Add league-level behavioural profiling and a disciplined market-specific feature development plan to the consolidated Visual Intelligence report.

## League DNA — evidence and limitations
The attached workbook's **League DNA** tab profiles all 50 governed leagues using three chronological walk-forward folds from the current selected-50 runtime:
- BTTS training-prevalence proxy: historical frequency of both teams scoring in the league training sample.
- DC_HOME prevalence proxy: historical home non-loss target prevalence.
- DC_AWAY prevalence proxy: historical away non-loss target prevalence.
- Per-market positive Brier-skill fold count and mean Brier skill versus the league-prevalence baseline.
- A diagnostic leading market candidate, selected by positive-fold count and then mean Brier skill.

These are pooled-model diagnostics and prevalence proxies, not independent league-specific models. Three folds are insufficient to certify a permanent league-market preference. No league is approved for production or betting on this basis.

**Important data limitation:** the current runtime export does not contain the complete league-level total-goals distribution required to classify each league as high-, medium- or low-scoring. The workbook therefore explicitly marks total-goal profile as not scored rather than infer it from BTTS prevalence. BTTS frequency is not interchangeable with average total goals: high totals can be driven by one-sided scorelines.

## Market feature development plan
The **Market Feature Strategy** tab proposes market-specific candidate inputs and treatment:
- **BTTS:** home/away scoring and conceding rates, xG for/against, shots on target, BTTS frequency and opponent clean-sheet rate.
- **Double Chance Home:** home non-loss form, home xG differential, opponent away resistance, draw propensity and league home advantage.
- **Double Chance Away:** away non-loss form, away xG differential, opponent home strength, defensive resistance and draw propensity.
- **Combo markets:** keep masked until target and settlement definitions are reconciled; model the joint event directly rather than multiplying marginal probabilities.

These are hypotheses for controlled testing, not claims of proven uplift. Any xG, odds, standings or team-strength input must first pass point-in-time provenance, identity and missingness checks.

## H2H evidence
Existing 20-feature baseline was compared with the same feature set plus four H2H features on a paired primary holdout (20 March 2025–20 September 2026; 19,991 paired fixtures; 95.75% H2H coverage). Results are included in the workbook:
- BTTS: accuracy uplift +0.120 percentage points; Brier improved by 0.00011; AUC improved by 0.00186.
- DC_HOME: accuracy uplift +0.095 pp; Brier improved by 0.00002; log loss worsened by 0.00007.
- DC_AWAY: accuracy decreased by 0.030 pp; Brier improved by 0.00006; log loss improved by 0.00013.
- COMBO_HOME and COMBO_AWAY: no consistent improvement; remain masked.

The 2024 chronological H2H folds show small and mixed effects. H2H should remain a low-weight contextual feature, not a dominant driver. The 2024 evidence is included as chronological folds; it does not establish that all candidate feature families improve prediction.

## Next controlled experiments
1. Build a verified league-level goal-distribution table from the canonical selected-50 archive: average total goals, median, over 1.5/2.5/3.5, BTTS, clean-sheet rate, draw rate, home/away goals and season-to-season stability.
2. Run one-feature-family-at-a-time chronological ablations for recent form, venue splits, xG, shots, standings/strength, rest/travel and odds.
3. Compare against the frozen 20-feature baseline on identical fixtures and folds; report Brier, log loss, AUC, calibration and confidence intervals.
4. Retain only features with repeatable out-of-sample improvement across multiple folds and leagues; shrink league-specific effects where sample sizes are small.
5. Keep all changes in research branch. Do not alter Oracle V1.6 production logic or probabilities without formal governance approval.

## Governance
`production_eligible=false`; `betting_eligible=false`. The workbook's League DNA and Market Feature Strategy tabs are research diagnostics and a test plan, not a release recommendation.

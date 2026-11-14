# Project Oracle — FootyStats Goal-Market Intelligence Breakthrough
Date: 2026-11-14 SAST
Branch: research/oracle-50-league-readiness-audit

## Objective
Extend the locked Market Intelligence view with the highest-value FootyStats goal-market percentages and signal inputs, while preserving Oracle V1.6 production logic and the 95-column baseline.

## Provider evidence
FootyStats documents that its Match CSV contains pre-match form fields including:
- average_goals_per_match_pre_match
- btts_percentage_pre_match
- over_15_percentage_pre_match through over_45_percentage_pre_match
- pre-match home/away PPG
- match odds fields
FootyStats also documents Team/Team Pt.2 and API statistics including BTTS %, clean-sheet %, failed-to-score %, first-team-to-score %, Over/Under percentages, xG for/against, and Prediction Risk. These provider fields are candidates for the research layer, not automatic Oracle probabilities.

## Implemented research/reporting extension
The Market Intelligence schema retains the original 95-column A:CQ baseline and adds an append-only FootyStats extension beginning at CT. The extension includes:
- FootyStats pre-match average goals
- pre-match BTTS %
- pre-match Over 0.5/1.5/2.5/3.5/4.5 %
- complementary Under 1.5/2.5/3.5/4.5 %
- verified FootyStats Home/Draw/Away percentages where actually supplied
- pre-match Home/Away PPG
- Home/Away BTTS %
- Home/Away Over 1.5 %
- Home/Away Clean Sheet %
- Home/Away Failed To Score %
- Home/Away Prediction Risk %
- Home/Away xG Avg and Total xG Avg
- FootyStats Goal Signal
- FootyStats Signal Quality

Under percentages are explicitly labelled derived complements, not separate provider fields.

## Governance
- Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance are unchanged.
- FootyStats enrichment is reporting/research only.
- Missing provider fields remain explicit NOT_RETRIEVED_FROM_FOOTYSTATS_SNAPSHOT.
- No bookmaker odds are substituted for missing FootyStats percentages.
- xG remains quarantined for predictive use until point-in-time provenance is proven.
- Goal Signal cannot use ad-hoc thresholds; it must be supported by chronological out-of-sample evidence.
- Existing five-match Team State governance remains unchanged.
- H2H <5 and genuine no-H2H remain non-blocking diagnostics.

## Research priority
The strongest goal-market candidates to test first are:
1. FootyStats pre-match BTTS %
2. FootyStats pre-match Over 1.5/2.5/3.5/4.5 %
3. FootyStats pre-match average goals
4. Team BTTS / Over 1.5 / clean-sheet / failed-to-score rates
5. Team PPG and GF/GA
6. FootyStats Prediction Risk
7. FootyStats xG for/against, only where temporal provenance is admissible
8. Convergence signals combining the above, only after walk-forward validation

Required validation: chronological out-of-sample Brier, log loss, AUC, calibration/ECE, probability-band hit rate, coverage, league stability and incremental value versus existing Oracle/research baselines.

## Current critical Oracle blocker
The latest successful prospective cycle identified 30 NO_BET rows whose diagnostic view has >=5 qualifying current pre-match observations on both sides. The next Oracle action remains exact state-key/league-namespace/state_asof/admission reconciliation for those 30 rows. The FootyStats extension must not bypass that admission gate.

## Next action
Generate the next governed Market Intelligence workbook using the updated schema and dictionary, then inspect actual FootyStats field population. Use the dedicated recalibration lane to rank the FootyStats signals before any production consideration.

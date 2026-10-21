# Project Oracle — season feature coverage matrix (research only)

Date: 2026-10-21  
Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39611213310  
Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39611213310/artifacts/12350840759  
Commit: 2b93e67b5a929db0fb00ca81e6d62c761939c418

## Result

The research-only coverage matrix completed successfully for all 126 archive season folders and 35,819 match rows. The same workflow rebuilt the feature table, ran the integrity audit, reconstructed provisional standings, and generated the provisional competition crosswalk.

- 35,819 match rows and 35,819 feature rows.
- 28,491 rows have an accepted settled status and complete score.
- 126 league-folder/season-folder groups included in the coverage matrix.
- 34,083 of 35,819 target rows have both provisional historical table positions (95.2%).
- Six existing parser/score/status unit tests passed.
- Zero archive parse errors, duplicate non-empty fixture IDs, duplicate feature IDs, missing team IDs, or missing team names in the integrity audit.
- No provider API calls were made in this run.

## What the coverage matrix records

The generated `feature_coverage_by_league_season.csv` reports recent-form sample availability (3 and 5 matches), prior H2H availability (at least 1 and 5 meetings), provisional home/away table-position availability, actual-xG field presence, pre-match-labelled xG field presence, and odds-field presence, per season folder.

## Critical interpretation limits

1. These counts measure archive field/sample availability, not guaranteed availability before kickoff.
2. Pre-match xG and odds provenance remain unverified; both are explicitly marked unverified and must not be treated as approved predictive inputs.
3. Provisional standings use conventional 3-1-0 points and simplified tie-breaks. Split phases, deductions, head-to-head tie-breaks, playoffs and other competition-specific formats are not modelled.
4. Provider catalogue crosswalk remains 43 names: 25 candidate matches requiring human review, 0 ambiguous, 18 unmatched. These names include non-league competitions; the intended 44-league universe is not reconciled.
5. The archive and matrix do not provide Oracle prediction accuracy. Prediction performance requires immutable timestamped Oracle predictions joined to verified settlements.

## Governance

Research only. Production eligibility is NOT_GRANTED. No production model logic, weights, probabilities, thresholds, calibration, model version, or canonical league registry was changed.

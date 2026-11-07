# H2H Reporting Run #64 — Accepted Execution Evidence

Date: 2026-11-07
Workflow: Oracle H2H Reporting
Run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/42391142276
Job: 128458844764
Branch: main
Head SHA: 3d0e171a5343f5dd09bb20be7a4510da64142ff3
Manual input: upcoming_fixture_window=15 days

## Finding
Run #64 completed successfully end-to-end. The 15-day fixture window produced 206 fixtures and the H2H reporting/quality gate passed.

## Evidence
- All workflow steps passed, including fixture refresh, historical archive extension, development-only challenger audit, research experiments, fuzzy alias regression tests, H2H report, exact-ID join, artifact upload and quality gates.
- Artifact: oracle-h2h-report-64, artifact ID 13582932762, SHA-256 92ea1e35cb2d743ebf77ea1bde142fd2c92b73491594c98270be7b8628a2e933.
- Historical archive: 75,849 rows, 2018-07-20 through 2026-11-07, 0 days old.
- Fixture count: 206; unique canonical Fixture IDs: 206.
- Exact Fixture ID join: 206/206 (100%); unmatched IDs 0; fuzzy Fixture ID joining false; Oracle probability values modified false; production model logic changed false.
- H2H results: 165 fixtures with at least one historical same-league H2H; 122 fixtures with 5+ meetings; 43 fixtures with 1-4 meetings; 41 fixtures with zero H2H.
- Zero H2H split: 22 NO_VERIFIED_HISTORICAL_H2H and 19 NO_HISTORICAL_H2H; both are non-blocking reporting statuses.
- H2H sample below 5: 84 fixtures (43 with 1-4 meetings and 41 with zero); non-blocking; no market promoted from insufficient sample.
- Audit unresolved identity diagnostic: 22/206 = 10.68%, below the unchanged 20% ceiling. Under the approved non-blocking policy, genuine absence of historical H2H/cross-league-only history must not block Oracle.
- H2H audit status: PASS_WITH_REVIEW_ITEMS. Quality gate failures: none.
- 1UP H2H truth rows available for 38 fixtures.
- Private production model logic/probabilities/calibration/thresholds/governance unchanged.

## Interpretation
The H2H report is operational for a 15-day window and exact-fixture-ID reconciliation is complete. H2H is supporting evidence, not an admission prerequisite. The 10.68% historical diagnostic is retained for investigation only; the 84 low/no-H2H fixtures do not block.

## Remaining programme critical path
1. Immutable prospective pre-match feature snapshot cohort.
2. Prediction-to-snapshot linkage and exact model-engine SHA.
3. Point-in-time xG provenance.
4. Timestamped odds provenance.
5. Verified prediction-to-settlement chain.
6. Prospective evidence sample/freshness gates.
7. 50-league OMI / Visual Intelligence release readiness.
8. Production eligibility remains false until all production evidence gates pass.

## Actions-minute control
Run #64 executed in public oracle-validation-learning. The private Oracle source was checked out read-only as input, but no private production workflow was invoked. Continue using public workflows for research/validation; reserve private Actions for necessary controlled production evidence only.
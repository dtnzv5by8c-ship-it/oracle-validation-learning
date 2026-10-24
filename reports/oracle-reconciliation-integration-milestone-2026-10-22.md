# Research Reconciliation Contract — Integration Milestone

Date: 2026-10-22
Scope: public research repository only
Status: synthetic contract and CLI tests pass in GitHub Actions; no live Oracle outputs have been reconciled through this CLI yet.

## Verified in CI
- The research contract test job compiles the reconciliation CLI and runs the failure-isolation and reconciliation test suites.
- Test cases cover expected fixture/market matrices, missing and unexpected fixtures, duplicate fixture/market rows, invalid probability bounds, empty expected schedules, missing-state skips, isolated league failures, and global preflight failures.
- The latest verified CI run at this milestone is Run #46 (success) on commit fbb777a5a1377b2e81e567b07eb7e1ccb86a663b.

## Current limit
These tests use synthetic CSV data. They prove the research validator behaves as specified for those cases; they do not prove the production predictor can be called per league, nor that real Oracle outputs pass reconciliation.

## Next validation step
Run the reconciliation CLI against an actual, immutable output artifact from a successful Oracle completion run and the exact schedule used by that run. Keep the output research-only. Do not run the live predictor again solely for this test.

The invocation must use the exact observed CSV paths and column names from that artifact; do not guess them. Expected market names must be the exact 22 governed selections:
BTTS_YES, BTTS_NO, HOME_1X, AWAY_X2, HOME_12, OVER_1_5, OVER_2_5, OVER_3_5, UNDER_1_5, UNDER_2_5, UNDER_3_5, UNDER_4_5, HOME_O05, HOME_O15, AWAY_O05, AWAY_O15, HOME_1X_O15, AWAY_X2_O15, HOME_1X_U45, AWAY_X2_U45, M1UP_HOME, M1UP_AWAY.

Required evidence:
1. The schedule and prediction files are from the same run and fixture window.
2. Fixture IDs map consistently; if IDs differ, use a documented research crosswalk and report unresolved joins, never silently guess.
3. All expected fixture IDs and all 22 market rows per fixture are accounted for.
4. Duplicate rows, unexpected fixture IDs, invalid probabilities, missing probabilities, stale outputs, and skipped fixtures are surfaced.
5. The reconciliation report records the source run ID/commit, source artifact names, fixture counts, market counts, missing/extra rows and status.
6. No probabilities are recalculated and no model/selection logic is changed.

## Runner isolation integration
Actual per-league runner integration remains blocked until the governed runner's supported invocation/input/output contract can be inspected. Do not invent CLI flags or modify production logic to simulate integration. Keep PR #20 draft and unmerged.

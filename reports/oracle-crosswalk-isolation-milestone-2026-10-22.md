# Oracle Crosswalk and Failure-Isolation Milestone
Date: 2026-10-22. Research-only. No production model logic, probabilities, calibration, thresholds or provider API usage changed.

## Expanded crosswalk
The Run #107 schedule has 244 fixtures across 27 configured league codes. The local FootyStats archive was reconciled to all league codes/competition folders and joined on competition, UTC calendar date and normalized home/away names.

- 104 unique archive fixture joins by competition folder + date + normalized home/away identity (archive match rows are marked incomplete, so these are identity joins only, not completed-result evidence).
- 15 additional rows have unique home and away team IDs in the same competition archive and pass the date-only base identity gate, but have no exact archive fixture row.
- 125 fixture identities remain unresolved because one or both team identities could not be established uniquely.
- 0 ambiguous rows were promoted.
- The archive-folder crosswalk covers the configured league codes; that does not imply fixture coverage or live readiness.

119/244 have research-level identity evidence. This is not production eligibility and must not be interpreted as 119 approved live fixtures. The local workbook/CSV contain row-level evidence and unresolved cases.

## Date-only gate
Date + competition + home/away identity is allowed for a base join when the downstream feature does not depend on within-day ordering. Missing kickoff must still block time-dependent calculations (time-to-kickoff, match chronology, same-day ordering). No model feature or probability was changed.

## Failure isolation contract tests
The local test suite `scripts/test_oracle_league_failure_isolation.py` passed 7/7 tests: missing prematch state, simulated runtime failure, unaffected fixture continuation, explicit exclusion statuses, date-only base identity allowed, missing kickoff blocks ordering-dependent features, and ambiguous identity blocks all joins. These are deterministic contract tests, not a live GitHub Actions acceptance run.

## Live workflow finding
At inspected public commit `f86eaf2586e2d2dc7df73de773a0214116f231bb`, `.github/workflows/oracle-completion-run.yml` uses one `completion` job with sequential steps and `set -euo pipefail` in key stages. This does not yet establish league-scoped failure isolation. The next implementation must process each league or fixture batch independently, record `PREDICTED`, `SKIPPED_DATA_GAP`, `FAILED_SOURCE`, or `FAILED_PROCESSING`, continue unaffected work, and retain global blockers for integrity, provenance and stale-data failures. Do not apply `continue-on-error` indiscriminately to hide systemic failures.

## Controlled completion check
Not dispatched in this milestone: the available GitHub connector exposes inspection and rerun actions but no workflow-dispatch action. No old run was rerun as a substitute. Run #107 remains the last inspected completion evidence: reconciliation partial, 234/244 eligible, 10 excluded for missing prematch state, production promotion blocked.

## Governance / next gate
- Keep the 125 unresolved identities out of identity-dependent joins.
- Keep the 15 team-ID/date-gate rows distinct from exact fixture joins.
- Preserve the governed 27-league scope; additional leagues remain research/onboarding only.
- Production hit rate remains data-gated until immutable production prediction records can be joined to verified final results.
- Next: implement league-scoped orchestration in the public research runner, test it end-to-end, then dispatch one controlled completion check and inspect per-league outputs.

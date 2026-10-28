# Selected-50 Snapshot Invalid-Score Quarantine — 2026-10-28 16:22 SAST

## Decision

**Research-only audit defect corrected; targeted local guard validation PASS (6/6). Full GitHub Actions validation of the committed audit suite is not yet verified.** Production and betting release remain NOT_GRANTED.

## Evidence reviewed first

- Canonical handover: `PROJECT_ORACLE_CANONICAL_HANDOVER.md`, sections 54–60.
- Latest detailed runtime audit available in the branch: `reports/oracle-selected50-runtime-audit-2026-10-28-1118-sast.md` (baseline Runtime #147).
- Latest feature blocker report: `reports/oracle-selected50-feature-blocker-diagnostic-2026-10-28-1523-sast.md`.
- Latest snapshot/runtime coverage report: `reports/oracle-selected50-snapshot-runtime-coverage-2026-10-28.md`.
- Branch head before this change: `33e1e6d86ba0eea687a2aea4d2935b374f35d47e`.

## Defect and correction

`scripts/audit_selected50_snapshot_runtime_coverage.py` previously accepted any finite non-negative numeric score, including fractional values and Python booleans. Because the audit uses score validity to determine whether a completed-status row is a settled historical fixture, this could falsely exclude an invalid row as completed.

The parser now accepts only finite, non-negative integer scores. Missing, negative, fractional, non-finite and boolean values are invalid. A row with a completed status but invalid score fields is explicitly emitted as `SNAPSHOT_QUARANTINED` with classification `QUARANTINE_FINISHED_STATUS_INVALID_SCORE`; it is not counted as a valid finished fixture, a snapshot-only upcoming candidate, or settlement truth. Integer-valued decimal strings such as `"1.0"` remain valid, and a genuine 0–0 completed score remains valid.

The summary records the quarantine count and exact source-scoped season/fixture keys. Quarantine does not create canonical joins, predictions, or production eligibility.

## Regression coverage

Five tests were added:
1. Fractional completed score is quarantined.
2. Boolean score is quarantined.
3. Negative score is quarantined.
4. Missing score on completed status is quarantined.
5. Integer-valued decimal score remains valid.

An isolated local guard-level test harness passed **6/6** cases, including preservation of valid 0–0 settlement status. This is targeted validation of the guard logic, not a claim that the full repository test suite has passed.

The identity/settlement workflow push path filter was also corrected to include both the snapshot/runtime audit script and its test file, so subsequent changes to these files trigger the offline workflow.

## Commits and live state

- Script fix: [`da1e8241bc2c8661838d3e7d6f81ff2522ed99fd`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/da1e8241bc2c8661838d3e7d6f81ff2522ed99fd)
- Regression tests: [`9cb02806a43558595ff1595ce097bd124e89612d`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9cb02806a43558595ff1595ce097bd124e89612d)
- CI path filter: [`d453a62c0d8a36a76a7828a12e10f779eb8f8c05`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/d453a62c0d8a36a76a7828a12e10f779eb8f8c05)
- Current branch head at checkpoint: `d453a62c0d8a36a76a7828a12e10f779eb8f8c05`.

The GitHub connector did not expose push-triggered workflow run records for these commits; combined commit status returned no status entries. Therefore no post-change Actions run is claimed.

## Required CI verification

Workflow: [Oracle Identity & Settlement Evidence Tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle_identity_resolver_tests.yml)

- Branch: `research/oracle-50-league-readiness-audit`
- Inputs: none
- Network/provider calls: none
- Private archive access: none
- Secrets: none required

The workflow includes the audit module, tests, and offline identity/settlement checks. Run it to establish full repository CI validation; do not report it as passed until its run logs confirm success.

## Preserved gates

- The latest previously verified runtime baseline remains Run #154; the research runtime/model code is unchanged by this audit-only correction, so no runtime rebuild was needed.
- The 25 feature-blocked fixtures remain blocked under the five-completed-home/away-match contract; no features were imputed.
- Combo target/settlement semantics remain unresolved; both Combo probability columns must remain masked.
- Canonical competition/fixture/team joins and official settlement truth remain unverified.
- No provider API calls, private-repository Actions, production repository writes, or changes to Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers or governance occurred.

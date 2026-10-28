# Project Oracle — Future-status quarantine guard for reporting-horizon assessment

**As of:** 2026-10-28 21:14 SAST  
**Scope:** Blocker 3 only — safe reporting-window assessment beyond seven days.  
**Decision:** Keep prediction generation capped at seven days; preserve per-fixture quarantine, exact identity/kickoff joins, market gates, Combo masking, and research-only release status.

## Evidence reviewed

- Canonical handover, Section 61, and the 14-day reporting-window assessment.
- Saved snapshot run [40734991542](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542), artifact [12835634404](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542/artifacts/12835634404).
- Saved runtime #162, run [40739426287](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287), artifact [12839157410](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287/artifacts/12839157410).
- Existing offline reconciliation files under `oracle_reporting_horizon_assessment/`. No provider API calls or 201-call probe were used.

## Concrete defect and fix

The safe report builder already quarantined missing, suspended/postponed/cancelled/abandoned/void/delayed statuses and rejected unsettled past kickoffs. However, a future kickoff paired with a status in the builder's `FINISHED` set (for example `finished`, `complete`, `ft`, or `played`) could fall through into horizon classification. A row beyond seven days could then be labelled as a clean out-of-runtime-window candidate instead of a source/status quarantine.

The builder now assigns `QUARANTINE_STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF` when a valid kickoff is later than the audit as-of time but the source status is a finished/completed status. This check occurs before horizon classification. The exclusion therefore receives `BLOCKED_SOURCE_QUARANTINE`, remains Combo-masked, emits no prediction, and retains `production_eligible=NO` and `betting_eligible=NO`.

- Code commit: [d919ffcf04b30ba0d3e4ee9b27f7626a4d00f7b0](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/d919ffcf04b30ba0d3e4ee9b27f7626a4d00f7b0)
- Regression-test commit: [4d887601c287666bb1508eed25e4e96da0499048](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/4d887601c287666bb1508eed25e4e96da0499048)

The new regression test covers a future `finished` row inside seven days and a future `complete` row beyond seven days. Both must be quarantined, not counted as ordinary out-of-window fixtures. It asserts the source-quarantine market gate, Combo masking, zero Combo emission, and false production/betting eligibility.

## Validation status

A focused local semantic harness passed five status/kickoff cases: future `finished` and `complete` are quarantined; past `finished` remains historical; future `scheduled` remains a candidate; future `suspended` remains quarantined. This harness validates the intended branch logic only; it is **not** the full repository contract test.

Latest previously verified workflow runs, all predating the new code/test commits:

- Safe Current Fixture Report Contract [run 40748586300](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40748586300): PASS, 6 tests.
- Safety Contract Tests [run 40748586208](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40748586208): PASS, 13 tests.
- Dry-Run Planner [run 40748586267](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40748586267): PASS, all 36 steps; zero network and paid-provider calls.

No successful CI run for commit `4d887601c287666bb1508eed25e4e96da0499048` has been verified. The available connected GitHub tools do not expose workflow dispatch or a complete push-run listing. Do not claim the new regression test or dry-run ran.

## Existing-data assessment (unchanged baseline)

The saved artifact reconciliation reports 2,250 snapshot rows; 863 future rows within fourteen days; 362 clean exact joins within the seven-day runtime horizon; 308 clean candidates on days 8–14; 188 quarantined future rows (179 flagged `no_home_away=1`, nine nonstandard status); 76 of the quarantined rows beyond seven days; and five rows inside the 15-minute minimum-lead cutoff. Among eligible in-window candidates, missing runtime rows, ordered-team-ID mismatches, and exact UTC-kickoff mismatches are all zero.

The saved snapshot contains zero future rows whose status is in the builder's `FINISHED` set. Therefore, the guard is a preventative correction and does not change the saved-artifact counts. These figures remain evidence from the prior artifact, not a regenerated trace under the new code.

**Decision:** Fourteen-day reporting remains assessment-only. Do not generate or publish predictions beyond seven days. Preserve source quarantine before horizon classification, exact selected-season/fixture and ordered-team-ID joins, exact UTC kickoff, the 15-minute lead cutoff, all market gates, and Combo masking. Canonical fixture/team joins and official settlement truth remain unverified; production and betting eligibility remain false.

## Exact manual validation action

Run the offline safe-report contract wrapper:

- Workflow: [Selected-50 Safe Current Fixture Report Contract](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/selected50-safe-current-report-contract.yml)
- Branch: the workflow's default-branch dispatch wrapper checks out `research/oracle-50-league-readiness-audit`.
- Inputs: none.
- Secrets, private archive, provider API credits: not required.

Then run the offline planner wrapper:

- Workflow: [Oracle Selected-50 Dry-Run Planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-dry-run-planner.yml)
- Branch: the wrapper checks out `research/oracle-50-league-readiness-audit`.
- Inputs: none.
- Network/provider calls: zero by contract.

No dispatch was started from this session. Do not run the 201-call probe, trigger provider refresh, modify production logic, or merge to production.

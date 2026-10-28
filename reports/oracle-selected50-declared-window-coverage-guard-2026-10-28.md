# Project Oracle — Declared Snapshot Window Coverage Guard

**Scope:** Blocker 3 only — safe reporting-window expansion beyond seven days.  
**Status:** Research-only code and regression test committed; full post-change CI is not verified.  
**Decision:** Do not claim complete 14-day coverage from a snapshot whose declared window ends before the requested report horizon. Prediction generation remains capped at seven days.

## Evidence reviewed

- Canonical handover and the existing [14-day reporting-window assessment](oracle-selected50-reporting-horizon-assessment-2026-10-28.md).
- Safe report builder and its contract tests on `research/oracle-50-league-readiness-audit`.
- Existing snapshot/runtime assessment: snapshot retrieved `2026-10-28T17:22:27Z`; runtime started `2026-10-28T17:49:57Z`, approximately 27.49 minutes later.
- Snapshot generator `scripts/oracle_selected50_current_fixture_probe.py`: `future_cutoff`/ `window_end_utc` are computed from `now_ts` before the per-league requests; `retrieved_utc` is written after those requests. Thus the declared window end is earlier than retrieval plus 14 days. The existing report end is runtime start plus 14 days, so it necessarily extends beyond this snapshot's declared window by at least the runtime-start/retrieval gap (about 27.5 minutes; exact shortfall requires the raw snapshot JSON).

No new provider API calls or 201-call probe were used.

## Defect and correction

The safe report builder previously enforced snapshot freshness and the rule that the snapshot must predate runtime start, but it did not verify that the snapshot's declared `window_end_utc` covered the entire requested reporting horizon. A snapshot can be fresh and pre-runtime yet still lack coverage for the final portion of a 14-day horizon.

The builder now fails closed for expanded reporting if:
- `window_end_utc` is missing, invalid or timezone-naive;
- the declared window end is not later than snapshot retrieval; or
- the requested report end exceeds the declared snapshot window end.

The QA output now records the declared window end, requested report end, a coverage boolean and an explicit coverage status. No prediction logic, probabilities, thresholds, or generation horizon changed.

- Code commit: [77d40e352a8ef3c64bc51d2cf8d4d95facfb1a4b](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/77d40e352a8ef3c64bc51d2cf8d4d95facfb1a4b)
- Regression commit: [9566436a236a6fd2916c3a6aca12137f5dbe344c](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9566436a236a6fd2916c3a6aca12137f5dbe344c)

The regression suite covers missing `window_end_utc` and a declared window ending one hour before the requested report end. Existing synthetic expanded-horizon fixtures were updated to declare their coverage end.

## Existing-data reconciliation

The previously saved assessment still records 2,250 snapshot rows; 863 future rows in the requested 14-day period; 362 clean exact joins in the runtime generation window; 308 clean candidates beyond the seven-day generation window; 188 quarantined future rows, including 76 beyond seven days; and five minimum-lead exclusions. The existing CSV independently passes checks that quarantined rows remain source-blocked, all Combo values remain masked/zero, out-of-runtime candidates retain the non-missing-join gate, and no predictions or production/betting eligibility are emitted.

Those counts describe the rows present in the retained snapshot. They do **not** prove complete coverage through runtime-start + 14 days. The new guard intentionally prevents the full-horizon report from being emitted when declared snapshot coverage ends early.

## Validation status

- The code and test commits were fetched back from GitHub and their diffs reviewed.
- The combined commit-status endpoint returned no status entries, and the connected GitHub tools do not expose workflow dispatch or complete push-run enumeration. Therefore, the new contract suite and dry-run planner are **not verified as passed**.
- Existing earlier safe-report and dry-run runs are baseline evidence only; they predate these commits.

### Exact manual validation

1. [Selected-50 Safe Current Fixture Report Contract](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/selected50-safe-current-report-contract.yml)  
   Branch: `research/oracle-50-league-readiness-audit`; inputs: none; no secrets, provider calls or private archive access.
2. [Oracle Selected-50 Dry-Run Planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-dry-run-planner.yml)  
   Branch: `research/oracle-50-league-readiness-audit`; inputs: none; the workflow contract requires zero network and paid-provider calls.

## Decision and next safe action

- Keep prediction generation at seven days.
- Preserve exact selected-season/fixture identity, ordered team IDs, UTC kickoff, minimum-lead, per-fixture quarantine, all market gates and Combo masking.
- Verify the two offline workflows. To use the existing snapshot for a safe assessment without provider refresh, request a shorter horizon whose report end is no later than its declared `window_end_utc`; do not label it a complete 14-day assessment.
- A full 14-day assessment requires a snapshot whose declared window actually covers the requested end. Obtaining a new snapshot would require provider requests, so it was not done under this task's constraints.

Production and betting eligibility remain `NO`. No private Actions, production writes or merges occurred. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.

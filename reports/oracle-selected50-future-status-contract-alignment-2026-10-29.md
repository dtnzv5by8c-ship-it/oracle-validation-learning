# Project Oracle — Future-Status Quarantine Contract Alignment

**Scope:** Blocker 3 only — reporting horizon and per-fixture quarantine.  
**Status:** Research-only guard and regression committed; GitHub Actions execution for these latest commits is not yet verified.

## Evidence

The live research branch contains two different future-status policies:

- `scripts/overlay_selected50_current_snapshot.py` uses `future_status_quarantine_reason`: only the provider-documented `incomplete` status is eligible for a future fixture. `complete` conflicts with a future kickoff; `suspended`, `canceled`, missing and unknown statuses are quarantined.
- `scripts/build_selected50_safe_current_fixture_report.py` already quarantined missing, suspended/canceled, and future-completed statuses, but did not quarantine an unknown future status such as `scheduled`. Such a row could be classified as a clean out-of-runtime-window fixture even though the overlay rejects it.

The retained snapshot's actual status distribution is `incomplete=858`, `complete=1,374`, `suspended=18`; it contains no unknown status values. Therefore the new guard is preventative and does not change the current snapshot's fixture counts.

## Research-only correction

Commit [`65a66f83c0aa403bb4c572d08e63062be1adb653`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/65a66f83c0aa403bb4c572d08e63062be1adb653) adds `QUARANTINE_UNKNOWN_OR_UNSUPPORTED_FUTURE_STATUS` before horizon classification whenever a future fixture's status is not `incomplete` and has not already received a more specific quarantine reason.

Regression commit [`b11037c6c5285ab69ac6ce745f9c31059268a66e`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/b11037c6c5285ab69ac6ce745f9c31059268a66e) updates synthetic eligible fixtures to use the documented `incomplete` status and adds a future `scheduled` fixture that must remain quarantined with Combo masked and production/betting eligibility `NO`.

## Validation

- A local five-case semantic harness passed for `incomplete`, unknown `scheduled`, future `complete`, `suspended`, and missing status.
- The current snapshot was rechecked and has no unknown status values; the existing 13-day/14-day boundary result is unchanged.
- The repository contract suite and dry-run planner have **not** been verified for these latest commits. The GitHub combined-status endpoint returned no status entries, and the connected interface does not expose workflow dispatch or complete push-run enumeration.

Manual offline workflows, branch `research/oracle-50-league-readiness-audit`, no inputs:
- [Safe Current Fixture Report Contract](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/selected50-safe-current-report-contract.yml)
- [Selected-50 Dry-Run Planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-dry-run-planner.yml)

## Release decision

No current artifact rows changed from this guard because no unknown statuses exist in the retained snapshot. The existing 13-day report-only assessment remains within the declared snapshot window; a full 14-day report remains blocked by the 20,689-second end-boundary shortfall at the recorded as-of time. The runtime generation horizon remains seven days.

Per-fixture quarantine, exact identity and kickoff joins, feature-support gates, market gates and Combo masking remain fail-closed. Canonical fixture/team joins and official settlement truth remain unverified. Production and betting eligibility remain `NO`.

No provider API calls, 201-call probe, private Actions, production writes or production merges occurred. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.

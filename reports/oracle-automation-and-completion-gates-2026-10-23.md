# Project Oracle — Expedite Completion Gate Update
Date: 2026-10-23
Scope: public research repository only. Production logic, protected registry, probabilities, weights, thresholds, and calibration unchanged.

## Live-run verification
Run #27 (GitHub Actions run 40015176531) is completed/successful. The completion job's listed steps succeeded, and two artifacts were uploaded: `oracle-fixture-level-predictions` and `oracle-sanitized-completion-report`. The artifact digest and expiry are available in the GitHub run's artifact metadata. This verifies execution and artifact delivery for this run only; it does not prove full 44-league coverage, production accuracy, or reliable future scheduling.

## Automation findings
- The main `.github/workflows/oracle-completion-run.yml` on `main` declares a weekly Monday schedule at 04:00 UTC (06:00 SAST) and manual dispatch.
- The inspected workflow explicitly defaults scheduled runs to a seven-day fixture horizon and fails if `OPENFOOT_API_KEY` is missing rather than using a demo-key fallback.
- Current-result refresh has a freshness gate; the live prediction step can fail while subsequent reconciliation/report steps still run with `if: always()`. Therefore the overall Actions run can be successful while the live prediction result is blocked or partial; downstream reporting must inspect stage outcomes, not just the green workflow badge.
- The inspected main completion workflow uploads sanitized diagnostics and fixture-level artifacts with `if: always()`, but has no explicit email/chat notification step. Notification delivery is not verified.
- The research recovery replay has push/manual triggers; it is not itself a scheduled autonomous refresh workflow.

## Completion disposition
| Gate | Status | Evidence needed to close |
|---|---|---|
| 44 target leagues vs 27-code registry | OPEN | Verified target-to-provider competition ID crosswalk for all 44, with explicit unsupported/unavailable status; reconcile extra governed codes separately |
| ZA/RSA | OPEN | Confirm same South African competition by provider ID, season and fixture/team identities; until then alias remains proposed only |
| Recent form/H2H | OPEN | Reconcile by stable IDs; audit unmatched/ambiguous rows; leave unresolved features null |
| League positions | OPEN | Historical as-of standings reconstructed from completed results before each kickoff, with season/rules provenance and independent spot checks |
| Prediction-to-settlement accuracy | OPEN | Immutable predictions keyed by fixture, market, timestamp and version joined to authoritative settled outcomes, with void/postponed handling |
| Scheduled refresh | PARTIAL | Observe a scheduled run, verify stage outcomes, current-source freshness and expected artifacts; a cron declaration is not sufficient |
| Failure alerts | OPEN | Add and test a failure notification route; capture run link, failing stage, freshness status, avoid secrets/raw provider payloads |
| Production promotion | BLOCKED | All gates pass, review evidence, and explicit owner approval |

## Non-negotiable handling
Do not backfill unsupported leagues with fabricated fixtures/probabilities. Do not turn a candidate team alias into an approved join without identity evidence. Do not report production accuracy from current/live predictions or from unpaired historical results. Keep PR #20 draft and unmerged pending owner approval.

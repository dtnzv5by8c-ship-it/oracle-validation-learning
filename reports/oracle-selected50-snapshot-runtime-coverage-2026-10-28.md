# Snapshot-to-Runtime Coverage Reconciliation — 2026-10-28

## Evidence

- Existing FootyStats snapshot artifact [#12796425175](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796425175), SHA-256 dafffac19952d1ca0705d9100f641b1bb273b30cedebbdddc0d90fd1bfced5c0.
- Runtime artifact [#12816016919 from Run #154](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715830/artifacts/12816016919), SHA-256 b7fb063b5d5f6b1e41b10930114468497fdd04cd2881bd56dd2e8ddb8e5bdb66.
- Runtime start used for comparison: 2026-10-28T12:25:49Z, from the existing workflow log.
- Snapshot retrieved at 2026-10-28T06:11:51.985177Z; age at runtime start 373.95 minutes.
- Comparison mirrors the runtime's strict >15-minute lead time, <=7-day horizon, completed-score predicate, and cancelled/postponed status exclusions. Keys are exact provider-native selected-season ID + fixture ID.

## Results

| Measure | Result |
|---|---:|
| Snapshot candidates in the runtime window | 473 |
| Runtime fixture rows | 463 |
| Exact season-ID + fixture-ID matches | 461 |
| Snapshot-only rows | 12 |
| Snapshot-only rows with no_home_away=1 | 9 |
| Snapshot-only rows with no_home_away=0 | 3 |
| Snapshot-only rows with unknown flag | 0 |
| Runtime-only rows | 2 |

The three snapshot-only rows with no_home_away=0 and status incomplete are:

- Serbia SuperLiga, Radnički Kragujevac–Železničar Pančevo, ID 8551578, kickoff 2026-10-28 14:00 UTC, selected season 17119.
- Serbia SuperLiga, Radnički Niš–Partizan, ID 8551579, kickoff 2026-10-28 16:00 UTC, selected season 17119.
- Chile Primera División, Universidad Católica–Audax Italiano, ID 8432254, kickoff 2026-10-28 23:30 UTC, selected season 16615.

The nine rows with no_home_away=1 remain separate review candidates; the flag is preserved rather than used to auto-exclude them. Two runtime-only rows are Sportivo Ameliano–Olimpia (Paraguay, ID 8581506) and Universitario–Sport Boys (Peru, ID 8578334). They must not be automatically removed on the basis of one snapshot.

## Interpretation

The saved snapshot and runtime output disagree on 14 fixture keys (12 snapshot-only and 2 runtime-only). The three no_home_away=0 snapshot-only fixtures are absent from the runtime report despite satisfying the declared time/status window. The runtime builder currently derives its candidate list from the private archive; it does not ingest the saved snapshot or the standalone adapter output. This confirms an integration/source-boundary gap, but the exact cause within the private archive or an earlier parse/filter step remains unverified because row-level archive-input trace is not in the artifact.

No prediction was created for the three missing fixtures, no source row was canonical-joined, and no settlement truth was inferred. The saved snapshot was already 6.23 hours old at the runtime start and is not a current slate now. A fresh provider request is outside this task; do not use this snapshot to release predictions.

## Safety and tests

- New offline script: scripts/audit_selected50_snapshot_runtime_coverage.py
- New tests: tests/test_selected50_snapshot_runtime_coverage.py
- Local tests: 13/13 passed.
- Generated diff CSV SHA-256: 22195107d8c303d5b15e18b6e1d706a5216764b577bdf783ef05bdf97ccb476b
- Generated summary JSON SHA-256: 3e656e367ea95ec197835cca6822c5d8a083770230ccb44abe61ecb332639faa
- Combo probability columns remained blank; the script refuses a nonblank Combo field.
- No provider API calls, no canonical joins, no production writes, no model/probability changes.
- GitHub Actions validation completed: identity/settlement Run #13 (40699110792) passed all 13 coverage tests; Safety Run #235 (40699110635) and Dry-Run #533 (40699110621) passed. The comparison remains research-only and does not grant production or betting eligibility.

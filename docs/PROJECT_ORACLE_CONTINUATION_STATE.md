# PROJECT ORACLE — CANONICAL CONTINUATION STATE

Last updated: 2026-11-07 — 80 HTTP-417 quarantine population mapped
Governed branch: `research/oracle-50-league-readiness-audit`

## Current objective
Clear the remaining 50-league validation and release gates and reach governed production prediction readiness without changing Oracle V1.6 production logic.

## Acquisition control-plane
- Universe: 50 leagues
- Provider-season partitions: 182
- Governed endpoint tasks: 728
- Current acquisition accounting: 648 completed + 80 HTTP-417 quarantined/provider-blocked + 0 pending = 728
- Exhausted private ingestion run #92 must NOT be rerun merely because it exited red; its terminal no-pending condition is implemented as an error.

## Major milestone 1 — FootyStats receipt/manifest/task reconciliation
Private FootyStats batch `42255401046`:
- 8,367 rows received
- 100 provider requests
- provider-recorded manifest blob/ref: `57fe9e1184b5035327feaa78307750e129c54bf3`
- manifest file SHA-256: `58bd06ed9c5a6a09ed55eb833319ca09cd4f01e2b175e4ca9127a1b3a7f689d7`
- 100 explicit completed task IDs

Deterministic reconciliation:
- The provider workflow's historical manifest URL at ref `57fe9e...` resolves to actual GitHub blob SHA `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`.
- Historical and current manifest contents are exactly identical (116,108 bytes).
- Current governed manifest contains 728 tasks.
- Receipt task IDs matched: 100/100.
- Missing task IDs: 0.

Admission: the 100-task receipt is admissible private evidence for its exact tasks and is a subset of the 728-task plan. Do not double-count it or treat it as proof of all 728 tasks.

Checkpoint:
`docs/checkpoints/2026-11-07-footystats-manifest-task-reconciliation-final.md`
Commit: `dc92fce87d8b4761242ac0994f023116c01b47e9`

## Major milestone 2 — 80 HTTP-417 quarantine population mapped
The 80 quarantined tasks are exactly 20 provider-season partitions × 4 endpoints.

Provider-season families:
- Finland Veikkausliiga: 2024, 2025, 2026
- India Indian Super League: 2023/2024, 2024/2025, 2025/2026, 2026/2027
- Republic of Ireland Premier Division: 2024, 2025, 2026
- Russia Russian Premier League: 2023/2024, 2024/2025, 2025/2026, 2026/2027
- South Korea K League 1: 2024, 2025, 2026
- Venezuela Primera División: 2024, 2025, 2026

Endpoints in each partition:
`league-matches`, `league-teams`, `league-tables`, `league-season`.

Root classification is exact: the private workflow records `BLOCKED_PROVIDER_417` after its controlled request variants receive HTTP 417. No fuzzy matching or silent league reassignment was used.

Checkpoint:
`docs/checkpoints/2026-11-07-80-http417-quarantine-root-cause-mapped.md`
Commit: `13bd99cb613ba8da3e6c490e597313fd32a9a6dc`

## Current validated research/readiness evidence
- Successful Selected-50 Market Intelligence repair #360 is a valid downstream research baseline.
- 717 runtime fixtures had exact archive joins in that artifact.
- xG numeric values are present but point-in-time capture timestamps are not verified.
- Actual-result register is not an admissible production settlement ledger.
- Canonical production settlement ledger remains header-only.
- 210 challenger shadow market rows across 42 fixtures are research-only.
- Chronological expanding-window research backtests exist, but are not production performance.
- Current production/betting eligibility remains false.

## Immediate next work
1. Reconcile evidence supporting the 648 completed-task population.
2. Determine whether the approved private FootyStats gateway can recover the exact 20 quarantined provider-season partitions without repeating completed tasks or exceeding request budget.
3. Validate identity, pagination completeness, chronology and freshness for admissible completed evidence.
4. Close point-in-time xG and odds provenance where possible.
5. Build immutable prediction → fixture → pre-kickoff feature snapshot → verified settlement linkage.
6. Advance OMI/release readiness from the resulting evidence.
7. If a new provider workflow is genuinely required, ask Nolan to run it; otherwise remain autonomous.

## Do not repeat
- Do not rerun ingestion #92 as a generic full-universe run.
- Do not rerun the disabled protected-repository audit.
- Do not rerun the completed Selected-50 Market Intelligence repair baseline.
- Do not reacquire batch 42255401046.
- Do not create another reconciliation loop for the resolved manifest issue.
- Do not reinterpret research/shadow metrics as production accuracy.
- Do not change Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility or governance.

## Coordination
- Validation lane owns 50-league data/readiness reconciliation.
- Evidence lane owns prediction/settlement linkage and leakage-safe backtesting.
- OMI lane owns consolidated OMI/Visual Intelligence/release reporting.
- Each lane must read this file and the lessons register before acting, inspect live HEAD before writes, reconcile intervening commits, and create a dated checkpoint after every major milestone.

## Definition of done
Production prediction readiness requires genuinely satisfied identity, chronology, point-in-time feature provenance, prediction/settlement linkage and required market/league gates. Missing or quarantined evidence remains excluded. Fail-closed remains active until gates pass.

# PROJECT ORACLE — CANONICAL CONTINUATION STATE

Last updated: 2026-11-07 — FootyStats receipt/manifest/task reconciliation completed
Governed branch: `research/oracle-50-league-readiness-audit`

## Current objective
Clear the remaining 50-league validation and release gates and reach governed production prediction readiness without changing Oracle V1.6 production logic.

## Acquisition control-plane
- Universe: 50 leagues
- Provider-season partitions: 182
- Governed endpoint tasks: 728
- Current acquisition accounting: 648 completed + 80 HTTP-417 quarantined/provider-blocked + 0 pending = 728
- Exhausted private ingestion run #92 must NOT be rerun merely because it exited red; its terminal no-pending condition is implemented as an error.

## MAJOR MILESTONE — FootyStats receipt/manifest/task reconciliation
Private FootyStats batch `42255401046`:
- 8,367 rows received
- 100 provider requests
- provider-recorded manifest blob/ref: `57fe9e1184b5035327feaa78307750e129c54bf3`
- manifest file SHA-256: `58bd06ed9c5a6a09ed55eb833319ca09cd4f01e2b175e4ca9127a1b3a7f689d7`
- 100 explicit completed task IDs

Deterministic reconciliation:
- The provider workflow's historical manifest URL at ref `57fe9e...` resolves to the same actual GitHub blob SHA as the current governed manifest: `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`.
- Historical and current manifest contents are exactly identical (116,108 bytes).
- Current governed manifest contains 728 tasks.
- Receipt contains 100 task IDs.
- Matched task IDs: 100/100.
- Missing task IDs: 0.

Therefore the earlier manifest-hash concern is resolved: it was a provider workflow ref/version-label distinction, not a manifest-content mismatch.

**Admission:** the 100-task receipt is admissible private evidence for its exact tasks and is a subset of the 728-task plan. Do not double-count it and do not treat it as proof of all 728 tasks.

Checkpoint:
`docs/checkpoints/2026-11-07-footystats-manifest-task-reconciliation-final.md`
Commit:
`dc92fce87d8b4761242ac0994f023116c01b47e9`

## Current validated research/readiness evidence
- Successful Selected-50 Market Intelligence repair #360 is a valid downstream research baseline.
- 717 runtime fixtures had exact archive joins in that artifact.
- xG numeric values are present but point-in-time capture timestamps are not verified.
- Actual-result register is not an admissible production settlement ledger.
- Canonical production settlement ledger remains header-only.
- 210 challenger shadow market rows across 42 fixtures are research-only.
- Chronological expanding-window research backtests exist, but are not production performance.
- Current production/betting eligibility remains false.

## Immediate next work — do not restart old work
1. Reconcile the evidence supporting the 648 completed-task population.
2. Enumerate/root-cause the 80 HTTP-417 quarantined tasks.
3. Validate identity, pagination completeness, chronology and freshness for admissible completed evidence.
4. Close point-in-time xG and odds provenance where possible.
5. Build immutable prediction → fixture → pre-kickoff feature snapshot → verified settlement linkage.
6. Advance OMI/release readiness from the resulting evidence.
7. Use the approved private FootyStats gateway only if a documented evidence gap remains after reconciliation; never use public provider transport from the validation/reporting repo.

## Do not repeat
- Do not rerun ingestion #92.
- Do not rerun the disabled protected-repository audit.
- Do not rerun the completed Selected-50 Market Intelligence repair baseline.
- Do not reacquire the already-reconciled 100-task receipt.
- Do not reinterpret research/shadow metrics as production accuracy.
- Do not change Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility or governance.

## Coordination
- Validation lane owns 50-league data/readiness reconciliation.
- Evidence lane owns prediction/settlement linkage and leakage-safe backtesting.
- OMI lane owns consolidated OMI/Visual Intelligence/release reporting.
- Each lane must read this file and the lessons register before acting, inspect live HEAD before writes, reconcile intervening commits, and create a dated checkpoint after every major milestone.

## Definition of done
Production prediction readiness requires genuinely satisfied identity, chronology, point-in-time feature provenance, prediction/settlement linkage and required market/league gates. Missing or quarantined evidence remains excluded. Fail-closed remains active until gates pass.

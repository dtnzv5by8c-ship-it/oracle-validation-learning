# Master OMI MI Root-Cause Cycle — 2026-11-27 04:57 SAST

## Release decision
FAIL-CLOSED. No release workbook certified.

## Fresh rolling spine evidence
- Governed leagues: 50
- Rolling fixture rows: 392
- Unique provider fixture IDs: 392
- Generated UTC: 2026-11-27T01:44:18.279672Z
- Window: 2026-11-27 through 2026-12-04
- Pre-match only: true
- Fuzzy matching: false
- Historical fallback: false
- Production model logic changed: false
- A:ET changed: false
- Last-5 fully verified fixtures: 391

## Current reconciliation evidence
- Generated UTC: 2026-11-27T01:32:23.322258Z
- Source generated UTC: 2026-11-27T01:32:13.080335Z
- Governed rows: 392
- Exact matches: 392
- Unmatched: 0
- Coverage: 100%
- Status: CURRENT
- Source errors: 0

## Root-cause matrix

| Scope | Cause | Authoritative evidence | Fix / regression control | Status |
|---|---|---|---|---|
| Weekly fixture spine | Rolling spine must be the sole current fixture authority | data/fixtures/governed_50league_current_manifest.json | Freshly rebuild each cycle; exact provider fixture IDs; no frozen spine admission | FIXED / FRESH |
| Fixture identity | Prior reconciliation path could read an obsolete competing spine | data/current_reconciliation_status.json and live 392-row spine | Reconcile exact provider fixture ID against the live rolling spine; fail closed on drift | FIXED / 392 of 392 |
| Current Team State | Durable current Team State is a downstream mandatory dependency | Latest QA: current Team State must be independently reconciled to all 392 fixtures | Fresh current-data workflow execution triggered; persistence validates non-empty rows, manifest parity, SHA-256 and remote persistence | IN PROGRESS |
| Prediction ledger | Authoritative current ledger is not present on public main | Latest QA and repository search | Do not fabricate/substitute; current-data/prediction workflow must publish authoritative ledger before MI admission | BLOCKER |
| MI schema | Provider artifact is 139 columns while canonical contract is 264 | Latest QA | Assemble only through canonical mapping; missing mandatory inputs must be explicitly UNAVAILABLE/UNVERIFIED | BLOCKER |
| PIT xG | xG requires capture-time provenance | Canonical QA contract | Admit only timestamped pre-kickoff evidence; otherwise UNVERIFIED | BLOCKER UNTIL AUDIT |
| A:ET | Protected workbook boundary | V2.1.1 baseline SHA and prior QA | No insert/delete/move/rename/rewrite; binary certification required | PROTECTED |
| Oracle V1.6 | Production model logic must remain unchanged | Latest manifest + QA | No threshold, probability, calibration or eligibility changes | PROTECTED |
| Persistence | Current state previously risked remaining on run-specific branch | prior remediation evidence + current workflow | Direct-to-main validated persistence with post-push size/hash/row verification | FIXED IN CODE; EXECUTION IN PROGRESS |
| Workflow dependency | Current-state refresh must execute after rolling spine refresh | workflow contract | Push trigger + hourly schedule; fresh execution explicitly retriggered this cycle | FIXED / EXECUTING |
| QA | Green workflow is not equivalent to release readiness | QA contract | Independent 100% cell/type/provenance/chronology/leakage gate remains mandatory | BLOCKED |

## Mandatory release gates
1. Fresh rolling 50-league spine: PASS.
2. Exact fixture identity/reconciliation: PASS at 392/392.
3. Current Team State: pending independent persistence/reconciliation.
4. Current prediction ledger: blocker until authoritative current ledger is present.
5. Canonical 264-column MI: blocker until assembled.
6. Mandatory blank classification: blocker until every field is populated or explicitly unavailable/unverified with reason/provenance.
7. Cell-level type/provenance/PIT/chronology/leakage audit: pending.
8. Native XLSX/XML/A:ET/hash certification: pending.
9. Independent final gate: pending; release remains FAIL-CLOSED.

## Safety
No stale or dated frozen weekly spine, fuzzy matching, estimates, guesses, missing-to-zero conversion, historical substitution, timezone normalization, post-kickoff leakage, unsupported provider substitution, Oracle V1.6 change, or A:ET mutation is permitted.

# Master OMI Formula Input Release Gate — Run 11 Final Audit

Date: 2026-11-21
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Canonical baseline: Master OMI V2.1.1
Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Production model: Oracle V1.6 unchanged

## Release decision

**FAIL-CLOSED / NOT RELEASE-ELIGIBLE**

No governed fixture is formula-ready or backtest-ready in this audit state.

## Structural gates

- Market Intelligence: 755 rows x 264 columns (A:ET)
- Governed heading definitions/comments: 264/264 present
- A:ET immutable contract: no insertion/reorder/rename or nonblank value mutation accepted
- Persisted canonical baseline comparison: 0 nonblank A:ET value differences
- Known legacy duplicate headings inside immutable A:ET: H2H Avg Total Goals; Historical Accuracy Status; A+ Setup Status. These are retained because removing/reordering them would violate the immutable contract.
- Fixture identity rows: 387
- FootyStats identity: exact fixture-ID joins only; no fuzzy matching admitted

## Per-fixture Formula Input QA

- FORMULA_INPUT_STATUS=READY: 0/387
- FORMULA_INPUT_STATUS=BLOCKED: 387/387
- BACKTEST_READY=YES: 0/387
- RELEASE_DECISION=PASS: 0/387
- RELEASE_DECISION=FAIL: 387/387
- Forbidden PASS + blocker combinations: 0
- Required MI coverage at 100%: 218/387
- Required MI coverage below 100%: 169/387
- Independently verified actuals: 31/387
- Kickoff/date reconciliation failures: 38/387
- Implausible goal-environment fixtures: 24/387
- xG point-in-time capture timestamps verified: 0/754

## Mandatory controls

Exact FootyStats identity, Last-3/Last-5 chronology, GF/M and GA/M status, venue metrics, LTSS/team-strength status and pre-match leakage controls are retained as governed QA gates. Missing/unavailable evidence remains UNAVAILABLE/UNVERIFIED and is never converted to zero or an estimate.

The immutable A:ET workbook contains some genuine text states such as INSUFFICIENT_DATA and NOT_AVAILABLE_FROM_ORACLE_OUTPUT; these are not converted to numeric zero. Schema-defined numeric fields must remain native Excel numeric cells when populated. Any required numeric-looking text remains a release blocker rather than being silently coerced in A:ET.

Implausible goal-environment values include league-average total-goal values such as 33.9185 and 19.5668. These remain UNAVAILABLE/UNVERIFIED. No divide-by-10, rescaling, estimation or guessed repair was performed.

xG remains quarantined because point-in-time capture provenance is not independently verified.

## Genuine QA-layer defect corrected this run

371 Formula Input QA rows contained an identity-review note while the Fixture Identity status still read PASS. The permanent gate requires identity review to be represented as a failed/reviewed gate rather than PASS. The QA layer was corrected so those rows now carry Fixture Identity=FAIL. A:ET and Oracle V1.6 were not modified.

## Evidence

Audited workbook SHA-256: d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597
Per-fixture QA manifest SHA-256: e38d5070b951e8b18cd8b31563c4b40db078825af6a5f0e8464e4297b9ef219e

The repaired workbook is fail-closed and is not release-eligible.

## Required next state

Continue hourly checks. Release may only change to PASS after every governed fixture passes schema, immutable A:ET, identity, kickoff/date, chronology, provenance, numeric type/range, missingness, leakage, actuals and formula-eligibility gates.

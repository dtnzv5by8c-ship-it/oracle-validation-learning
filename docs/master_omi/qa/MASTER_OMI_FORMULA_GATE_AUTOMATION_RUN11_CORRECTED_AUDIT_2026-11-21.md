# Master OMI Formula Input Release Gate — Automation Run 11 Corrected Audit — 2026-11-21

## Final release status
FAIL-CLOSED.

## Canonical integrity
- Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Audited candidate: Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_AUTOMATION11_CORRECTED_FAIL_CLOSED.xlsx
- Candidate SHA-256: 22a014c10fe04337fc783ffc1902cf9c039f45a20bdfa30f71f0d37ff1122f6c
- Market Intelligence dimensions: 755 x 264
- A:ET value differences: 0
- A:ET nonblank type differences: 1269 (canonical float vs candidate int serialization); no coercion performed.

## Corrected QA configuration defect
The prior Formula Input QA layer incorrectly applied a generic IDENTITY_REVIEW_REQUIRED blocker to rows that already had exact FootyStats fixture identity (EXACT_FIXTURE_ID_JOIN) and passed the fixture identity field. This was a status/mapping configuration defect, not a data identity defect.

The correction removes that generic blocker when exact governed identity is already established. Genuine kickoff/date failures, sub-100% required coverage, identity failures, immutable native numeric-type failure, and schema certification failure remain hard blockers.

## Per-fixture decisions
- Governed fixtures: 387
- FORMULA_INPUT_STATUS=READY: 0/387
- FORMULA_INPUT_STATUS=BLOCKED: 387/387
- BACKTEST_READY=YES: 0/387
- RELEASE_DECISION=PASS: 0/387
- RELEASE_DECISION=FAIL: 387/387
- VERIFIED_PREMATCH: 0/387
- VERIFIED_ACTUALS: 31/387
- UNAVAILABLE/UNVERIFIED actuals: 356/387

## Mandatory blockers
- Explicit V2.1.1 schema marker not independently certified.
- Required PPG/GF/M/GA/M fields in immutable A:ET fail the native Excel numeric-type gate; no coercion performed.
- 169/387 governed fixtures have required MI coverage below 100%.
- 67/754 schedule records require kickoff/date reconciliation review.
- 15 implausible goal-environment records remain quarantined as UNAVAILABLE/UNVERIFIED.
- 754/754 xG rows lack verified point-in-time capture timestamps.

## Other controls
- Exact FootyStats identity only; no fuzzy matching.
- Last-3/Last-5 chronology, PPG/GF/M/GA/M denominator and pre-match cutoff controls retained.
- Venue, BTTS/goal intelligence, LTSS V1.1, source/status/confidence/as-of, duplicate, missingness, leakage and actuals controls remain fail-closed.
- Missing values are not converted to zero or estimated.
- Oracle V1.6 production logic unchanged.
- A:ET not inserted, reordered, renamed, value-mutated or coerced.

## Release rule
No fixture can pass if any mandatory gate fails. Overall Master OMI release remains FAIL-CLOSED because mandatory schema, native numeric-type, coverage, kickoff/date, goal-environment and xG provenance gates are unresolved.

# Master OMI Formula Input Release Gate — Automation Run 11 Audit

Audit timestamp: 2026-11-21 20:52 SAST
Candidate: Oracle_Master_OMI_Run11_FINAL_RELEASE_GATE_FAIL_CLOSED.xlsx
Candidate SHA-256: 4780634b3c7ce118390d9fc96f7a0da8a7b418f3bf3ce748c4b8e87d8d13e1ca
Canonical: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Canonical A:ET contract: 150 columns, rows 1:755.

## Result
RELEASE_DECISION = FAIL-CLOSED

## Immutable A:ET
- Dimensions: 755 x 150.
- A:ET value differences: 0.
- A:ET native-type differences: 1,269 (canonical float vs candidate integer; numerically equal).
- A:ET was not coerced, reordered, inserted, deleted, or renamed.
- Because the permanent contract requires native Excel representation to match the immutable baseline, the candidate fails the A:ET gate.

## Schema / governance
- configuration_version: 2.1.1 — PASS.
- Market Intelligence dimensions: 755 x 264 — PASS.
- Header comments A:ET: 150/150 — PASS.
- Exact Fixture Identity: 387/387 PASS.
- Fuzzy fixture matching: none.
- Duplicate governed fixture keys: 0.
- Oracle V1.6 production logic: unchanged.

## Fixture gate
- Governed fixtures: 387.
- FORMULA_INPUT_STATUS: BLOCKED 387/387.
- PREMATCH_STATE: UNAVAILABLE/UNVERIFIED 387/387.
- BACKTEST_READY: NO 387/387.
- RELEASE_DECISION: FAIL 387/387.
- Verified actuals: 31/387.
- Actuals UNAVAILABLE/UNVERIFIED: 356/387.
- Required MI coverage 100%: 218/387.
- Required MI coverage <100%: 169/387.
- Kickoff/date reconciliation blockers: 38/387.
- Goal-environment quarantine: 15/387.
- xG capture timestamps independently verified: 0/754.
- Post-match leakage gate: PASS for all governed fixtures.
- Last-3/Last-5 chronology and PPG/GF/M/GA/M controls: PASS where governed data exists.
- Venue metrics remain explicitly unavailable where source coverage is insufficient; missingness is not converted to zero.

## Release-rule enforcement
No PASS row may coexist with identity review, kickoff/date review, invalid numeric range, sub-100% coverage, provenance failure, or immutable A:ET defects. No such PASS rows exist.

## Remediation
No safe in-place repair is authorised for A:ET. The candidate must be regenerated from the canonical extraction/mapping path preserving the canonical native representation. No guessing, zero-filling, estimation, division, or rescaling was performed.

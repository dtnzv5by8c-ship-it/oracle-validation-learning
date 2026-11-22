# Master OMI Formula Input Release Gate — Automation Run 11

Timestamp: 2026-11-22 03:30 SAST

## Final status

**FAIL-CLOSED. No Master OMI release is authorised.**

## Canonical integrity

- Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED(1).xlsx
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Candidate source SHA-256: c2674761d2b5fa3ec3a4e4e01c3fc57eec39bf66ebbdb9b55328711ee9083171
- A:ET dimensions: 755 x 150
- A:ET semantic/value differences: 0
- A:ET native-type differences: 1,269
- No A:ET repair/coercion/reordering/insertion/deletion was performed.

## Current workbook population

- Market Intelligence: 755 x 264
- Governed fixtures: 754
- Formula Input QA: rebuilt to 754 fixture rows
- Verified actuals: 31 exact fixture/date rows
- Verified pre-match: 0
- Formula-ready: 0
- Backtest-ready: 0
- Release PASS: 0
- Release FAIL: 754

## Mandatory blockers

1. Immutable A:ET native-type mismatch: 1,269 cells.
2. Kickoff/date reconciliation review: 67 fixtures.
3. xG temporal provenance unverified: 754/754; no independently verified capture timestamps.
4. Goal Market Research remains non-production (EXPERIMENTAL_UNCALIBRATED / baseline-blocked states).
5. Required formula-input coverage cannot be proven at 100% for every fixture, so the gate fails closed.

## State separation

- VERIFIED_PREMATCH: 0
- VERIFIED_ACTUALS: 31
- UNAVAILABLE/UNVERIFIED: all remaining pre-match states
- Missing values were not converted to zero or estimates.
- No post-match leakage was admitted into pre-match eligibility.

## Protection

Oracle V1.6 production logic unchanged. A:ET was not modified. No fuzzy fixture matching was used. No guessed goal-environment transformation was performed. Implausible goal-environment values remain quarantined as unavailable/unverified.

## Release rule

A fixture can only be formula-ready when all mandatory pre-match gates pass. A backtest row additionally requires independently verified actuals and exact governed fixture/date identity. RELEASE_DECISION remains FAIL whenever any mandatory gate or coverage/provenance/identity/kickoff-date condition fails.

# Master OMI MI QA — Run 11 — 2026-11-22 23:29 SAST

## Scope
Canonical candidate: `Oracle_Master_OMI_RUN11_AUTOMATION11_EXHAUSTIVE_REAUDIT_1527SAST.xlsx`
Workbook SHA-256: `cc46eb23ae91b614eeec7cbf40f3a75ab897faafcca4926eb186d2593372a93f`
Market Intelligence: 755 rows × 264 columns = 754 governed fixtures × 264 MI columns.

## Gates
- Heading/comment coverage: 264/264 PASS
- Fixture IDs: 754/754 populated
- Duplicate Fixture IDs: 0
- Excel errors: 0
- FootyStats identity: 754/754 PASS
- Last-3 chronology: 754/754 PASS
- Last-5 chronology: 754/754 PASS
- Venue: 754/754 PASS
- Mandatory blanks: 0
- Kickoff/date: 687 PASS; 67 REVIEW_REQUIRED
- xG provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Actuals: 31 VERIFIED_ACTUALS; 723 UNAVAILABLE/UNVERIFIED
- Formula Input: 754 BLOCKED
- Backtest: 754 NO
- Release: 754 FAIL

## Numeric type gate
Direct workbook scan: 15,574 numeric-looking text cells across 21 governed numeric-dominant columns. These remain in immutable A:ET and were not coerced.

## CMOI
The Row Exception Matrix records CMOI=PASS for 754/754, but the workbook contains no literal CMOI governed header/output field in the Market Intelligence tab. This is treated as a schema/research-output verification blocker; no CMOI value was inferred.

## Production protection
A:ET was not modified. Oracle V1.6 was not modified. No fuzzy matching, timezone normalization, historical backfill, zero substitution, estimation, or guessing was used.

## Release decision
FAIL-CLOSED. 100% QA is not achieved because numeric-type, kickoff/date review, xG temporal provenance, explicit CMOI output, formula/backtest eligibility remain unresolved.

## Matrix hashes
- Column coverage: 46518134e4f1aecb200332fd8e82b64d4f40a30a5c22776a175653da8142fedc
- Row exceptions: 975e05a87994dd5590a88a0c45e6b509f1b3f98d50f44e7308a24175163e7da6

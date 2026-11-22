# Master OMI MI QA — Automation Run 11 — Exhaustive Re-audit

**Final release: FAIL-CLOSED**

## Scope
- Market Intelligence: 755 rows × 264 columns
- Governed fixtures: 754
- Audit scope: every governed fixture row and every Market Intelligence column

## Canonical / immutable gate
- Canonical workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Candidate workbook SHA-256: 5a868b00f8eed176c878bc04faa7e42bd6962cef10db9ec085fd4616bf9cfd3c
- A:ET value differences: 0
- A:ET native/type differences: 140
- The 140 differences are blank-cell serialization differences; no A:ET repair was performed.
- Oracle V1.6: unchanged.

## Schema / structural QA
- V2.1.1 configuration: 2.1.1
- Heading comments: 264/264
- Duplicate governed Fixture IDs: 0
- Excel error cells: 0
- CMOI blanks: 0/754

## Numeric-type gate
- The existing Column Coverage Matrix records 15,574 numeric-looking text cells across 21 governed numeric-dominant columns.
- This directly violates the requested 100% QA definition.
- No coercion was performed inside A:ET because A:ET is immutable.
- The earlier claim of zero numeric-looking text in governed numeric fields is superseded by this direct re-audit.

Affected columns include BTTS Yes, Home 1X, Away X2, Fixture ID/provider/team IDs, GF/M, GA/M, PPG, research goal percentages, expected-goal lambda and goal-research sample fields.

## Formula / backtest gate
- FORMULA_INPUT_STATUS READY: 0/754
- FORMULA_INPUT_STATUS BLOCKED: 754/754
- BACKTEST_READY: 0/754
- RELEASE_DECISION PASS: 0/754
- RELEASE_DECISION FAIL: 754/754
- MI coverage below 100%: 754/754

## Provenance / reconciliation
- Exact FootyStats identity: 754/754
- Silent fuzzy matching: none
- Last-3 / Last-5 chronology: no chronology blocker recorded
- Kickoff/date review: 67
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Verified actuals: 31 exact governed links
- Remaining unmatched source actuals remain separate
- Missing evidence was not converted to zero, estimated or guessed.

## Final disposition
The Master OMI release remains FAIL-CLOSED. The permanent gate cannot pass while the immutable A:ET representation is not exact, governed numeric-looking text remains, required coverage is below 100%, kickoff/date reviews remain, and xG point-in-time provenance is unverified. No A:ET or Oracle V1.6 production logic was changed.

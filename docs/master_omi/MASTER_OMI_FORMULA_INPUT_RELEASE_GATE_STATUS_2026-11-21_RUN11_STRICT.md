# Master OMI Permanent Formula Input Release Gate — Run 11 Strict Re-audit — 2026-11-21

**RELEASE_STATUS: FAIL-CLOSED**

Canonical baseline SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
Audited candidate SHA-256: `22976945971c2f7d5e88a20f0c7302dd759cb60ce8cb76ee0085d5b942f245e`

## Immutable A:ET — corrected direct comparison
Direct comparison of the current candidate against the canonical workbook found **21,774 cell-level value/representation differences** in A:ET and **23,043 nonblank type differences**. These include numeric-string/float and float/int representation changes. The immutable range therefore fails closed. No A:ET coercion or repair was performed.

## Workbook/fixture gates
- Market Intelligence: 755 x 264
- Governed heading comments: 264/264
- Exact FootyStats identity: 387/387 according to QA; no fuzzy matching permitted.
- Kickoff/date review required: 67/754
- Required MI coverage below 100%: 169/387
- xG capture timestamps verified: 0/754
- Goal-environment anomalies quarantined: 15
- Independently verified actuals: 31/387
- Explicit V2.1.1 schema marker: not found; certification fails closed.

## Per-fixture release gate
Because the immutable A:ET gate fails, no fixture is accepted as formula-ready for release certification. `BACKTEST_READY=NO` remains enforced. `RELEASE_DECISION=FAIL` remains the authoritative release state.

## State model
Maintain `VERIFIED_PREMATCH`, `VERIFIED_ACTUALS`, and `UNAVAILABLE/UNVERIFIED` separately. Missing values are never converted to zero or estimates. Post-match evidence is not admitted into pre-match inputs.

## Production protection
Oracle V1.6 production logic is unchanged. No A:ET insertion, deletion, reordering, renaming, coercion, or repair was performed.

## Release rule
Any immutable-range mutation, unresolved schema/provenance defect, identity/kickoff defect, invalid numeric range, sub-100% required coverage, or leakage defect forces FAIL. No blocker note may coexist with PASS. Overall Master OMI release remains FAIL-CLOSED.
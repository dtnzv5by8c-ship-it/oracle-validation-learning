# Master OMI MI Exhaustive QA — Automation Turn 11 — 2026-11-24 10:34 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Scope
- Canonical V2.1.1 Market Intelligence contract: 755 rows x 264 columns
- Governed fixture rows: 754
- Full tab audited, not restricted to report-date window.

## Workbook identity
- Audited Run 37 workbook: Oracle_Master_OMI_V2_1_1_REMEDIATION_RUN37_2026-11-24_EXACT_AET.xlsx
- Workbook SHA-256: bd7ba47c05fce966f2b6f4155776b25d37dc84dccafbeca92dd5b3429abeef49
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Schema / identity
- 264/264 headings present
- 264/264 header comments present
- 754/754 Fixture IDs populated and unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel error cells: 0
- A:ET value differences vs canonical: 0
- A:ET native-type differences vs canonical: 0
- Oracle V1.6: preserved

## Numeric native-type gate
- Numeric-looking text total: 15,599
- Numeric-looking text inside immutable A:ET: 15,574
- Numeric-looking analytical text outside ET: 0
- Residual numeric-looking text outside ET: 25, all verified FootyStats source-fixture IDs in GG:GJ
- No A:ET coercion performed.

## Source / chronology / provenance
- FootyStats exact Fixture-ID joins: 754/754
- Schedule reconciliation MATCH: 687/754
- Schedule REVIEW_REQUIRED: 67/754
- History cutoff timestamps present: 754/754
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- xG betting eligibility: 0/754
- Goal production eligibility: 0/754
- Goal betting eligibility: 0/754
- FootyStats data quality: 754/754 GOOD_RESEARCH_EVIDENCE
- LTSS V1.1: 754/754
- Team-score status: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH
- Actuals verified: 275/754
- Actuals unavailable/unverified: 479/754
- Formula Input READY: 0/754
- Formula Input BLOCKED: 754/754
- BACKTEST_READY: 0/754

## CMOI
The 264-column Run 37 Market Intelligence contract contains no CMOI columns. The separate locked CMOI workbook was independently inspected: CMOI_MATCH_OUTCOME and CMOI_CONFIDENCE are blank for all 754 governed rows. Therefore authoritative CMOI population is 0/754 and all 754 are explicitly treated as UNAVAILABLE/UNVERIFIED. No inferred, estimated, zero-filled or prototype CMOI values were imported.

## QA matrices
- Column-by-column coverage matrix SHA-256: 9d83e2a0c4b9a6b972b77822fed5da739e7950b7d5487aa65dd82ba5fbd50f5e
- Row-by-row exception matrix SHA-256: 2aba92dedc58f32952791dcc6bf0cdd65583f8ff4e92314c4de90842cd8e171b

## Corrections
No new source-backed production correction was justified. Run 37 is a zero-change carry-forward of the already-supported numeric-type remediation lineage.
- A:ET unchanged
- Oracle V1.6 unchanged
- No fuzzy matching
- No timezone normalization
- No historical backfill
- No estimation or zero-fill
- No unsupported provenance substitution

## Release blockers
1. 15,574 numeric-looking analytical values remain inside immutable A:ET.
2. 67 schedule reconciliation records remain REVIEW_REQUIRED.
3. 754/754 xG capture timestamps remain unverified.
4. 754/754 Formula Input records remain BLOCKED.
5. 0/754 BACKTEST_READY.
6. CMOI authoritative evidence is unavailable for all 754 rows.
7. 479/754 actuals remain unavailable/unverified.

100% QA is not achieved. Release remains fail-closed.

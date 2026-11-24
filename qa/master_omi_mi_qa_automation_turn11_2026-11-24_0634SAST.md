# Master OMI MI QA — Automation Turn 11

Audit timestamp: 2026-11-24 06:34 SAST

## Candidate workbook
- File: Oracle_Master_OMI_Report_14-24_Nov_2026_MARKET_INTELLIGENCE_QA.xlsx
- SHA-256: 4da0f8e92afba24e989bd6025e36e9e30ffbd9eaa16956099b8a74f0342b63cc
- Worksheet: Market Intelligence
- Dimensions: 755 rows x 266 columns
- Governed fixture rows: 754
- Current MI columns: 266, including CMOI_MATCH_OUTCOME and CMOI_CONFIDENCE appended after the 264-column contract surface

## QA findings
- Header headings: 266/266 nonblank
- Header comments: 266/266
- Fixture IDs (column 39): 754/754 nonblank, 754 unique, 0 duplicates
- Excel error literals: 0
- Formula cells: 0
- Numeric-looking text in immutable A:ET: 5,158 cells (release blocker under zero-text gate)
- Numeric-looking text outside ET: 0
- CMOI_MATCH_OUTCOME populated: 387/754
- CMOI_MATCH_OUTCOME blank: 367/754
- CMOI_CONFIDENCE populated: 387/754
- CMOI_CONFIDENCE blank: 367/754
- FootyStats xG Temporal Provenance Status: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- FootyStats Source / Join Status: governed exact-join evidence present in audited rows
- Formula Input / backtest: release remains blocked by mandatory gates

## CMOI cross-check
The available CMOI_POPULATED workbook was compared by exact Fixture ID against the current QA workbook. All 754 fixture IDs matched. There were 0 additional CMOI values in the comparison workbook for the 367 blank rows and 0 CMOI value differences for rows where values exist. Therefore no source-backed CMOI correction is justified.

## Contract / release
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Column coverage matrix hash: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Row exception matrix hash: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45
- A:ET: no production changes made
- Oracle V1.6: unchanged
- No fuzzy matching, timezone normalization, historical backfill, estimation, zero-fill, or unsupported provenance substitution
- RELEASE_DECISION: FAIL-CLOSED

## Gate blockers
1. Immutable A:ET contains 5,158 numeric-looking text cells and cannot be rewritten without violating the permanent contract.
2. 367 CMOI output pairs are blank; the comparison workbook provides no authoritative values to populate them. They remain unavailable rather than guessed.
3. xG temporal capture provenance is unverified for all 754 fixtures.
4. Formula Input / backtest eligibility remains blocked by mandatory gates.

This evidence deliberately does not certify 100% QA. The audit must be rerun after any authoritative source-backed correction.
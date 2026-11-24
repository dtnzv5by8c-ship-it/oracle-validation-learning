# Master OMI MI Exhaustive QA — Automation Turn 11 — 2026-11-24 08:05 SAST

RELEASE_DECISION=FAIL-CLOSED

## Binary audited
- Workbook: Oracle_Master_OMI_Report_14-24_Nov_2026_MARKET_INTELLIGENCE_QA.xlsx
- SHA-256: 4da0f8e92afba24e989bd6025e36e9e30ffbd9eaa16956099b8a74f0342b63cc
- Market Intelligence dimensions: 755 rows x 266 columns
- Permanent V2.1.1 governed MI contract: 264 columns / 754 fixture rows
- Additional research-only columns: CMOI_MATCH_OUTCOME and CMOI_CONFIDENCE

## Direct binary checks
- 266/266 headings present
- 266/266 header comments present
- 754/754 Fixture IDs present and unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel error cells: 0
- Governed analytical numeric-looking text outside ET: 0
- Numeric-looking provenance/source IDs in GG:GJ: 25, retained as text
- A:ET preserved; no production logic mutation performed

## Formula Input / governance
- FootyStats source identity: 754/754 EXACT_FIXTURE_ID_JOIN
- Last-3 PPG: 754/754 PASS
- Last-5 PPG: 754/754 PASS
- GF/M & GA/M: 754/754 PASS
- Venue metrics: 754/754 PASS
- Team strength: 754/754 PASS
- Pre-match leakage check: 754/754 PASS
- Formula Input: 0/754 READY; 754/754 BLOCKED
- Prediction Input Ready: 0/754
- Backtest Ready: 0/754
- Release Decision: 754/754 FAIL
- PREMATCH_STATE: 754/754 UNAVAILABLE/UNVERIFIED
- Verified actuals: 31/754; 723/754 UNAVAILABLE/UNVERIFIED
- MI Coverage % field: 0/754 proven as 100%

## Schedule / chronology
- Schedule Reconciliation contains 67 REVIEW_REQUIRED records.
- No timezone normalization or silent reconciliation was performed.
- xG temporal capture provenance remains UNVERIFIED; workbook evidence does not establish when the xG values became available.

## CMOI
- CMOI outcome populated: 387/754
- CMOI confidence populated: 387/754
- CMOI outcome unavailable/unverified: 367/754
- CMOI confidence unavailable/unverified: 367/754
- No unsupported CMOI values were inferred or zero-filled.

## QA matrices
- Column coverage matrix hash: 76dbebb0adf55260655c9c404d45c2403fc9c57127e0394e65ce6f12177672f9
- Row exception matrix hash: f05191a3531b4b7ea76f74a71c79e2ab0a78305c9671b640c8f2a2d6c1535803
- Full audit JSON hash: 88fff3dbdb37217177d175fb0652d1fae3f80335586a4997a0ea795cc981fb15

## Release blockers
1. Formula Input remains blocked for all 754 fixtures.
2. Backtest eligibility remains 0/754.
3. xG temporal provenance is not verified.
4. 67 schedule/kickoff records remain REVIEW_REQUIRED.
5. CMOI is unavailable/unverified for 367 fixtures.
6. Required MI coverage is not proven at 100% in the workbook gate.
7. 723 fixtures lack verified actuals.

No missing evidence was converted to zero, estimates, or guessed values. No fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, or leakage was introduced. A:ET and Oracle V1.6 were preserved exactly.

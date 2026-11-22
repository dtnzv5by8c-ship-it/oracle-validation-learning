# Master OMI MI QA — Automation Run 11 — 2026-11-22 17:32 SAST

**MASTER_OMI_RELEASE = FAIL-CLOSED**

Scope: 754 governed fixtures × 264 Market Intelligence columns.

## Direct audit
- Candidate SHA-256: `5a868b00f8eed176c878bc04faa7e42bd6962cef10db9ec085fd4616bf9cfd3c`
- Heading comments: 264/264
- Fixture IDs: 754/754
- Duplicate Fixture IDs: 0
- Excel errors: 0
- CMOI blanks: 0/754
- Direct numeric-looking text: **17,082 cells across 23 governed numeric-looking columns**
- Mandatory blanks: 0 in the existing QA layer

## Formula / release state
- FORMULA_INPUT_STATUS=BLOCKED: 754/754
- PREMATCH_STATE=UNAVAILABLE/UNVERIFIED: 754/754
- VERIFIED_ACTUALS: 31/754
- BACKTEST_READY=NO: 754/754
- RELEASE_DECISION=FAIL: 754/754

## Other gates
- Kickoff/date REVIEW_REQUIRED: 67
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Goal intelligence production eligible: 0/754
- Exact FootyStats identity: 754/754
- Fuzzy matching: none
- Missing evidence was not converted to zero/estimate/guess.
- No timezone normalization or historical backfill.

## QA evidence discrepancy
The workbook's existing Column Coverage Matrix reports **15,574** numeric-looking text cells across 21 columns. A fresh direct cell-type scan of the canonical candidate finds **17,082** across 23 columns. The direct scan is authoritative for this run; the discrepancy is recorded as a QA evidence defect and no A:ET production data was rewritten.

## Immutable production
- A:ET value differences from the established baseline: 0
- A:ET type/serialization differences: 140 (blank-cell representation differences)
- A:ET mutation: none
- Oracle V1.6 mutation: none

## Direct numeric-looking text counts
BTTS Yes=714; Home 1X=714; Away X2=714; Home Evidence Risk=754; Away Evidence Risk=754; Fixture ID=754; Provider Season ID=754; Home Team ID=754; Away Team ID=754; Home Goals For Avg=754; Home Goals Against Avg=754; Home Points Per Game=754; Away Goals For Avg=754; Away Goals Against Avg=754; Away Points Per Game=754; Research Over 1.5 %=734; Research Over 2.5 %=734; Research Under 4.5 %=734; Research Home Over 1.5 %=734; Research Away Over 1.5 %=734; Home Expected Goals Lambda=734; Away Expected Goals Lambda=734; Goal Research League Prior N=754.

**Disposition:** continue fail-closed hourly until every mandatory gate genuinely passes.

# Master OMI MI QA — Automation Run 11 — 2026-11-22 21:42 SAST

**RELEASE_DECISION=FAIL-CLOSED**

## Scope
- Candidate: `Oracle_Master_OMI_V2_1_1_REMEDIATION_CANDIDATE_2026-11-22.xlsx`
- Candidate SHA-256: `f70194648c89d729908fd87b185cc32fd8483dc73da1bba2245ac10b57e24f78`
- Market Intelligence: 755 rows × 264 columns; 754 governed fixture rows.
- Canonical V2.1.1 baseline SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Oracle V1.6: unchanged.

## Immutable A:ET audit
Direct workbook-to-canonical comparison:
- A:ET value differences: 0
- A:ET native type differences: 0
- A:ET comment differences: 0
- Header comments: 264/264
- No A:ET mutation was made.

## Identity / structure
- Fixture IDs populated: 754/754
- Duplicate Fixture IDs: 0
- Excel errors: 0
- Exact FootyStats Source/Join Status: 754/754 `EXACT_FIXTURE_ID_JOIN`
- Fuzzy matching: none.
- Timezone normalization: none.
- Historical backfill: none.

## Numeric native-type gate
The direct scan found 17,107 numeric-looking text cells across 27 columns. Of these, 1,533 are legitimate categorical/source-ID text cases (Home/Away Evidence Risk and four FootyStats source-fixture-ID fields). The governed numeric gate therefore fails on **15,574 numeric-looking text cells across 21 governed numeric columns**, all inside immutable A:ET.

Affected governed numeric columns:
BTTS Yes; Home 1X; Away X2; Fixture ID; Provider Season ID; Home Team ID; Away Team ID; Home Goals For Avg; Home Goals Against Avg; Home Points Per Game; Away Goals For Avg; Away Goals Against Avg; Away Points Per Game; Research Over 1.5 %; Research Over 2.5 %; Research Under 4.5 %; Research Home Over 1.5 %; Research Away Over 1.5 %; Home Expected Goals Lambda; Away Expected Goals Lambda; Goal Research League Prior N.

The append-only remediation outside ET converted 21,749 valid numeric-looking strings to native numeric values with zero value changes. The candidate reports zero remaining numeric-looking text in governed candidate fields outside ET. The immutable A:ET defect remains and cannot be coerced without violating the contract.

## Coverage / chronology / provenance
- Schedule reconciliation: 687 MATCH, 67 REVIEW_REQUIRED.
- All 67 review rows retain `MANUAL_AUTHORITATIVE_EVENT_TIME_REVIEW_ONLY_NO_AUTO_CORRECTION`.
- History Cutoff UTC populated: 754/754.
- FootyStats History Cutoff UTC populated: 754/754.
- Last-3 / Last-5 evidence present; chronology gates remain governed.
- FootyStats xG temporal provenance: 754/754 `UNVERIFIED_NO_CAPTURE_TIMESTAMP`.
- xG betting eligibility: 0/754.
- Production Eligible: 0/754.
- Betting Eligible: 0/754.
- Goal Research Status: 734 `EXPERIMENTAL_UNCALIBRATED`; 20 `BLOCKED_LEAGUE_BASELINE_LT20`.
- Team Score Status: 406 `BACKTESTED_LEAGUE_WINDOW`; 348 `STATE_FALLBACK_RESEARCH`.
- Verified actuals: 31/754; remaining 723 explicitly unavailable/unverified in the governed QA state.

## Missingness / coverage
- Field Coverage QA: PASS for field-by-field selected-50 audit.
- Field Coverage Summary: 348 field occurrences audited.
- Field Coverage Exceptions: 950 exception rows.
- Exception states: 207 PARTIAL_VALUE_COVERAGE; 648 EXPLICITLY_UNAVAILABLE_OR_BLOCKED; 95 NO_USABLE_VALUES.
- Unmapped source rows: 0.
- Mandatory identity fields have no unexplained blank records in the governed coverage summary.
- Optional/research/actual blanks are not promoted to zero or estimates.

## CMOI
The candidate contains **no literal CMOI field/header or CMOI string anywhere in the XLSX package**. Therefore CMOI cannot be independently certified as a populated workbook output in this run. This is treated as an unresolved research-output/schema gate, not silently inferred from other fields.

## Formula/backtest gate
- Formula input ready: 0/754.
- Formula input blocked: 754/754.
- Backtest ready: 0/754.
- Release pass: 0/754.
- Release fail: 754/754.

## Remediation
The latest remediation converted 21,749 append-only numeric-looking strings outside ET with zero value changes. A:ET was preserved exactly. No production logic was redesigned and Oracle V1.6 was not changed.

## Final disposition
**MASTER_OMI_RELEASE=FAIL-CLOSED**

Hard blockers:
1. 15,574 governed numeric-looking text cells remain inside immutable A:ET.
2. 67 kickoff/date reviews remain unresolved.
3. 754/754 xG records lack independently verified point-in-time capture timestamps.
4. CMOI is not explicitly represented in the workbook and therefore cannot be independently certified.
5. Formula input remains blocked for 754/754 fixtures.
6. Backtest-ready remains 0/754.

The complete audit must repeat after every remediation change; no release certification is permitted until every mandatory gate passes.

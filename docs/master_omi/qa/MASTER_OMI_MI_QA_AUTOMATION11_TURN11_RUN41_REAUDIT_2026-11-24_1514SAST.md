# Master OMI MI QA — Automation Turn 11 — 2026-11-24 15:14 SAST

## Release
RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Exact Run 41 binary audit
Candidate workbook: Oracle_Master_OMI_V2_1_1_REMEDIATION_RUN41_EXACT_AET.xlsx
Candidate SHA-256: efeea8101814f7d207d9396cb4182b15a952f2dc3a476e5f51f28a5da4915f8f
Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Dimensions: 755 rows x 264 columns
Governed fixtures: 754
Headers: 264/264 populated
Header comments: 264/264
Fixture IDs: 754/754 populated, 754 unique
Duplicate Fixture IDs: 0
Formula cells: 0
Excel error literals: 0

## Immutable A:ET integrity
A:ET cell-fragment SHA-256, canonical: fc13ceae478cc1fe308ccb44abd0fe896996f537ae34487c587fcc594fef074a
A:ET cell-fragment SHA-256, Run 41: fc13ceae478cc1fe308ccb44abd0fe896996f537ae34487c587fcc594fef074a
A:ET exact content/fragment integrity: PASS
Oracle V1.6: unchanged

## Numeric native-type gate
Numeric-looking text in immutable A:ET: 15,574
Numeric-looking text outside ET: 25
The 25 outside ET are GG:GJ FootyStats provenance/source-fixture IDs and remain text.
Supported analytical numeric-looking text outside ET: 0.
No further supported numeric-type correction is justified.
A:ET cannot be coerced without violating the permanent V2.1.1 contract.

## Identity / chronology / provenance
FootyStats Source / Join Status: 754/754 EXACT_FIXTURE_ID_JOIN
FootyStats Data Quality Status: 754/754 GOOD_RESEARCH_EVIDENCE
Schedule Reconciliation: 687 MATCH / 67 REVIEW_REQUIRED
FootyStats xG Temporal Provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
FootyStats xG Betting Eligibility: 754/754 NO
Production Eligible: 0/754
Betting Eligible: 0/754
TEAM_SCORE_STATUS: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH

## Actuals / CMOI
Actuals / Research Review Status: 275 ACTUAL VERIFIED / 479 blank.
The 479 blank statuses are not silently treated as verified or zero; they remain an explicit release exception.
The separate CMOI surface remains outside the 264-column production contract. Latest authoritative evidence: 387/754 populated, 367/754 blank, with exact Fixture-ID cross-check showing 0 additional authoritative values. The 367 remain UNAVAILABLE/UNVERIFIED.

## Research-layer checks
FootyStats PPG, GF/M, GA/M, venue metrics, BTTS/goal intelligence, LTSS V1.1, Last-3/Last-5, H2H, actuals and derived intelligence were rechecked against the governed workbook state. No source-backed value correction was justified on this run.
Goal Research Block Reason: 734 NONE_FORECASTABLE_RESEARCH_ONLY; 11 and 9 rows blocked for insufficient prior settled league matches.
No fuzzy matching, timezone normalization, historical backfill, estimation, zero-fill, unsupported provenance substitution, or leakage remediation was performed.

## Coverage / exception matrices
Column coverage matrix and row exception matrix were regenerated from the exact Run 41 binary. They record, per column: populated count, unexplained blank count, explicit unavailable/unverified count, numeric count, text count, schema/comment status, and release-gate status; and per fixture: identity, schedule, provenance, numeric-type, chronology, leakage, actuals, CMOI, and formula/backtest exceptions.

## Mandatory blockers
1. 15,574 numeric-looking analytical values remain in immutable A:ET.
2. 67 schedule rows remain REVIEW_REQUIRED.
3. 754/754 xG temporal capture timestamps are unverified.
4. 479 actual-status fields are blank rather than explicitly classified unavailable.
5. CMOI has 367 unavailable/unverified output pairs.
6. Formula Input/backtest release remains blocked.
7. 0/754 production eligible; 0/754 betting eligible.

No production logic was changed. Release remains fail-closed.
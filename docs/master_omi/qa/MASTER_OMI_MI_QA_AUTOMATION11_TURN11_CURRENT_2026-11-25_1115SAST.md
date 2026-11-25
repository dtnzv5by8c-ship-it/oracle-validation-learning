# Master OMI MI QA — Automation Turn 11 — 2026-11-25 11:15 SAST

RELEASE_DECISION=FAIL-CLOSED

## Scope
- Contract: Master OMI V2.1.1
- Production model: Oracle V1.6
- Market Intelligence: 755 rows x 264 columns
- Governed fixtures: 754

## Directly supported controls
- Fixture IDs: 754/754 populated and unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel error cells: 0
- Numeric-looking text in immutable A:ET: 15,574
- Previously authorised analytical numeric-type conversions: 21,749
- Numeric-looking text outside ET: 25
- Remaining outside-ET numeric-looking text in GG:GJ provenance/source-ID fields: 25
- Governed analytical numeric-looking text outside ET: 0
- A:ET unchanged
- Oracle V1.6 unchanged
- No fuzzy matching, timezone normalization, estimation, zero-fill, historical backfill, unsupported provenance substitution, or fixture-ID rewriting

## Remaining exceptions / gates
- Actuals/review-status discrepancy: 41 populated research-actual rows with blank immutable DI status: 4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402
- Schedule REVIEW_REQUIRED / KICKOFF_MISMATCH: 67/754
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Production Eligible: 0/754
- Betting Eligible: 0/754
- Formula Input/backtest: BLOCKED
- CMOI: UNAVAILABLE/UNVERIFIED; no CMOI fields exist in the permanent 264-column contract
- Remaining venue, Last-3/Last-5, H2H, BTTS/goal, LTSS, actual and derived-field issues without authoritative source evidence remain QA-owned

## Binary certification limitation
Latest remediation evidence is Run 61, dated 2026-11-25 10:03 SAST, with 0 additional cells changed. Candidate SHA-256: 8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742. sheet3.xml SHA-256: f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830.

The exact XLSX bytes for Run 61 are not exposed through the connected GitHub file surface. Therefore this run does not claim independent workbook/XML certification of Run 61. The latest independently binary-audited workbook remains the previously certified QA artifact.

## Release
FAIL-CLOSED. No source-backed production correction was justified. The QA task must continue until all mandatory gates pass and the exact candidate binary can be independently re-audited.

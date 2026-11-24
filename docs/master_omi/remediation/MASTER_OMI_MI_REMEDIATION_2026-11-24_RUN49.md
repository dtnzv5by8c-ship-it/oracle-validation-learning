# Master OMI MI Remediation — Run 49 — 2026-11-24

## Release posture
FAIL-CLOSED. No release PASS is declared.

## Latest QA evidence
- QA commit: bd3696005b7a2806f9e6a519cc0a9aba82be28a6
- QA report: docs/master_omi/qa/MASTER_OMI_MI_QA_RUN48_2026-11-24.md
- QA decision: FAIL-CLOSED
- QA audited workbook SHA-256: 8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Direct validation
- Market Intelligence: 755 x 264
- Governed fixtures: 754
- Fixture IDs: 754/754 nonblank and unique
- Numeric-looking text inside immutable A:ET: 15,574
- Numeric-looking text outside ET: 25
- Governed analytical numeric-looking text outside ET: 0
- Genuine GG:GJ provenance/source-ID strings: 25
- Formula cells: 0
- Excel errors: 0

The 25 residual numeric-looking strings outside ET are genuine FootyStats provenance/source-fixture IDs and remain text.

## Remediation
The previously authorised 21,749 type-only conversions remain intact in EW:FB, FG:FL, FO:GB and HD:HF. No analytical values changed.

Run 49 made 0 additional cell changes because no new safe mutation is supported outside immutable A:ET.

## QA/direct-scan discrepancy
The QA row-exception matrix reports 40 ACTUALS_POPULATED_REVIEW_STATUS_BLANK rows. Direct cell-level validation of the exact audited binary finds 41.

All 41 have populated History Source Fixture IDs, Actual Home/Away/Total Goals, Actual Match Result, BTTS, O1.5, O2.5, U4.5, Actual Settlement Status=SETTLED and Actual Results Source=FootyStats. All 41 pass internal score/result/BTTS/O1.5/O2.5/U4.5 consistency.

The affected worksheet rows are:
4,25,49,54,55,78,79,80,134,186,187,188,189,190,191,221,222,224,232,233,234,235,236,237,238,239,269,313,338,353,357,364,366,367,368,397,398,399,400,401,402.

The review-status field is column DG, inside immutable A:ET. Therefore the evidence-supported correction cannot be applied without violating the permanent contract. All 41 remain unchanged and explicitly handed to QA. The direct count of 41 supersedes the matrix count of 40 for this exception class.

## Integrity
- Run 49 candidate SHA-256: 8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742
- Run 49 sheet3.xml SHA-256: f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830
- A:ET SHA before/after: 7aa591955c69d7a4419028b63f345c963451671c1c5b66cfec8a62b99e2dee57
- A:ET: byte-identical
- Oracle V1.6: unchanged
- Run 49 cells changed: 0

## Remaining blockers
- 15,574 immutable A:ET numeric-looking text cells
- 41 authoritative populated-actual rows with blank review status inside immutable A:ET
- 67/754 schedule REVIEW_REQUIRED / KICKOFF_MISMATCH
- 754/754 xG temporal provenance UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Formula Input/backtest gates blocked
- CMOI unavailable/unverified in the 264-column production contract
- Other source-unsupported venue, Last-3/Last-5, H2H, BTTS/goal, LTSS, actual and derived-field exceptions remain untouched

No estimation, invention, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewrite, A:ET mutation, Oracle V1.6 redesign, or post-match leakage remediation was performed.

Release remains FAIL-CLOSED.
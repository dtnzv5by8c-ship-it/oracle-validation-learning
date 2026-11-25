# Master OMI MI Remediation Run 53 — 2026-11-25

RELEASE_DECISION=FAIL-CLOSED

## Authoritative inputs
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Latest independent QA: docs/master_omi/qa/MASTER_OMI_MI_QA_RUN48_2026-11-24.md
- QA commit: bd3696005b7a2806f9e6a519cc0a9aba82be28a6
- QA-audited Run 48 SHA-256: 8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742
- QA decision: FAIL-CLOSED

## Direct canonical reconciliation
- Market Intelligence: 755 rows x 264 columns
- Governed fixtures: 754
- Numeric-looking text inside immutable A:ET: 15,574
- Numeric-looking text outside ET: 21,774
- Supported governed analytical numeric-looking text converted: 21,749
- Genuine nonnumeric text in controlled numeric ranges preserved: 117
- Fixture IDs: 754/754 nonblank and unique; duplicates: 0
- Canonical SHA verified: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Remediation
Converted only valid numeric-looking text in EW:FB, FG:FL, FO:GB and HD:HF to native Excel numerics.
- Cells changed: 21,749
- Analytical value changes: 0
- Genuine GG:GJ provenance/source-fixture IDs remain text.
- No A:ET mutation.
- Oracle V1.6 unchanged.
- Manifest records cell, fixture ID AM, before/after value/type, and GG:GJ source IDs.

## Candidate validation
- Candidate SHA-256: 838549f6188a392037103f4052598e35fcf806a1444e19de937210a6742fca08
- Candidate sheet3.xml SHA-256: e3f5c423b0e9f0ef2754a225491096e9a6a12fd2b997c8b5db5d2b22d1b30e28
- Numeric-looking text inside A:ET: 15,574
- Numeric-looking text outside ET: 25; all genuine GG:GJ provenance/source IDs
- Governed analytical numeric-looking text outside ET: 0
- Formula cells: 0
- Excel error literals: 0
- Fixture IDs: 754/754 unique
- A:ET value differences vs canonical: 0
- A:ET native-type differences vs canonical: 0

## QA/direct-scan discrepancy
QA reports 40 populated-research-actual rows with blank review status. Direct cell-level validation finds 41. Rows: 4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402.

The affected field is DI, inside immutable A:ET. These cells were left unchanged; no status was invented, inferred or backfilled.

## Unresolved QA exceptions
- 15,574 immutable A:ET numeric-looking text cells.
- 41 populated-actual rows with blank review status in A:ET; authoritative direct count = 41.
- 67/754 schedule REVIEW_REQUIRED / KICKOFF_MISMATCH.
- 754/754 xG UNVERIFIED_NO_CAPTURE_TIMESTAMP; prediction use quarantined.
- Production Eligible 754/754 NO.
- Betting Eligible 754/754 NO.
- Formula Input/backtest blocked.
- CMOI explicitly UNAVAILABLE/UNVERIFIED because no CMOI fields exist in the 264-column production contract.
- Other venue, Last-3/Last-5, H2H, BTTS/goal, LTSS, actual and derived-field issues without authoritative source evidence remain unchanged.

No invention, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, Oracle V1.6 redesign, or post-match leakage remediation was performed.

## Artifact hashes
- Candidate workbook: 838549f6188a392037103f4052598e35fcf806a1444e19de937210a6742fca08
- Cell-change manifest: c190d8282ab6d7624621560a833dd48d8d06b75d2d11ae1396d9a070e772beef
- Candidate sheet3.xml: e3f5c423b0e9f0ef2754a225491096e9a6a12fd2b997c8b5db5d2b22d1b30e28

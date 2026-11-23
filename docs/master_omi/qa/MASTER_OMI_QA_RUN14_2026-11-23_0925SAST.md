# Master OMI MI QA — Run 14 Evidence — 2026-11-23 09:25 SAST

## Release posture
RELEASE_DECISION=FAIL-CLOSED

## Audit scope
The canonical V2.1.1 Master OMI Market Intelligence contract remains 754 governed fixtures x 264 MI columns (755 worksheet rows including header).

This run re-audited the latest GitHub repository state and checked for any newer exhaustive QA certification or workbook-level QA artifact after the authoritative 2026-11-23 00:53 SAST audit.

## Latest repository state
Latest commit: 36872cee212b9fb9fd458641c10d74b5804d426f
Commit message: Master OMI MI remediation Run 13 evidence
Commit time: 2026-11-23T05:50:08Z

No newer commit exists in the repository history at this run.
No GitHub Actions workflow run is attached to the Run 13 commit.

## Authoritative workbook QA carried forward
QA workbook SHA-256: cc46eb23ae91b614eeec7cbf40f3a75ab897faafcca4926eb186d2593372a93f
Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Current gate results
- Governed fixtures: 754/754
- MI columns: 264/264
- Heading/comments: 264/264
- Fixture IDs: 754/754 nonblank and unique
- Excel errors: 0
- Formulas in audited MI artifact: 0
- Numeric-looking text in governed A:ET fields: 15,574 across 21 fields
- Numeric-looking text outside ET: 25, all legitimate FootyStats provenance/source-fixture identifiers in GG:GJ
- Analytical numeric-looking text outside ET: 0
- Kickoff/date: 687 MATCH / 67 REVIEW_REQUIRED
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Formula Input: 0/754 READY; 754/754 BLOCKED
- Backtest: 0/754 READY
- CMOI: UNAVAILABLE/UNVERIFIED; no output inferred
- Release: FAIL-CLOSED

## Production protection
A:ET values unchanged.
A:ET schema unchanged.
Oracle V1.6 unchanged.
No fuzzy matching, timezone normalization, historical backfill, estimation, zero-fill, or post-match leakage.

## Matrix evidence
Column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Decision
No source-backed production correction is safe under the permanent V2.1.1 contract in this run. The separate QA task remains the sole release authority. A new independent workbook-level exhaustive QA certification is still required after the Run 13 remediation candidate before release can move from FAIL-CLOSED.

MASTER_OMI_RELEASE=FAIL-CLOSED

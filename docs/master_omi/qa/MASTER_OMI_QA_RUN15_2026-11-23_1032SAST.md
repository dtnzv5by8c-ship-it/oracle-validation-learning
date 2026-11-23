# Master OMI MI QA — Run 15 — 2026-11-23 10:32 SAST

## Release
RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Scope
Permanent V2.1.1 contract; Formula Input Release Gate; all governed fixtures and all Market Intelligence columns.

## Authoritative artifacts
- Canonical V2.1.1 workbook SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest candidate SHA-256: `56ae85e325de1babfd62d6c0836a9b58a6503ef0a5ada9ae74c3a59d2bb947b5`
- Latest candidate Market Intelligence worksheet XML SHA-256: `bb821c1c9f0cd7e33bae5e3cd3c733a577a8808f701c98ec44ce3052c1b8b4e3`
- Latest authoritative workbook-level QA artifact: `cc46eb23ae91b614eeec7cbf40f3a75ab897faafcca4926eb186d2593372a93f`
- Latest remediation evidence commit reviewed: `5ccf562dad5747e2e7b4ac7f4f2ffe3a8c82b77a`
- Candidate and Run 14 hashes are identical; remediation reports zero workbook changes.

## Exhaustive QA coverage state
- Market Intelligence: 755 rows x 264 columns.
- Governed fixtures: 754/754.
- Heading/comments: 264/264.
- Fixture IDs: 754/754 nonblank and unique.
- Duplicate fixture IDs: 0.
- Excel errors: 0.
- Formulas in audited artifact: 0.
- Governed A:ET numeric-looking text: 15,574 across 21 fields; immutable and not coerced.
- Numeric-looking text outside ET: 25; all are provenance/source-fixture identifiers in GG:GJ.
- Analytical numeric-looking text outside ET: 0.
- Kickoff/date reconciliation: 687 MATCH / 67 REVIEW_REQUIRED.
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- Formula Input: 0/754 READY; 754/754 BLOCKED.
- Backtest: 0/754 READY.
- CMOI: UNAVAILABLE/UNVERIFIED; no output inferred.

## Required intelligence checks
FootyStats PPG/GF/M/GA/M, venue metrics, BTTS/goal intelligence, xG provenance, LTSS V1.1, Last-3/Last-5 chronology, H2H, CMOI, actuals and derived intelligence remain subject to the authoritative Run 14 workbook-level evidence. No new source-backed correction was identified in Run 15. Missing optional evidence is not converted to zero, estimated or guessed.

## Immutable production protections
- A:ET values changed: 0.
- A:ET schema changed: 0.
- Oracle V1.6 changed: 0.
- Source IDs changed: 0.
- No fuzzy matching.
- No timezone normalization.
- No historical backfill.
- No post-match leakage.
- No zero-fill or estimation.

## Coverage matrices
- Column coverage matrix SHA-256: `746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed`
- Row exception matrix SHA-256: `7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45`

## Release blockers
1. 15,574 immutable A:ET numeric-type exceptions.
2. 67 kickoff/date REVIEW_REQUIRED records.
3. 754/754 xG capture timestamps unverified.
4. CMOI unavailable/unverified.
5. 754/754 formula inputs blocked.
6. 0/754 backtest-ready.

## Audit limitation
The latest Run 15 remediation evidence is available, but a new binary-level workbook and independent post-remediation 754 x 264 QA artifact are not exposed in the connected GitHub repository at this run. Therefore this run validates the latest persisted candidate/evidence and preserves fail-closed status; it does not falsely claim a fresh cell-level binary audit of an unavailable workbook.

## 100% QA definition
100% is NOT achieved unless there are zero schema defects, zero unexplained mandatory blanks, zero governed numeric-looking text, zero duplicate fixture IDs, zero Excel errors, zero chronology/leakage/provenance defects, and every unavailable optional value is explicitly classified.

## Final
RELEASE_DECISION=FAIL-CLOSED

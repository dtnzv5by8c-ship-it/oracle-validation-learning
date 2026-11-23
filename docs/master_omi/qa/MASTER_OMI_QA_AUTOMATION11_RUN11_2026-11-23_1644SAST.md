# Master OMI MI QA — Automation Run 11 — 2026-11-23 16:44 SAST

## Release
RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Scope
Permanent V2.1.1 contract; Formula Input Release Gate; all 754 governed fixtures and all 264 Market Intelligence columns.

## Latest remediation reviewed
- Run 20 remediation
- Workbook SHA-256: efeea8101814f7d207d9396cb4182b15a952f2dc3a476e5f51f28a5da4915f8f
- Market Intelligence XML SHA-256: f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830
- Manifest SHA-256: 741aaa66ae4acda98d1b9421612b0ff2f197d5d5addcb700589b5c0c65c7888f
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Exhaustive governed state
- Market Intelligence: 755 rows x 264 columns.
- Governed fixtures: 754/754.
- Heading/comments: 264/264.
- Fixture IDs: 754/754 nonblank and unique.
- Duplicate fixture IDs: 0.
- Excel errors: 0.
- Formulas: 0.
- Governed A:ET numeric-looking text: 15,574 across 21 immutable fields.
- Analytical numeric-looking text outside ET: 0.
- Strict scalar provenance/source-ID text outside ET: 20; five additional compound semicolon-delimited provenance strings are intentionally text.
- Kickoff/date reconciliation: 687 MATCH / 67 REVIEW_REQUIRED.
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- Formula Input: 0/754 READY; 754/754 BLOCKED.
- Backtest: 0/754 READY.
- CMOI: UNAVAILABLE/UNVERIFIED; no output inferred.

## Required intelligence checks
FootyStats PPG/GF/M/GA/M, venue metrics, BTTS/goal intelligence, xG provenance, LTSS V1.1, Last-3/Last-5 chronology, H2H, CMOI, actuals and all derived intelligence remain governed. No source-backed correction was safe to apply without an independent binary-level audit of the Run 20 workbook.

## Production protections
- A:ET values changed: 0.
- Oracle V1.6 changed: 0.
- Source/provenance IDs changed: 0.
- No fuzzy matching.
- No timezone normalization.
- No historical backfill.
- No post-match leakage.
- No zero-fill or estimation.

## Coverage matrices
- Column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Release blockers
1. 15,574 immutable A:ET numeric-type exceptions.
2. 67 kickoff/date REVIEW_REQUIRED records.
3. 754/754 xG capture timestamps unverified.
4. CMOI unavailable/unverified.
5. 754/754 formula inputs blocked.
6. 0/754 backtest-ready.
7. The connected GitHub repository does not expose the Run 20 workbook binary through the available connector, so a fresh independent 754 x 264 binary-level audit cannot be honestly certified.

## 100% QA
Not achieved. Release remains fail-closed until all mandatory gates pass and a fresh independent binary-level audit certifies the candidate.

## Final
RELEASE_DECISION=FAIL-CLOSED

# Master OMI MI QA — Automation Run 11 — 2026-11-23 15:51 SAST

## Release
RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Scope
Permanent V2.1.1 contract; Formula Input Release Gate; all governed fixtures and all 264 Market Intelligence columns.

## Latest GitHub state reviewed
- Latest commit: 0db188d4570d1b05efe742425f870fc046af5553 — Persist public final gate audit.
- Prior remediation evidence: 63111876dfa76b0690163816261c3504e8a6291e — remediation Run 20.
- Latest persisted exhaustive MI QA evidence: 939b6f0e8d6ee8b9929fa82e5af370478fcc238d.
- Latest public final-gate audit artifact: recovery/fixtures/current/intelligence/public_final_gate_audit_summary.json.

## Current exhaustive MI evidence
- Market Intelligence: 755 rows x 264 columns.
- Governed fixtures: 754/754.
- Heading/comments: 264/264.
- Fixture IDs: 754/754 nonblank and unique.
- Duplicate fixture IDs: 0.
- Excel errors: 0.
- Governed A:ET numeric-looking text: 15,574 across 21 immutable fields.
- Numeric-looking text outside ET: 25, all verified GG:GJ provenance/source-fixture IDs.
- Analytical numeric-looking text outside ET: 0.
- Kickoff/date reconciliation: 687 MATCH / 67 REVIEW_REQUIRED.
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- Formula Input: 0/754 READY; 754/754 BLOCKED.
- Backtest: 0/754 READY.
- CMOI: UNAVAILABLE/UNVERIFIED; no output inferred.

## Public final-gate evidence
The latest public final-gate summary is independently persisted at:
recovery/fixtures/current/intelligence/public_final_gate_audit_summary.json
It reports status BLOCKED_FAIL_CLOSED, completion_percent 90, 385 governed fixture rows in that separate public-final-gate scope, 364 exact-identity rows, 21 unmatched rows, V1.6 production certification false, Master OMI final assembled false, A:ET integrity verified false, formula-count preserved false, PIT chronology final verified false, and production_ready false.
This is a separate public-final-gate scope and is not substituted for the 754 x 264 Master OMI MI contract scope.

## Required intelligence checks
FootyStats PPG/GF/M/GA/M, venue metrics, BTTS/goal intelligence, xG provenance, LTSS V1.1, Last-3/Last-5 chronology, H2H, CMOI, actuals and derived intelligence remain governed by the permanent contract. No source-backed correction is safe to apply without a fresh binary-level workbook audit and authoritative source evidence.

## Production protections
A:ET values changed: 0
A:ET schema changed: 0
Oracle V1.6 changed: 0
Source IDs changed: 0
No fuzzy matching; no timezone normalization; no historical backfill; no post-match leakage; no zero-fill/estimation.

## Coverage matrices
Column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Release blockers
1. 15,574 immutable A:ET numeric-type exceptions.
2. 67 kickoff/date REVIEW_REQUIRED.
3. 754/754 xG capture timestamps unverified.
4. CMOI unavailable/unverified.
5. 754/754 formula inputs blocked.
6. 0/754 backtest-ready.
7. Latest candidate workbook binary is not exposed through the connected GitHub repository, so a fresh independent 754 x 264 cell-level binary audit cannot be honestly claimed.

## 100% QA definition
100% requires zero schema defects, zero unexplained mandatory blanks, zero governed numeric-looking text, zero duplicate fixture IDs, zero Excel errors, zero chronology/leakage/provenance defects, and every unavailable optional value explicitly classified.

## Final
RELEASE_DECISION=FAIL-CLOSED

# Master OMI MI QA — Automation Run 11 — 2026-11-23 13:48 SAST

## Release
RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Scope
Permanent V2.1.1 contract; Formula Input Release Gate; all 754 governed fixtures and all 264 Market Intelligence columns.

## Current authoritative state
- Latest remediation: Run 17
- Latest remediation commit: 6a7fa1d67e6aa0fe3fc53c713f549d3b2174ffd5
- Candidate SHA-256: e741eae321e99ded8f3e266e4e0023ed3dff5e26c8fb274a36043abd9fcf0a7c
- Market Intelligence worksheet XML SHA-256: f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Exhaustive persisted coverage
- Market Intelligence: 755 rows x 264 columns
- Governed fixtures: 754/754
- Heading/comments: 264/264
- Fixture IDs: 754/754 nonblank and unique
- Duplicate fixture IDs: 0
- Excel errors: 0
- Formulas: 0
- Governed A:ET numeric-looking text: 15,574 across 21 fields; immutable
- Numeric-looking text outside ET: 25, all verified GG:GJ provenance/source-fixture IDs
- Analytical numeric-looking text outside ET: 0
- Kickoff/date reconciliation: 687 MATCH / 67 REVIEW_REQUIRED
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Formula Input: 0/754 READY; 754/754 BLOCKED
- Backtest: 0/754 READY
- CMOI: UNAVAILABLE/UNVERIFIED; no output inferred

## Required intelligence checks
FootyStats PPG/GF/M/GA/M, venue metrics, BTTS/goal intelligence, xG provenance, LTSS V1.1, Last-3/Last-5 chronology, H2H, CMOI, actuals and derived intelligence remain governed by the permanent contract. No source-backed correction is safe to apply without a fresh binary-level audit and authoritative evidence.

## Remediation integrity
Run 17 performed 21,749 type-only conversions in append-only fields outside ET. A:ET values/XML/schema, Oracle V1.6, and source/provenance IDs were unchanged.

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
7. No fresh independent binary-level 754 x 264 QA artifact exposed after Run 17 remediation.

## Audit limitation
The connected repository exposes remediation evidence and workbook/worksheet hashes, but not the candidate workbook binary or a fresh independent 754 x 264 cell-level QA artifact. This run therefore verifies the latest persisted evidence, remediation integrity, coverage state and fail-closed posture; it does not falsely claim a binary-level cell audit.

## 100% QA definition
100% requires zero schema defects, zero unexplained mandatory blanks, zero governed numeric-looking text, zero duplicate fixture IDs, zero Excel errors, zero chronology/leakage/provenance defects, and every unavailable optional value explicitly classified.

## Final
RELEASE_DECISION=FAIL-CLOSED

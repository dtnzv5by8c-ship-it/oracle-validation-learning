# Master OMI MI QA — Automation Turn 11 — 2026-11-25 13:59 SAST

RELEASE_DECISION=FAIL-CLOSED

## Scope
Permanent V2.1.1 Master OMI contract; Formula Input Release Gate; 754 governed fixtures × 264 Market Intelligence columns. Oracle V1.6 preserved exactly. A:ET immutable.

## Latest remediation reviewed
Run 64 remediation evidence:
- Commit: 02e5119c8ba292b29652e30aa68d0fe8adbf2df1
- Candidate workbook SHA-256: f75309cedb203bd7e3aafda14b19eae230f02a63af9e5302603cc2a0eb1506cc
- Candidate sheet3.xml SHA-256: 6fc167e0ac52f864d8988983664ac11343149f2189c26e795726bc4f5aa5e79f
- Canonical workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical sheet3.xml SHA-256: bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf
- 21,749 authorised numeric-looking analytical cells changed from inline-string to native Excel numeric type; analytical values changed: 0.
- A:ET XML/value/type equality: PASS, 96,641 cells identical.
- Non-MI ZIP members: unchanged.
- Residual analytical numeric-looking text outside ET: 0.
- Residual numeric-looking strings outside ET: 25, all verified GG:GJ FootyStats provenance/source-fixture IDs.
- Genuine nonnumeric controlled-range values: 117, preserved.

## Governed QA controls
- Market Intelligence: 755 rows × 264 columns.
- Governed fixtures: 754.
- Fixture IDs: 754/754 nonblank and unique.
- Duplicate Fixture IDs: 0.
- Formula cells: 0.
- Excel error literals: 0.
- Overall source IDs: 754/754.
- History/pre-match cutoff fields: 754/754 populated.
- Schedule exceptions: 67/754 REVIEW_REQUIRED / KICKOFF_MISMATCH.
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- LTSS/team-score: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH.
- H2H Sample N: 754/754.
- Production Eligible: 0/754.
- Betting Eligible: 0/754.
- Formula Input/backtest: BLOCKED.
- CMOI: UNAVAILABLE/UNVERIFIED; no CMOI fields exist in the permanent 264-column contract.
- Immutable A:ET numeric-looking analytical values: 15,574.
- Authorised governed analytical numeric-type conversions: 21,749.
- Actuals exception: 41 populated research-actual rows with blank immutable DI review status.

## Exception matrix
The 41 actual-status rows remain:
4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402.

No DI status was inferred. No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema mutation, Oracle V1.6 redesign, or unsupported leakage remediation was performed.

## Matrix hashes
Column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Certification limitation
The exact Run 64 XLSX binary is not exposed through the connected GitHub file surface. The repository exposes the Run 64 remediation manifest and direct SHA/XML integrity evidence, but not the workbook bytes required for an independent fresh workbook/XML audit. Therefore this cycle does not claim independent binary certification of Run 64. The release gate remains fail-closed.

## Release
FAIL-CLOSED. 100% QA is not demonstrated.

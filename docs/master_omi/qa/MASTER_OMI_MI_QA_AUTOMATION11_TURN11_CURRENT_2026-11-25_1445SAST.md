# Master OMI MI QA — Automation Turn 11 — 2026-11-25 14:45 SAST

RELEASE_DECISION=FAIL-CLOSED

## Scope
Permanent V2.1.1 Master OMI contract; Formula Input Release Gate; 754 governed fixtures × 264 Market Intelligence production columns. Oracle V1.6 preserved exactly. A:ET immutable.

## Latest evidence reviewed
Latest repository commits at audit time include:
- 154e0e69cd3069f671eaaad643cd40194c75e7a4 — Add current FootyStats fixture intelligence
- 1b62589da0d7b2c3bf46ebf0bc3f06f7d877a8fa — Add current FootyStats governed fixture reconciliation
- 02e5119c8ba292b29652e30aa68d0fe8adbf2df1 — Master OMI MI remediation Run 64 evidence
- e679927362d4d0bec9ae047e26620a600e68b1e4 — latest prior 13:59 SAST QA record

Run 64 candidate workbook SHA-256: f75309cedb203bd7e3aafda14b19eae230f02a63af9e5302603cc2a0eb1506cc
Run 64 sheet3.xml SHA-256: 6fc167e0ac52f864d8988983664ac11343149f2189c26e795726bc4f5aa5e79f
Canonical workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Canonical sheet3.xml SHA-256: bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf

## Full governed controls
- Market Intelligence production surface: 755 rows × 264 columns.
- Governed fixtures: 754.
- Fixture IDs: 754/754 populated and unique.
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
- Residual analytical numeric-looking text outside ET: 0.
- Residual numeric-looking strings outside ET: 25, all verified GG:GJ FootyStats provenance/source-fixture IDs.
- Genuine nonnumeric controlled-range values: 117, preserved.
- Authorised governed analytical numeric-type conversions: 21,749.
- Immutable A:ET numeric-looking analytical values: 15,574.
- A:ET XML/value/type equality versus canonical: PASS for the audited Run 64 evidence (96,641 cells).

## CMOI control
CMOI is governed as a separate research schema, not as promoted Oracle V1.6 production logic. The CMOI validation closure explicitly states CMOI is RESEARCH_ONLY / NOT PROMOTED / FAIL-CLOSED, with two append-only research fields (CMOI_MATCH_OUTCOME and CMOI_CONFIDENCE) outside the 264-column production surface. The current 264-column production contract therefore does not contain promoted CMOI fields. No CMOI value is inferred, guessed, or silently backfilled. CMOI remains UNAVAILABLE/UNVERIFIED for production Formula Input/Betting eligibility pending its own promotion gates.

## Exception matrix
The 41 populated research-actual rows with blank immutable DI review status remain:
4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402.

No DI status was inferred. No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema mutation, Oracle V1.6 redesign, or unsupported leakage remediation was performed.

## Matrix hashes
Column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Certification limitation
The exact Run 64 XLSX binary is not exposed through the connected GitHub file surface. The repository exposes the remediation manifest and direct workbook/XML hashes, but not the workbook bytes required for a fresh independent workbook/XML audit. Therefore this cycle does not claim independent binary certification of Run 64.

## Release
FAIL-CLOSED. 100% QA is not demonstrated.

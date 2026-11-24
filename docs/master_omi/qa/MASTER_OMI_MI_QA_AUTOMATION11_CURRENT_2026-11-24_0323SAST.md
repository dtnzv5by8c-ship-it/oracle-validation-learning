# Master OMI MI QA — Automation Run 11 — 2026-11-24 03:23 SAST

## Release
RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Contract and scope
- Permanent contract: Master OMI V2.1.1
- Production model: Oracle V1.6
- Market Intelligence: 755 rows x 264 columns = 754 governed fixture rows x 264 MI columns
- Canonical baseline SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Audited Run 29 workbook SHA-256: `efeea8101814f7d207d9396cb4182b15a952f2dc3a476e5f51f28a5da4915f8f`
- Market Intelligence sheet XML SHA-256: `5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde`

## Direct binary audit
- Schema headings: 264/264 present
- Header comments: 264/264 present
- Blank headings: 0
- Header-name duplicates: 3 groups; existing canonical duplicate headings are preserved and are not treated as silent renames/reordering
- Fixture IDs: 754/754 nonblank and unique
- Duplicate fixture IDs: 0
- Formula cells: 0
- Excel error cells: 0
- A:ET value differences vs canonical: 0
- A:ET native-type differences vs canonical: 0
- ZIP/package changes: sheet3.xml only, consistent with append-only type remediation

## Numeric type gate
- Governed analytical numeric-looking text outside immutable A:ET: 0
- Remaining numeric-looking text outside ET: 25, all GG:GJ FootyStats provenance/source-fixture IDs and intentionally retained as text
- Immutable A:ET numeric-looking text: 15,574; unchanged and therefore still a release blocker under the permanent gate
- Type-only remediation performed: 21,749 analytical cells converted to native Excel numerics in EW:FB, FG:FL, FO:GB and HD:HF
- Analytical values changed by remediation: 0

## Identity, chronology and provenance
- FootyStats source/join status: 754/754 EXACT_FIXTURE_ID_JOIN
- Fixture identity: exact; no fuzzy matching
- Schedule reconciliation: 67 REVIEW_REQUIRED; no timezone normalization or silent correction
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- xG prediction use: 754/754 QUARANTINED_RESEARCH_AUDIT_ONLY
- xG betting eligibility: 754/754 NO
- FootyStats data-quality status: 754/754 GOOD_RESEARCH_EVIDENCE

## Market Intelligence checks
- FootyStats Last-5 PPG/GF/M/GA/M fields present and numerically typed in append-only layer
- Venue PPG/GF/M/GA/M fields: no unsupported correction made; unavailable evidence remains represented as missing/explicit source status
- BTTS and goal-market intelligence: retained; no inferred values added
- LTSS V1.1: 754/754 version marker; 406 BACKTESTED_LEAGUE_WINDOW and 348 STATE_FALLBACK_RESEARCH
- Last-3 PPG: explicit N/A where evidence is unavailable; no zero-fill
- H2H: retained under existing research-only governance; no identity rewrite
- Actuals: 275 ACTUAL VERIFIED; remaining rows are not silently promoted to verified actuals
- CMOI: no production promotion; research output remains UNAVAILABLE/UNVERIFIED and no output was inferred
- Derived intelligence: no unsupported recalculation or value substitution

## Formula Input Release Gate
- Formula Input READY: 0/754
- Formula Input BLOCKED: 754/754
- Backtest READY: 0/754
- RELEASE: FAIL-CLOSED

## Persisted matrices
- Column coverage matrix SHA-256: `746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed`
- Row exception matrix SHA-256: `7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45`

## Exceptions requiring further evidence
1. 15,574 immutable A:ET numeric-type exceptions.
2. 67 schedule kickoff/date REVIEW_REQUIRED records.
3. 754/754 xG temporal provenance records without verified capture timestamps.
4. 754/754 Formula Input BLOCKED.
5. 0/754 backtest-ready.
6. CMOI remains unavailable/unverified and is not promoted.
7. No source-backed basis exists for estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, or leakage remediation.

## Fixes
No additional source-backed data correction was justified in this audit. Run 29's 21,749 supported numeric-type conversions were independently rechecked and confirmed type-only. A:ET and Oracle V1.6 remain exactly preserved.

## Certification
100% QA is NOT achieved. RELEASE_DECISION remains FAIL-CLOSED until all mandatory gates pass and the Formula Input Release Gate is independently satisfied.

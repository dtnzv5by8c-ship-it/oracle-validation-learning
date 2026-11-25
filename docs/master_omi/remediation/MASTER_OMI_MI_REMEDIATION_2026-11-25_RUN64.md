# Master OMI MI Remediation Evidence — Run 64 — 2026-11-25

RELEASE_DECISION=FAIL-CLOSED

## Authoritative QA
- Latest QA evidence: `docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_1227SAST.md`
- QA blob SHA-1: `1375bd5a132b2980e5f45e301261777539e44023`
- QA commit: `db59b56add16923826d79408ba1da01fde0b028b`
- QA decision: **FAIL-CLOSED**

## Canonical baseline
- Workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Market Intelligence: 755 rows × 264 columns
- Governed fixtures: 754
- Immutable production boundary: A:ET
- Oracle V1.6: unchanged

## Authoritative source evidence
- Prior authorised remediation evidence: Run 59, GitHub blob SHA `37b5640ff54479ec6b93a467add8f84304449882`
- Run 59 established exactly 21,749 supported governed analytical numeric-looking text cells for type-only conversion in `EW:FB`, `FG:FL`, `FO:GB`, `HD:HF`; analytical values changed: 0.
- Latest FootyStats fixture reconciliation: `recovery/fixtures/current/governed_fixture_reconciliation_summary.json`, blob SHA `fa38d0d00581bcc8ef54fc56c929291d635bd796`.

## Remediation performed
The candidate was rebuilt **from the canonical workbook**, not from Run 63. Only the 21,749 previously authorised governed analytical cells were changed from inline-string numeric-looking text to native Excel numeric cells. No values were altered.

- Total cells changed: **21,749**
- EW:FB: **4,524**
- FG:FL: **4,407**
- FO:GB: **10,556**
- HD:HF: **2,262**
- Before → after type: **inline-string → numeric: 21,749**
- Analytical value changes: **0**
- A:ET cells changed: **0**
- Residual analytical numeric-looking text outside ET: **0**
- Residual numeric-looking strings outside ET: **25**, all verified GG:GJ FootyStats provenance/source-fixture IDs
- Genuine nonnumeric text in controlled numeric ranges: **117**, preserved

The complete cell-by-cell before/after manifest is `MASTER_OMI_RUN64_CELL_CHANGE_MANIFEST_EXACT.tsv`.

## Direct integrity validation
- Candidate SHA-256: `f75309cedb203bd7e3aafda14b19eae230f02a63af9e5302603cc2a0eb1506cc`
- Candidate sheet3.xml SHA-256: `6fc167e0ac52f864d8988983664ac11343149f2189c26e795726bc4f5aa5e79f`
- Canonical sheet3.xml SHA-256: `bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf`
- A:ET cell XML/value/type equality vs canonical: **PASS — 96,641 A:ET cells identical**
- Non-MI ZIP members vs canonical: **unchanged**

## QA-owned unresolved exceptions
- 15,574 immutable A:ET numeric-looking analytical values.
- 41 populated research-actual rows with blank immutable DI review status.
- 67/754 schedule records: REVIEW_REQUIRED / KICKOFF_MISMATCH.
- 754/754 xG temporal provenance: UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- LTSS/team-score: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH.
- H2H Sample N: 754/754.
- Production Eligible: 0/754.
- Betting Eligible: 0/754.
- Formula Input/backtest: BLOCKED.
- CMOI: UNAVAILABLE/UNVERIFIED; no CMOI fields exist in the permanent 264-column contract.

No DI status was inferred. No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema mutation, Oracle V1.6 redesign, or unsupported post-match leakage remediation was performed.

## Release
**FAIL-CLOSED.** The separate QA task remains the sole release authority and must independently re-audit the exact Run 64 binary.
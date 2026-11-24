# Master OMI MI Remediation — Run 32 — 2026-11-24

RELEASE_DECISION=FAIL-CLOSED

## Authoritative inputs
- Canonical V2.1.1 workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest QA: `docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_CURRENT_2026-11-24_0323SAST.md`
- QA commit: `9f7549834e586f9d66b4451f8c433977e90f8312`
- QA decision: `FAIL-CLOSED`

## Remediation
- Exactly **21,749** governed analytical numeric-looking text cells converted from `inlineStr` to native Excel numeric.
- Governed fields: `EW:FB`, `FG:FL`, `FO:GB`, `HD:HF`.
- Analytical values changed: **0**.
- Remaining governed analytical numeric-looking text outside ET: **0**.
- Remaining numeric-looking provenance/source IDs outside ET: **25**, preserved as text in `GG:GJ`.

## Direct validation
- Market Intelligence: **755 x 264**.
- Governed fixtures: **754**.
- A:ET cell fragments: **byte-identical** to canonical.
- ZIP entries changed: **sheet3.xml only**.
- Oracle V1.6: unchanged.
- Source/provenance IDs: unchanged.

## Hashes
- Candidate workbook: `5cd77c447e78665636702be818a9f12a443525165cf761eb9d0e0cd8f5f3c029`
- Candidate Market Intelligence XML: `8ef91f3feb9bece66672caf56ea3d31e88b81734ddad67fa7d283ee8b1ae122b`
- Cell-change manifest: `74de1f4dcda7396a3cbf6cd5bfaa6f8da8ec0920e4817204639b50b63cf5e38a`

## Unresolved exceptions for independent QA
1. 15,574 immutable A:ET numeric-type exceptions; not mutated.
2. 67 schedule kickoff/date `REVIEW_REQUIRED`; no timezone normalization or silent correction.
3. 754/754 xG temporal provenance `UNVERIFIED_NO_CAPTURE_TIMESTAMP`.
4. 754/754 Formula Input `BLOCKED`.
5. 0/754 Backtest `READY`.
6. CMOI remains `UNAVAILABLE/UNVERIFIED`; no output inferred.
7. Venue metrics, Last-3/Last-5 chronology, H2H, BTTS/goal intelligence, LTSS, actuals and derived fields were not changed without authoritative source evidence supporting a safe correction.

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, or post-match leakage remediation was performed.

Release remains **FAIL-CLOSED**. The separate Master OMI MI QA task is the release authority and must independently re-audit the candidate.

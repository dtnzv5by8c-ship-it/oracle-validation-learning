# Master OMI MI Remediation Run 63 — 2026-11-25

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Authoritative QA
- Latest QA evidence: `docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_0952SAST.md`
- QA commit: `3af426a2cf78448ad4d1d943299d7f7631f482e1`
- QA file SHA: `84523395792900d2a7aff2ceeadd7ecc241399cc`
- QA decision: FAIL-CLOSED
- QA states latest GitHub commit at audit time was `014b7ea4c513b91586601adf4697e7441f23b933` and no newer QA/remediation commit was exposed by commit search at that audit time.

## Canonical / contract
- Canonical V2.1.1 SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Oracle V1.6 preserved exactly.
- A:ET immutable.
- Permanent numeric data-type rule: `docs/master_omi/MASTER_OMI_FORMULA_INPUT_DATA_TYPE_CONTRACT_2026-11-20.md`.

## Remediation
- Run 63 starts from the controlled Run 62 candidate, which itself was rebuilt from the canonical V2.1.1 baseline and applied only the authorised append-only numeric type correction.
- Latest QA evidence identifies no new source-backed production mutation beyond the already-authorised numeric type correction.
- Run 63 additional cells changed: **0**.
- Analytical value changes: **0**.
- A:ET changes: **0**.
- Oracle V1.6 changes: **0**.
- No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, or post-match leakage remediation was performed.

## Direct validation
- Market Intelligence shape: **755 x 264**
- Governed fixtures: **754**
- Fixture IDs: **754/754 nonblank + unique**
- Duplicate Fixture IDs: **0**
- Immutable A:ET numeric-looking analytical values: **15,574**
- Remaining outside-ET numeric-looking strings: **25**; all are verified `GG:GJ` FootyStats provenance/source-fixture IDs per latest QA.
- Formula cells: **0**
- Excel error literals: **0**

## Authoritative unresolved exceptions
- Schedule REVIEW_REQUIRED: **67/754**, all KICKOFF_MISMATCH.
- xG temporal provenance: **754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP**.
- LTSS/team-score: **406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH**.
- H2H Sample N: **754/754**.
- Production Eligible: **0/754**.
- Betting Eligible: **0/754**.
- Formula Input/backtest: **BLOCKED**.
- CMOI: **UNAVAILABLE/UNVERIFIED**; no CMOI fields exist in the permanent 264-column contract.
- Direct validation confirms **41** populated research-actual rows with blank immutable DI review status: `4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402`.

## Hashes
- Candidate workbook SHA-256: `32921bf4575525862b486c9b76b199e6050c22e91e29c4def943193f25da5731`
- `sheet3.xml` SHA-256: `6fc167e0ac52f864d8988983664ac11343149f2189c26e795726bc4f5aa5e79f`
- Cell-change manifest SHA-256: `6784d47a40e88df6d057f0e6f7cd4d06f44632601ead429b4fb015d9a59d8749`

## Release
**FAIL-CLOSED.** The separate QA task must independently re-audit the exact Run 63 binary and decide release status.

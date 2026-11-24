# Master OMI MI Remediation — Run 42 — 2026-11-24

## Release posture

**RELEASE_DECISION=FAIL-CLOSED**

No release PASS is declared. The separate Master OMI MI QA task remains the sole release authority and must independently re-audit the exact Run 42 binary.

## Authoritative baseline

- Canonical workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Canonical Market Intelligence XML SHA-256: `bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf`
- Market Intelligence contract: 755 rows × 264 columns
- Governed fixtures: 754
- Immutable production boundary: `A:ET`
- Oracle V1.6: preserved exactly

## Latest authoritative QA evidence consumed

- GitHub repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- QA evidence: `docs/master_omi/qa/MASTER_OMI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-24_1034SAST.md`
- QA evidence commit: `c7aea71f37e68c77a3054ed84bf0575a0368d5e4`
- QA decision: `FAIL-CLOSED`
- QA audited workbook: `Oracle_Master_OMI_V2_1_1_REMEDIATION_RUN37_2026-11-24_EXACT_AET.xlsx`
- QA audited workbook SHA-256: `bd7ba47c05fce966f2b6f4155776b25d37dc84dccafbeca92dd5b3429abeef49`

## Direct cell-level reconciliation before change

A fresh direct scan was performed against the canonical baseline, not against a prior candidate.

- Total numeric-looking text in canonical workbook: **37,348**
- Numeric-looking text inside immutable `A:ET`: **15,574**
- Numeric-looking text outside `ET`: **21,774**
- Supported governed analytical numeric-looking text outside `ET`: **21,749**
- Genuine numeric-looking provenance/source-ID strings outside `ET`: **25**
- Fixture IDs: **754/754 nonblank and unique**
- Formula cells: **0**
- Excel error literals: **0**

The 25 non-analytical numeric-looking strings are genuine FootyStats provenance/source-fixture identifiers in `GG:GJ` and were preserved as text.

This direct scan resolves the recurring QA-matrix/direct-scan discrepancy: the latest QA evidence audited the already-remediated Run 37 binary, while this remediation is required to start from the immutable canonical baseline. The canonical baseline count is therefore the authoritative starting-state count for this run.

## Remediation applied

Only the supported append-only data-type defect was corrected.

Exactly **21,749** cells were converted from Excel `inlineStr` numeric-looking text to native Excel numeric cells. No underlying analytical value was changed.

Governed ranges:

- `EW:FB` — Last-5 PPG / GF/M / GA/M
- `FG:FL` — venue PPG / GF/M / GA/M
- `FO:GB` — BTTS / goal-market analytical rates
- `HD:HF` — pre-match xG audit fields

The 112 non-numeric `INSUFFICIENT_DATA` strings encountered in governed ranges were preserved as genuine explicit classification text; they were not coerced or zero-filled.

## Provenance / source IDs

Every changed cell is captured in `MASTER_OMI_RUN42_CELL_CHANGE_MANIFEST_EXACT.tsv` with cell address, canonical Fixture ID from `AM`, before/after value and type, and `GG:GJ` FootyStats source-fixture IDs. No source/provenance identifier was changed.

## Integrity controls

- Run 42 candidate workbook SHA-256: `efeea8101814f7d207d9396cb4182b15a952f2dc3a476e5f51f28a5da4915f8f`
- Run 42 Market Intelligence XML SHA-256: `5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde`
- Run 42 A:ET fragment SHA-256: `55c5b9e5f67295c042457041ada630407158f0cc86ea2c70f478103e235806a8`
- Canonical A:ET fragment SHA-256: `55c5b9e5f67295c042457041ada630407158f0cc86ea2c70f478103e235806a8`
- Run 42 cell-change manifest SHA-256: `2e805b5fb801797d16f211b846405d64f9290884e8f8f03454438a4280ef0aa9`
- Package entries changed: **`xl/worksheets/sheet3.xml` only**
- Analytical value changes: **0**
- A:ET value/type/schema changes: **0**
- Oracle V1.6 changes: **0**

## Latest QA exceptions deliberately left unchanged

1. **15,574 immutable A:ET numeric-looking text cells** — prohibited from mutation by the production contract.
2. **CMOI:** the 264-column Run 37 MI contract contains no CMOI columns. The separately inspected locked CMOI workbook reports CMOI Match Outcome and CMOI Confidence blank for all 754 governed rows; therefore CMOI remains explicitly **UNAVAILABLE/UNVERIFIED**, with no inferred values imported.
3. **xG temporal provenance:** **754/754 `UNVERIFIED_NO_CAPTURE_TIMESTAMP`**; no timestamp evidence was invented or backfilled. xG betting eligibility remains **0/754**.
4. **Formula Input / backtest:** mandatory gates remain blocked; no release-ready backtest was inferred.
5. **Schedule/date reconciliation:** unresolved kickoff/date exceptions remain review-only; no timezone normalization or automatic correction was applied.
6. Any venue, Last-3/Last-5 chronology, H2H, BTTS/goal, LTSS, actual or derived-field discrepancy without authoritative source evidence remains unchanged.

## Prohibited actions explicitly not performed

No estimation, invention, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewrite, A:ET mutation, Oracle V1.6 modification, or post-match leakage remediation was performed.

## Candidate

`Oracle_Master_OMI_V2_1_1_REMEDIATION_RUN42_2026-11-24_EXACT_AET.xlsx`

The candidate is derived directly from the canonical V2.1.1 baseline with only the 21,749 supported append-only numeric-type corrections above.

**Release remains FAIL-CLOSED.** The separate Master OMI MI QA task must independently audit the exact Run 42 binary and decide release status.

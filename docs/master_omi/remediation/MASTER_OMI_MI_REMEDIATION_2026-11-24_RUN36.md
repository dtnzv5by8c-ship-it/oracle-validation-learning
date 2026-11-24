# Master OMI MI Remediation Run 36 — 2026-11-24

## Release status

`RELEASE_DECISION=FAIL-CLOSED`

This remediation does not declare release PASS. The separate Master OMI MI QA process remains the release authority and must independently re-audit the exact Run 36 binary.

## Authoritative inputs

### Canonical V2.1.1 baseline
- Workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Market Intelligence contract: 755 rows × 264 columns
- Immutable production boundary: `A:ET` (150 columns)
- Oracle V1.6: preserved exactly

### Latest QA evidence
- QA file: `qa/master_omi_mi_qa_automation_turn11_2026-11-24_0634SAST.md`
- QA commit: `1a9d780e8117ffafc059d8d73aa5d3c4f92dc58e`
- QA audited workbook SHA-256: `4da0f8e92afba24e989bd6025e36e9e30ffbd9eaa16956099b8a74f0342b63cc`
- QA decision: `FAIL-CLOSED`

## Important QA/direct-scan discrepancy resolved

The latest QA artifact audits a **different 755 × 266 workbook**:
`Oracle_Master_OMI_Report_14-24_Nov_2026_MARKET_INTELLIGENCE_QA.xlsx`.

Its reported counts are:
- numeric-looking text in immutable A:ET: 5,158
- numeric-looking text outside ET: 0
- CMOI_MATCH_OUTCOME populated: 387/754
- CMOI_MATCH_OUTCOME blank: 367/754
- xG temporal provenance: 754/754 `UNVERIFIED_NO_CAPTURE_TIMESTAMP`

Because the remediation instruction requires starting from the canonical V2.1.1 baseline, the canonical workbook was independently scanned at cell level before any change.

Authoritative canonical direct-scan counts:
- Market Intelligence: **755 × 264**
- Governed fixture rows: **754**
- Numeric-looking analytical text outside immutable A:ET: **21,749**
- Numeric-looking text inside immutable A:ET: **15,574**
- Fixture IDs: **754/754 nonblank and unique**
- Formula cells: **0**
- Excel error cells: **0**

The 21,749 outside-ET cells are in governed analytical numeric fields and are valid numeric-looking values. The latest QA's `0` outside-ET count therefore cannot be applied to the canonical baseline because it refers to a different 266-column audited workbook. The canonical direct scan is the authoritative count for the starting artifact used in this remediation.

The 15,574 A:ET count is likewise authoritative for the canonical baseline and was **not changed**, because A:ET is immutable.

## Remediation applied

Only the supported append-only data-type defect was corrected.

Exactly **21,749** cells were converted from Excel `inlineStr` text to native Excel numeric cells.

Governed ranges:
- `EW:FB` — FootyStats Home/Away Last-5 PPG, GF/M, GA/M
- `FG:FL` — FootyStats Home/Away Venue PPG, GF/M, GA/M
- `FO:GB` — FootyStats BTTS / goal-market percentages
- `HD:HF` — FootyStats pre-match xG audit values

Conversion was type-only:
- analytical value changes: **0**
- text-to-number conversions: **21,749**
- numeric-looking analytical text remaining outside ET: **0**
- genuine text preserved: **25** numeric-looking `GG:GJ` FootyStats provenance/source-fixture identifiers

For every changed cell, the manifest records:
- cell address
- fixture ID
- field heading
- before value/type
- after value/type
- QA source commit
- FootyStats source-fixture IDs from `GG:GJ`

## Direct validation after remediation

| Control | Result |
|---|---:|
| Market Intelligence | 755 × 264 |
| Governed fixture rows | 754 |
| Fixture IDs nonblank/unique | 754/754 |
| Duplicate fixture IDs | 0 |
| Native numeric cells created | 21,749 |
| Governed numeric-looking text outside ET | 0 |
| Residual numeric-looking strings outside ET | 25 |
| Immutable A:ET numeric-looking text | 15,574 |
| A:ET cell-fragment hash vs canonical | identical |
| Formula cells | 0 |
| Excel error cells | 0 |
| ZIP/package entries changed | 1 (`xl/worksheets/sheet3.xml`) |

### Immutable A:ET verification

Canonical A:ET cell-fragment SHA-256:
`2978469e364a0627697600e60b451a8e126503e479029b36e74909d71ce04367`

Run 36 A:ET cell-fragment SHA-256:
`2978469e364a0627697600e60b451a8e126503e479029b36e74909d71ce04367`

Result: **byte-identical at the cell-fragment level**.

## Hashes

- Canonical workbook SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Canonical Market Intelligence XML SHA-256: `bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf`
- Run 36 candidate workbook SHA-256: `bd7ba47c05fce966f2b6f4155776b25d37dc84dccafbeca92dd5b3429abeef49`
- Run 36 Market Intelligence XML SHA-256: `3fc03157acd7f01657a428d8d6e3261d6234516ea8524893f46cb58ccf013df1`
- Run 36 cell-change manifest SHA-256: `225d3048986917769cb39a1a25a21de0e6f874c48180328b8fd72b01230bcdc5`

## Unresolved exceptions — explicitly left for QA

1. **15,574 immutable A:ET numeric-looking text cells** — unchanged by contract.
2. **367/754 CMOI output pairs blank** in the latest QA evidence. The latest authoritative CMOI cross-check reports zero additional values and zero differences for populated rows; no safe correction exists.
3. **754/754 xG temporal provenance `UNVERIFIED_NO_CAPTURE_TIMESTAMP`** — no timestamp evidence was invented or backfilled.
4. Formula Input / backtest eligibility remains blocked by mandatory gates.
5. Schedule reconciliation remains subject to the QA evidence; no timezone normalization or silent correction was applied.
6. H2H remains research-only; no identity rewrite was performed.
7. Last-3/Last-5 chronology, venue metrics, BTTS/goal intelligence, LTSS, actuals and derived fields were not altered where the evidence did not establish a safe source-backed correction.

## Prohibited actions not performed

- no estimation
- no zero-fill
- no fuzzy matching
- no timezone normalization
- no historical backfill
- no unsupported provenance substitution
- no fixture identity rewrite
- no Oracle V1.6 change
- no A:ET mutation
- no post-match leakage remediation

## Certification

Run 36 is a **candidate remediation artifact only**.

`RELEASE_DECISION=FAIL-CLOSED`

The separate QA task must independently re-audit the exact Run 36 workbook and decide release status.
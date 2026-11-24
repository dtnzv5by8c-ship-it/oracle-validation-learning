# Master OMI MI Remediation — Run 29

**Release decision:** FAIL-CLOSED

## Authoritative inputs

- Canonical V2.1.1 workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest authoritative QA: `docs/master_omi/qa/MASTER_OMI_QA_AUTOMATION11_CURRENT_2026-11-23_2348SAST.md`
- QA commit: `e1ee4b98a19f73af96c706ad2f5ca9495a90017d`
- QA file blob SHA: `b76191436fe6de32f0ab5afb36e9c2e4ed6bf0fe`
- QA decision: `FAIL-CLOSED`
- Latest QA reviewed candidate: Run 24
- Column coverage matrix SHA-256: `746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed`
- Row exception matrix SHA-256: `7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45`

## Remediation

Run 29 rebuilt from the canonical V2.1.1 baseline.

The latest QA evidence identifies:
- 21,749 governed analytical numeric-looking text cells outside immutable A:ET.
- 25 numeric-looking values outside ET are genuine FootyStats provenance/source-fixture IDs in GG:GJ and remain text.
- 15,574 numeric-looking values inside immutable A:ET remain unchanged.

Exactly **21,749** supported analytical cells were converted from Excel inline-string text to native Excel numeric cells. Lexical numeric values were preserved exactly.

Governed converted columns: `EW:FB`, `FG:FL`, `FO:GB`, `HD:HF`.

No source-backed correction was justified for CMOI, FootyStats metrics beyond the type defect, venue metrics, Last-3/Last-5 chronology, H2H, BTTS/goal intelligence, xG provenance, LTSS, source IDs, actuals, or derived intelligence.

## Direct validation

- Market Intelligence: **755 × 264**
- Governed fixtures: **754/754**
- Fixture IDs: **754/754 nonblank and unique**
- Duplicate fixture IDs: **0**
- Analytical numeric-looking text outside ET after remediation: **0**
- Remaining numeric-looking text outside ET: **25**, all in GG:GJ
- Immutable A:ET numeric-looking text: **15,574**, unchanged
- Formula cells: **0**
- Excel error cells: **0**
- ZIP/package entries changed: **1** (`xl/worksheets/sheet3.xml` only)
- A:ET cell fragments changed: **0**
- Oracle V1.6 changes: **0**
- Source/provenance ID changes: **0**
- Analytical value changes: **0**; conversions were type-only

### Per-column conversion counts

EW 754; EX 754; EY 754; EZ 754; FA 754; FB 754; FG 734; FH 735; FI 734; FJ 735; FK 734; FL 735; FO 754; FP 754; FQ 754; FR 754; FS 754; FT 754; FU 754; FV 754; FW 754; FX 754; FY 754; FZ 754; GA 754; GB 754; HD 754; HE 754; HF 754.

## Source/provenance trace

The accompanying manifest records every changed cell with cell address, fixture ID from AM, field heading, before/after value and type, row-level GG:GJ provenance IDs, canonical SHA-256, and authoritative QA artifact identifier.

The 25 residual numeric-looking GG:GJ values were not converted because they are provenance/source-fixture IDs, not analytical measurements.

## Integrity hashes

- Candidate workbook SHA-256: `efeea8101814f7d207d9396cb4182b15a952f2dc3a476e5f51f28a5da4915f8f`
- Market Intelligence worksheet XML SHA-256: `5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde`
- Run 29 A:ET cell-fragment SHA-256: `cebd8755b0e80fda9b941b76f2a47b71bec78f043b1a40e795b02827e437561c`
- Cell-change manifest SHA-256: `bfc391bd567a867454a0fbc5ea3a150bd3c48aecdf258175dd0c6ef57e57dcfe`
- Latest QA file SHA: `b76191436fe6de32f0ab5afb36e9c2e4ed6bf0fe`

## Unresolved exceptions

- **15,574** immutable A:ET numeric-type exceptions.
- **67** kickoff/date REVIEW_REQUIRED.
- **754/754** xG temporal provenance UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- CMOI UNAVAILABLE/UNVERIFIED; no output inferred.
- **754/754** Formula Input BLOCKED.
- **0/754** Backtest Ready.
- No fresh independent binary-level 754 × 264 certification of the Run 29 binary.

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, or post-match leakage was introduced.

## Release

**RELEASE_DECISION=FAIL-CLOSED**

The separate Master OMI MI QA automation remains the sole release authority and must independently re-audit the Run 29 binary.

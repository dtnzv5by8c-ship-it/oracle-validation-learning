# Master OMI MI Remediation — Run 28 — 2026-11-24

RELEASE_DECISION=FAIL-CLOSED

## Authoritative inputs
- Canonical V2.1.1 workbook SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest QA: `docs/master_omi/qa/MASTER_OMI_QA_AUTOMATION11_CURRENT_2026-11-23_2348SAST.md`
- Latest QA commit: `e1ee4b98a19f73af96c706ad2f5ca9495a90017d`
- Latest QA file blob SHA: `b76191436fe6de32f0ab5afb36e9c2e4ed6bf0fe`
- QA decision: `FAIL-CLOSED`

## Remediation
Run 28 rebuilt from the canonical baseline. Only governed append-only numeric fields outside immutable A:ET were examined for supported type defects.

- Supported conversions: **21,749**
- Governed analytical numeric-looking text remaining in governed ranges: **0**
- Immutable A:ET changes: **0**
- Oracle V1.6 changes: **0**
- Source/provenance ID changes: **0**
- Analytical values changed: **0**

Column conversion counts: EW 754; EX 754; EY 754; EZ 754; FA 754; FB 754; FG 734; FH 735; FI 734; FJ 735; FK 734; FL 735; FO 754; FP 754; FQ 754; FR 754; FS 754; FT 754; FU 754; FV 754; FW 754; FX 754; FY 754; FZ 754; GA 754; GB 754; HD 754; HE 754; HF 754.

## Direct-scan reconciliation
- Market Intelligence dimensions: **755 × 264**
- Governed fixtures: **754**
- Remaining numeric-looking strings outside ET after field-aware classification: **25**, all GG:GJ FootyStats provenance/source-fixture identifiers; preserved as genuine text.
- Direct residual inline-string numeric values in governed numeric ranges: **0**

## Integrity
- Candidate workbook SHA-256: `91816ea140cefa210b38ab8eeaaddf8e287b75bac5fdb4829d3aa5caddd0b57e`
- Market Intelligence XML SHA-256: `5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde`
- Cell-change manifest SHA-256: `405605bc351c1a811e9f0a64321d84325a4a048e6b88604ff106115a3e8ab8c4`
- A:ET and Oracle V1.6 were not mutated.

## Unresolved exceptions left for QA
- 15,574 immutable A:ET numeric-type exceptions.
- 67 kickoff/date REVIEW_REQUIRED.
- 754/754 xG temporal provenance UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- CMOI UNAVAILABLE/UNVERIFIED; no output inferred.
- 754/754 Formula Input BLOCKED; 0/754 Backtest READY.
- No fresh independent binary-level 754 × 264 certification of this candidate is exposed by the latest QA evidence.
- FootyStats PPG/GF/M/GA/M, venue metrics, Last-3/Last-5 chronology, H2H, BTTS/goal intelligence, xG provenance, LTSS, actuals and derived fields were not altered without source-backed evidence.

No estimation, zero-fill, fuzzy-match, timezone normalization, historical backfill, unsupported provenance substitution, or post-match leakage was used.

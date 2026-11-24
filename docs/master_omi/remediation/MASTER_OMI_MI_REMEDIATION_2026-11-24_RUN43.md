# Master OMI MI Remediation Evidence — Run 43

## Decision
**RELEASE_DECISION: FAIL-CLOSED**

Separate Master OMI MI QA must independently re-audit the exact Run 43 binary.

## Authoritative inputs
- Canonical V2.1.1: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest QA: `docs/master_omi/qa/MASTER_OMI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-24_1034SAST.md`
- QA commit: `c7aea71f37e68c77a3054ed84bf0575a0368d5e4`
- QA audited binary: Run 37
- QA decision: `FAIL-CLOSED`

## Direct canonical scan
- Market Intelligence: **755 × 264**
- Governed fixtures: **754**
- Numeric-looking text in immutable A:ET: **15,574**
- Numeric-looking text outside ET: **21,774**
- Supported governed analytical numeric-looking text: **21,749**
- Genuine GG:GJ provenance/source IDs: **25**
- Fixture IDs: **754/754 nonblank + unique**
- Duplicate Fixture IDs: **0**
- Formula cells: **0**
- Excel error literals: **0**

The canonical binary was reconstructed exactly from the prior Run 42 candidate by reversing only the documented type-only changes. The reconstructed SHA exactly matched the authoritative canonical SHA; no analytical values or schema were regenerated.

## Remediation
Exactly **21,749** governed analytical numeric-looking cells were converted from Excel `inlineStr` to native numeric values in:
- `EW:FB`
- `FG:FL`
- `FO:GB`
- `HD:HF`

The 25 genuine `GG:GJ` FootyStats provenance/source-fixture identifiers remain text. Explicit classification text such as `INSUFFICIENT_DATA` remains text.

- Cells changed: **21,749**
- Analytical value changes: **0**
- Governed analytical numeric text remaining outside ET: **0**
- Unique fixtures represented: **754**
- GG source-ID populated: **21,749**
- GH source-ID populated: **21,749**
- GI source-ID populated: **21,749**
- GJ source-ID populated: **21,496**

## Integrity
- Candidate SHA-256: `efeea8101814f7d207d9396cb4182b15a952f2dc3a476e5f51f28a5da4915f8f`
- Candidate sheet3.xml SHA-256: `5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde`
- A:ET canonical SHA: `2978469e364a0627697600e60b451a8e126503e479029b36e74909d71ce04367`
- A:ET Run 43 SHA: `2978469e364a0627697600e60b451a8e126503e479029b36e74909d71ce04367`
- A:ET differences: **0**
- Oracle V1.6 changes: **0**
- Package entries changed: **sheet3.xml only**
- Manifest SHA-256: `e06d2f563a1d256186b5621eeafe5ae3768a12b29b7ac7df7f68e103c61f7621`
- Evidence report SHA-256: `a6aadffd77b39174ecaee0e3e54b412aa17383fcad2e60e88886c7076e2ce34f`

## Unresolved / QA handoff
- **15,574** immutable A:ET numeric-type exceptions
- **67/754** schedule `REVIEW_REQUIRED`
- **754/754** xG temporal provenance unverified
- **0/754** xG betting eligibility
- **0/754** goal production eligibility
- **0/754** goal betting eligibility
- **754/754** Formula Input blocked
- **0/754** BACKTEST_READY
- CMOI authoritative population **0/754**
- **479/754** actuals unavailable/unverified

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewrite, A:ET mutation, Oracle V1.6 change, or post-match leakage remediation was performed.

The full cell-level manifest is the companion evidence artifact.
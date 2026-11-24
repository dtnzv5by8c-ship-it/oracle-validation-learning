# Master OMI MI Remediation — Run 41 — 2026-11-24

RELEASE_DECISION=FAIL-CLOSED

Run 41 rebuilt from the canonical V2.1.1 baseline and applied only the supported append-only numeric type correction. Latest QA evidence: qa/master_omi_mi_qa_automation_turn11_2026-11-24_0634SAST.md at commit 1a9d780e8117ffafc059d8d73aa5d3c4f92dc58e. QA decision FAIL-CLOSED.

Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e.

Fresh canonical scan before remediation:
- 755 x 264 Market Intelligence
- 754 governed fixtures
- 21,774 numeric-looking text values outside ET
- 21,749 supported governed analytical numeric fields
- 25 genuine GG:GJ FootyStats provenance/source-fixture IDs
- 15,574 numeric-looking text values inside immutable A:ET
- 754/754 fixture IDs nonblank and unique
- 0 formulas
- 0 Excel error literals

Exactly 21,749 governed analytical cells were converted from inlineStr numeric-looking text to native Excel numeric values. Ranges: EW:FB, FG:FL, FO:GB, HD:HF. No analytical values changed. The 25 GG:GJ provenance IDs remain text.

Post-remediation:
- Governed analytical numeric-looking text outside ET: 0
- Residual numeric-looking text outside ET: 25, all GG:GJ provenance IDs
- A:ET unchanged
- Oracle V1.6 unchanged
- Only xl/worksheets/sheet3.xml changed

Candidate SHA-256: efeea8101814f7d207d9396cb4182b15a952f2dc3a476e5f51f28a5da4915f8f
Candidate sheet3.xml SHA-256: 5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde
Manifest SHA-256: f55d4e0a73aacb0ebdf42ad6dc4bc99ef088be72755dc5fa383639ad11f101f1

A:ET cell-fragment SHA canonical and candidate: fc13ceae478cc1fe308ccb44abd0fe896996f537ae34487c587fcc594fef074a

Unresolved: 15,574 immutable A:ET numeric-type exceptions; 367 CMOI blank pairs with no authoritative values; 754/754 xG temporal provenance UNVERIFIED_NO_CAPTURE_TIMESTAMP; Formula Input/backtest blocked; other chronology/H2H/BTTS/venue/LTSS/actual/derived exceptions without authoritative evidence.

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewrite, A:ET mutation, Oracle V1.6 change, or leakage remediation was performed.

The separate QA task must independently re-audit the exact Run 41 binary and determine release status.
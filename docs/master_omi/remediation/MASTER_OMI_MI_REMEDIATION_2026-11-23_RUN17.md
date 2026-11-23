# Master OMI MI Remediation — Run 17 — 2026-11-23

## Release posture
RELEASE_DECISION=FAIL-CLOSED

## Authoritative evidence
- Canonical V2.1.1 workbook SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest independent QA: `docs/master_omi/qa/MASTER_OMI_QA_AUTOMATION11_RUN16_REAUDIT_2026-11-23_1207SAST.md` (commit `3e8c313f8cc8f9a487bbb81c0dc1382f9f002464`)
- Latest QA candidate SHA: `56ae85e325de1babfd62d6c0836a9b58a6503ef0a5ada9ae74c3a59d2bb947b5`
- Run 16 remediation evidence commit: `f040955a838b9d6945de1237dbf9f940ae2e2542`

## Direct canonical scan and remediation
- Market Intelligence: **755 rows × 264 columns**.
- Canonical numeric-looking text in A:ET: **15,574**.
- Canonical numeric-looking text outside ET: **21,774**.
- Verified legitimate source-ID strings retained as text in GG:GJ: **25**.
- Safe analytical numeric-text conversions outside ET: **21,749**.
- Post-remediation analytical numeric-looking text outside ET: **0**.
- Post-remediation numeric-looking text outside ET: **25**, all source IDs.
- Excel errors: **0**; formulas: **0**.

The 21,749 changes are type-only conversions. The original lexical numeric values are preserved as native Excel numeric values; no analytical value was recalculated or inferred.

## Immutable protection
- A:ET value changes: **0**.
- A:ET XML cell-fragment differences: **0**.
- A:ET schema changes: **0**.
- Oracle V1.6 changes: **0**.
- Source/provenance IDs changed: **0**.

## Conversion counts by column

| Column | Cells converted |
|---|---:|
| EW | 754 |
| EX | 754 |
| EY | 754 |
| EZ | 754 |
| FA | 754 |
| FB | 754 |
| FG | 734 |
| FH | 735 |
| FI | 734 |
| FJ | 735 |
| FK | 734 |
| FL | 735 |
| FO | 754 |
| FP | 754 |
| FQ | 754 |
| FR | 754 |
| FS | 754 |
| FT | 754 |
| FU | 754 |
| FV | 754 |
| FW | 754 |
| FX | 754 |
| FY | 754 |
| FZ | 754 |
| GA | 754 |
| GB | 754 |
| HD | 754 |
| HE | 754 |
| HF | 754 |

## Preserved source IDs
The 25 numeric-looking strings outside ET were preserved because they are FootyStats provenance/source-fixture identifiers in GG:GJ, not analytical numeric fields. Cells: `GI24,GJ35,GG40,GI40,GI163,GJ164,GJ165,GJ177,GH340,GI340,GG341,GJ341,GH455,GI455,GJ455,GJ466,GI610,GJ610,GI611,GG612,GI612,GJ621,GH622,GJ711,GJ755`.

## Latest QA blockers retained for independent QA
- 15,574 immutable A:ET numeric-type exceptions
- 67 kickoff/date REVIEW_REQUIRED records
- 754/754 xG capture timestamps UNVERIFIED_NO_CAPTURE_TIMESTAMP
- CMOI UNAVAILABLE/UNVERIFIED
- 754/754 Formula Input BLOCKED
- 0/754 Backtest READY
- No independent post-Run-16 binary-level 754 × 264 QA artifact exposed in the connected repository

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, or post-match leakage was introduced.

## Candidate
- File: `Oracle_Master_OMI_V2_1_1_REMEDIATION_RUN17_2026-11-23_EXACT_AET.xlsx`
- SHA-256: `e741eae321e99ded8f3e266e4e0023ed3dff5e26c8fb274a36043abd9fcf0a7c`
- Worksheet XML SHA-256: `f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830`
- Complete cell-change manifest: `MASTER_OMI_RUN17_CELL_CHANGE_MANIFEST.tsv`

## Decision
Run 17 remediates only supported append-only numeric-type defects found by direct canonical scanning and reconciled against the latest QA evidence. Immutable A:ET defects and all evidence-dependent blockers remain unchanged and are explicitly left for independent QA. **RELEASE_DECISION=FAIL-CLOSED.**

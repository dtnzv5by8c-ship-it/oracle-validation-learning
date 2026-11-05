# Project Oracle — Historical Plan Partition Count Reconciliation
## Research-only audit — 2026-11-05

**Branch:** `research/oracle-50-league-readiness-audit`  
**Source HEAD verified immediately before commit:** `b82fde131bcbd4e9928a2eb7f65f3d05ce3d87eb`  
**Evidence mode:** offline/sanitized metadata only. No FootyStats API calls, no private-repository access, no raw payloads, and no Oracle V1.6 production changes.

## Finding

The current mapping-audit summary confirms **182 planned provider-season partitions**, but one existing report contains an arithmetic/count-label inconsistency in its cross-year season summary.

The report `reports/ORACLE_HISTORICAL_FEATURE_CHRONOLOGY_PROVENANCE_GATES_2026-11-05.md` states:

- 35 × 2023/24
- 35 × 2024/25
- 35 × 2025/26
- 36 × 2026/27

Those four values sum to **141**, not 182.

The authoritative sanitized mapping summary at the audited HEAD reports the following history-season-label counts across the 49 mapping decisions:

| Provider season label | Count |
|---|---:|
| 2024 | 14 |
| 2025 | 14 |
| 2026 | 13 |
| 2023/24 | 35 |
| 2024/25 | 35 |
| 2025/26 | 35 |
| 2026/27 | 36 |
| **Total** | **182** |

The three calendar-year labels (14 + 14 + 13 = 41) account for the difference between 141 and 182.

## Governance interpretation

This is a **documentation reconciliation issue**, not evidence that the 182-season plan is wrong. The mapping summary itself is internally consistent:

- provider catalogue rows: 756;
- provider catalogue unique season IDs: 756;
- planned season rows: 182;
- planned league count: 49;
- planned IDs unique: true;
- planned + excluded IDs exactly partition the catalogue: true.

The 35 and 36 cross-year counts therefore remain valid, but they must be accompanied by the 41 calendar-year partitions when presenting the full 182-partition composition.

## Required downstream rule

Any future report must describe the 182 planned partitions using either:

1. the full seven-label breakdown above; or
2. a clearly stated aggregation that sums to 182.

Do not present the four cross-year counts as if they were the complete composition of the 182-partition plan.

No mapping-owned files were changed to correct this finding. The mapping automation remains the owner of its catalogue/date-audit paths.

## Safety / eligibility

- FootyStats API requests: **0**
- Preflight Run 41869437030: **not rerun**
- Historical ingestion: **0 completed / 728 planned**
- Production eligible: **false**
- Betting eligible: **false**
- Oracle V1.6 logic/probabilities/thresholds/calibration/ledgers: **unchanged**

This audit does not establish fixture-level identity, chronology, H2H, recent form, home/away form, standings or xG readiness.

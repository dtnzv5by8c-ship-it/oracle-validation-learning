# FootyStats Historical Season Partition Integrity Audit — 2026-11-05

## Scope

Research-only audit of the live FootyStats historical season plan at commit `b30d15ed183cc18bd04f8a7d76d9a76e4c08f7ce`. No provider API calls were made.

## Verified counts

- Catalogue leagues: **49**
- Catalogue season rows: **756** (catalogue-level figure)
- Historical provider-season partitions: **182**
- Unique provider season IDs in the 182-row plan: **182**
- Planned/not retrieved partitions: **182**
- Rows with the required fixture-level UTC filter: **182/182**
- Rows with the exact configured date boundaries: **182/182**
- Production eligible: **0**
- Betting eligible: **0**

## Historical partition label distribution

| Provider season label | Rows |
|---|---:|
| 2024 | 14 |
| 2025 | 14 |
| 2026 | 13 |
| 2023/2024 | 35 |
| 2024/2025 | 35 |
| 2025/2026 | 35 |
| 2026/2027 | 36 |
| **Total** | **182** |

## Boundary contract

Every row in the plan specifies:

- fixture filter start: `2024-01-01T00:00:00Z`
- fixture filter end inclusive: `2026-11-04T23:59:59.999999Z`
- fixture kickoff filtering required: `True`

No row deviated from those values.

This means season partitions that straddle the research window must not be admitted wholesale. In particular, 2023/2024 and 2026/2027 partitions require fixture-level UTC kickoff filtering. Season labels are acquisition partitions, not substitutes for fixture chronology.

## Identity integrity

All 182 provider season IDs are unique within the plan. This verifies planning-key uniqueness only; it does **not** establish fixture-ID uniqueness, team-ID continuity, chronology, or provider-to-Oracle canonical identity.

## Evidence limitation

The plan is still `PLANNED_NOT_RETRIEVED`. This audit therefore proves the integrity of the research plan and its boundary contract, not historical data coverage.

The earlier 910-request provider preflight remains the sole preflight evidence and must not be rerun merely to recover the historical Git push conflict.

## Governance

No canonical mapping was promoted. No fuzzy join, parent-ID inference, imputation, or silent exclusion was performed.

All outputs remain:

- `production_eligible=false`
- `betting_eligible=false`

Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility were not modified.

## Next dependency

The next admissible research step remains exact fixture/team identity reconciliation from an independently validated private archive receipt. Until the protected archive path and centrally budget-gated provider workflow are validated, historical ingestion remains dispatch-disabled.

# Project Oracle — 80 HTTP-417 Quarantine Root-Cause Mapping — 2026-11-07

## Major milestone

The 80 quarantined Selected-50 tasks are now deterministically mapped to **20 provider-season partitions**, with exactly 4 endpoint tasks per partition.

### Root-cause population

| Provider season | League | Season | Tasks |
|---|---|---:|---:|
| 16572 | Finland Veikkausliiga | 2024 | 4 |
| 16572 | Finland Veikkausliiga | 2025 | 4 |
| 16572 | Finland Veikkausliiga | 2026 | 4 |
| 17964 | India Indian Super League | 2023/2024 | 4 |
| 17964 | India Indian Super League | 2024/2025 | 4 |
| 17964 | India Indian Super League | 2025/2026 | 4 |
| 17964 | India Indian Super League | 2026/2027 | 4 |
| 16537 | Republic of Ireland Premier Division | 2024 | 4 |
| 16537 | Republic of Ireland Premier Division | 2025 | 4 |
| 16537 | Republic of Ireland Premier Division | 2026 | 4 |
| 17178 | Russia Russian Premier League | 2023/2024 | 4 |
| 17178 | Russia Russian Premier League | 2024/2025 | 4 |
| 17178 | Russia Russian Premier League | 2025/2026 | 4 |
| 17178 | Russia Russian Premier League | 2026/2027 | 4 |
| 16627 | South Korea K League 1 | 2024 | 4 |
| 16627 | South Korea K League 1 | 2025 | 4 |
| 16627 | South Korea K League 1 | 2026 | 4 |
| 16617 | Venezuela Primera División | 2024 | 4 |
| 16617 | Venezuela Primera División | 2025 | 4 |
| 16617 | Venezuela Primera División | 2026 | 4 |

**Total: 20 provider-season partitions × 4 endpoints = 80 quarantined tasks.**

Endpoints:
- league-matches
- league-teams
- league-tables
- league-season

## Evidence basis

The mapping was performed by exact task-ID joins between:
- the governed 728-task Selected-50 manifest; and
- the private provider `blocked-task-registry.json`.

No fuzzy matching or league reassignment was used.

The private ingestion workflow classifies these tasks as `BLOCKED_PROVIDER_417` after its controlled request variants receive HTTP 417.

## Interpretation

This is no longer an anonymous “80 missing tasks” blocker. The blocked population is precisely identified and bounded to six league/season families:
- Finland
- India
- Republic of Ireland
- Russia
- South Korea
- Venezuela

The 80 tasks remain quarantined. No production or betting evidence is promoted from them.

## Next decision gate

Before spending more provider requests, determine whether the approved private gateway can recover these exact 20 provider-season partitions with a controlled request strategy. If recovery requires a new workflow run, manual user dispatch may be required.

No Oracle V1.6 production logic was changed.

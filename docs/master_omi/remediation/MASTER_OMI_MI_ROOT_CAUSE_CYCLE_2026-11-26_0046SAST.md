# Master OMI MI Root-Cause Cycle — 2026-11-26 00:46 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Evidence
- Latest independent QA: 2026-11-26 00:32 SAST
- QA blob: d92c5dd6d74e08ab281284b3216cacef04bb9fa1
- Live main HEAD: b290dbeac1ffff031ebbe84942bb29acbe6b2baa
- Current spine blob: df5eaf5bf65ff88f39ccf66ab1429b19687b61c7
- Current spine rows: 368
- Unique provider fixture IDs: 368/368
- Latest persisted generated_utc: 2026-11-25T22:44:40.582516+00:00
- Audit time: 2026-11-26 00:46 SAST
- Freshness gate: FAIL (age > 90 minutes)

## Root-cause status
| Field/domain | Cause | Authoritative source | Fix/status |
|---|---|---|---|
| Rolling fixture spine | Persisted current artifact becomes stale between hourly cycles | FootyStats rolling producer + manifest | Freshness fail-closed gate active; next producer execution required |
| Last-5 chronology | Fixture-specific cutoff logic | FootyStats league-matches | Fixed in workflow; fresh execution required |
| FootyStats PPG/GF/M/GA/M/BTTS | Producer persistence mapping | FootyStats API | Fixed in workflow; fresh execution required |
| H2H | Missing fixture-level derivation | FootyStats league-matches | Fixed in workflow; fresh execution required |
| Current prediction ledger | Public current ledger absent | Oracle production source | BLOCKED; do not fabricate/substitute |
| Current prematch state | Public current state absent | Oracle production source | BLOCKED; do not fabricate/substitute |
| Current matches | Public current matches absent | Oracle production source | BLOCKED; do not fabricate/substitute |
| xG temporal provenance | No authoritative capture timestamp | Source evidence | BLOCKED/UNVERIFIED |
| Kickoff reconciliation | 67/754 mismatches | Current reconciliation evidence | BLOCKED |
| A:ET / Oracle V1.6 | Immutable production surface | Canonical V2.1.1 | No changes |

## Release rule
No workbook release. No stale-source reuse. No fabrication, estimation, zero-fill, fuzzy match, timezone normalization, historical backfill, post-kickoff evidence, A:ET mutation, or Oracle V1.6 change accepted.

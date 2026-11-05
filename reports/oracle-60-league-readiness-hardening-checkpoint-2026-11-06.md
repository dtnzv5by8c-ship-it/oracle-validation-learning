# Oracle 60-League Readiness Hardening Checkpoint — 2026-11-06

## Change
Hardened the offline 60-league feature-readiness contract to require provider-season identity, not only provider league identity.

Required identity is now:
- canonical league ID
- provider league ID
- provider season ID

Provider league IDs and provider season IDs must each be unique across the 60 governed rows.

The historical window is now explicitly anchored to the 2024 season start; a row beginning in 2023 or 2025 cannot be admitted as satisfying the 2024-current governed history.

## Regression coverage
Added tests for:
- blank provider season ID
- duplicate provider season ID
- duplicate provider league ID
- valid 60-league matrix
- 59-league scope
- duplicate canonical league ID
- missing xG/goals
- non-2024 season start
- missing provider league ID

## Safety
- Offline only; no provider calls.
- No provider-sensitive data added.
- Oracle V1.6 production logic and probabilities unchanged.
- Gateway/private archive gate unchanged.
- Broad ingestion remains BLOCKED until the verified 60-league private receipt exists.

## Commits
- 5fecc4de8e7ae17dd307729cb7dba974a8391282 — readiness contract hardening
- 48f34aa7d05f7d847a73727b434e81295283b7f3 — regression coverage

## Next action
When the approved private receipt becomes available, validate its provider-season manifest against this contract before admitting the first bounded batch.
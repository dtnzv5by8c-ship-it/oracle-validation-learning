# Oracle 60-League Gateway UTC Transport-Proof Checkpoint — 2026-11-06

## Change
Hardened the private gateway receipt admission contract so `transport_verified_at_utc` must be explicitly UTC (zero offset), not merely timezone-aware.

## Why
A receipt timestamp such as `2026-11-06T05:00:00+02:00` is timezone-aware but is not a UTC timestamp despite the field contract naming it `*_utc`. Accepting it weakens the transport freshness/audit contract.

## Validation
Added regression coverage proving a non-zero-offset timestamp is BLOCKED with `transport_verified_timestamp_not_utc`.

Existing freshness, future-time, archive digest, private-reference, 60-league scope, bounded-request, auth, rate-limit, transport and public-data safety controls remain unchanged.

## Governance
- No provider request made.
- No provider-sensitive data added.
- No public FootyStats bypass.
- Oracle V1.6 production logic/probabilities/thresholds unchanged.
- Historical 2024-current ingestion remains fail-closed until a verified private 60-league receipt exists.

## Commits
- b18939f4074de5dcade5dcb9dd494237f3d1d905 — UTC transport-proof enforcement
- 947d827aad495352590e6f08c071cfb509820e37 — regression coverage

## Next action
When a genuine private 60-league receipt is supplied by the approved gateway/archive, validate the receipt and artifact digest immediately, then activate the existing bounded ingestion plan without broad dispatch.

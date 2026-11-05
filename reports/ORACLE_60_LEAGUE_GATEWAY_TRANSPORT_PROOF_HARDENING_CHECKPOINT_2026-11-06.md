# Oracle 60-League Gateway Transport Proof Hardening Checkpoint — 2026-11-06

## Evidence reviewed
- Governed branch: `research/oracle-50-league-readiness-audit`
- Public FootyStats caller remains retired after persistent HTTP 417/Cloudflare transport failure.
- The private Oracle source repository was inspected for the governed 60-league receipt locator `gateway/receipts/footystats-60-league-latest.json`; no such receipt is currently evidenced.
- The private source repository contains existing Oracle/FootyStats archive and research assets, but no receipt matching the new 60-league admission contract was found.

## Engineering change
The existing private gateway receipt validator was hardened to require `transport_verified_at_utc`.

Transport proof is now rejected when:
- the field is missing or malformed;
- the timestamp has no timezone;
- the proof is more than 24 hours old;
- the proof timestamp is materially in the future.

This prevents an old/private archive artifact from being treated as current proof that the blocked public transport path has been safely replaced.

## Regression evidence
Offline contract tests now cover:
- valid recent transport proof;
- 60-league scope failure;
- HTTP 417/blocked transport;
- public raw-payload visibility;
- archive digest mismatch;
- public archive reference;
- unapproved gateway ID;
- bounded-request overflow;
- public transport mode/evidence;
- historical-end overflow;
- stale transport proof;
- future-dated transport proof.

No provider request was made.

## Admission state
**BLOCKED — no verified private 60-league receipt.**

The validator still requires:
- exact 60-league scope;
- 2024-current history;
- approved private gateway/archive;
- immutable archive SHA-256;
- bounded request count;
- PASS transport/auth/rate-limit;
- private transport evidence;
- recent transport verification;
- production/betting eligibility false.

## Next action
When the genuine private 60-league receipt appears, validate it immediately. If it passes, validate the corresponding private archive artifact against its SHA-256 before admitting the first bounded ingestion batch. Only then may the 2024-current 60-league ingestion planner proceed batch-by-batch.

Oracle V1.6 production logic, probabilities, thresholds and governance are unchanged.

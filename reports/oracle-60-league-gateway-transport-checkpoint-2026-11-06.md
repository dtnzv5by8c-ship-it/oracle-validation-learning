# Oracle 60-League Gateway Transport Checkpoint — 2026-11-06

## Status
- Governed universe: Oracle-60-League.
- Historical window: 2024-01-01 through current.
- Public FootyStats HTTP 417/Cloudflare route: retired; no bypass/retry dispatched.
- Broad historical ingestion: BLOCKED until a verified private archive receipt exists.

## Hardening completed
The private gateway receipt contract now requires:
- approved private gateway identity;
- private archive reference;
- exactly 60 leagues;
- 2024-current window;
- bounded positive request/row counts (max 100 provider requests);
- transport/auth/rate-limit PASS;
- approved transport mode: controlled_gateway, private_archive, or private_mirror;
- private transport evidence reference;
- immutable archive SHA-256;
- VERIFIED_PRIVATE_ARCHIVE receipt status;
- no public raw provider payloads;
- no public credentials;
- production_eligible=false;
- betting_eligible=false.

## Regression coverage
Added cases for:
- 49-league scope rejection;
- HTTP 417 transport rejection;
- public archive rejection;
- public gateway rejection;
- archive digest mismatch;
- >100 requests rejection;
- future historical end rejection;
- unapproved public transport mode rejection;
- public transport evidence reference rejection.

## Governance
Oracle V1.6 production logic, probabilities, thresholds and calibration are untouched. No provider-sensitive payloads or credentials were added to the public repository.

## Evidence limitation
GitHub Actions execution could not yet be observed for the latest receipt-contract commit through the available workflow-run association endpoint. The commit itself is present on the governed branch. No ingestion is admitted on commit presence alone.

## Next action
When an approved private gateway produces a bounded 60-league batch, validate the receipt and archive digest immediately, then run the existing fixture/team/pagination/chronology and OMI feature-readiness contracts before admitting any further historical batches.

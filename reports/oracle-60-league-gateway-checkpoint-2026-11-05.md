# Oracle 60-League Gateway Checkpoint — 2026-11-05

## Governed objective

- Universe: **60 leagues**
- Historical ingestion: **2024-01-01 through current**
- Provider: **FootyStats**
- Production model: **Oracle V1.6 unchanged**

## Evidence reviewed

The latest public-repository provider caller was retired after repeated HTTP 417 responses on the Cloudflare-fronted provider path. The retired workflow explicitly records that no further public-runner provider retries are permitted and that the previously verified 50-league / 182-season / 728-task plan must not be dispatched through that path.

Existing private-archive work remains useful as an evidence source, but the known archive/gateway state is not sufficient evidence for 60-league admission. A 49-league archive must not be promoted to 60 by inference.

## New admission contract

`scripts/validate_private_gateway_receipt.py` now provides a fail-closed admission contract for a future approved gateway/private archive receipt.

The contract requires:

- FootyStats provider identity;
- exact **Oracle-60-League** universe identity;
- exactly 60 governed leagues;
- historical start at 2024-01-01;
- bounded batch identifiers and row/request counts;
- immutable private archive reference and SHA-256 digest;
- transport, authentication and rate-limit status = PASS;
- explicit `VERIFIED_PRIVATE_ARCHIVE` receipt state;
- raw provider payloads absent from public storage;
- credentials absent from public storage;
- production and betting eligibility remain false at ingestion.

The contract does not call FootyStats and does not read provider credentials.

## Regression evidence

Offline scenarios cover:

1. valid private receipt;
2. 49-league admission attempt;
3. HTTP 417/transport-blocked receipt;
4. public raw-payload exposure;
5. archive checksum mismatch.

The local regression run passed.

## Current gate

**BLOCKED — gateway/private archive receipt not yet proven for the 60-league universe.**

Therefore:

- no broad historical ingestion is dispatched;
- no provider data is fabricated;
- no public 417 retry is performed;
- no Oracle V1.6 production logic/probabilities/thresholds are modified.

## Next bounded action

When an approved private gateway becomes available, the first permitted action is:

**60-league manifest → one bounded private gateway smoke batch → immutable archive → SHA-256 receipt → contract validation → fixture/team/pagination/chronology checks → feature coverage checks → next bounded batch.**

The receipt contract must pass before any broad 2024-current ingestion is admitted.

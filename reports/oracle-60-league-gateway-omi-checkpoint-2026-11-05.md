# Oracle 60-League Gateway + OMI Checkpoint — 2026-11-05

## Current state
- Governed target: **60 leagues**.
- Historical ingestion window: **2024-01-01 through current**.
- Oracle V1.6 production logic, probabilities, thresholds and calibration: **unchanged**.
- Broad historical ingestion: **BLOCKED** until a private gateway/archive receipt proves the approved transport path.

## Evidence inspected
The existing private repository dtnzv5by8c-ship-it/oracle-football-data contains a controlled FootyStats historical gateway, but its latest controlled-ingestion workflow is explicitly scoped to **49 leagues**, not 60. Therefore it cannot yet be treated as proof of 60-league gateway admission.

The public direct provider caller remains retired after the previously observed HTTP 417/Cloudflare transport failure. No new direct-provider retries were made.

## Hardening completed
- Added scripts/validate_gateway_receipt.py.
- Added tests/test_gateway_receipt.py.
- Hardened scripts/validate_omi_universe_readiness.py so canonical provider league ID/name fields are required and missing recent-form, league-position, H2H or xG feature evidence now blocks admission instead of being counted only as a diagnostic.
- Extended the OMI readiness workflow to execute the gateway-receipt safety tests.

## Gateway receipt admission contract
A future receipt must prove:
1. approved private gateway repository;
2. real workflow run identifier;
3. immutable governed manifest reference;
4. immutable private archive SHA-256 and release tag;
5. FootyStats provider identity;
6. positive bounded provider request count;
7. exact **60-league** governed count;
8. history starts at 2024-01-01;
9. raw provider payloads remain private;
10. production/betting eligibility remain false at ingestion admission;
11. explicit GATEWAY_RECEIPT_VERIFIED status.

Any missing, malformed or contradictory field fails closed.

## Next bounded action
1. Establish the canonical 60-league/provider-season manifest.
2. Extend the private controlled gateway from 49 to 60 only using that manifest.
3. Execute one bounded private gateway smoke batch, not the full historical plan.
4. Publish only a sanitized receipt containing the immutable evidence above.
5. Verify the receipt against the new contract.
6. Only after that receipt passes, dispatch bounded 2024-current ingestion batches and reconcile fixture/team IDs, pagination, kickoff chronology, H2H, recent form, league position, xG/goals and market fields.

No provider data is fabricated or inferred from the 49-league gateway state.

# Oracle 60-League Private Receipt Admission Checkpoint — 2026-11-06

## Change
Added a private-repository admission workflow that validates the existence and contents of the governed 60-league FootyStats gateway receipt before any historical ingestion can be dispatched.

## Safety controls
- Requires the private Oracle repository to report `private=true`.
- Requires the receipt at the fixed private locator:
  `gateway/receipts/footystats-60-league-latest.json`
- Reuses `scripts/validate_private_gateway_receipt.py`.
- Does not print credentials or provider payloads.
- Does not write provider data to the public repository.
- Fails closed when the token, repository, receipt, or receipt validation is unavailable.
- Does not dispatch ingestion.
- Oracle V1.6 production logic and probabilities are untouched.

## Current evidence
No verified 60-league private receipt is currently evidenced. Existing private historical infrastructure remains selected-50/49-league evidence and is not promoted to the 60-league universe.

## Next action
When the governed private receipt exists, this workflow becomes the first admission check. Only after PASS should the bounded 3 x 20 provider-season ingestion planner be allowed to proceed.

## Governance
Provider/auth/rate-limit/transport failures remain BLOCK. HTTP 417/Cloudflare on the public FootyStats path remains retired and is not bypassed.

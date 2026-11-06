# Oracle 60-League Gateway Receipt Numeric Fail-Closed Checkpoint — 2026-11-06

## Change
Hardened `scripts/validate_private_gateway_receipt.py` so malformed numeric receipt fields cannot raise an uncaught exception or accidentally pass admission. `requested_rows`, `received_rows`, and `request_count` are now parsed through a fail-closed helper and explicitly return validation errors for non-integer values.

## Regression coverage
Added offline cases for:
- non-numeric `request_count` -> BLOCK
- non-numeric `requested_rows` -> BLOCK
- non-numeric `received_rows` -> BLOCK

Existing controls remain unchanged: 60-league scope, 2024-current window, private archive/evidence references, approved transport modes, recent transport proof, auth/rate-limit PASS, bounded request count, digest validation, and no public provider payloads/credentials.

## Evidence
No provider was called and no private receipt was fabricated. The public FootyStats HTTP 417/Cloudflare path remains retired. No broad historical ingestion was dispatched.

## Next action
Continue offline contract validation and admit a bounded 20/20/20 ingestion sequence only after the genuine private 60-league receipt is present and passes the complete admission contract.

## Governance
Oracle V1.6 production logic, probabilities, thresholds and governance remain unchanged.

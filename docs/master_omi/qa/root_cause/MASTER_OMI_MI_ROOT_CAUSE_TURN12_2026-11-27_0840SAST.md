# Master OMI MI Root Cause Register — Turn 12
Audit time: 2026-11-27 08:40 SAST

## Root cause
The current-data workflow introduced a fail-closed hash-parity gate that expected `rolling_spine_sha256` and `rolling_spine_fixture_ids_sha256` fields in `data/current_reconciliation_status.json`, but the persisted reconciliation producer does not emit those fields. The workflow therefore failed after a successful fresh FootyStats ingestion and successful 392/392 exact fixture reconciliation.

## Remediation
Commit **978a61b52166ce3d98bc97664dbae55811fde6cf** removes the invalid dependency on absent status fields and instead:
- verifies manifest timestamp == reconciliation source timestamp;
- verifies reconciliation status timestamp == source timestamp;
- verifies manifest fixture row count == live unique fixture count;
- verifies manifest unique-provider-ID count == live unique fixture count;
- retains CURRENT status and 100% coverage gates;
- continues deriving live spine hashes in-run for evidence.

## Regression protection
The corrected gate remains fail-closed on timestamp drift, row drift, ID-count drift, non-CURRENT status and sub-100% coverage.

## Release state
Still FAIL-CLOSED until the corrected workflow completes successfully and the downstream ledger, Team State, 754×264 MI rebuild and independent candidate-binary certification pass.

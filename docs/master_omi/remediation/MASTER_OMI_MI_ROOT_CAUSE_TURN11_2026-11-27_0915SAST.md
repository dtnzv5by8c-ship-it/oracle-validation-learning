# Master OMI MI Root Cause Register — 2026-11-27 09:15 SAST

## Scope
Fresh remediation cycle against the live public rolling 50-league spine and current production repository state.

## Root cause
The public rolling-spine gate had been hardened to require persisted rolling-spine SHA-256 and Fixture-ID-set SHA-256 values in `data/current_reconciliation_status.json`. The private reconciliation producer already calculated those values in memory, but its persisted status contract did not reliably include the complete evidence required by the public gate in the live production state.

This created a workflow dependency failure: valid fresh FootyStats ingestion and exact fixture reconciliation could be completed, but the downstream public gate could not independently prove that the reconciled fixture snapshot was the exact live rolling snapshot.

## Fix
Private production commit `6c7ee512023f40337716590db190c3ef9ef14252` extends the persisted reconciliation contract with:
- rolling spine SHA-256;
- exact Fixture-ID-set SHA-256;
- rolling-spine manifest SHA-256;
- rolling-spine generated timestamp;
- rolling-spine row count;
- rolling-spine unique Fixture-ID count;
- existing exact metadata mismatch and venue status evidence.

The existing exact provider-ID, kickoff, league/season and provider-team-ID reconciliation remains unchanged.

## Regression protection
The public gate remains fail-closed on:
- rolling-spine hash drift;
- Fixture-ID-set hash drift;
- row-count drift;
- unique provider-ID-count drift;
- non-CURRENT reconciliation status;
- sub-100% exact coverage.

The private workflow is path-triggered by `scripts/reconcile_current_data.py`, so this producer-contract correction automatically enters the next controlled current-data execution.

## Release blockers
- Fresh post-fix current-data execution must complete.
- Durable current Team State must be non-empty and hash/row-count verified.
- Current prediction ledger must be present and exactly reconciled to the same governed Fixture-ID set.
- Canonical Master OMI MI candidate must satisfy the locked 264-column schema while preserving A:ET and append-only post-ET intelligence.
- Every mandatory field must be populated from authoritative pre-kickoff evidence or explicitly classified UNAVAILABLE/UNVERIFIED with reason/provenance.
- Independent cell/type/provenance/chronology/PIT/leakage QA must reach 100%.
- Native XLSX/XML and exact-hash certification must pass.

## Release state
FAIL-CLOSED. No release workbook is certified or promoted by this cycle.

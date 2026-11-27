# Master OMI MI Root Cause Register — 2026-11-27 07:44 SAST

## Cycle result
**FAIL-CLOSED / NOT RELEASED**

## Root cause closed this cycle
The public Current Data workflow's new rolling-spine drift gate expected rolling_spine_sha256, rolling_spine_fixture_ids_sha256, and the rolling-spine manifest timestamp to be persisted by the private reconciliation producer. The private scripts/reconcile_current_data.py was fetching and reconciling the rolling 50-league spine exactly, but its persisted status JSON did not include those immutable snapshot fingerprints. The public gate therefore failed at CURRENT_RECONCILIATION_SPINE_HASH_DRIFT even though the underlying reconciliation was 392/392 exact and fresh.

## Evidence
- Failing run: 45941640683
- Ingestion: PASS
- Reconciliation: PASS — 392/392, 100%
- Drift gate: FAIL — missing persisted rolling-spine hash provenance
- No downstream state was admitted because the gate failed closed.

## Remediation
Private production commit 44f8cf65dc00055f1f62be0f97dadbab7bb6d0ec updates scripts/reconcile_current_data.py to fetch the authoritative rolling-spine manifest, persist the rolling CSV SHA-256, persist the exact Fixture-ID-set SHA-256, persist the rolling-spine generated timestamp, and persist exact fixture metadata mismatches plus venue availability classification.

Public workflow commit 7b79859aeefda5569dc1a1c4335a66a06e118f6f triggers Current Data when the rolling spine or its manifest changes and compares the live manifest timestamp with rolling_spine_generated_utc rather than the unrelated FootyStats source timestamp.

## Regression protection
The public gate now requires live rolling spine row count = reconciliation row count; live rolling spine SHA-256 = persisted reconciliation SHA-256; live Fixture-ID-set SHA-256 = persisted reconciliation Fixture-ID-set SHA-256; live manifest generated timestamp = persisted rolling-spine generated timestamp; status = CURRENT; and exact coverage = 100%.

## Current blockers
1. Fresh post-fix Current Data execution must complete.
2. Current Team State must be independently published and fresh.
3. Authoritative current prediction ledger must be present and exact-ID aligned.
4. Full 264-column Master OMI candidate must be rebuilt from the fresh spine.
5. Every mandatory field must be populated from authoritative pre-kickoff evidence or explicitly classified UNAVAILABLE/UNVERIFIED with reason/provenance.
6. Exhaustive cell/type/provenance/chronology/leakage audit must pass.
7. Native XLSX/XML/hash certification must pass.
8. Independent final gate must reach 100%.

## Protection
Oracle V1.6 unchanged. A:ET unchanged. No fuzzy matching, estimates, zero-fill, stale fallback, historical substitution, timezone normalization, unsupported provider substitution, or post-kickoff evidence admitted.
# Master OMI MI QA — 2026-11-27 04:10 SAST

## Release decision
FAIL-CLOSED. No release workbook certified.

## Current rolling fixture gate
- Rolling governed fixture spine: 392 rows
- Governed leagues: 50
- Unique provider fixture IDs: 392
- Exact provider-ID reconciliation: 392/392
- Unmatched: 0
- Coverage: 100%
- Freshness: FRESH
- Latest governed kickoff UTC: 2026-12-04T20:00:00+00:00
- Source errors: 0
- Fuzzy matching: false
- Historical fallback: false
- Pre-match only: true

## Current FootyStats source
- Current match rows: 2,733
- Current goal-event rows: 6,788
- Last-5 fully verified fixtures: 391
- Current source manifest is fresh and persisted.
- Current rolling MI artifact: 392 rows × 139 columns.

## Canonical contract
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical MI schema: 264 columns
- Immutable A:ET boundary: preserved
- Oracle V1.6: unchanged

## Remaining blockers
1. Current Team State must be independently reconciled to all 392 current governed fixtures.
2. Current authoritative prediction ledger must be independently present and tied to the same rolling spine.
3. Current MI must be assembled to the full 264-column canonical schema; the 139-column provider artifact is not a release surface.
4. Every unsupported/missing field must be explicitly classified UNAVAILABLE or UNVERIFIED; blank mandatory cells are not acceptable.
5. Exhaustive cell-level coverage/type/provenance/chronology/leakage audit must pass.
6. Fresh candidate XLSX/XML/native Excel/hash certification must pass.
7. Final release gate must report 100% PASS.

## Safety
No stale or dated frozen weekly spine, fuzzy matching, timezone normalization, estimation, zero-fill, historical backfill, or post-kickoff evidence was admitted.

## Evidence
- Current reconciliation: `data/current_reconciliation_status.json`
- Current source manifest: `data/current_source_manifest.json`
- Rolling manifest: `data/fixtures/governed_50league_current_manifest.json`
- Current MI build summary: `oracle_upcoming_50/build_summary.json`
- Latest rolling persistence commit: `318facc47efa1d16e6487ce6aab16d7581e7f2e3`

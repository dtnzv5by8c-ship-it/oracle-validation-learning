# Master OMI — Independent 100% Release Gate
Date: 2026-11-27 23:12 SAST
Decision: FAIL-CLOSED / NOT RELEASED

## Historical-first evidence reviewed
- docs/PROJECT_ORACLE_LESSONS_LEARNED.md
- docs/PROJECT_ORACLE_CONTINUATION_STATE.md
- live HEAD recent commits
- current rolling spine + manifest
- current reconciliation certificate
- current Team State manifest + CSV
- authoritative current prediction ledger
- current FootyStats Market Intelligence CSV
- recent GitHub Actions runs and job steps

Closed defects were not reopened.

## Current rolling 50-league spine
- Governed leagues: 50
- Fixture rows: 369
- Unique provider Fixture IDs: 369
- Fixture-bearing league-season IDs: 41 (valid; not required to equal 50)
- Provider: FootyStats
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- production_model_logic_changed: false
- A:ET changed: false
- Manifest generated_utc: 2026-11-27T19:10:26.070640Z
- Earliest kickoff: 2026-11-27T19:30:00Z
- Latest kickoff: 2026-12-04T20:00:00Z
- At audit time 21:12:15Z, the persisted 19:10 snapshot is temporally expired and contains already-started fixtures.
- No later producer run is present in the live Actions history.

## Current reconciliation
Persisted current_reconciliation_status.json:
- generated_utc: 2026-11-27T21:08:18.988834Z
- source_generated_utc: 2026-11-27T21:08:11.971318Z
- governed_upcoming_spine_rows: 369
- matched: 369
- unmatched: 0
- coverage: 1.0
- rolling_spine_sha256: d6804eb2921bd2b2df16d69dd9cfd250b87295822def6897a604a6f7907a3e6e
- rolling_spine_fixture_ids_sha256: 2af753592e00abc884c36ba502efff7563aaa29f11dcd0b9a23faaf08a1f7e1e
- rolling_spine_generated_utc: 2026-11-27T19:10:26.070640Z
- rolling_spine_row_count: 369
- rolling_spine_unique_fixture_id_count: 369
- metadata_mismatches: []
- status: CURRENT

These hashes are accepted as persisted reconciliation evidence for the 369-row snapshot; independent generation timestamps are not treated as identity.

## Current Team State
- database/current_prematch_team_state.csv: 369 rows, 42 columns, 0 duplicate Fixture IDs
- Exact Fixture-ID set parity with the 369-row rolling spine: PASS
- Mandatory state fields checked: 0 blanks across league namespace, provider IDs, Last-3/Last-5 PPG/GF/M/GA/M, BTTS/FTS/CS, shots and SOT
- home_history_status: 369 VERIFIED
- away_history_status: 369 VERIFIED
- venue_status: 369 UNAVAILABLE_SOURCE_SCHEMA (explicit classification; not imputed)
- provenance spine SHA matches the current reconciliation rolling-spine SHA

## Authoritative prediction ledger
- research/four_model/outputs/omi_prediction_ledger_current.csv: PRESENT
- Rows: 369 data rows
- Columns: 16
- Duplicate Fixture IDs: 0
- Exact Fixture-ID set parity with rolling spine: PASS (369/369)
- Status distribution: NO_BET 309, WATCH 19, CONTROLLED 41
- NO_BET rows contain explicit status/risk classifications; blanks in raw probability fields are not treated as unexplained current-state blanks.
- Current model readiness: READY for BTTS/DC/COMBO/M-1UP according to data/model_readiness.json.

## Current FootyStats MI
- oracle_upcoming_50/footystats_market_intelligence.csv: 369 rows x 139 columns
- Exact Fixture-ID parity with rolling spine: PASS (369/369)
- Duplicate Fixture IDs: 0
- intelligence_status: DIRECT_PROVIDER_PREMATCH for 369/369
- Last-5: 369 VERIFIED_PRE_KICKOFF
- Venue Last-5: 354 VERIFIED_PRE_KICKOFF; 15 UNAVAILABLE_INSUFFICIENT_SAMPLE
- H2H: 39 VERIFIED_PRE_KICKOFF; 330 UNAVAILABLE_NO_AUTHORITATIVE_H2H
- xG: 369 UNVERIFIED_NO_CAPTURE_TIMESTAMP — inadmissible for production
- FootyStats home/away PPG: 369/369 VERIFIED_PRE_KICKOFF
- Direct GF/M, GA/M and BTTS provider fields in this current artifact are explicitly UNAVAILABLE and were not inferred or zero-filled.

## Canonical workbook gate
- Locked production surface: 754 fixtures x 264 MI columns
- Current upstream MI: 369 x 139
- No current candidate XLSX/XML is exposed in the live public repository.
- Latest Oracle Master OMI Excel Export runs visible in Actions are failures from 02:58-02:59 UTC; no newer successful export is present.
- Native Excel types, formula compatibility, Excel error scan, exact A:ET cell equality, workbook SHA-256 and binary provenance therefore remain UNVERIFIED/BLOCKED.

## Preservation
- A:ET: unchanged / protected
- Oracle V1.6: unchanged
- No estimation, zero-fill, fuzzy matching, stale fallback, timezone normalization or post-kickoff evidence admitted.

## Release blockers
1. Current rolling spine is stale/temporally expired at audit time; no later producer run is evidenced.
2. Current MI is only 139 columns, not the locked 264-column production surface.
3. xG remains inadmissible without capture timestamp <= PIT.
4. Direct GF/M, GA/M and goal/BTTS provider fields remain unavailable in the current 139-column artifact.
5. LTSS, CMOI, actuals and downstream formula inputs are not certified in a canonical workbook.
6. Candidate XLSX/XML and all native Excel/A:ET/hash gates are unavailable.

## Positive closures confirmed this cycle
- Current Data Run 46066784664 completed successfully through ingestion, reconciliation, exact rolling-spine hash gate, Team State build/persistence, prediction compatibility, model readiness, OTMS, exact-identity regression, current prediction ledger build/publication and validated current-state bundle publication.
- Current source validation Run 46068428427 completed successfully.
- Prediction ledger now exists and exactly matches the current 369-fixture governed set.
- Team State now exists, is non-empty, and exactly matches the current 369-fixture governed set.
- Reconciliation now persists the required rolling-spine and Fixture-ID-set hashes.
- No new root cause was opened; the stale-spine condition is the already-recorded operational freshness/materialisation gap.

## Final decision
FAIL-CLOSED. No canonical Master OMI workbook is certified for release.

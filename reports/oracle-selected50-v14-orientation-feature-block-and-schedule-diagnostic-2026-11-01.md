# Selected-50 v1.4 candidate — orientation, runtime feature blocks and schedule diagnostics

**Date:** 2026-11-01  
**Branch:** research/oracle-50-league-readiness-audit  
**Status:** Research/reporting-only; v1.3 remains the last verified canonical reference.

## Verified source artifacts

- Report workflow run: [41268816105](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41268816105), completed successfully.
- Report artifact: 13068825279, digest sha256:bf75ba3fb17ed6b6ef432369e65a0ecca717161d76fef16bfa834ab086d3d7e1.
- Workbook SHA-256: a39030b4c7bd37dc2e37c9d53962a70cce069c309e3f51c7c77f7edcac917f20.
- Source runtime run: 41175230838, artifact 13032880970, digest sha256:e4bca38c8ab8e6afd5c23d241e4b55fe3ce6277e656172e8cda910718c897ae0.
- Source snapshot run: 41174900415, artifact 13031728960, snapshot file SHA-256 052d4c854426a195e0c7db2a419102f28e671486314fe1cbe08f35f1899714d0.
- Pinned historical archive SHA-256: 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f.

The downloaded workbook was inspected: exactly 19 worksheets in the locked order; Oracle V1.6 Output has 38 columns and Market Intelligence has 83. The v1.3 reference workbook is retained unchanged.

## 1. Exact snapshot orientation evidence

The runtime artifact contains a 2,262-row current_snapshot_candidate_trace.csv. Its exact key (selected season ID, fixture ID, ordered home team ID, ordered away team ID) is unique. A one-to-one exact join against the 434 runtime fixture rows returns:

| Result | Rows |
|---|---:|
| Exact snapshot trace matches | 434/434 |
| no_home_away=1 | 66 |
| no_home_away=0 | 368 |
| Unknown orientation in matched runtime rows | 0 |

The flag is sourced from the trace, not inferred from venue or team names. Flag 1 means no home/away distinction for the match; it is not automatically a neutral-venue label.

## 2. Runtime feature blockers — source runtime, not score-only reconstruction

The exact runtime report contains 24 fixtures with BLOCKED_MISSING_REQUIRED_FEATURES. Across these, 25 team-side histories have fewer than five feature-complete prior matches:

| Side | Histories below five |
|---|---:|
| Home | 15 |
| Away | 10 |
| Total | 25 |

Sample distribution: 21 sides have four eligible matches; four sides have three.

Missing-feature pattern:
- Six pair/environment fields are missing on all 24 blocked fixtures: pair_btts_mean, pair_fts_mean, pair_cs_mean, score_environment, shot_environment, score_gap5.
- Seven home-side fields are missing on 15 fixtures: home_gf5, home_ga5, home_btts5, home_fts5, home_cs5, home_shots5, home_sot5.
- Seven away-side fields are missing on 10 fixtures: away_gf5, away_ga5, away_btts5, away_fts5, away_cs5, away_shots5, away_sot5.

A reporting discrepancy is confirmed: the workbook's Team Form Evidence tab recomputes descriptive score-complete samples from the archive and can show five matches where the source runtime's feature-complete history gate has only three or four. These are different measures. The v1.4 candidate exposes the source runtime gate separately; it does not replace or relax it.

The runtime artifact does not provide the exact per-feature historical source-row IDs for every excluded feature record. Therefore the individual excluded historical match causing each side's shortfall remains unresolved until a sanitized row-level feature provenance export can be produced inside the private-archive workflow. No private raw archive rows are copied to the public artifact.

## 3. Schedule discrepancies — observed patterns, not proven causes

The existing schedule queue has 19 exact-identity kickoff conflicts and includes runtime kickoff, archive kickoff, signed delta, exact fixture identity, archive source file and source row.

Observed indicators:
- Nine archive kickoff values are at 00:00 UTC.
- Seven absolute kickoff deltas exceed 24 hours.
- Five absolute deltas are 150 minutes or less.

These indicators overlap and are not root-cause labels. They suggest a mix of midnight/date-only-looking values and larger stale or inconsistent schedule values, but no authoritative event-time source is present in this artifact to certify which timestamp is correct. All 19 remain REVIEW_REQUIRED; no auto-correction.

## 4. FootyStats historical pre-match xG

- Archive: 59,049 match records across 200 season folders; 51,983 finished/status-and-score-complete records; zero parse errors.
- Archive ingestion manifest rows: 0.
- Non-empty pre-match-labelled xG fields: 59,049/59,049 for each of the three named fields (field presence only).
- Current fixture candidates: 434 numeric home/away/total values.
- Verified capture timestamps: 0/434.
- Prediction/betting eligible xG rows: 0/0.

The missing manifest and blank capture timestamp are the technical provenance blocker. The public API's current historical response is not proof of the value available before kickoff, and no documented immutable per-fixture revision history has been established. All xG remains quarantined. No authenticated provider calls or credits were used.

## 5. Versioned reporting-only change prepared

A v1.4 candidate has been prepared without modifying the v1.3 reference:
- exact 19-sheet structure/order retained;
- 38-column Oracle V1.6 Output retained;
- 83-column Market Intelligence retained;
- 15 new report-only fields added to Data Quality & Risk;
- exact snapshot-trace validation added to the existing workflow;
- a 25-side runtime feature-block CSV and a 434-fixture orientation CSV/QA are emitted;
- field audit target becomes 340 fields x 50 groups = 17,000 records.

This candidate is not canonical until the governed workflow produces a new workbook and all release checks pass. All rows remain production-ineligible and betting-ineligible. No Oracle V1.6 logic or probabilities are changed.

## Next action

After the push-triggered regression workflow passes, manually dispatch the existing Selected-50 report repair workflow on this branch with the read-only pinned-archive confirmation and source runtime run 41175230838. Then inspect the new 19-sheet workbook, 38/83 schemas, 340-field matrix, orientation QA, 24/25 blocker audit, 19-row schedule queue and unchanged xG quarantine. Keep v1.3 as canonical until every v1.4 gate passes.

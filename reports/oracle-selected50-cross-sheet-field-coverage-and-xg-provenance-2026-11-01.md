# Project Oracle — Selected-50 Cross-Sheet Field Coverage & xG Provenance Addendum

**Evidence cutoff:** 1 November 2026 (SAST)  
**Source:** Selected-50 Run #124 (`41175230838`), runtime artifact `13032880970`, pinned archive SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`  
**Lane:** Research/reporting only. No production writes, model changes or authenticated FootyStats API calls.

## Executive finding

The latest local audit extends the earlier 50 × 83 Market Intelligence matrix. It covers **325 field occurrences across nine workbook sheets**, for **50 selected league-season groups**, yielding **16,250 league/field scope rows** and **1,090 exception rows**.

The 1,090 exceptions are **league/field-scope records, not 1,090 missing fixtures**. Denominators vary by sheet: fixture rows, team-side rows, H2H meeting rows, schedule-review rows or league-group rows. Expected states such as `NO_VERIFIED_PRIOR_H2H`, a blank schedule delta where no mismatch exists, and a blank `blocked_reason` where a forecast is not blocked must not be misclassified as ingestion failures.

The local expanded workbook passed reconciliation: 50 selected season IDs, 325 fields, 16,250 matrix rows, 1,090 exception rows, and no change to the raw Oracle V1.6 output tab. It is not proof of a successful GitHub Actions rebuild.

## 1. Exception taxonomy

### By coverage state

| State | Scope exception rows | Interpretation |
|---|---:|---|
| Explicitly unavailable / blocked | 769 | Includes intentionally unsupported markets and explicit no-evidence states; not all are ingestion failures. |
| No usable values | 133 | Includes missing capture timestamps, expected N/A schedule deltas, and fields blocked by the experimental goal baseline. |
| Partial value coverage | 98 | Some records in the scope have values and others do not. |
| Status missing | 81 | Mostly expected blank status fields where no block or schedule mismatch exists. |
| Status partial | 9 | Nine league groups contain schedule mismatch review statuses. |
| **Total** | **1,090** | Scope-aware exception count, not a fixture count. |

### By field role

| Field role | Scope exception rows |
|---|---:|
| Market / probability | 723 |
| Head-to-head | 120 |
| Descriptive / supporting | 118 |
| Status / governance | 90 |
| Team form / performance | 25 |
| xG / goal-model evidence | 12 |
| Identity / provenance | 2 |
| **Total** | **1,090** |

## 2. Main root causes and controls

1. **Unsupported markets — 644 scope exceptions.** Fourteen additional market/derived columns are explicitly `NOT_AVAILABLE_FROM_ORACLE_OUTPUT` across the 46 groups with fixtures (14 × 46 = 644). These are deliberate schema masks, not evidence of provider ingestion failure. Do not populate them from experimental estimates or external sources without a separately governed model.
2. **Core supported markets — 45 partial scope exceptions.** BTTS Yes, Home 1X and Away X2 each have 410/434 raw research outputs. Twenty-four fixtures are feature-blocked across 15 groups; each supported field therefore has partial coverage in those 15 groups. Keep the runtime five-match/required-feature gate unchanged.
3. **H2H — 108 explicit no-prior scope exceptions plus 12 partial.** At least one exact prior meeting exists for 144/434 fixtures (188 meeting rows); 290 fixtures show `NO_VERIFIED_PRIOR_H2H`. The 108 explicit scope exceptions include duplicated H2H-average header occurrences plus the two last-five H2H fields. This is an absence-of-evidence status, not an instruction to invent meetings.
4. **Experimental goal-market baseline — two groups blocked.** A-League has 11 prior settled league matches and Indian Super League has 16; both are below the 20-match research minimum. This blocks 12 fixture forecasts (5 A-League, 7 Indian Super League). Related research probabilities/lambdas remain blank or blocked; do not lower the threshold or treat them as Oracle V1.6 outputs.
5. **Venue-split form — sample support, not general form loss.** The audit reports 610/868 team sides with five venue-specific matches, 845/868 with at least three, and 23 sides with fewer than three. Keep venue values unavailable/partial where the sample requirement is not met; do not silently substitute overall form.
6. **Schedule reconciliation — 19 fixture mismatches across nine groups.** 415/434 fixture kickoffs match the archive; 19 require authoritative event-time review. The 37 groups with no mismatch naturally have no schedule delta/reason; nine groups have partial mismatch status. Do not auto-correct.
7. **xG capture timestamp — absent for all 46 fixture groups.** All 434 upcoming fixtures have numeric pre-match-labelled xG candidates, but zero have a verified capture timestamp. This is a provenance failure, not numeric-value coverage failure.
8. **Schema hygiene.** The 83-column Market Intelligence sheet has three duplicate header pairs (`H2H Avg Total Goals`, `Historical Accuracy Status`, `A+ Setup Status`). QA confirms each duplicate pair has identical values across all 434 rows. Do not rename/deduplicate until downstream consumers are reviewed.

## 3. Archive-level xG provenance — technical root cause

The pinned archive audit summary reports 59,049 match records across 200 season folders, 51,983 settled-status/score-complete records, zero parse errors, and **`manifest_rows = 0`**. It reports non-empty field-presence counts of 59,049 for each of `team_a_xg`, `team_b_xg`, `total_xg`, `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`.

Those are **non-empty presence counts**, not numeric-validity or point-in-time certification. The archive feature builder counts a field as present when it is neither `None` nor an empty string. It explicitly writes `xg_capture_time_utc` as empty and `xg_temporal_provenance_status` as `UNVERIFIED_NO_CAPTURE_TIMESTAMP`. It looks for `ingestion_manifest.csv`; the pinned archive audit found no manifest rows.

**Concrete blocker:** the existing archive is rich in xG field presence but lacks the ingestion/capture evidence needed to prove when a pre-match-labelled xG value was captured or whether it was revised after kickoff.

### Public FootyStats documentation

- Match Details documents `key` and `match_id` query parameters. Its public completed-match example (`match_id=579101`) returns actual-match xG and the three `*_xg_prematch` values, but no capture timestamp, snapshot ID or revision history. A current response for a 2019/20 match proves that the fields are returned now, not that they were available before kickoff.
- League Matches documents `max_time` as returning league/team statistics up to a timestamp. It is not documented as an immutable per-fixture xG snapshot or revision-history mechanism.
- The FAQ says match statistics are usually available around 20 minutes after full-time and that coverage varies by league/competition. It does not define the pre-match xG publication/revision lifecycle.

Official references:
- https://footystats.org/api/documentations/match-details
- https://api.football-data-api.com/match?key=example&match_id=579101
- https://footystats.org/api/documentations/match-schedule-and-stats
- https://footystats.org/api/documentations/faq

**Decision:** keep all 434 Selected-50 xG candidates quarantined from historical pre-match backtests, forecasts and betting. No authenticated provider request or private API credit was used.

## 4. Workbook and model integrity

- The expanded local workbook has 20 tabs, including `50-League Field Coverage` (16,250 rows), `Field Coverage Summary` (325 rows), `Field Coverage Exceptions` (1,090 rows), and `Priority Findings`.
- `Oracle V1.6 Output` remains an exact cell-level match to the Run #124 source workbook (38 columns; zero differences).
- The original source tabs were verified unchanged in the enhanced workbook.
- The enriched analyst `Market Intelligence` sheet derives H2H average goals from exact prior-meeting detail; this descriptive enrichment is not a production probability or model change.
- The local expanded workbook is not a successful GitHub Actions rebuild artifact. The full report rebuild workflow is manual-dispatch; the local QA records `report_rebuild_execution_status = NOT_RUN`.
- Production eligibility: 0. Betting eligibility: 0. Oracle V1.6 production logic, thresholds and probabilities remain unchanged.

## 5. Next actions

1. Add the 325-field cross-sheet matrix and exception taxonomy to the recurring report-builder workflow, with regression tests for scope-specific denominators and expected N/A statuses. Reporting-only; preserve the raw 38-column Oracle output and 83-column source schema.
2. Complete the existing 19-fixture authoritative kickoff review; no automatic corrections.
3. Obtain the pinned raw archive within the analysis workflow to replay the 25 blocked team-side histories and identify exact excluded records/statuses; keep the five-match runtime gate.
4. Ask FootyStats to confirm the definition of each `*_xg_prematch` field, first-availability time, revision/update policy, and whether an immutable per-fixture as-of snapshot/export exists. If unavailable, only prospective snapshots captured before kickoff can establish a new provenance trail.
5. Keep all xG and experimental goal outputs research-only and non-betting eligible until their separate validation gates pass.

**Governance:** no production model logic, probability, threshold, market definition or setting was modified. No PR merge is proposed.

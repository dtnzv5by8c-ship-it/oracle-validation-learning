# Project Oracle — Selected-50 Operational Coverage and xG Provenance Check

**Evidence cutoff:** 1 November 2026 (SAST)  
**Source runtime:** Run #124, run `41175230838`, artifact `13032880970`  
**Runtime commit:** `ea3f46dab4e54b71a818ab8d8723f36426e36bef`  
**Pinned archive SHA-256:** `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`  
**Lane:** Report-only. No authenticated FootyStats API calls, no workflow dispatch, no production writes.

## Executive position

The report-builder branch now contains code to generate a 50-row league coverage tab and a provenance-led coverage summary. A local operational workbook was independently checked against the Run #124 source workbook. This local workbook is not yet evidence of a successful GitHub Actions rebuild or a recurring scheduled report.

## Verified Selected-50 coverage

- 50 unique selected season IDs represented.
- 434 fixture rows across 46 groups in the seven-day horizon; 4 groups have no fixture in that horizon.
- 15 groups have partial raw prediction coverage.
- BTTS Yes, Home 1X and Away X2 each have 410/434 raw research outputs.
- 24 fixtures are blocked by the runtime's required-feature gate, affecting 25 team-side histories.
- 19 kickoff mismatches require manual review across 9 selected groups.
- 422 experimental goal-market forecasts are available; 12 are blocked by the minimum 20-match league baseline: A-League has 11 prior settled league matches (5 blocked fixtures), Indian Super League has 16 (7 blocked fixtures).
- Historical accuracy graded: 0/434. A+ setup graded: 0/434.
- Production eligible: 0. Betting eligible: 0.

The 4 no-fixture groups are Canada — Canadian Premier League (16741), China — Chinese Super League (16789), Republic of Ireland — Premier Division (16537), and South Korea — K League 1 (16627). They are N/A for the current fixture horizon, not automatically data failures.

## Blocked fixture diagnosis

The runtime report identifies 24 blocked fixtures and the exact missing feature set. The missing features are the seven required home or away last-five features for the side with fewer than five runtime-eligible matches, plus derived pair/environment features. Runtime history counts are 3 or 4 for the affected side. The existing descriptive report path may show a different score-based form count because it accepts additional completed-status labels and does not apply the runtime's full feature-support contract.

The five-match runtime gate remains unchanged. The available Run #124 artifacts do not include the raw archive match records needed to identify the exact excluded historical fixture and status for each of the 25 sides. That row-level replay remains blocked until the pinned archive itself is available to the analysis environment.

## Workbook reconciliation

Local operational workbook SHA-256:

`2907ca3eef326a3e8bfd5018926bdbfe255dd188071b45664f7c4ee50874d28f`

- `Oracle V1.6 Output`: exact cell-level match to the source workbook (0 differences; 38 columns).
- `Market Intelligence`: 19 cell differences, all in the schedule reconciliation status column. The local overlay label is `MISMATCH_REVIEW_REQUIRED`; the source workbook and checked-in report builder use `REVIEW_REQUIRED`. No probability or market cells differ. This is a reporting-label normalization discrepancy and must be reconciled before treating the local workbook as the canonical workflow artifact.
- The workbook's 50-League Coverage tab contains 50 unique groups; its aggregate totals reconcile to 434 fixtures, 410 outputs per supported market, 24 feature-blocked fixtures, 19 kickoff mismatches, 422 experimental goal forecasts and 12 baseline-blocked estimates.
- Its xG audit contains 434 numeric pre-match-labelled candidate rows, 0 verified capture timestamps and 434 quarantined rows.

## FootyStats xG provenance — documentation update

The public Match Details example for historical fixture 579101 returns `date_unix`, actual-match xG and the three pre-match-labelled xG fields. The response does not expose a capture timestamp, immutable snapshot ID or revision history. A current response for a historical match therefore proves field availability now, not availability before that match's kickoff.

The League Matches documentation describes `max_time` as an as-of timestamp for league/team statistics. It does not document it as an immutable per-fixture xG snapshot or revision-history endpoint, and the Match Details endpoint documents only `key` and `match_id` query parameters. The FootyStats FAQ says match statistics are usually available around 20 minutes after full-time and that coverage varies by competition. None of these facts establishes point-in-time provenance for `*_xg_prematch`.

Official documentation reviewed:
- Match Details: https://footystats.org/api/documentations/match-details
- Public Match Details example: https://api.football-data-api.com/match?key=example&match_id=579101
- League Matches / `max_time`: https://footystats.org/api/documentations/match-schedule-and-stats
- FAQ: https://footystats.org/api/documentations/faq

**Decision:** keep all 434 Selected-50 xG candidates quarantined, excluded from historical pre-match features, prediction and betting. No authenticated provider request or user API credit was used.

## Workflow and governance

The checked-in workflow `.github/workflows/oracle-selected50-market-intelligence-repair.yml` is manual-dispatch for the full archive/report rebuild; its push trigger runs tests only. It pins the archive SHA, verifies the runtime artifact provenance, requires explicit read-only archive confirmation, and uploads the workbook plus the 50-league coverage CSV. No full report rebuild was dispatched or verified in this check.

Oracle V1.6 production logic, thresholds and probabilities were not changed. The report remains `PARTIAL_RESEARCH_ONLY`, non-production and non-betting eligible. No merge is proposed.

## Next actions

1. Obtain a successful full workflow-dispatch artifact and verify the 50-league workbook and coverage CSV from that run before calling the enhancement recurring.
2. Reconcile the 19 schedule status labels and authoritative kickoff times; do not auto-correct.
3. Replay the 25 blocked team-side histories against the pinned raw archive to identify the exact excluded records; preserve the five-match feature gate.
4. Ask FootyStats for a historical per-fixture xG snapshot/export with effective timestamp, capture timestamp, revision history and a documented `*_xg_prematch` definition. If unavailable, retain quarantine and begin timestamped prospective snapshots only after a controlled, budgeted API probe is authorised.

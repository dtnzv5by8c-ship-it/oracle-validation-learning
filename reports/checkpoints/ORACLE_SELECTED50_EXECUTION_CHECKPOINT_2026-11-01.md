# Project Oracle — Selected-50 Execution Checkpoint

**Date:** 1 November 2026 (SAST)  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Verified branch head before this checkpoint:** `04be57da0f14b76c35e1b31a87e218c02d482be2`  
**Scope:** Research/reporting-only. No production model, probability, threshold or eligibility changes.

## Live state recovered

- Pull request #31 remains **open and draft**; it must not be merged as a shortcut.
- The full report workflow exists on both `main` and the governed research branch. The `main` workflow blob remains `ba53267d251e559d1bf8ce980129e42d82d6ea02`; the research branch contains the newer candidate workflow.
- Full report workflow is `workflow_dispatch` for its rebuild path. Push-triggered runs execute tests only; they do not download the private archive/runtime artifact or generate the full v1.4 workbook.
- Required manual inputs remain:
  - branch: `research/oracle-50-league-readiness-audit`
  - `confirm_private_archive_read=true`
  - `private_archive_release_tag=research-selected50-footystats-history-40375285207`
  - `runtime_run_id=41175230838`

## Verified CI

The following push-triggered jobs were independently inspected and completed successfully:

| Workflow run | Job | Result |
|---|---|---|
| 41273597499 | Market Intelligence repair tests | SUCCESS |
| 41273597521 | Selected-50 safety contract tests | SUCCESS |
| 41273597538 | Selected-50 dry-run planner | SUCCESS |

The report test job ran 23 report-builder tests, 6 goal-market research tests and 3 field-coverage tests (32 total). The separate full rebuild was not part of these push-triggered jobs.

## Current evidence and known blockers

- Governed universe: 50 selected league-season IDs.
- Source runtime: run `41175230838`, 434 fixtures; 410 raw research outputs and 24 blocked fixtures.
- Exact runtime-to-snapshot trace: 434/434 matches, zero duplicate snapshot identities.
- Orientation: 66/434 fixtures carry `no_home_away=1`; this is not a neutral-venue label and home/away-oriented markets require review.
- Feature gate: 24 blocked fixtures, 25 affected team-side histories (15 home, 10 away); 21 sides have four feature-complete prior matches and four have three. Six pair/environment fields are also absent on all 24 blocked fixtures. Do not relax the five-match gate or impute values.
- Schedule: 19 exact-identity kickoff conflicts remain manual-review-only. Indicators are not root-cause diagnoses; no authoritative event-time source has been established and no kickoff may be auto-corrected.
- xG: 434 numeric pre-match-labelled candidates but 0/434 verified capture timestamps. All remain quarantined from prediction, backtesting and betting.
- Historical accuracy/calibration: not validated for this report. Contemporaneous odds, trusted settlements and chronological out-of-fold history remain necessary.
- Eligibility: all Selected-50 outputs remain research-only, production-ineligible and betting-ineligible.

## Release decision

**v1.3 remains canonical. v1.4 is a candidate only.** The prior reference artifact (run `41268816105`, artifact `13068825279`) is the last verified workbook and has 19 worksheets, 38 Oracle V1.6 Output columns and 83 Market Intelligence columns. It does not include the new v1.4 orientation/feature support additions.

The latest v1.4 workflow definition pins and verifies the archive SHA-256 and the exact runtime artifact, requires the private-repository token, and does not call provider APIs. A full workflow dispatch and fresh artifact QA are still required before v1.4 can be called complete.

## Next execution sequence

1. User manually dispatches the existing full report workflow with the exact inputs above; this connector session has no workflow-dispatch action.
2. Inspect the resulting run, job steps/logs and artifact inventory.
3. Download/inspect the workbook and sidecar CSV/QA artifacts. Verify 19 worksheets, 38/83 columns, 340-field × 50-group matrix (17,000 rows), 434-fixture orientation audit, 25-side blocker audit, 19-row kickoff triage and unchanged Oracle V1.6 source values.
4. Keep v1.4 blocked if any provenance, schema, reconciliation or eligibility gate fails.
5. Resolve schedule conflicts only with authoritative event-time evidence. Obtain a sanitized row-level runtime feature provenance export before claiming the 25 history shortfalls have been repaired.
6. Keep xG quarantined until immutable pre-kickoff snapshots or provider revision semantics are independently evidenced.

**Governance:** no merge, no production writes, no model changes, no probability changes, no threshold relaxation, no imputation, no API-credit spend, and no betting eligibility granted by this checkpoint.


## Full rebuild completed — Run #154 (2026-11-01)

**Workflow:** [Run #154](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41276694062)  
**Run ID:** `41276694062`  
**Run attempt:** 1  
**Head commit:** `bdc053f138f8df559abd25670cbbfd18a2fd4838`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Conclusion:** SUCCESS (48 seconds total; job completed in 44 seconds).  
**Job:** `market-intelligence-repair` / job ID `124760189970`.

### Workflow steps verified
- Pinned private archive downloaded and SHA-256 verified: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- Exact runtime artifact downloaded and run/branch/commit/digest provenance verified.
- Exact joins, chronology, duplicate guards and unsupported market masking tests passed.
- Archive-wide pre-kickoff evidence built and archive audit digest/coverage verified.
- Research-only goal-market estimates and chronological backtest completed.
- 38-column Oracle V1.6 / Market Intelligence rebuild and QA passed.
- Orientation and runtime feature-block QA passed.
- Kickoff discrepancy triage passed.
- 50-league field-by-field coverage audit passed.
- Rebuilt report, evidence trace, QA and schedule queue uploaded. The conditional join-diagnostics-on-block step was skipped because the QA gate did not block.

### Artifact and workbook integrity
- Artifact ID: `13071003389`
- Artifact name: `oracle-selected50-market-intelligence-repair`
- Artifact ZIP SHA-256: `443e3f0be7d4640d4f166dddd4ae6611e68ecc74a86be3f8823f82fdafb41965`
- Artifact contains 27 files; GitHub retention through 2026-11-15.
- Workbook: `market-intelligence-output/oracle_selected50_market_intelligence.xlsx`
- Workbook SHA-256: `ba0171c7b317061749d6128416a882a774c060ec97ae0686ba606bcb53e02480`
- Workbook size: 2,673,237 bytes.
- Independently inspected workbook: exactly 19 worksheets; Oracle V1.6 Output = 434 data rows × 38 columns; Market Intelligence = 434 data rows × 83 columns; 50-League Field Coverage = 17,000 data rows × 19 columns.
- Durable Library copy saved at `/Project Oracle/Selected-50/Oracle_Selected50_Market_Intelligence_Report_2026-11-01.xlsx`.

### Reconciled QA findings
- Runtime/report rows: 434/434; exact archive joins: 434; unmatched/quarantined identity rows: 0; duplicate runtime and archive composite keys: 0.
- Selected league-season groups: 50; fixture-bearing league IDs in this horizon: 46. Four selected groups have no fixtures in this horizon; do not label these as missing ingestion without further evidence.
- Orientation: 66 fixtures flagged `no_home_away=1`; 368 retain home/away distinction; zero unknown. The flag is not a neutral-venue diagnosis. Flagged rows carry manual review status; all remain production- and betting-ineligible.
- Runtime feature support: 24 blocked fixtures; 25 affected team-side histories (15 home, 10 away). Four histories have three feature-complete prior matches; 21 have four. Pair/environment fields are missing on all 24. Do not relax the five-match gate or impute.
- Kickoff: 19 exact-identity discrepancies; all manual-review-only. Nine archive UTC-midnight indicators; seven >24-hour delta indicators; five <=150-minute indicators (indicators may overlap). No authoritative event-time rows verified; zero auto-corrections; root cause not established.
- Field audit: 340 fields × 50 groups = 17,000 matrix rows; 965 exceptions: 99 partial value coverage, 770 explicitly unavailable/blocked, 96 no usable values; zero unmapped source rows.
- xG: 434 rows have numeric home/away/total xG values; verified capture timestamp rows = 0; prediction-eligible rows = 0. Keep all xG quarantined pending point-in-time capture and revision provenance.
- Goal-market research: 434 rows; 422 forecastable and 12 blocked for league baseline <20. Backtest metrics are explicitly uncalibrated research-only; no promotion or betting claims.
- All Selected-50 outputs remain production-ineligible and betting-ineligible. Production model logic and probabilities unchanged; no provider API calls.

### Next controlled priorities
1. Preserve Run #154 workbook and QA as the reproducible baseline; do not overwrite it.
2. Build an authoritative kickoff reconciliation evidence process for the 19 conflicts; no automatic schedule edits.
3. Trace the 66 orientation flags to their source field semantics and upstream coverage; do not reinterpret them as neutral venues.
4. Investigate the 24 feature-blocked fixtures and 25 team-side histories using row-level provenance; retain five-match feature gate and no-imputation rule.
5. Resolve xG capture-time/revision provenance before any xG feature can be considered.
6. Complete historical calibration only with contemporaneous odds, trusted outcomes/settlements and chronological out-of-fold predictions.
7. Keep v1.3 canonical until v1.4 candidate passes formal release gates. No merge of PR #31, no production logic/probability/threshold changes.

**Run #154 is a successful report rebuild and QA milestone, not a declaration of 50-league production readiness.**

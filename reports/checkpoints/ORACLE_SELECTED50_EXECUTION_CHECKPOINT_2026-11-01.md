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


## Kickoff source evidence QA — Run #164 (2026-11-01)

**CI run:** [Run #164](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41278097171)  
**Run ID:** `41278097171`  
**Head commit:** `23aa98a9337df5acbc698170962bdfc19f9dac2a`  
**Result:** SUCCESS. Push-triggered tests plus actual source-evidence validation against the preserved Run #154 schedule queue.

### Implementation committed
- `scripts/validate_selected50_kickoff_source_evidence.py` — offline, fail-closed validation of exact fixture-ID joins, runtime/archive timestamps, timezone conversion, evidence status and no-auto-correction contract.
- `tests/test_selected50_kickoff_source_evidence.py` — six unit tests covering exact joins, timezone conversion, unresolved-source handling, runtime disagreement and no-auto-correction.
- `.github/workflows/oracle-selected50-market-intelligence-repair.yml` — test path and test invocation added; push CI downloads the preserved Run #154 artifact, validates the 19-row evidence register against its exact schedule queue, and uploads a QA JSON. The manual full rebuild also validates the register against the newly generated queue and includes the QA JSON in the report artifact.
- `reports/oracle-selected50-kickoff-source-evidence-2026-11-01.csv` — repaired malformed CSV quoting and updated official source evidence.

### Verified actual QA
- Preserved queue rows: 19.
- Evidence register rows: 19.
- Exact fixture-ID set match: true; IDs unique: true.
- Runtime/archive timestamps match original queue: all 19.
- Source local-time/timezone conversions verified for all 18 corroborated rows.
- Authoritative source corroborates runtime: 18.
- Unresolved/conflicted: 1 (CD Tondela vs Felgueiras 1932).
- Original schedule queue remains 19/19 `REVIEW_REQUIRED`; zero auto-corrections.
- Production eligible: false; betting eligible: false; network/provider calls: 0.

QA artifact:
- Artifact ID: `13072720459`
- Artifact ZIP SHA-256: `bb5f4cf3ef1238839f32769b2e51a2e30c19370057576493fadba068e720c0d8`
- Saved Library copy: `/Project Oracle/Selected-50/Oracle_Selected50_Kickoff_Evidence_QA_2026-11-01.json`

### Authoritative schedule evidence updates
- Six Saudi Pro League fixture times were confirmed from the Saudi Arabian Football Federation schedule.
- Lorient–Brest was confirmed from official LFP and FC Lorient notices as Monday 2 November 20:45 local.
- Reims–Sochaux remains corroborated from the official page body with a title/slug caveat.
- One Liga Portugal 2 fixture remains unresolved due lack of authoritative exact kickoff evidence.
- These are external evidence overlays only; the original schedule queue and workbook remain unchanged.

### Run #164 interpretation
This validates the external evidence register against the preserved Run #154 queue. It does **not** rewrite the original queue, certify automatic schedule corrections, or complete a new workbook rebuild. All 19 queue entries remain review-required pending formal controlled reconciliation.

## Remaining execution gate
The full manual report-repair workflow has not yet been rerun after adding the source-evidence validator. Before v1.4 candidate release review, manually dispatch the same workflow on the governed research branch with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`
- `runtime_run_id=41175230838`

Then verify the fresh report artifact contains `oracle_selected50_kickoff_source_evidence_qa.json` and re-check the unchanged 19-sheet / 38-column / 83-column workbook contract, exact joins, 17,000-row field matrix, orientation and feature blocker audits, xG quarantine, and eligibility masks.

**Governance remains unchanged:** v1.3 canonical; v1.4 candidate only; no merge of PR #31; no production model/probability/threshold changes; no API-credit spend.


## Team-level feature blocker diagnostics — Run #168 (2026-11-01)

**CI run:** [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41278235512)  
**Run ID:** `41278235512`  
**Head commit:** `d6ebb26949427eddfc71a60e2987f0eb16ee8246`  
**Result:** SUCCESS. Push CI downloaded the preserved runtime artifact and executed the existing offline diagnostic against the exact runtime prediction CSV.

### Diagnostic result
- Input runtime rows: 434; unique fixture IDs: 434.
- Blocked fixtures: 24.
- Blocked team-side rows: 25 (15 home, 10 away).
- Provider-season/team-ID profiles: 23.
- Repeated affected profiles: Coventry City (two side gaps) and Kruger United (two side gaps).
- One fixture has both sides below the minimum history gate.
- All 25 sides are below the five-match requirement: 21 have four oriented-history matches and 4 have three.
- Count contradictions (count >=5 but side features missing): 0.
- Unknown history counts: 0.
- All blocked fixtures have training support for all markets.
- Combo probabilities remain masked.
- No imputation, predictions, provider calls, canonical team mapping or production eligibility.

The diagnostic is deliberately count-only. It inherits history counts and feature names from the runtime report; it does not replay the private archive cutoff, expose the historical match IDs used/excluded, or prove why the fifth qualifying match is absent. Do not describe this as a root-cause fix.

### Artifact
- Artifact ID: `13072152007`
- Artifact ZIP SHA-256: `f21362e24363ccf70e6b4c10aac2c8d80a02a450b23019ff17d4c741c70594f8`
- Files: side-level diagnostics CSV, team-level diagnostics CSV, QA JSON.
- Saved Library copies:
  - `/Project Oracle/Selected-50/Oracle_Selected50_Feature_Blocker_Side_Audit_2026-11-01.csv`
  - `/Project Oracle/Selected-50/Oracle_Selected50_Feature_Blocker_Team_Audit_2026-11-01.csv`
  - `/Project Oracle/Selected-50/Oracle_Selected50_Feature_Blocker_QA_2026-11-01.json`

### Implementation and workflow
- The existing offline `diagnose_selected50_feature_blockers.py` and its 14 unit tests are now part of the repair workflow test contract.
- The manual report rebuild now emits side-level, team-level and QA JSON diagnostics from the exact verified runtime artifact.
- Push CI also validates the preserved Run #154 kickoff evidence register and executes the feature blocker diagnostics against the pinned runtime artifact; no provider API calls.

## Updated next controlled priorities
1. Manually dispatch the full report-repair workflow from the current governed branch head after these CI changes, using the same pinned archive and runtime inputs recorded above. This is required to create a fresh report artifact containing both new QA sidecars.
2. Obtain a runtime-side row-level feature provenance export: exact historical fixture IDs, kickoff cutoffs, source status, oriented team IDs and per-feature completeness/exclusion reasons for each of the 25 affected sides. Keep the five-match gate; no imputation.
3. Continue manual authoritative schedule review for the 19 queue rows; 18 runtime times now have external source corroboration, but the original queue remains review-required and no schedule correction is authorized. Tondela–Felgueiras remains unresolved.
4. Preserve the 66 runtime orientation warnings and official FootyStats semantics; do not infer neutral venue or alter home/away probabilities.
5. Keep xG quarantined until field definition, capture time and revision provenance are evidenced.
6. Keep v1.3 canonical until v1.4 release gates are formally passed. No PR #31 merge, production model changes, probability changes, threshold relaxation, or API-credit spend.

**Run #154 remains the frozen workbook baseline. Run #164 and #168 add validated report-only evidence and diagnostics; neither changes the workbook or production model.**

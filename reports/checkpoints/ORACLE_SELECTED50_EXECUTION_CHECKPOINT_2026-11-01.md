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


## Full Selected-50 Market Intelligence rebuild — Run #169 (2026-11-01)

**Workflow:** [Run #169](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41279308002)  
**Run ID:** `41279308002`  
**Head commit:** `ba1d33652bbbb06e5de1ff5466f28d1cfafc2df6`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Conclusion:** SUCCESS. Job `market-intelligence-repair`, ID `124767767827`; all applicable build, provenance, QA and upload steps passed.

### Run #169 execution evidence
- Pinned private archive downloaded and SHA-256 verified: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- Exact runtime artifact downloaded and run/branch/commit/digest provenance verified against runtime run `41175230838`, runtime commit `ea3f46dab4e54b71a818ab8d8723f36426e36bef`.
- Report-only diagnostics built: archive-wide pre-kickoff evidence, experimental goal-market estimates/backtest, 38-column Market Intelligence report, exact orientation and feature-block audits, kickoff discrepancy triage, and 50-league field-by-field coverage audit.
- Exact joins, chronology, duplicate guards and market masking tests passed.
- No provider API calls. No production model or probability changes.
- Conditional join-diagnostics upload and preserved Run #154 secondary CI-only checks were skipped because the applicable QA gates did not block; all required Run #169 build and upload steps succeeded.

### Run #169 artifact and independently checked workbook
- Artifact ID: `13073055114`; artifact name: `oracle-selected50-market-intelligence-repair`.
- Artifact ZIP SHA-256: `6cdec9fd99f1a93ffc4cfadd90b54d337f026a15a9d224ed370ab71202bc8c1c`.
- Artifact size: 2,992,896 bytes; GitHub expiry: 2026-11-15.
- Workbook: `market-intelligence-output/oracle_selected50_market_intelligence.xlsx`.
- Workbook SHA-256: `8526cfea9ba147ab85262e2dd28321605956d9669e01f28d00e56e31b7bd4456`; size 2,673,235 bytes.
- Independently opened workbook: exactly 19 worksheets. `Oracle V1.6 Output`: 434 data rows × 38 columns. `Market Intelligence`: 434 data rows × 83 columns. `50-League Field Coverage`: 17,000 data rows × 19 columns.
- Artifact has 27 files, including workbook, report CSV, 50-league coverage, QA, evidence trace, schedule queue, join quarantine, xG audit, orientation audit, runtime feature-block audit, 17,000-row field matrix and exceptions, kickoff triage, archive audit, goal-market research and xG provenance research notes.

### Run #169 QA findings
- Runtime/report rows: 434/434; exact archive joins: 434; unmatched/quarantined identity rows: 0; duplicate archive composite keys/history rows/runtime keys: 0.
- 50 selected league-season IDs are represented in the coverage register; 46 selected IDs have fixtures in this runtime horizon and four have no fixture rows in this horizon. Do not mislabel those four as ingestion failures.
- Schedule: 19 exact-identity kickoff discrepancies remain `REVIEW_REQUIRED`; zero authoritative event-time verifications and zero automatic corrections. Root cause remains unestablished. All are manual-review-only.
- Orientation: exact snapshot trace join 434/434; 66 `no_home_away` flags and 368 with home/away distinction; zero unknown. This flag is not a neutral-venue label.
- Runtime feature support: 24 blocked fixtures; 25 affected team-side histories (15 home, 10 away); 21 have four qualifying prior matches and four have three. Keep the five-match gate; no imputation. Count-only diagnostics do not establish the historical row-level root cause.
- Field coverage: 340 fields × 50 groups = 17,000 matrix rows; 965 exceptions (99 partial, 770 explicitly unavailable/blocked, 96 no usable values); zero unmapped source rows.
- xG: numeric home/away/total values appear on 434 rows, but verified capture-time rows = 0 and prediction-eligible rows = 0. Keep xG quarantined until point-in-time capture and revision provenance are proven.
- Historical accuracy remains `NOT_VALIDATED`; A+ setup is not graded. H2H total meetings 188; verified cross-season meetings 0. Risk columns measure evidence coverage gaps, not outcome probability or probability of losing.
- Market availability: BTTS Yes, Home 1X and Away X2 copied unchanged from runtime; 24 rows have unavailable source predictions for these markets. Other markets are explicitly unavailable; combo probabilities remain masked. No synthetic probability fields.
- QA reports `production_model_logic_changed=false`, `production_probabilities_changed=false`, `production_eligible=false`, `betting_eligible=false`; report status `PARTIAL_RESEARCH_ONLY`.

### Updated controlled priorities
1. Preserve Run #169 workbook and artifact as the latest full rebuild; do not overwrite Run #154 baseline.
2. Obtain sanitized row-level provenance for all 25 affected team-side histories: exact prior fixture IDs, kickoff cutoffs, source status, oriented team IDs and per-feature inclusion/exclusion reasons. Keep five-match gate and no imputation.
3. Continue authoritative schedule evidence review for the 19 kickoff conflicts; no automatic correction. Run #164 corroborated 18 runtime times but one remains unresolved; Run #169 queue is still review-required.
4. Trace all 66 orientation flags to official source semantics; do not infer neutral venues or change home/away probabilities.
5. Keep xG quarantined until capture-time and revision semantics are independently evidenced.
6. Historical calibration/backtesting requires contemporaneous odds, trusted outcomes/settlements and chronological out-of-fold predictions. Do not present research estimates as calibrated.
7. Preserve v1.3 as canonical. v1.4 remains a report-only candidate pending formal release/governance gates; do not merge PR #31.
8. Do not alter production V1.6 logic, production probabilities, thresholds, eligibility, or spend provider API credits.

**Run #169 is a successful full research/report rebuild with QA, not Selected-50 production readiness or betting approval.**


## Row-level historical feature provenance audit implementation — 2026-11-01

**Latest governed branch HEAD at checkpoint:** `ebd4522368e5f7deaef4ac9e5a8ba130b1e0c13c`  
**Scope:** Research/reporting-only. No production model, probability, threshold, eligibility or archive changes.

### Implemented
- `scripts/audit_selected50_row_level_history_provenance.py` — new standard-library-only replay audit over the pinned private archive and exact runtime prediction report.
- `tests/test_selected50_row_level_history_provenance.py` — six unit tests.
- `.github/workflows/oracle-selected50-market-intelligence-repair.yml` — manual-dispatch-only archive replay step, test invocation, and artifact sidecars for side-level summary, match-level provenance and QA JSON.

### Replay contract
The audit mirrors the existing Selected-50 research runtime's current historical feature rules without changing them:
- Exact country + competition label mapping from the Selected-50 manifest to the existing selected-ID competition grouping.
- Provider team IDs preserved as the only team identity key; no display-name joins or canonical mapping.
- Separate home-oriented and away-oriented history, matching the runtime's `home_history` and `away_history` stores.
- Strictly pre-kickoff history; same-time and later matches are excluded.
- Existing finished-status and valid integer-score requirements.
- Existing competition-scoped fixture-ID conflict quarantine, exact duplicate handling and duplicate completed-signature quarantine.
- Five-match minimum unchanged; no imputation, prediction generation or production eligibility.

The output design records target fixture/team-side identity, archive season, considered historical fixture IDs, included and excluded IDs, source file/record index/hash, kickoff relation to cutoff, orientation, status/score, duplicate decisions, shot/SOT evidence and per-feature completeness. A missing archive match is reported as no matching team-ID record found in the mapped archive; the audit does not invent a provider-missing reason.

### CI and test evidence
- Run #170 (`41280110832`) failed on an intermediate workflow commit because the manual-only condition was escaped incorrectly and the archive step ran during a push test without the private archive. No archive access occurred.
- Run #171 (`41280145141`) succeeded after correcting the manual-dispatch condition.
- Run #172 (`41280185972`) failed on an intermediate script/test commit because the expected orientation label had not yet been updated.
- Run #173 (`41280188782`) succeeded on the latest implementation commit `ebd4522368e5f7deaef4ac9e5a8ba130b1e0c13c`. The six new row-level provenance unit tests all passed; the complete report repair push-test job passed.
- In push-triggered CI, the private-archive replay step was correctly skipped. Therefore the actual 25-side archive replay has **not yet been executed or validated**.

### Outstanding execution gate
The existing GitHub connector exposes repository/file/run reads and workflow reruns, but no workflow-dispatch action. A user must manually dispatch:
`.github/workflows/oracle-selected50-market-intelligence-repair.yml`
from `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`
- `runtime_run_id=41175230838`

This workflow reads the existing pinned archive and existing runtime artifact only; it makes no provider API calls. After dispatch, inspect the generated `oracle_selected50_history_provenance_sides.csv`, `oracle_selected50_history_provenance_matches.csv` and `oracle_selected50_history_provenance_qa.json`. Any count mismatch must remain `REVIEW_REQUIRED`; do not relax the five-match gate.

### Governance and preserved state
- Run #169 workbook/artifact and Run #154 frozen baseline remain untouched.
- PR #31 remains open and draft; not merged.
- v1.3 remains canonical; v1.4 remains a research/reporting candidate.
- Production V1.6 logic/probabilities, thresholds and eligibility are unchanged.
- No provider API credits were spent.
- All Selected-50 outputs remain production-ineligible and betting-ineligible.


## Row-level history audit hardening and xG manifest schema inventory — 2026-11-01

**Branch head before the first hardening commits:** `70602da4c205ed1a63a1c093f02873b96ad40e54`  
**Scope:** Research/reporting-only. No workbook was rebuilt in this change set. No production model, probability, threshold or eligibility changes.

### Row-level history provenance audit correction

The row-level replay script was compared directly with the existing archive feature builder's accepted source-field aliases. The earlier replay script used a narrower set of keys, which could have falsely excluded source history where FootyStats records used alternate documented/archive aliases.

Corrected the audit to accept the same source aliases as the archive feature builder for:
- Home/away provider team IDs, including `team_a_id` and `team_b_id`.
- Fixture IDs: `id`, `match_id`, `fixture_id`, `game_id`.
- Score fields, including `home_goal_count`, `homeGoalsCount` and corresponding away fields.
- Status fields: `status`, `status_name`, `match_status`, `game_status`.
- Completed statuses including AET / after extra time / penalties.

The shot and shots-on-target evidence classification was also tightened. A feature is no longer labelled complete when only one of five source values is numeric; the side audit now records numeric counts and reports partial 1–4-of-5 coverage explicitly.

Regression tests were added for alternate source aliases and partial shot/SOT coverage. These tests are wired into the existing governed workflow. **Their GitHub Actions execution is not yet verified in this checkpoint.** The last previously verified row-level unit-test run remains Run #173, which tested the earlier implementation; it did not execute the private archive replay.

### FootyStats xG archive-manifest clarification

A code-path review found that the earlier `manifest_rows=0` statement was too broad:

- `build_footystats_archive_features.py` searches specifically for `ingestion_manifest.csv` when calculating its manifest row count.
- `audit_selected50_row_level_history_provenance.py` expects `ingestion_manifest.json` for archive season-to-Selected-50 mapping, but that code path has not yet run against the pinned archive; actual file presence is not yet verified.
- Therefore, the zero count refers to the CSV-form manifest path; it does not prove either the presence or absence of a JSON manifest.

The JSON manifest's actual presence, field inventory and granularity have not yet been verified. No claim is made that it contains, or does not contain, per-fixture capture timestamps, response hashes or revision metadata.

### New research-only inventory added

Added:
- `scripts/audit_footystats_xg_manifest_provenance.py`
- `tests/test_footystats_xg_manifest_provenance.py`

Integrated both into the existing Selected-50 repair workflow. The manual-dispatch path will require exactly one JSON ingestion manifest in the pinned archive, fail closed if it is missing or duplicated, inventory its metadata and the match-record fields, then emit:
- `oracle_selected50_xg_manifest_field_inventory.csv`
- `oracle_selected50_xg_manifest_provenance_qa.json`

The inventory emits field names and counts only, never raw metadata values or credentials. It reports candidate capture, revision, hash and fixture-linkage fields but always leaves `xg_point_in_time_provenance_verified=false` and `xg_quarantine_required=true`. It makes no provider API calls and does not add or alter workbook columns.

The xG provenance report and point-in-time specification were corrected to distinguish the CSV-only zero count from the unverified JSON-manifest expectation in the row-level history audit.

### Current preserved evidence and gates

- Run #169 remains the latest verified full workbook rebuild: 19 worksheets; Oracle V1.6 Output 38 columns; Market Intelligence 83 columns; 17,000-row field matrix. v1.3 remains canonical; v1.4 remains an unpromoted candidate.
- Orientation sidecar: 66 `no_home_away` flags, 368 with home/away distinction, zero unknown. No neutral-venue inference or probability changes.
- Schedule: the separate Run #164 source-evidence QA corroborates 18 of 19 runtime kickoff times; one Tondela–Felgueiras row remains unresolved. The workbook's original 19-row queue remains `REVIEW_REQUIRED`; no automatic correction.
- Runtime feature support: 24 blocked fixtures and 25 blocked team-side histories (15 home, 10 away). The prior count-only diagnostic found 21 sides with four eligible matches and four with three. The corrected archive replay has not yet run; no root cause is certified.
- xG: 434 upcoming candidates remain quarantined; zero verified capture timestamps; zero prediction-eligible and zero betting-eligible. The JSON manifest schema inventory has not yet executed against the pinned private archive.
- No provider API calls or credits were used. Oracle V1.6 production logic/probabilities, thresholds and eligibility remain unchanged.

### Next controlled action

Manually dispatch the existing `.github/workflows/oracle-selected50-market-intelligence-repair.yml` from `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`
- `runtime_run_id=41175230838`

This uses only the existing pinned private archive and exact runtime artifact. It will run the corrected 25-side history replay and the new xG manifest inventory, then rebuild the workbook through the existing generator. It does not call FootyStats or consume provider credits.

After dispatch, inspect the history side/match/QA outputs and xG manifest field inventory/QA. Any history count mismatch remains `REVIEW_REQUIRED`; the five-match gate is unchanged. xG remains quarantined regardless of metadata-key presence until the provider semantics and point-in-time evidence are independently validated.


## Follow-up hardening — diagnostic blockers must not stop the canonical workbook

**Latest code/test commit included in this follow-up:** `167a10253830ab5c8b983fd2577a0f17fbf8509a`.

A second safety review identified that the new archive diagnostics could otherwise fail the entire report-repair job if the expected JSON manifest were absent, duplicated or unmappable. These are research-data blockers; they must be visible without preventing the existing canonical workbook generator from completing.

Changes made:

1. The xG manifest inventory now reports `BLOCKED_MANIFEST_MISSING`, `BLOCKED_MANIFEST_AMBIGUOUS` or `BLOCKED_MANIFEST_INVALID` rather than aborting. It still inventories available match-record field names/counts, writes explicit QA, and keeps xG quarantined.
2. The row-level history audit now writes `BLOCKED_ARCHIVE_MANIFEST_OR_MAPPING` QA when the JSON manifest is absent, invalid, duplicated or cannot map archive seasons to Selected-50 labels. It does not invent history rows or relax the five-match rule.
3. The workflow QA guards check archive digest, quarantine and governance invariants, but do not require these research diagnostics to pass before the existing report generator can run.
4. Regression tests cover alternate FootyStats team/fixture/score/status aliases, partial shot/SOT coverage, missing archive manifest handling, and missing/ambiguous xG manifest inventory.

These are research scripts, tests, workflow wiring and documentation only. The canonical v1.3 template, workbook generator, Oracle V1.6 output and probabilities were not changed.

**Verification limitation:** the latest GitHub Actions status lookup for commit `167a10253830ab5c8b983fd2577a0f17fbf8509a` returned no commit-status entries. The new tests are present in the governed workflow but are not yet certified as passing. The last verified passing CI remains Run #173 on the earlier implementation; it predates these latest corrections.

No full workbook rebuild was run in this follow-up. Run #169 remains the latest verified full workbook artifact. The next manual dispatch will run the updated diagnostics and use the existing report generator; if archive manifest evidence is unavailable, the workbook build can still complete with explicit blocked sidecars.


## Latest continuation checkpoint — 2026-11-01 08:30 SAST

**Verified research branch head at checkpoint:** `175f76c07ff23e06555e6fc88aa12726253008a1`  
**Latest code/test CI run:** Run #179 (`41280651255`), commit `20c45a98e43c6d9c98123c938906be0774d327be`, conclusion `success`.  
**Previous exporter-fix CI:** Run #178 (`41280648334`), commit `5a8a9e998f61e5840485294fbc5a65fcd0d2404a`, conclusion `success`.

### Completed since prior checkpoint

- Fixed the row-level provenance CSV export failure caused by heterogeneous home/away feature columns. The writer now uses the ordered union of keys across all side rows.
- Added a regression test proving distinct home/away feature columns export correctly.
- The complete governed push-CI job passed in Runs #178 and #179. Run #179 is the latest passing code/test verification.
- The existing report artifact from Run #169 was retrieved for review. Artifact ID `13073055114`; 27 files; workbook SHA-256 `8526cfea9ba147ab85262e2dd28321605956d9669e01f28d00e56e31b7bd4456`; archive ZIP SHA-256 `6cdec9fd99f1a93ffc4cfadd90b54d337f026a15a9d224ed370ab71202bc8c1c`.

### Current report evidence (Run #169; latest complete full workbook)

- 434 runtime fixtures; 434 report rows; 434 exact archive joins; zero unmatched/quarantined joins.
- 50 selected league groups; workbook has 19 worksheets. Oracle V1.6 Output: 434 rows x 38 columns. Market Intelligence: 434 rows x 83 columns. Field-coverage matrix: 17,000 rows x 19 columns.
- Schedule reconciliation: 19 rows remain `REVIEW_REQUIRED`; no automatic kickoff corrections.
- Orientation: 66 no-home/away flags; 368 fixtures with home/away distinction; zero unknown.
- Runtime feature audit: 24 blocked fixtures / 25 blocked team-side histories; prior count-only evidence: 21 sides with four qualifying prior matches and four with three. The corrected row-level archive replay remains unexecuted, so no root cause is certified.
- xG remains quarantined: 434 candidates, zero verified capture timestamps, zero prediction-eligible and zero betting-eligible.
- Historical accuracy remains `NOT_VALIDATED`; production eligibility and betting eligibility remain false.

### Execution and governance state

- Run #176 (`41280596249`) was the last manual private-archive dispatch and failed at the row-level CSV export. The exporter correction is now CI-tested, but the private archive replay has **not** yet been rerun after that fix.
- Push CI intentionally skips private archive replay; Run #179 passing does not certify row-level archive output or JSON manifest inventory.
- Next action: manually dispatch `.github/workflows/oracle-selected50-market-intelligence-repair.yml` on `research/oracle-50-league-readiness-audit` with `confirm_private_archive_read=true`, `private_archive_release_tag=research-selected50-footystats-history-40375285207`, and `runtime_run_id=41175230838`. Then inspect all history provenance and xG manifest sidecars before treating them as verified.
- PR #31 remains open/draft/unmerged. v1.3 remains canonical; v1.4 remains a research/reporting candidate. Run #154 remains frozen. Production Oracle V1.6 logic, probabilities, thresholds and eligibility are unchanged. No provider API credits were spent.


## H2H cross-season coverage repair — 2026-11-01 11:20 SAST

**Latest H2H code/report CI:** Run #207 (`41288126229`), conclusion `success`, commit `d394cd724a7fa36b9543499076f719bc9f51e741`.  
**Archive mapping regression suite:** included in Run #207; 11 tests passed.  
**Market Intelligence report regression suite:** included in Run #207; 29 tests passed.

### Confirmed root cause in Run #169
The report builder grouped H2H pairs by raw `provider_league_id`. In the archived FootyStats data this field is sourced from the match-level `competition_id`, which is season-scoped in this archive. Consequently, historical meetings in prior season folders were not consistently joined to current-season fixtures. The 50-league coverage tab therefore showed zero prior H2H for entire league groups such as Germany Bundesliga (selected season 17210), Netherlands Eredivisie (17097), and Mexico Liga MX (17099), even though the pinned archive contains multiple historical seasons for those groups.

### Reporting-only repair implemented
1. `build_footystats_archive_features.py` now reads the pinned `ingestion_manifest.json` and the governed Selected-50 manifest. It maps each archive season folder to its selected competition using exact `selected_country` + `selected_competition_name` labels. It does not infer a parent competition ID or use fuzzy matching.
2. Every normalized archive match row now carries `selected_id` and its mapping basis. The archive audit emits `season_selected_id_crosswalk.csv` and a mapping QA object in `summary.json`.
3. H2H report pairing now uses the exact selected competition mapping plus the exact unordered provider team-ID pair, with strict `historical kickoff < target kickoff`. Team form, league table and production output logic are unchanged.
4. Target archive rows must themselves map to the runtime selected ID; otherwise H2H is blocked rather than falling back to a season ID.
5. H2H history is deduplicated by selected competition + fixture ID. Conflicting fixture-ID groups and duplicate completed signatures are quarantined.
6. Historical `no_home_away` is preserved. Such meetings may contribute goal totals, but the home-perspective W/D/L result is recorded as `N/A`, not inferred.
7. Workbook H2H Intelligence exposes the H2H scope ID, source season ID, home/away IDs, orientation flag, scores and result. Coverage Audit Summary now reports mapping status, mapped/unmapped archive rows and H2H duplicate/quarantine counts.
8. Workflow upload now includes `archive-audit/season_selected_id_crosswalk.csv`.

### Verification
- Run #207 (`41288126229`) passed on commit `d394cd724a7fa36b9543499076f719bc9f51e741`.
- Market Intelligence tests: 29/29 passed, including cross-season mapping, foreign-competition isolation, pre-cutoff chronology, duplicate fixture quarantine and orientation uncertainty.
- Archive feature tests: 11/11 passed, including exact Selected-50 label mapping and duplicate-label rejection.
- CI push mode skips the private archive replay by design. Therefore these tests prove code behavior on fixtures, not yet the actual 200-season archive mapping or the rebuilt workbook H2H counts.

### Required manual execution to produce the corrected report
Manually dispatch `.github/workflows/oracle-selected50-market-intelligence-repair.yml` from branch `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`
- `runtime_run_id=41175230838`

The workflow uses the pinned archive SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f` and the exact existing runtime artifact. It makes no provider API calls. Inspect mapping QA before accepting H2H coverage:
- Expect `PASS_EXACT_SELECTED_MANIFEST_LABEL_MAPPING`, 200 mapped season folders, 50 mapped selected groups, and zero unmapped archive seasons.
- Review the new `season_selected_id_crosswalk.csv`.
- Check Germany Bundesliga, Netherlands Eredivisie, Mexico Liga MX and all other 50 groups in `50-League Coverage`.
- Verify nonzero H2H rows only where exact prior meetings exist; zero-meeting fixtures remain explicitly marked as no verified prior meeting.
- Confirm strict pre-kickoff cutoff, deduplication QA, and no cross-competition leakage.

### Governance
All changes are research/reporting-only. Oracle V1.6 production logic, probabilities, thresholds, five-match runtime gate and eligibility are unchanged. No FootyStats API credits were used. PR #31 remains open/draft/unmerged. Run #154 remains frozen. The new corrected full archive report has **not** yet been generated; Run #169 remains the last completed workbook until the manual archive dispatch succeeds.

## H2H provider team-ID drift repair — 1 November 2026

**User-reported defect:** a large set of fixtures in Run #208 displayed `NO_VERIFIED_PRIOR_H2H`, including repeat meetings where the archive may contain the clubs under historical provider IDs.

### Root cause established from report-builder code
- Run #208 had repaired archive season → Selected-50 competition mapping.
- The remaining H2H index and lookup still keyed solely on the exact unordered provider team-ID pair.
- The pinned archive contains season-scoped competition identifiers and can also contain provider team-ID changes between seasons. Exact ID-pair matching therefore silently omitted a historical meeting when one or both clubs had a different provider ID in an earlier season.
- This is distinct from the earlier season-to-Selected-50 competition mapping defect.

### Report-only repair committed
- `4f69576ab4c63eb0f4d427c81930716c4502b1b0`: exact normalized team-name cross-season H2H index and lookup.
- `bf0619b9891f2d82032bc4904a08bb636e74748e`: regression tests for team-ID drift and non-fuzzy matching.
- `d78ccb3dd1972ad0f53744a4520cf2ddd600ece7`: expose match basis and historical team names in H2H evidence.
- `0b3cf345084ca0df533051c77b3b3e244c4a76c4`: corrected Unicode/name normalization regex.
- Current branch head at checkpoint: `0b3cf345084ca0df533051c77b3b3e244c4a76c4`.

### Identity and safety policy
- H2H prefers exact normalized unordered team-name pairs within the same Selected-50 competition.
- Normalization is limited to Unicode NFKC, case-folding, punctuation removal and whitespace normalization.
- Exact provider team-ID pair is the fallback when no name-pair candidate exists.
- No fuzzy matching, guessed aliases, cross-league joins, parent-competition inference, or cutoff relaxation.
- Historical meeting results are oriented using the exact team-name identity, with provider IDs as a secondary orientation check; if orientation cannot be established, result is N/A.
- H2H evidence now carries historical team names and `match_basis`; summary QA counts name-based matches, ID-based matches and no-pair matches.
- Production model logic and probabilities remain unchanged; PR #31 remains open/draft/unmerged; no provider API calls or credits.

### CI verification
- Run `41289245346` — Market Intelligence repair CI: SUCCESS.
- Run `41289245345` — contract tests: SUCCESS.
- Run `41289245395` — research planner: SUCCESS.
- The report-builder suite ran 31 tests, including:
  - `test_h2h_bridges_provider_team_id_changes_with_exact_team_names`
  - `test_h2h_name_matching_is_not_fuzzy`
  - existing selected-competition isolation, chronology, duplicate quarantine and no-home-away tests.
- All applicable tests passed.

### Required archive-level verification — NOT YET COMPLETE
The code and regression tests are committed, but the pinned 59,049-row archive has not yet been replayed against the repaired builder. The successful Run #208 artifact predates this repair and must not be presented as proof that these user-listed fixtures now have H2H.
- Manually dispatch `.github/workflows/oracle-selected50-market-intelligence-repair.yml` on `research/oracle-50-league-readiness-audit`.
- Inputs:
  - `confirm_private_archive_read=true`
  - `private_archive_release_tag=research-selected50-footystats-history-40375285207`
  - `runtime_run_id=41175230838`
- Inspect the rebuilt workbook and evidence trace for every user-listed fixture.
- Reconcile each result as one of: recovered by exact normalized names; recovered by exact IDs; genuinely no qualifying pre-kickoff meeting in the pinned Selected-50 archive; or unresolved name/identity mismatch requiring a source-backed exact alias crosswalk.
- Do not fabricate H2H or add cross-competition meetings to the Selected-50 league-scoped H2H definition without an explicit governance decision.
- Preserve all production/betting eligibility masks and unchanged Oracle V1.6 probabilities.

**Release status:** implementation + CI verified; archive replay and fixture-by-fixture verification pending. Do not call the user-facing H2H defect fully resolved until the manual rebuild artifact confirms the outcomes.




## H2H cross-division coverage correction — 2026-11-01

**Scope:** Research/reporting-only correction following user review of 70+ fixture rows showing no H2H. No Oracle production model logic, probabilities, thresholds, or eligibility changes.

### Confirmed report-builder defect
The prior cross-season repair still restricted the H2H pair index to the fixture's current Selected-50 competition ID. This excluded valid earlier meetings when a club had moved between selected divisions (for example, Premier League / Championship / EFL League One; Bundesliga / 2. Bundesliga; Ligue 1 / Ligue 2; La Liga / Segunda División).

The Run #208 workbook contains 73 rows with `H2H N = 0` and `NO_VERIFIED_PRIOR_H2H`. The user's supplied fixtures are present among those zero-H2H rows. Team Form Evidence independently confirms both teams have archive histories for examples including Cambuur–Go Ahead Eagles, Real Betis–Málaga, Schalke–RB Leipzig, Wolfsburg–Osnabrück, Watford–Lincoln and Everton–Coventry. The earlier report therefore cannot classify every zero as "no historical meetings"; it only proves no pair was found under the old league-scoped lookup.

### Reporting-only correction implemented on governed branch
- Archive season crosswalk now carries exact `selected_country` and `selected_competition_name` values from the Selected-50 manifest into normalized archive rows.
- H2H candidate indexes now use exact country scope, not current selected competition ID. This allows a pair to be found across selected divisions in the same country.
- Exact normalized team-name matching remains the fallback for provider team-ID changes, but is now country-scoped. Exact provider team-ID pairs are also country-scoped.
- No fuzzy name matching, no cross-country joins, no inferred parent competition IDs, and no unverified/cross-source fixture joins.
- H2H meeting evidence now records source `selected_id`, country and competition so the report shows where each meeting occurred.
- Strict pre-kickoff cutoff, completed status, valid score, deduplication/quarantine and `no_home_away` handling remain in force.
- The 38-column Oracle V1.6 Output schema and raw production probabilities remain unchanged.

### Commits and test status
- `0d11ea7555cfce4b144f28a994c570919c5d57c4` — exact country and competition added to archive crosswalk.
- `6f6a242305bcd9cf8110fca6e7ea5f7d7272ecbf` — country-scoped cross-division H2H lookup.
- `04f20ccc87729a0b0c44d15107b337b6770ae1b8` — cross-division and country-isolation regression tests.
- `816281f7f61dc3cc7504bdb880c6c8d2c09920f5` — corrected fail-closed test fixture for unmapped countries.
- Run #207 / #208 remain historical evidence for the previous H2H repair; they do not verify this new country-scope change.
- Run #41289370036 passed all governed push-CI tests on `816281f7f61dc3cc7504bdb880c6c8d2c09920f5`. A further regression test for exact team-name identity across selected divisions is being run on the subsequent branch head.

### Mandatory full-archive verification gate
The latest full pinned-archive rebuild remains Run #208, which predates this correction. The GitHub connector does not expose a workflow-dispatch action. Manually dispatch `.github/workflows/oracle-selected50-market-intelligence-repair.yml` on `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`
- `runtime_run_id=41175230838`

The run reads only the pinned archive (SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`) and the existing runtime artifact. It must make zero provider API calls. After completion, verify the user's full fixture list against the rebuilt `H2H Intelligence` sheet and confirm every included meeting has source country/competition, source season, fixture ID, score and kickoff strictly before the target. Zero H2H is valid only where the archive contains no qualifying same-country Selected-50 meeting. Keep any unresolved fixture explicitly `NO_VERIFIED_PRIOR_H2H`; do not fabricate or infer meetings.

**Governance:** PR #31 remains open/draft/unmerged. Run #154 frozen baseline untouched. Production V1.6 logic/probabilities/thresholds/eligibility unchanged. No provider API credits used.


### Follow-up verification — source league provenance field and final push CI
- H2H meeting detail now exports `meeting_selected_id`, `selected_country` and `selected_competition_name` as explicit meeting-level columns in the H2H Intelligence sheet.
- Added regression coverage for cross-division matching by exact provider team IDs and by exact normalized team names, plus country isolation and unmapped-country fail-closed behavior.
- Latest complete governed push-CI run: **Run #41289454045**, success, commit `755e2686c3b582eacfba6bfde0a8bdaf62c7a2a9`. Market Intelligence repair test step passed: 33 tests; all subsequent workflow test suites passed (6, 3, 4, 6, 15, 10, 5 and 11 tests respectively).
- Branch head: `755e2686c3b582eacfba6bfde0a8bdaf62c7a2a9`. PR #31 remains open/draft/unmerged.
- These are CI unit/regression tests only. They do not execute the private archive replay. Run #208 remains the last full archive build, so the requested fixture-by-fixture H2H recovery is not yet empirically verified. The manual workflow-dispatch gate above remains mandatory.

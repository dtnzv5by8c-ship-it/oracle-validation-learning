# Project Oracle checkpoint — 2026-10-21 (updated)

## Status
Research workflow #33 completed successfully: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39642654783
- 55 automated tests passed, including the result-observed-before-kickoff regression test.
- Archive feature audit processed 35,819 records across 126 season folders with zero parser errors.
- Archive freshness gate passed; no provider API calls were made.
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39642654783/artifacts/12366320771

## Guardrails
Research-only changes. No production model logic, model weights, probabilities, thresholds, or canonical registry were changed. No paid API calls were made. No production promotion is authorized.

## Production/evaluation readiness
The canonical archive prediction ledger has 210 rows across 42 fixtures, all marked CHALLENGER in the last completed audit. The canonical settlement ledger is empty; the canonical scorecard has headers but no data rows. Therefore production accuracy cannot be calculated from these canonical ledgers; this is not a zero-percent accuracy result.

The separate four-model live settlement manifest says DEVELOPMENT_ONLY, 0 settled rows and 75 unsettled rows; promotion is BLOCKED. The separate live prediction export is staging/development material, not a substitute for canonical production settlements.

## Evaluation pipeline
The research-only score-verified join now:
- pins the exact result snapshot hash and checks the source manifest hash against a caller-provided expected hash;
- requires exact fixture identity (fixture ID, competition, kickoff, home/away team IDs);
- rejects predictions at/after kickoff;
- derives outcomes from final scores for supported markets;
- rejects result rows with observation timestamps before scheduled kickoff;
- records exclusions and computes research-only metrics.

Important limitations remain: the manifest's approval flag and source URI are not independently authenticated by the code; hashes establish file identity, not source authenticity. The evaluation join has not yet been run against a complete set of genuine immutable predictions and independently verified results. No defensible current hit rate, Brier score, log loss or calibration result is established for production.

## Data/league limitations
- Archive: 35,819 records; 126 season groups.
- Provisional standings populated both positions for 34,083 records, but league-format and official tie-break validation is incomplete.
- Competition crosswalk: 43 provider competition names; 25 candidates need review, 18 unmatched; 0 mappings approved.
- The intended 44-league universe is not reconciled to the canonical 27-league registry.
- Prematch xG and odds point-in-time provenance remain unverified.
- Feature coverage is not equivalent to production eligibility.

## Source-trust control added in this checkpoint
A research-only policy document defines the required independent allowlist, acquisition evidence, raw-snapshot hash, fixture reconciliation, audit trail and fail-closed exclusions. A new validator and regression tests were added to the research repository. The validator now requires caller-pinned hashes for the result snapshot, acquisition manifest and independent allowlist; verifies the manifest snapshot hash; requires an approved source ID and exact source URI match against the allowlist; rejects empty snapshots, non-final rows, malformed chronology and row/source mismatches. Workflow #34 passed. Workflow #36 also passed after adding regression tests for source-URI mismatch and empty snapshots; the full archive audit and all workflow steps succeeded. Until a real allowlist is independently pinned/reviewed and a genuine source snapshot is supplied, source approval remains pending. Structural validation does not independently authenticate a provider.

Policy: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/docs/oracle-result-source-trust-policy-research-only-2026-10-21.md

## New work in this checkpoint — prediction-ledger adapter

A research-only adapter was added:
- `scripts/adapt_oracle_prediction_ledger.py`
- `tests/test_oracle_prediction_adapter.py`

The adapter preserves the original CSV row, records source-column mappings, and separates schema-adaptable rows from quarantined rows. It does not infer team IDs, convert local kickoff strings to UTC, or treat challenger rows as production. Invalid probabilities, missing required identifiers, missing timezone-aware timestamps, and non-production status are quarantined with explicit reasons.

The research workflow was updated to read the canonical prediction ledger from the existing private branch `fix/epl-btts-team-state-aliases`, run the adapter, and include its outputs in the research artifact. Workflow integration commit: `4f12cda672552986f442683d7490cb29ff901585`. Follow-up commits added fail-closed handling for unsupported composite market labels (`e7dc615b435758f9e132b71cb63f46da914c6e40`) and regression tests for explicit market aliases and composite-market quarantine (`9d450df9c94ed4e209778c32f6eb76188ab36773`). The resulting workflow run and adapter counts have **not yet been independently verified**; do not interpret these commits as proof that the workflow passed. The available GitHub connector did not return run-listing data in this session, so the workflow run link/status remains unconfirmed.

Code: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/scripts/adapt_oracle_prediction_ledger.py
Tests: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/tests/test_oracle_prediction_adapter.py
Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-footystats-archive-feature-audit.yml

## Next actions
1. Verify the workflow triggered by the adapter/test commits; inspect test results and the adapter artifact.
2. Confirm actual accepted/quarantined row counts and quarantine reasons from the canonical ledger; validate market mapping only for explicit known labels.
3. Obtain a separately reviewed allowlist and genuine frozen result snapshot before attempting real source-provenance validation.
4. Run evaluation only on prediction/result pairs that pass all gates; publish coverage and exclusion counts alongside any metrics.
5. Review provider competition mappings and reconcile the intended league universe only with authoritative evidence.

## Progress estimate
Project-management estimate: 78% for research audit infrastructure and groundwork before this adapter integration. The adapter implementation and workflow integration are additional progress, but the overall percentage is held at 78% until the new workflow run and artifact are verified. This is not model accuracy, production readiness, or a claim that the end-to-end autonomous prediction/settlement/evaluation pipeline is complete.


## Checkpoint correction — execution/verification loop identified

Owner-facing status correction: repeated checkpoint messages had restated the same next steps without confirming the newly integrated workflow or its artifact. That is a genuine execution/verification loop, not evidence that the end-to-end project is progressing through all stages.

The adapter and its workflow integration are committed, including explicit fail-closed market-label handling. However, this session could not retrieve the latest Actions run list through the connected GitHub interface, and the commit status query returned no status checks. Therefore the adapter workflow is **UNVERIFIED**, not passed. No accepted/quarantined counts are claimed.

The current critical path is narrowed to:
1. Obtain a readable Actions run/result and inspect the artifact for the adapter commit(s).
2. If the workflow did not trigger, manually run the existing research-only workflow from GitHub Actions; do not run production workflows.
3. Confirm adapter counts and quarantine reasons; preserve challenger/shadow status and quarantine unsupported composite markets.
4. Use genuine frozen result evidence and an independently reviewed allowlist before producing any performance metrics.
5. If genuine immutable production predictions do not exist, document production historical accuracy as unreconstructable from the available canonical ledgers and start prospective capture only through an explicitly approved, isolated research workflow.

No model logic or production data was changed. No performance metric is established by this checkpoint.


## Follow-up static review — hash provenance correction

A further static review found that the adapter previously allowed the prediction ledger's `source_manifest_hash` value to populate the `archive_sha256` field. These are not interchangeable hashes. This mapping has been removed; if the archive hash is absent, the row is quarantined with `SOURCE_MANIFEST_HASH_IS_NOT_ARCHIVE_HASH`. A regression test was added. Code commit: `382d226c8dc716db8d1be2bba1c5e886dfe675de`; test commit: `6ca6edef51e49c9904f1876e843af2d35cd1ba90`.

This is a meaningful correctness fix, but it is **not yet runtime-verified**. The connected GitHub workflow-run lookup returns no runs for these commits (it only exposes pull-request-triggered runs), and combined commit status has no checks. Therefore do not claim the new adapter tests or workflow succeeded. The canonical ledger's known missing UTC kickoff and team IDs mean the adapter is expected to quarantine rows unless an authoritative source supplies those values; this must be confirmed by artifact counts, not assumed.

Immediate next action: verify a workflow run through the repository Actions UI or another authorized Actions endpoint and inspect its artifact. If no run exists, manually dispatch the research-only workflow. Continue no further feature expansion until this run has a confirmed result.


## Checkpoint update — 2026-10-21 follow-up

Further code review found an adapter validation-order defect: required fields were assessed before an explicitly supported market alias could populate market and selection. The adapter now recomputes missing fields after explicit alias mapping (commit `7ce28866ad51953dd599c515a7eae61c6befc381`). This is a static code correction only; runtime tests remain unverified because the connected workflow lookup has not exposed a run or status checks.

Current status remains:
- Last confirmed complete research workflow: run #36, `39645298749`; this predates the adapter integration and follow-up corrections.
- Adapter workflow after the later commits: UNVERIFIED.
- Adapter accepted/quarantined counts: UNKNOWN; no artifact inspected.
- Production accuracy: UNAVAILABLE from current canonical ledgers; settlement ledger has no rows.
- Overall project-management estimate: 78%, held until workflow and artifact verification.

The next useful action is still to obtain an actual run of the research-only workflow and inspect the adapter output. Do not add further adapter features until the current changes have passed runtime tests. No production logic, probabilities, calibration, or registry was changed.


## Artifact review — workflow #44 (user-uploaded ZIP)

The uploaded `oracle-footystats-archive-feature-audit.zip` was inspected directly. Workflow #44 succeeded and produced the artifact, but the adapter summary revealed:
- 210 input prediction rows;
- 0 accepted rows and 210 quarantined rows;
- all 210 were marked CHALLENGER, so the adapter's previous production-only gate blocked research use;
- all 210 lacked `scheduled_kickoff_utc`, `home_team_id`, `away_team_id`, and `archive_sha256` in the target schema;
- all 210 carried `source_manifest_hash`, which correctly cannot be substituted for an archive hash;
- 84 rows had unsupported composite market labels (`*_U45`).

This is not evidence that predictions lost. It exposes an adapter/schema issue plus unresolved evaluation identity evidence. Archive audit itself passed: 35,819 records, 126 season groups, zero parse errors; production readiness remains NOT_ASSESSED. Feature coverage still does not verify pre-match xG/odds provenance. Competition crosswalk remains 25 candidate matches requiring review, 18 unmatched, 0 approved; 44-league universe not reconciled.

## Adapter correction committed after #44

The adapter was revised to separate research staging from production eligibility:
- Challenger rows can be staged for research without being relabelled production.
- The source manifest hash is retained under its correct field rather than requiring/pretending it is an archive SHA.
- Kickoff date/time is combined only when the source time carries an explicit timezone offset; naive times remain untrusted.
- Missing canonical home/away team IDs are recorded as evaluation blockers rather than silently invented.
- Unsupported composite markets, invalid probabilities, missing core fields and predictions at/after kickoff remain quarantined.
- Tests were rewritten for these semantics.

Adapter commit: `5208d0c648358f4d6c41dd4f844f8e49bcbd53aa`
Test commit: `c668a17ab96b58c72c9b93a3d5635de11f0b96f4`

These changes should trigger the existing research-only workflow, but runtime result is not yet verified. The next run must be inspected for research-staged counts and evaluation blockers. Even staged rows are not yet eligible for scoring until canonical team IDs are resolved and result truth is independently verified. No production logic, probabilities, calibration, or registry changed.


## Artifact review — updated workflow after adapter correction

User uploaded the artifact from the newer successful run (Run #46). The archive audit summary reports 35,819 records, 126 match files/season groups, 35,819 parseable kickoffs, 28,491 settled-status-and-score-complete records, 35,819 feature rows, zero parse errors, and no duplicate/non-empty fixture IDs or missing archive team IDs. Production readiness remains NOT_ASSESSED; no provider API calls were made.

Prediction adapter summary:
- input_rows: 210
- research_staged_rows: 126
- quarantined_rows: 84
- quarantines: 84 `UNSUPPORTED_COMPOSITE_MARKET` rows (labels ending `_U45`)
- staged_rows_blocked_from_evaluation: 126
- evaluation blockers: 126 missing home team ID and 126 missing away team ID (both blockers occur on each staged row)
- production eligibility: NOT_GRANTED

This is an improvement over the previous artifact: challenger rows are now research-staged rather than rejected solely because they are not production. Kickoff normalization was performed for rows whose source time explicitly carries a UTC offset. It does not yet make the rows evaluable: canonical home/away team IDs are absent from the prediction ledger and must be mapped to the archive's team IDs with deterministic, competition-scoped matching and ambiguity quarantine. Unsupported combined markets remain quarantined until settlement semantics are defined and tested; do not split them into simpler markets or score them as if they were simple markets.

Archive feature coverage summary reports 126 league-season groups and 35,819 archive rows, but `prematch_xg_provenance_verified=false`, `prematch_odds_provenance_verified=false`, and production eligibility NOT_GRANTED. Provisional standings have both positions for 34,083/35,819 rows; league-specific formats/tie-breakers remain unverified. Competition crosswalk: 43 provider names, 25 candidate matches needing review, 18 unmatched, zero approved canonical mappings, intended 44-league universe not reconciled. Alias decisions: 31 likely leagues for review, 6 likely cup/supercup, 6 unresolved; 43 human decisions pending.

Next work:
1. Build a deterministic research-only team identity mapping audit for the 126 staged rows using provider archive team IDs/names, constrained by the correct competition/season where resolvable. Normalize names conservatively; never fuzzy-assign silently. Report exact matches, normalized matches, ambiguous and unmatched.
2. Keep 84 composite-market rows quarantined until the combined market semantics and settlement logic are explicitly supported and tested.
3. Only after team mapping and fixture identity are validated, pair predictions with independently verified final results and calculate market-specific metrics.
4. Do not treat field presence as point-in-time provenance; xG/odds pre-match provenance remains unverified.
5. Keep all work research-only; no production logic/probability/calibration/registry changes.

The 126 staged rows are **not** 126 evaluated predictions. No hit rate, Brier score, log loss or production accuracy is established by this artifact.


## Next step implemented — research team identity audit

Added `scripts/audit_prediction_team_identity.py` and `tests/test_prediction_team_identity.py`. The workflow now runs this audit after the adapter and before artifact upload, using staged predictions and `match_field_audit.csv`.

The audit uses conservative normalized team names and reports exact/normalized unique-name candidates, ambiguous identities and unmatched names. It does **not** assert fixture identity, assign canonical IDs to the prediction ledger, or enable scoring. Every candidate remains research-only until competition, season, kickoff and fixture identity are separately verified. The test suite includes diacritic/suffix normalization, unique candidate not equal to fixture verification, ambiguous IDs and unmatched names.

Script commit: `0777e187136f77cecc465a6214c6dff0b4b7925e`
Test commit: `3770a7e492cefa7a89c66a183e66f7fc9c5f10e3`
Workflow integration commit: `76694afe5babf6a86b8909c60f6338cc378fc73d`

Next step is to inspect the workflow run produced by these commits and report real identity candidate counts. Composite markets remain quarantined. No result evaluation should run until exact fixture identity and trusted result evidence pass their gates. No production logic, probabilities, calibration, or registry was changed.


## Fixture-level candidate audit added — 2026-10-21

Added research-only `scripts/audit_prediction_fixture_candidates.py` and tests `tests/test_prediction_fixture_candidates.py`. The existing archive workflow now runs this step and includes its script/tests in push-trigger paths. It matches normalized home/away names and exact timezone-aware kickoff, then reports candidate archive fixture IDs, season/league folders, competition-hint consistency and ambiguity. Every row is explicitly marked `fixture_identity_verified=false` and `eligible_for_scoring=false`; no prediction or canonical ID is rewritten.

Commits:
- Script: `0123284de4e0bf99ac688113f4ae2fc071d04ada`
- Tests: `280b0969bf8e64955b3ef233196ed7c340659475`
- Workflow integration: `197c33a9e14a57a93af9f50195a88f25dc4ec4f2`

The workflow should auto-trigger on the workflow-file push. Runtime outcome has not yet been verified. The new step is a candidate audit, not a validated prediction-to-result join. Competition hints are provisional and must be reviewed before any scoring. Existing 84 composite-market rows remain quarantined pending explicit market/settlement semantics. No production logic, probabilities, calibration or registry changed.


## Current verified status — Run #52 (2026-10-21)

The earlier sections above are chronological notes and include statuses that were accurate at the time but have since been superseded. **Use this section as the current status.**

- [Research workflow Run #52](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39658148278) completed successfully on validation-repository `main`, commit `96bc5d800a0e1cafb53ec795b248fa17a5f7ba15`.
- Artifact ID `12371679825`, SHA-256 `80a354dcd2b183c1a25416fb5ebfc05d8a32900b7d0c35076abf228d79132fab`.
- The research-only PR [#14](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/14) has been merged to the **validation/research repository only**. This does not alter production model logic.
- Archive audit: 35,819 match records across 126 season folders; zero parse errors; 35,819 parseable kickoffs and archive team IDs; 28,491 rows with score and settled status; archive freshness gate passed.
- Prediction adapter: 210 rows staged, zero quarantined; all 210 remain blocked from evaluation due to missing canonical home and away team IDs.
- Team-name audit: 150 rows have unique candidates for both team names; 60 remain unresolved. Fixture candidate audit: 105 provisional competition-hint-aligned, 20 competition mismatch/crosswalk gap, 85 without an exact kickoff/team candidate; **zero fixture identities verified and zero rows eligible for scoring**.
- Crosswalk remains 43 provider competition names, 25 candidate mappings requiring review, 18 unmatched and zero approved mappings. The intended 44-league universe is not reconciled with the 27-league canonical registry.
- Pre-match xG and odds provenance remain unverified. Canonical production settlement/scorecard evidence still does not support a production accuracy claim.

**Current decision:** archive research audit is complete; historical prediction evaluation and autonomous production readiness remain blocked. Do not report hit rate, Brier score, log loss, calibration or profitability until immutable pre-kickoff predictions, approved exact fixture identities, and independently trusted frozen results pass all gates.

Detailed current report: [Run #52 checkpoint](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/reports/oracle-project-checkpoint-2026-10-21-run52.md).

Next work is a reviewable identity/crosswalk decision table based on the existing audit outputs, followed by authoritative mapping review and trusted result-source setup. Do not silently approve mappings, modify production logic, or purchase provider/API plans. Overall project estimate remains 78%; the successful archive audit does not justify increasing it.


## Follow-up identity diagnosis — Run #52 archive rows (2026-10-21)

A second diagnostic compared each of the 42 unique source fixtures against all 35,819 acquired archive match rows using the same conservative normalized home/away team names, ignoring kickoff only for diagnostic purposes. This is a candidate-discovery check, not a fixture-identity approval.

- 25/42 unique source fixtures have exactly one archive candidate at the exact normalized home/away pair and kickoff: 21 provisionally competition-aligned and 4 marked competition mismatch/crosswalk gap.
- 17/42 unique source fixtures have no exact normalized home-away team pair anywhere in the acquired archive, not merely a kickoff mismatch. These must be checked against the original fixture schedule and authoritative provider/team identifiers; do not create substitute IDs.
- At prediction-row level, the counts remain 105 provisional competition-aligned rows, 20 competition mismatch/crosswalk-gap rows and 85 rows with no exact kickoff/team candidate (5 market rows per fixture).
- The archive pair absence could indicate incomplete selected-league/season coverage, source schedule differences, alias/team-identity differences, or a bad upstream fixture row. The current evidence does not distinguish these causes; no one cause is asserted.

A revised review workbook adds a **Missing Pair Diagnostics** tab listing the 17 unresolved fixtures and required next action:
`Oracle_Run52_Identity_Review_v3.xlsx` (delivered in the conversation). Suggested canonical competition IDs in the workbook are explicitly marked NOT APPROVED and must not be treated as accepted mappings.

Next technical priority is to compare those 17 fixtures with the original prediction-run schedule/manifest and source catalogue team/competition identifiers. If that source does not contain authoritative identifiers, quarantine them. For the 25 candidate fixtures, validate canonical competition/season/team/fixture identity with source evidence before any score join. The result-source allowlist and genuine frozen snapshot remain separate mandatory gates. Production logic and the canonical registry remain unchanged.


## Follow-up diagnostic — missing fixture pairs (2026-10-21)

A second comparison was performed against the exact Run #52 archive artifact, using normalized home/away team pairs independent of kickoff. This narrows the previous 42-fixture review:
- 25 unique fixtures have one exact normalized team-pair candidate at the expected timezone-aware kickoff.
- 21 of those are only provisionally competition-hint-aligned.
- 4 have a competition mismatch/crosswalk gap.
- 17 have no exact normalized home/away team pair anywhere in the acquired archive.

This is a diagnostic finding, not a verified identity join. The 17 may reflect missing archive coverage, source-name/alias differences, schedule/source-row mismatches, or competition/season discrepancies; the current evidence does not distinguish those causes. Do not create IDs or score them by inference.

The review workbook was extended with a `Missing Pair Diagnostics` tab listing the 17 affected fixtures and, where available, archive pair candidates. File produced in the working session: `Oracle_Run52_Identity_Review_v3.xlsx`. It contains 42 unique fixture review rows, 210 prediction-level rows, 43 competition alias review rows, and the missing-pair diagnostic. All approvals remain pending.

## Next actions after Run #52

1. Compare the 17 no-pair fixtures against the original immutable prediction-run schedule and provider fixture/team identifiers. If those records are absent, record an explicit archive-coverage gap and keep the fixtures quarantined.
2. For the 25 exact kickoff/team candidates, verify canonical competition and season, team IDs, and unique fixture ID against authoritative evidence; provisional folder hints are not approval.
3. Obtain a genuine frozen result snapshot and an independently reviewed allowlist with separately pinned hashes. No such trust root has been verified yet.
4. Execute the exact-ID evaluation only for rows that pass every identity, chronology and source-provenance gate; report exclusion reasons before any performance metric.
5. Validate prospective prediction capture and settlement on a repeatable schedule in research before any separate production-readiness decision.

No production changes, provider API calls, or paid plan changes were made for this follow-up diagnostic. Evaluation remains blocked; no accuracy/calibration/profitability claim is supported.


## Root-cause review — missing canonical team IDs (2026-10-21)

Inspection of the live research adapter confirms the immediate blocker is explicit in the input schema:
- `scripts/adapt_oracle_prediction_ledger.py` maps `home_team_id` only from a source column named `home_team_id`, and `away_team_id` only from `away_team_id`.
- When those source fields are absent, it records `MISSING_HOME_TEAM_ID` and `MISSING_AWAY_TEAM_ID` as evaluation blockers. The adapter does not silently substitute team IDs from names.
- The separate team identity audit can propose archive team IDs from unique normalized names, but marks those as candidates and leaves `fixture_identity_verified=false`. It does not write candidate IDs back into the adapted prediction or canonical ledger.

**Immediate technical root cause:** the prediction export does not supply canonical home/away team IDs in the field names and form the adapter currently accepts. The upstream reason those IDs are absent—and whether authoritative provider IDs exist in the original run schedule/manifest—has not been established from the audited artifacts. Do not bypass this fail-closed behavior by filling IDs from name similarity.

Safe remediation:
1. Locate the immutable source prediction export and original run manifest.
2. Check whether they contain stable provider home/away team IDs and fixture/competition IDs under alternate column names. If present, add an explicit research-only schema mapping with regression tests while preserving source columns.
3. If absent, obtain a reviewed provider team/competition/fixture crosswalk from authoritative identifiers. Name-derived matches remain candidates until competition, season, kickoff and fixture identity are reconciled.
4. Re-run the research workflow and verify row-level blocker reductions. Do not modify the production ledger, canonical registry or prediction probabilities.
5. Keep absent or ambiguous identities excluded from scoring.

This explains the immediate missing-ID blocker; it does not resolve the 17 archive team-pair absences or establish trusted result-source provenance. Evaluation remains blocked and no accuracy metrics are warranted.


## Run #53 — manually dispatched audit completed (2026-10-21)

Run #53 completed successfully on `main`, commit `66c2c17eb7b5d5dcb1adf01de3f56285ecf05507`.
- Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39662641163
- Artifact ID: `12375010712`
- Artifact SHA-256 reported by GitHub: `455efdbd9317cbf788793699fdb603d56ffdf525f9422415ea2802fc514359b1`
- All workflow steps, including test suite, archive/catalogue retrieval, archive integrity, feature coverage, crosswalk, prediction adapter, team identity, fixture candidates and artifact upload, completed successfully.
- Archive freshness: `FRESH`, 0.62 days old at the workflow check; no new provider API calls were required.

### Run #53 verified results

- Archive: 35,819 match rows, 126 season groups, zero parser errors, no missing archive team IDs, zero duplicate non-empty fixture IDs.
- Prediction input/staged: 210 / 210; quarantined 0; blocked from evaluation 210.
- Blocker counts: `MISSING_HOME_TEAM_ID=210`, `MISSING_AWAY_TEAM_ID=210`.
- Team-name candidate audit: both team names have unique candidates in 150 rows; 60 rows unresolved; zero fixture identities verified.
- Fixture candidate audit: 105 prediction rows provisionally competition-aligned, 20 competition mismatch/crosswalk gap, 85 no exact kickoff/team candidate; zero eligible scoring rows.
- Crosswalk: 43 provider competition names, 25 candidates requiring review, 18 unmatched, zero approved mappings; intended 44-league universe still not reconciled with the canonical 27-league registry.
- Pre-match xG/odds provenance remains unverified; production eligibility remains `NOT_GRANTED`.

### New source-schema finding

Inspection of the actual source rows inside the Run #53 artifact confirms the canonical prediction export contains `fixture_id`, `competition`, team **names**, `fixture_date`, `kickoff_time`, `prediction_timestamp`, `feature_snapshot_id`, `source_manifest_hash`, probabilities, model version and hashes. It does **not** contain provider/canonical home-team or away-team ID columns, nor a distinct provider fixture ID. The research adapter is therefore correctly refusing to infer those IDs from names.

A search of the private repository found the canonical ledger schema and the prediction publisher, but no matching provider IDs for the staged predictions in the available searched artifacts. The source-export schema gap is verified; whether upstream data can supply IDs without changing the production model is still unresolved. The safe path is to recover provider IDs from the original fixture source/catalogue if present, or use a reviewed external crosswalk that proves competition, season, team and fixture identity. Do not mutate the canonical prediction ledger or assign IDs by name similarity.

### Decision and next step

Run #53 is a successful **research audit**, not a successful evaluation. It confirms that the current data is insufficient for exact identity joins. The next useful step is a research-only diagnostic that compares the 42 source fixture IDs and source schedule rows against the acquired provider catalogue/season manifest, documenting which identities can be linked by authoritative provider identifiers and which remain absent. No further workflow rerun is needed until that source-level diagnostic or a trusted results snapshot changes the evidence. Do not report accuracy/calibration/profitability or production readiness.


## Artifact-level continuation review — 2026-10-22

Run #53 artifact was downloaded and inspected directly (artifact ID 12375010712; 51,603,721 bytes). This is a review of the existing artifact; no new provider calls were made.

### Exact fixture-candidate counts
The 210 staged market rows collapse to 42 distinct source fixtures. At distinct-fixture level:
- 21 have one provisional archive candidate in a competition-aligned folder.
- 4 have a competition mismatch/crosswalk gap.
- 17 have no exact kickoff-and-team candidate.
- 0 are verified fixture identities; 0 are eligible for scoring.

The first example reviewed is HNK Gorica vs Rudeš, scheduled 2026-10-09 16:00 UTC. The artifact proposes FootyStats fixture ID 8546303 in Croatia_Prva_HNL / season 2026_17087; the team identity audit independently proposes home team ID 1875 (normalized unique candidate) and away team ID 1858 (exact unique candidate). These remain candidates only: the prediction export contains no canonical home/away IDs, and the competition crosswalk is not approved. Do not write these candidates back into the source ledger or score them as verified.

### Root cause status
The immediate structural cause is confirmed: the exported prediction rows include `fixture_id`, `competition`, `fixture_date`, `kickoff_time`, `home_team`, and `away_team`, but not separate provider/canonical home-team IDs, away-team IDs, or a distinct provider fixture ID. The research adapter intentionally fails closed rather than synthesizing IDs from names. Whether authoritative IDs can be recovered from an upstream source manifest/catalogue is still unproven.

### Next controlled action
Build a human-review queue for all 42 fixtures, retaining source fixture ID, kickoff, source team names, candidate archive fixture/team IDs, candidate season/competition, candidate status, and explicit approval fields. Keep all candidate IDs unapproved by default. Then trace the original source manifest/catalogue for authoritative provider IDs; if absent, document the required upstream export-schema change as a separate research recommendation. Competition aliases and the 44-vs-27 league-universe reconciliation remain independent review gates. Production eligibility remains NOT_GRANTED.


### Upstream fixture-ID generation traced
Inspection of the private production repository's research publication adapter (`scripts/prepare_prospective_four_market_publication.py`) confirms the source of the ID mismatch: `fixture_id(r)` constructs a local synthetic ID from league code, date, and slugified home/away names. It does not carry a provider fixture ID. The publication schema and canonical ledger schema likewise contain fixture ID and team-name fields, but no separate provider home/away IDs. This explains why the archive join can find candidates but cannot satisfy exact canonical identity gates from the exported prediction rows alone.

This is a schema/provenance gap, not a reason to loosen the research join. The safe fix path is to add source provider fixture/team IDs at the upstream fixture-ingestion/publication boundary, preserve them as separate provenance fields, and backfill only where authoritative source records prove the mapping. That would require a separately reviewed change in the private production repository and must not be implemented as an unapproved production change. Until approved, continue with candidate-only research reporting.


## Run #53 review-queue milestone — 2026-10-22

A fixture-level review queue was generated directly from artifact 12375010712 and saved locally for owner review as `oracle-run53-fixture-review-queue.csv` (42 distinct fixture rows, one per source fixture; each represents five market rows). Candidate IDs and team IDs are explicitly labelled as candidates; every row remains unverified, pending human review, and NOT_GRANTED for production eligibility.

The accompanying research status report is committed at `reports/oracle-run53-fixture-review-queue-status-2026-10-22.md`. Distinct-fixture counts are 21 provisional competition-aligned candidates, 4 competition/crosswalk gaps, and 17 without exact kickoff/team candidates. This differs from market-row counts of 105/20/85 in the workflow summary. No fixture was approved or scored.

Upstream inspection confirmed synthetic fixture ID generation in the private publication adapter and absence of separate provider fixture/team IDs in the canonical exported schema. The next unresolved decision is whether authoritative IDs exist in original upstream fixture inputs; if not, a separately reviewed schema change is required. No private production changes were made because this is outside the approved research-only scope. Historical production accuracy remains unavailable/data-gated.

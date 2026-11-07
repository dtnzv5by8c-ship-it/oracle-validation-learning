# PROJECT ORACLE — CANONICAL CONTINUATION STATE

Last updated: 2026-11-07 10:xx SAST — prospective feature-snapshot capture gap confirmed
Governed branch: `research/oracle-50-league-readiness-audit`

## Current objective
Clear the remaining 50-league validation and release gates and reach governed production prediction readiness without changing Oracle V1.6 production logic.

## Acquisition control-plane
- Universe: 50 leagues
- Provider-season partitions: 182
- Governed endpoint tasks: 728
- Current acquisition accounting: 648 completed + 80 HTTP-417 quarantined/provider-blocked + 0 pending = 728
- Exhausted private ingestion run #92 must NOT be rerun merely because it exited red.

## Major milestone — FootyStats manifest compatibility gate CLOSED
Private FootyStats batch `42255401046`:
- 8,367 rows received
- 100 provider requests
- provider-recorded manifest reference field: `57fe9e1184b5035327feaa78307750e129c54bf3`
- manifest file SHA-256: `58bd06ed9c5a6a09ed55eb833319ca09cd4f01e2b175e4ca9127a1b3a7f689d7`
- 100 explicit completed task IDs

Direct artifact verification:
- Manifest fetched at provider reference `57fe9e...` resolves to actual Git blob `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`.
- Manifest fetched from current governed branch resolves to the SAME Git blob `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`.
- Both files are exactly identical: 116,108 bytes.
- Receipt task IDs matched current governed manifest: 100/100.
- Missing receipt task IDs: 0.

Therefore the provider reference value is not an incompatible manifest. The manifest compatibility gate is **CLOSED**. The 100-task receipt is admissible for those exact tasks and remains a subset of the 728-task universe; it is not additional task completion.

Checkpoint:
`docs/checkpoints/2026-11-07-manifest-compatibility-gate-closed.md`
Commit: `701c34859f00197095465288f2a2b2fcb036b74e`

## Major milestone — 80 HTTP-417 quarantine mapped
The 80 quarantined tasks are exactly 20 provider-season partitions × 4 endpoints:
- Finland Veikkausliiga: 2024, 2025, 2026
- India Indian Super League: 2023/2024, 2024/2025, 2025/2026, 2026/2027
- Republic of Ireland Premier Division: 2024, 2025, 2026
- Russia Russian Premier League: 2023/2024, 2024/2025, 2025/2026, 2026/2027
- South Korea K League 1: 2024, 2025, 2026
- Venezuela Primera División: 2024, 2025, 2026
Endpoints: `league-matches`, `league-teams`, `league-tables`, `league-season`.

## Validated research/readiness evidence
- Selected-50 Market Intelligence repair #360 is complete.
- 717 runtime fixtures had exact archive joins in that artifact.
- Chronological expanding-window research backtests exist but are research-only.
- Canonical settlement ledger now contains 25 settled CHALLENGER rows across 5 fixtures; settlement_source and event_truth_source remain blank, so settlement provenance is incomplete and production admission remains blocked.
- Current private prediction archive contains 900 CHALLENGER rows; 25 rows across 5 fixtures have SETTLED status, but remain research/shadow because the canonical append-only settlement ledger still contains pre-correction blank provenance.
- xG numeric values exist, but point-in-time capture timestamps are not verified.
- Timestamped odds provenance is not verified.
- Production/betting eligibility remains false.

## Major milestone — 648 completed-task evidence VERIFIED — 2026-11-07
The governed 648-completed population is now deterministically reconciled against the current 728-task manifest and private blocked registry.

- 11 private completion checkpoints inspected.
- 748 checkpoint rows contained 648 unique completed task IDs; 100 rows were duplicate IDs from repeated runs and were not double-counted.
- Current governed manifest: 728 task IDs.
- Private blocked registry: 80 task IDs.
- Completed ∩ blocked: 0.
- Manifest IDs missing from completed or blocked: 0.
- Completed IDs outside manifest: 0.
- Exact partition: **648 completed + 80 quarantined + 0 pending = 728**.

Checkpoint:
`docs/checkpoints/2026-11-07-648-completed-task-evidence-reconciled.md`
Commit: `f6f36f33e5f19cd6bece19847e73b988e3ef8502`

The 648 evidence gate is CLOSED/VERIFIED. Do not repeat this reconciliation or rerun ingestion to reproduce the count.

## Major milestone — OMI / Visual Intelligence consolidated readiness matrix
Research-only OMI integration consumed the completed Selected-50 Repair #360 artifact without rerunning it or making provider/API calls.
- 717 runtime fixtures; 717/717 exact archive joins; 0 unmatched/quarantined joins; 0 schedule discordance rows.
- 45 selected leagues represented by fixtures; 5 selected leagues have no fixtures in the inspected report horizon and remain UNVERIFIED, not READY.
- Recent overall form: 1,398/1,434 team-side slots at full five-match depth (97.49%).
- Venue/home-away form: 836/1,434 team-side slots at full five-match depth (58.30%).
- Exact H2H: 604/717 fixtures have prior exact H2H history (84.24%); no H2H inference permitted.
- Goal research: 699/717 (97.49%); BTTS: 678/717 (94.56%).
- xG: 717/717 numeric, but 0/717 verified capture timestamps; production admission BLOCKED.
- Odds: timestamped bookmaker/market provenance unavailable in the baseline; BLOCKED.
- Actual settlement: 717/717 rows remain NOT_RETRIEVED_NO_CREDIT_APPROVAL; no production settlement promoted.
- Runtime feature-block audit: 39 fixtures / 40 team-side histories blocked by minimum-history/required-feature gates.
- Risk fields are diagnostic-ready for represented fixtures; confidence/recency and production performance remain UNVERIFIED.
- Per-league matrix: reports/oracle-omi-release-readiness-matrix-2026-11-07.csv
- Checkpoint: docs/checkpoints/2026-11-07-omi-release-readiness-0744.md

OMI decision: production/betting remains FAIL-CLOSED. The next OMI dependency is the canonical prediction/fixture bridge plus immutable pre-kickoff feature snapshot and verified settlement evidence owned by the Evidence/Validation lanes. No production probability is changed or inferred.

## Major milestone — exact HTTP-417 recovery path prepared — 2026-11-07
The 80 quarantined tasks were given a dedicated fail-closed recovery workflow in the private provider repository:
`.github/workflows/footystats-private-http417-recovery.yml`

Private workflow commit: `632237a2533459af5593f2f683dd00060f66eea2`.

Design controls:
- exact blocked-registry IDs only;
- no completed-task checkpoint reuse or reacquisition;
- governed 728-task manifest subset validation;
- 200/300/500/800 request caps;
- controlled HTTP transport matrix;
- endpoint-specific identity/data validation before admission;
- private-only raw recovery payloads;
- only independently validated recovered IDs are removed from quarantine;
- production/betting eligibility remain false.

## Major milestone — HTTP-417 recovery attempt #1: NO RECOVERY — 2026-11-07
Nolan manually executed the targeted recovery workflow with approved FootyStats API access and a 500-request cap.

Private recovery evidence commit: `e204520257429f984b2e0581f3ea2bc1ebb179d1`.
Recovery identifier: `42345182566`.

Result:
- Target blocked tasks: 80
- Provider requests actually used: 300
- Recovered tasks: **0**
- Remaining blocked tasks: **80**
- Production eligible: false
- Betting eligible: false

The workflow completed successfully, but all tested transport variants continued to produce HTTP 417 / invalid provider responses. The blocked registry was not reduced.

Checkpoint:
`docs/checkpoints/2026-11-07-http417-recovery-attempt-1-no-recovery.md`
Commit: `a9b09b64e35e4e8fb2575efef0fe03f8884b3c88`

Interpretation: this is a successful **negative recovery result**, not a workflow failure. The current transport/parameter experiment is exhausted. Do not repeat the same 300-request experiment without new evidence of a materially different recovery mechanism.

## Major milestone — HTTP-417 access root-cause diagnostic PREPARED — 2026-11-07
Because recovery attempt #1 exhausted the current transport matrix with 300/300 HTTP-417 responses and 0/80 recoveries, a materially different two-call provider-access diagnostic was prepared.

Private diagnostic workflow: `.github/workflows/footystats-private-access-diagnostic.yml`
Commit: `75b22ecadca933a32b3477bc1265bd870c5682cb`
Checkpoint: `docs/checkpoints/2026-11-07-http417-access-root-cause-diagnostic-prepared.md`

Diagnostic purpose: distinguish among account entitlement/selected-league restriction, provider database coverage gap, endpoint/transport problem, or inconclusive provider-list access.

It makes only two provider calls:
- `league-list?chosen_leagues_only=true`
- `league-list`

It compares the exact 20 blocked provider-season IDs against the account's chosen-access seasons and the provider database seasons. It does not call match/team/table/season recovery endpoints and does not admit any production data.

Manual execution is required because the GitHub connector cannot dispatch a newly-created `workflow_dispatch` workflow. Recommended input: `confirm_provider_api_usage=true`.

Production/betting eligibility remains false and Oracle V1.6 production logic/governance are unchanged.

## Major milestone — HTTP-417 access diagnostic: ENTITLEMENT GAP CONFIRMED — 2026-11-07
Nolan executed the two-call diagnostic on the private repository `main` branch.

- Workflow run: `42346762971`
- Workflow source commit: `afdde0f4226c9eba8dbe5bb44d133918e20025be`
- Evidence persisted in private repo commit: `d8ba931c`
- Exact result: both provider league-list calls returned HTTP 200.
- Chosen-league account view contained 756 season IDs.
- Full provider catalogue contained 11,653 season IDs.
- All 20/20 blocked provider-season IDs were absent from chosen-league access but present in the full provider catalogue.
- Classification: **ENTITLEMENT_OR_LEAGUE_SELECTION_GAP**.
- Calls consumed: 2.
- Blocked registry remains unchanged: 80 tasks.

This establishes the current failure as an account-side chosen-league entitlement/selection gap, not a missing provider-database season. Exact league/season mapping was independently read from the full provider catalogue and matches the 20 blocked partitions recorded above.

Checkpoint: `docs/checkpoints/2026-11-07-http417-access-diagnostic-entitlement-gap-confirmed.md`
Commit: `6e60be6d97cd3c4019e950f4ed0c38e8b1ff3d5c`.

Next action: FootyStats account owner/support must enable the exact 20 provider seasons for this account. No further recovery calls should be made until entitlement is confirmed. Once access is granted, perform one low-volume, single-season endpoint validation before any wider recovery. Production/betting eligibility remains false.

## Major milestone — current private prediction archive AUDIT — 2026-11-07
A direct audit of the current private `oracle-football-data/main` canonical archive established that the prediction ledger is populated and later governed executions expanded the archive beyond the earlier 555-row snapshot.

Historical snapshot (superseded, retained for auditability):
- 555 prediction rows
- 111 unique fixtures
- 5 model/market rows per fixture
- fixture dates included 2026-10-09 through 2026-11-15
- all audited rows were CHALLENGER-only
- prediction timestamps, feature snapshot IDs, source manifest hashes, pre-match state hashes, model code SHAs and calibration IDs were present
- chronology checks passed
- canonical settlement ledger was then header-only

Current governed state supersedes that snapshot:
- Private prediction archive: **900 CHALLENGER rows**
- Canonical settlement ledger: **25 settled rows across 5 fixtures**
- Prospective shadow gate: **COLLECTING**
- Production readiness: **HOLD_PROSPECTIVE_AND_RESEARCH_EVIDENCE**
- Automatic promotion: false
- Production change made: false

The 900-row archive remains CHALLENGER-only and therefore does not establish Oracle V1.6 production performance. The key remaining evidence problem is admissible prediction-to-feature-to-settlement linkage and prospective sample maturity, not absence of prediction capture.

The private repository already contains the governed prospective chain:
`prepare_prospective_four_market_publication.py` -> `publish_prediction_run.py` -> `build_prospective_settlement_truth.py` -> `settle_prediction_run.py` -> `feed_learning_ledgers.py`, orchestrated by `.github/workflows/oracle_prospective_learning.yml`.

Checkpoint:
`docs/checkpoints/2026-11-07-current-private-prediction-archive-audit.md`
Commit: `ed1aed7daf31773dbca72db18d6d3a1c12b2d142`.

Do not treat the older 555-row snapshot as current state.

## Major milestone — prospective settlement blocker root cause identified — 2026-11-07
Direct audit of the current private prediction archive against `database/current_matches.csv` found:
- 555 current challenger prediction rows / 111 unique fixtures.
- Exact date + normalized home/away match joins: **0/111**.
- Current truth snapshot covers 2026-10-30 through 2026-11-08.
- Prediction dates include 2026-10-09 through 2026-10-17 (outside the current truth snapshot), plus 2026-11-06 through 2026-11-08.
- Stored 2026-11-06 through 2026-11-08 rows are present but marked `finished=False` in the persisted snapshot, so the settlement builder correctly excludes them.
- 2026-11-14 and 2026-11-15 predictions are future and must remain unsettled.

Therefore the current zero-settlement result is a **result-truth freshness/coverage blocker**, not evidence that the prediction ledger or settlement rules are broken.

Checkpoint: `docs/checkpoints/2026-11-07-prospective-settlement-root-cause.md`
Commit: `57a4d8d8d9bac2b5aa0067de0cb7764e5f0fe61c`.

The next safe action is to execute the existing governed `Oracle Prospective Learning Cycle` on private `main` so it refreshes current result truth and re-attempts exact settlement. Historical 2026-10-09 to 2026-10-17 rows still require an independently verified historical result source; they must not be inferred from current/future snapshots.

## Major milestone — OMI market release-readiness consolidation — 2026-11-07 08:43 SAST
The OMI lane consumed the existing 50-league matrix and the completed Selected-50 Repair #360 baseline without rerunning repair or making provider/API calls.

New report:
`reports/oracle-omi-market-readiness-2026-11-07.md`
Checkpoint:
`docs/checkpoints/2026-11-07-omi-release-readiness-0843.md`

Deterministic 50-league matrix accounting:
- Fixture identity: 45 READY / 5 UNVERIFIED.
- Chronology: 45 READY / 5 UNVERIFIED.
- Recent overall form: 43 READY / 2 INSUFFICIENT SAMPLE / 5 UNVERIFIED.
- Home/away: 15 READY / 19 PARTIAL / 11 INSUFFICIENT SAMPLE / 5 UNVERIFIED.
- Exact H2H: 21 READY / 24 PARTIAL / 5 UNVERIFIED; no inferred H2H.
- Goals/goal rates: 43 READY / 2 INSUFFICIENT SAMPLE / 5 UNVERIFIED.
- BTTS: 31 READY / 14 PARTIAL / 5 UNVERIFIED.
- Over 1.5: 43 READY / 2 INSUFFICIENT SAMPLE / 5 UNVERIFIED.
- Over 2.5: 42 READY / 1 BLOCKED / 2 INSUFFICIENT SAMPLE / 5 UNVERIFIED.
- Over 3.5: 45 BLOCKED / 5 UNVERIFIED.
- xG: 1 READY / 44 BLOCKED / 5 UNVERIFIED; point-in-time provenance remains a production gate.
- Standings/strength: 45 READY / 5 UNVERIFIED.
- Odds provenance: 45 BLOCKED / 5 UNVERIFIED.
- Sample size: 45 READY / 5 UNVERIFIED.
- Recency: 50 UNVERIFIED.
- Confidence: 50 UNVERIFIED for production.
- Risk: 45 READY as diagnostics / 5 UNVERIFIED.
- Actual results: 45 BLOCKED / 5 UNVERIFIED.
- Leakage-safe production backtest: 50 UNVERIFIED.
- Production eligibility: 50 BLOCKED.

Production probability strings and the canonical Oracle V1.6 fixture/probability bridge are not present in the public OMI artifact; no probability was inferred or reconstructed. Team DNA and League DNA were not inferred from proxy fields and remain UNVERIFIED for production integration.

OMI release gates remain: canonical fixture/probability bridge; immutable pre-kickoff feature snapshots; point-in-time xG; timestamped odds; verified official settlement; prediction-to-feature-to-settlement linkage; per-market sample gates; and current-feed recency/freshness. Quarantined evidence remains excluded.

Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance remain unchanged. Production/betting remain fail-closed.

## Major milestone — provenance correction exercised — 2026-11-07 10:xx SAST
The controlled private builder correction `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7` has now been exercised by subsequent governed execution. The generated `research/four_model/outputs/prospective_settlement_truth.csv` contains explicit `settlement_source=FotMob governed current-match feed: database/current_matches.csv` and `event_truth_source=NOT_REQUIRED_FINAL_SCORE_MARKETS` for final-score markets.

The canonical append-only settlement ledger was not rewritten and remains at 25 pre-correction settled rows with blank provenance. This is correct evidence preservation: the old rows are not retroactively mutated. The current generated truth artifact proves the correction works, but a new legitimate settlement append carrying the corrected provenance has not yet occurred.

Private evidence commit exercising the correction: `ff12451558e100fc2717985d2ed3ca8ee7596937`.
Checkpoint: `docs/checkpoints/2026-11-07-provenance-correction-exercised.md`

## Major milestone — settlement provenance admission gate hardened — 2026-11-07
Live audit found that the corrected truth artifact carried provenance but the feeder did not itself reject blank provenance. Private `scripts/feed_learning_ledgers.py` was hardened at commit `ee77a592d71f00bf0033f7dc1f0f65f0873138a1` so any newly admitted `SETTLED` row missing `settlement_source` or `event_truth_source` now fails closed. Existing pre-correction ledger rows remain immutable and are not rewritten.

Checkpoint: `docs/checkpoints/2026-11-07-settlement-provenance-admission-gate.md`

## Major milestone — historical prediction chain audit — 2026-11-07
The live private prediction archive was audited for 2026-10-09 through 2026-10-17: 210 prediction rows across 42 fixtures, with prediction IDs, fixture IDs, kickoff/prediction timestamps, data/event cutoffs, feature snapshot IDs, source manifest hashes and pre-match state hashes present. Chronology is structurally valid. However all 210 rows are explicitly CHALLENGER evidence; calibrated probability is blank and model-code/calibration fields are not production-admissible. Therefore the identity chain exists at ledger level but cannot be promoted as Oracle V1.6 production evidence. Feature snapshot contents and verified settlement still require admissible linkage.

Checkpoint: `docs/checkpoints/2026-11-07-historical-prediction-chain-audit.md`

## Major milestone — prospective persistence race fixed — 2026-11-07
Private Oracle Prospective Learning Cycle run #430 (`42354024509`) completed stages 01–16 successfully but failed only in stage 17, Persist prospective evidence.

Root cause:
- the dedicated current-data workflow advanced `main` from `ee77a592` to `645b698` while the learning cycle was running;
- the learning cycle attempted `git pull --rebase origin main`;
- `data/current_source_manifest.json` had changed concurrently, causing a rebase conflict and exit code 1.

This was a Git persistence race, not a prediction, settlement, provenance, model, or production-readiness failure.

Repair:
- private workflow commit `82d024f4913311d8d9d45394c8b8cdf14b1cee08`;
- shared current-data staging files are no longer committed by the learning cycle;
- persistence now fetches latest `origin/main`;
- a rebase race is handled by rebuilding the evidence commit on the latest `main`;
- Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance were not changed.

Checkpoint:
`docs/checkpoints/2026-11-07-prospective-persistence-race-fixed.md`
Commit: `1be6f7a41253e43c0ecec1dbe7bab495a9657e9b`.

The workflow-file repair automatically triggers a fresh prospective cycle. Do not manually rerun failed run #430.

## Major milestone — prospective cycle 431 SUCCESS — 2026-11-07
Private Oracle Prospective Learning Cycle 431 (`42354699246`) completed all 17 governed stages successfully on repaired workflow commit `82d024f4913311d8d9d45394c8b8cdf14b1cee08`.

- Stage 17 persistence succeeded and pushed evidence commit `85c630e` without the previous rebase race.
- Corrected settlement truth builder produced 25 truth rows with explicit FotMob settlement provenance and `NOT_REQUIRED_FINAL_SCORE_MARKETS` event-truth provenance.
- Settlement append count was 0 because the 25 settlements were already present; no historical ledger rows were mutated.
- Prediction rows: 900; settled rows: 25; shadow gate: COLLECTING; production readiness: HOLD_PROSPECTIVE_AND_RESEARCH_EVIDENCE.
- Point-in-time leakage audit: PASS, 12,836 matches / 12,836 state rows / 25,672 checked rows / 0 violations.
- No provider acquisition or HTTP-417 recovery was run; quarantine remains 80 tasks.

The canonical append-only 25 rows retain their original blank provenance by design. A future newly settled prediction must pass the hardened provenance admission gate to create the first corrected canonical append. No retroactive mutation is permitted.

Checkpoint: `docs/checkpoints/2026-11-07-prospective-cycle-431-success.md`
Commit: `b0825f9563dcf0ce71ecd3ad9827d82a252d5da5`

## Major milestone — prospective feature-snapshot capture gap CONFIRMED — 2026-11-07
A direct audit of private `oracle-football-data/main` after prospective cycle #431 identified a genuine evidence-control blocker.

Live state:
- private main HEAD: `85c630e677c1ac408672973e4f0c643d31a9fc19`
- prediction archive: 900 CHALLENGER rows / 180 fixtures
- canonical settlement ledger: 25 rows / 5 fixtures
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv`: header-only, 0 snapshot rows

The current publication adapter generates `feature_snapshot_id` from metadata/probability/source hashes, but does not materialize the actual pre-match feature vector used by the prediction engine. Therefore the ID is not sufficient evidence of an immutable feature snapshot.

Independent reconstruction against the locked historical prematch-state artifact found:
- 175/180 prediction fixtures have both home and away pre-match states available before fixture date;
- 4/180 have one side;
- 1/180 has neither.

This demonstrates that the underlying dataset is substantially available, but the exact feature vector was not captured as an immutable prediction-time artifact.

A second provenance defect was confirmed: current prospective `model_code_sha` values are inherited from the workflow `GITHUB_SHA`. The latest batch uses `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7`, which is the settlement-provenance commit rather than the prediction-engine code revision. The prediction-engine file is unchanged at that commit and has blob SHA `fe28863f24609dad7536e9a6a964a864b9f4bb5b`.

Decision:
- classify this as an evidence/reporting-control blocker;
- do not alter Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility or governance;
- do not rewrite the 900 historical prediction rows;
- repair future challenger evidence capture so actual feature vectors and the true prediction-engine revision are immutably bound to each prediction.

Checkpoint:
`docs/checkpoints/2026-11-07-prospective-feature-snapshot-capture-gap.md`
Commit: `590d68f2264d4fdfba914961851c1afadea9a5d9`.

## Major milestone — feature-snapshot capture implementation corrected — 2026-11-07
A live audit found that the first feature-snapshot repair referenced the new capture routine but the helper implementation was not actually persisted in the publication adapter. The feature-snapshot evidence gate therefore remained open.

Corrected private commit:
`714b85c5f1e7cbef2f541b6b5db81a61c11d95c6`

The corrected adapter now materializes the actual pre-match team-state feature inputs used by `oracle_four_model_predict.py`, writes immutable `FEATURE_SNAPSHOT_MANIFEST.csv` and `FEATURE_SNAPSHOT_VALUES.csv`, binds fixture-level prediction rows to the snapshot, and records the exact Git blob SHA of the prediction-engine file for model-code provenance.

Run #434 is still executing the prior revision and has not reached publication. Run #435 was automatically queued from the corrected commit. The feature-snapshot gate remains OPEN until a fresh governed execution persists non-empty snapshot artifacts and exact prediction-to-snapshot linkage is independently verified.

Checkpoint: `docs/checkpoints/2026-11-07-feature-snapshot-capture-implementation-corrected.md`
Commit: `0c8af2c9e5326a3e8af7d04b81999ba9be2a8191`.

## Immediate next work — priority order
1. Keep all 80 HTTP-417 tasks quarantined; do not substitute other seasons/providers or infer missing data.
2. Determine whether an evidence-backed alternative acquisition path exists for the exact 20 blocked provider-season partitions, without reopening the exhausted full ingestion queue.
3. Build/validate the immutable prediction → fixture → pre-kickoff feature snapshot → verified settlement linkage using existing evidence.
4. Establish production scoreability: admissible production probability strings, model/version identity, feature-release hash, prediction timestamp, exact fixture/market identity, and verified settlement source.
5. Run leakage-safe chronological backtests only on admissible prediction/settlement pairs; keep research/shadow metrics research-only.
6. Close xG/odds point-in-time provenance only where evidence genuinely supports it.
7. Hand validated evidence to OMI/Visual Intelligence/release readiness; keep production and betting gates fail-closed.

The 648/80 acquisition reconciliation and manifest-compatibility gate are CLOSED/VERIFIED and must not be repeated.

## Do not repeat
- Do not rerun ingestion #92 as a generic full-universe run.
- Do not rerun the disabled protected-repository audit.
- Do not rerun the completed Selected-50 Market Intelligence repair baseline.
- Do not reacquire batch `42255401046`.
- Do not repeat manifest compatibility reconciliation.
- Do not repeat the identical HTTP-417 recovery transport experiment without new evidence.
- Do not reinterpret research/shadow metrics as production accuracy.
- Do not change Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility or governance.

## Coordination
- Validation lane: 50-league data/readiness and provider-gap reconciliation.
- Evidence lane: prediction/settlement linkage and leakage-safe backtesting.
- OMI lane: consolidated OMI/Visual Intelligence/release reporting.
- All lanes must read this state + lessons, inspect live HEAD, reconcile intervening commits, and checkpoint every major milestone.

## Major milestone — settlement provenance control corrected — 2026-11-07
The latest private prospective cycle produced 25 settled CHALLENGER rows across 5 fixtures. Direct inspection of the live settlement chain showed that final-score truth was correctly derived from completed `database/current_matches.csv` rows, but the builder did not emit `settlement_source` or `event_truth_source`. The downstream settlement script already preserves those fields.

Controlled correction:
- Private repo `oracle-football-data`, branch `main`
- File: `scripts/build_prospective_settlement_truth.py`
- Commit: `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7`
- Final-score settlement provenance is now explicitly emitted as `FotMob governed current-match feed: database/current_matches.csv`.
- Final-score markets explicitly mark event-truth provenance as `NOT_REQUIRED_FINAL_SCORE_MARKETS`.
- M1UP/event chronology remains blank and data-gated; no first-goal truth is inferred.

This is an evidence/provenance correction only. Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance are unchanged.

The correction was made without running a private GitHub Actions workflow, preserving the 3,000-minute private Actions budget. The next legitimate prospective cycle will exercise the corrected builder. No duplicate manual run is requested.

## Current prospective evidence after latest governed execution
- Private prediction archive: 900 CHALLENGER rows.
- Canonical settlement ledger: 25 settled rows across 5 fixtures.
- Prospective shadow gate: COLLECTING; 5 settled observations per governed model, below the 100-row / 8-day minimum.
- Production readiness: HOLD_PROSPECTIVE_AND_RESEARCH_EVIDENCE.
- No automatic promotion; production models remain on the existing governed benchmark.

## Remaining release blockers
1. 80 HTTP-417 tasks remain quarantined across 20 provider-season partitions because the FootyStats account diagnostic confirmed an entitlement/league-selection gap. Do not repeat the exhausted transport experiment until entitlement changes.
2. Historical 2026-10-09 and 2026-10-10 Bundesliga result truth is independently reconfirmed (Dortmund 2-2 Bremen; Mainz 3-4 Leverkusen). The broader 2026-10-09 through 2026-10-17 production linkage still requires exact prediction-ID/feature-snapshot/result linkage.
3. The canonical append-only settlement ledger still contains 25 pre-correction rows with blank provenance; the corrected truth builder is exercised and the feeder is now fail-closed on missing provenance. A fresh corrected settlement append is still required.
4. xG numeric values exist but point-in-time capture timestamps are not verified.
5. Timestamped odds provenance is not verified.
6. Immutable prediction → fixture → pre-kickoff feature snapshot → verified settlement linkage must be demonstrated for production-admissible evidence.
7. Per-market prospective sample and observation-window gates remain open.
8. OMI/Visual Intelligence production readiness remains blocked until the canonical probability bridge, point-in-time features, verified settlement and current-feed freshness gates are satisfied.

## Resource-control rule
Private `oracle-football-data` Actions are scarce (3,000 minutes/month). Use the public `oracle-validation-learning` repository for research, validation, reconciliation, reporting and non-sensitive computation whenever private credentials/provider access are not required. Do not launch duplicate private workflows.

## Definition of done
Production prediction readiness requires genuinely satisfied identity, chronology, point-in-time feature provenance, prediction/settlement linkage and required market/league gates. Missing/quarantined evidence remains excluded. Fail-closed remains active until gates pass.


## Major milestone — OMI final release-gate register — 2026-11-07 10:40 SAST
The OMI lane consumed the authoritative continuation state, lessons learned, latest checkpoints and the existing Selected-50 Repair #360 artifact. No acquisition, provider/API call, repair rerun, settlement rerun or production-model change was performed.

New research-only report:
- reports/oracle-omi-release-gate-register-2026-11-07.md
- Checkpoint: docs/checkpoints/2026-11-07-omi-final-release-gate-register-1040.md

The report consolidates 22 release gates and explicitly separates READY, PARTIAL, BLOCKED, INSUFFICIENT SAMPLE and UNVERIFIED evidence. It does not infer production probabilities, H2H, point-in-time availability, xG provenance, odds provenance or settlement.

Current release-critical blockers remain:
1. Canonical Oracle V1.6 production probability -> fixture/market bridge.
2. Immutable materialization of the actual pre-match feature vector used for each new challenger prediction.
3. Correct prediction-engine code revision attribution, separate from workflow commit SHA.
4. Point-in-time xG provenance.
5. Timestamped odds provenance.
6. Current-feed freshness/recency proof.
7. Verified settlement append using corrected provenance plus immutable prediction/feature linkage.
8. Per-market sample and observation-window gates.

The 80 HTTP-417 tasks remain quarantined and excluded. The 900 historical challenger rows remain immutable research/shadow evidence; no retroactive feature snapshots are fabricated. Production and betting eligibility remain false.

Next OMI action is deterministic consumption of the next canonical Evidence/Validation outputs and exact-ID/market-key reconciliation into the existing matrix. No manual OMI dispatch is required for this milestone.

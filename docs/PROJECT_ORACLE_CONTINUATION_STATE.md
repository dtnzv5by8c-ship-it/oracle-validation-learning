# PROJECT ORACLE — CANONICAL CONTINUATION STATE

Last updated: 2026-11-07 10:xx SAST — exact prediction-engine commit attribution repair
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

## Major milestone — prospective persistence snapshot guard corrected — 2026-11-07
Prospective Learning Cycle #434 completed stages 01–16 and failed only at stage 17 because `archive/FEATURE_SNAPSHOT_VALUES.csv` did not exist:
`fatal: pathspec 'archive/FEATURE_SNAPSHOT_VALUES.csv' did not match any files`.

This was an evidence-persistence robustness defect, not a model/prediction/settlement failure. The artifact is optional when no complete feature-value rows are materialized; the workflow must not fabricate it.

Private workflow correction:
`da549a80db2b545a739b9301b050131611a5afd1`

Stage 17 now conditionally stages the feature snapshot manifest/values files only when they actually exist, while retaining fail-closed evidence requirements. The feature-snapshot gate remains OPEN until a fresh governed execution proves non-empty immutable snapshots, complete admissible feature values, exact prediction-to-snapshot linkage, strict pre-kickoff status and exact prediction-engine code attribution.

Checkpoint: `docs/checkpoints/2026-11-07-prospective-persistence-snapshot-guard-corrected.md`
Commit: `f510381c6f9cd51413aa5a2167a832f15b126502`.

## Major milestone — prospective persistence YAML corrected — 2026-11-07
The conditional feature-snapshot persistence change was initially mis-indented in the private workflow. Run #436 failed before job execution as a result. The workflow was corrected at private commit `2e9110ac2f0a076c797fc54de309f57caf41e439`.

The normal and rebase-rebuild evidence staging paths now correctly conditionally stage `FEATURE_SNAPSHOT_MANIFEST.csv` and `FEATURE_SNAPSHOT_VALUES.csv` only when those artifacts exist. No empty evidence is fabricated.

Feature-snapshot evidence remains OPEN pending a fresh governed execution through successful persistence and independent artifact/linkage verification.

Checkpoint: `docs/checkpoints/2026-11-07-prospective-persistence-yaml-correction.md`
Commit: `5cb79b6b539cc4107349cf8433e01078cfd4c76f`.

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


## Major milestone — exact prediction-engine commit attribution repaired — 2026-11-07
The prospective publication adapter now records model_engine_commit_sha separately from the existing model_code_sha Git blob SHA. This closes the identified attribution-control defect for newly generated challenger evidence without changing Oracle V1.6 production logic or governance.

Private production repository commit: dd8464867467312a78f11f53745c6cbb6366ace0.

Validation run #588: 42357365438 in progress. Prospective Learning Cycle #438: 42357365453 pending behind cycle #437. Existing historical 900 challenger rows remain immutable and were not rewritten.

Checkpoint: docs/checkpoints/2026-11-07-exact-prediction-engine-commit-attribution.md.
## Major milestone — evidence-control live re-audit after prediction-engine attribution repair — 2026-11-07 10:59 SAST
The latest private evidence was re-audited after the exact prediction-engine commit-attribution repair dd8464867467312a78f11f53745c6cbb6366ace0.

Verified private main state:
- Private HEAD: dd8464867467312a78f11f53745c6cbb6366ace0.
- Validation workflow run 42357365438 completed successfully; Python syntax/compile validation passed.
- Prospective Learning Cycle 42357365453 is pending behind the preceding cycle; no duplicate/manual rerun was performed.
- Prediction archive: 900 unique CHALLENGER prediction rows across 5 governed markets; no Oracle V1.6 production prediction rows.
- Canonical settlement ledger: 25 unique SETTLED CHALLENGER rows across 5 fixtures; all 25 still have blank settlement_source and event_truth_source.
- archive/FEATURE_SNAPSHOT_MANIFEST.csv remains header-only (0 persisted snapshot rows); FEATURE_SNAPSHOT_VALUES.csv is absent on private main.

Control interpretation:
- The prediction-engine attribution repair is code-validated but not yet exercised into a persisted non-empty feature-snapshot artifact. Feature-snapshot evidence gate remains OPEN.
- Settlement provenance correction is exercised in the generated truth artifact, but the canonical append-only ledger remains unchanged at the 25 pre-correction rows. Do not rewrite historical rows. A fresh corrected settlement append is still required before the settlement provenance gate can close.
- No new provider/API acquisition was performed. The 80 HTTP-417 tasks remain quarantined.
- No production/betting evidence is promoted. production_eligible=false; betting_eligible=false.

Highest-value next gate: allow the already-pending governed prospective cycle to execute on the repaired private main, then independently verify non-empty feature snapshot manifest/values, exact prediction-to-snapshot linkage, true prediction-engine commit attribution, pre-kickoff leakage status, and any newly admitted settlement provenance. Do not launch a duplicate cycle while the pending run is queued.


## Major milestone — prospective cycle #438 exercised exact engine attribution — 2026-11-07
Prospective Learning Cycle #438 (run `42357365453`) completed successfully on private HEAD `dd8464867467312a78f11f53745c6cbb6366ace0`. All 17 stages completed. The publication adapter emitted the exact prediction-engine commit attribution `model_engine_commit_sha=dd8464867467312a78f11f53745c6cbb6366ace0`, confirming the attribution repair is exercised in a governed execution.

The cycle produced no new eligible future-kickoff prediction rows: 0 candidates, 36 kickoff-gated rows and 630 duplicates skipped. Consequently, feature-snapshot capture produced 0 new snapshots. `archive/FEATURE_SNAPSHOT_MANIFEST.csv` remains header-only and `archive/FEATURE_SNAPSHOT_VALUES.csv` remains absent. No retroactive or fabricated snapshots were created.
The corrected settlement truth builder also executed successfully and emitted governed final-score provenance in `research/four_model/outputs/prospective_settlement_truth.csv`, but the canonical append-only settlement ledger remains at 25 pre-correction rows with blank provenance because there were no new eligible predictions to settle. Historical rows were not rewritten.

Checkpoint: `docs/checkpoints/2026-11-07-prospective-cycle-438-exercised-attribution-no-eligible-new-fixtures.md` (commit `4c051828cc5dd191606c969b143938bb9c79ff0c`).

Control interpretation: the prediction-engine attribution gate is now code-validated and execution-exercised; the immutable feature-snapshot gate remains OPEN due to absence of new admissible prediction rows. The next useful evidence event is a governed cycle containing genuinely new future fixtures. Do not launch duplicate cycles merely to manufacture snapshots, and do not rewrite historical challenger evidence.

Current production posture remains fail-closed: `production_eligible=false`, `betting_eligible=false`. The 80 HTTP-417 tasks remain quarantined. xG/odds point-in-time provenance and canonical prediction→snapshot→settlement linkage remain unresolved.


## Major milestone — 50-league prospective fixture coverage gap quantified — 2026-11-07
A live-state audit established a new release-critical mismatch: the governed historical universe contains exactly 50 selected leagues, but the prospective fixture-ingestion layer remains a legacy 27-league registry and the latest persisted fixture board contains only 14 unique league codes.

Evidence:
- `data/footystats/selected50-full-ingestion-manifest.csv`: exactly 50 selected leagues / 728 endpoint tasks.
- Private receipt `gateway/receipts/footystats-50-league-latest.json`: Oracle-50-League, expected_leagues=50, historical private archive receipt; non-production/non-betting eligible.
- `data/fixtures/oracle_upcoming_fixtures_manifest.json`: 27 targets, 14 `OK_FALLBACK`, 13 `SOURCE_ERROR`.
- `data/fixtures/oracle_upcoming_fixtures.csv`: only 14 unique league codes currently persisted.
- `scripts/ingest_upcoming_fixtures.py`: active registry is explicitly hardcoded to 27 leagues.

Root cause: historical 50-league acquisition identity and prospective fixture coverage are separate controls; the prospective registry was never advanced to 50 leagues. The existing 27-league source/fallback path also has 13 current source errors.

Impact: the prospective lane cannot claim governed 50-league fixture coverage, so 50-league production prediction readiness cannot be admitted. This is distinct from the already-closed 648/80 historical acquisition accounting and HTTP-417 quarantine.

Next action: build the canonical 50-league prospective fixture registry from the existing governed identity set, verify explicit current-season source/competition identifiers, preserve fail-closed diagnostics, and require fixture-board reconciliation before prediction publication. Do not rerun generic ingestion or repeat FootyStats recovery merely to address this finding.

Report: `reports/oracle-50-league-upcoming-coverage-audit-2026-11-07.md`
Checkpoint: `docs/checkpoints/2026-11-07-50-league-prospective-coverage-gap.md` (commit `7afaf34352379587fcf3d7ca55585dc22f2961ad`).

Production remains fail-closed; Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance remain unchanged.


## Major milestone — canonical 50-league prospective source registry established — 2026-11-07
The Validation lane has now converted the existing governed 50-league identity set into an explicit prospective source registry without changing Oracle V1.6 production logic or touching the exhausted historical acquisition queue.

New artifact:
- `data/prospective/oracle_50_league_fixture_source_registry.csv`
- 50/50 governed identities represented.
- 49/50 have an explicit current-season OpenFoot catalogue mapping.
- Greece Super League maps to `comp_super_league_grc`, but OpenFoot currently advertises only 2024/25 for that competition; it is therefore explicitly `CURRENT_SEASON_NOT_VERIFIED` and remains DATA_GATED.

OpenFoot coverage evidence confirms stable competition IDs and season labels; its own documentation warns that coverage/fields vary by competition and that empty responses must not be interpreted as no data. No fixture availability is inferred from the catalogue alone.

Checkpoint: `docs/checkpoints/2026-11-07-50-league-source-registry-milestone.md` (commit `fe12add538ac373a3d78b82922ffb2f9db839ea7`).

Next highest-value action: probe the explicit 49 current-season competition IDs plus the Greece data-gated path for the governed upcoming window, persist per-league source evidence, and reconcile the resulting fixture board exactly to the 50-league registry. Keep fail-closed behavior for missing/ambiguous sources. Do not publish predictions until that reconciliation passes.


## Major milestone — downstream 50-league prediction scope audit — 2026-11-07
The next downstream control gap is now confirmed: `scripts/oracle_four_model_predict.py` still contains a hardcoded 27-league `ACTIVE` allow-list and filters incoming fixtures with `league_code.isin(ACTIVE)`.

This means a 50-league fixture board would not currently flow end-to-end into the prediction batch. The finding is separate from the fixture-ingestion registry gap and has been recorded without changing production code.

Audit: `reports/oracle-50-league-downstream-scope-audit-2026-11-07.md`
Checkpoint: `docs/checkpoints/2026-11-07-50-league-downstream-scope-audit.md` (commit `0c4db381529a0ed370a0e7dc506bbacd36474e25`).

Control rule: do not simply expand the production allow-list yet. First validate actual current-season fixture responses for the canonical source registry. Then update downstream scope as a controlled data/universe configuration change, preserving strict missing-state gates and all Oracle V1.6 model/calibration/governance logic.

## 50-league end-to-end scope lock
- Governed Oracle universe is **50 leagues**, not 27, for the full Oracle prediction and intelligence stack.
- The 50-league scope applies end-to-end across: fixture ingestion, all governed markets, Oracle predictions, Visual Intelligence/OMI, recent-form/current-team-state features, home/away splits, exact H2H, goals/goal rates, BTTS, Over/Under markets, DC/Combo markets, M1UP where event-truth gates permit, risk/confidence diagnostics, settlement/actuals, and downstream validation/reporting.
- A league being data-gated or source-error does **not** remove it from the governed universe; it remains represented and fail-closed until evidence makes that league/market admissible.
- No 27-league allow-list is an acceptable production scope for any end-to-end Oracle layer.
- This scope statement is a control-plane requirement only; it does not alter Oracle V1.6 model logic, probabilities, thresholds, calibration, betting eligibility or governance.
- Next controlled implementation: reconcile the canonical 50-league source registry to live fixture responses, then replace legacy 27-league downstream scope controls with the governed 50-league registry/codes while preserving strict missing-data gates.

## Major milestone — 50-league live fixture-source validator prepared — 2026-11-07
A read-only validator has been added against the canonical 50-league prospective source registry. It probes the explicit current-season OpenFoot competition IDs for the governed window 2026-11-07 through 2026-11-21 and classifies every governed league as READY, DATA_GATED or SOURCE_ERROR. It preserves all 50 identities even when no usable fixture evidence is returned.

- Script: `scripts/validate_oracle_50_league_live_fixture_sources.py`
- Research workflow: `.github/workflows/oracle-50-league-live-fixture-source-validation.yml`
- Scheduled execution is hosted from validation-repository default branch and checks out the governed `research/oracle-50-league-readiness-audit` branch before probing.
- Evidence artifact: `artifacts/oracle_50_league_live_fixture_source_validation.json`
- No FootyStats calls are made.
- No Oracle V1.6 production code, probabilities, thresholds, calibration, betting eligibility or governance are changed.
- The validator is intentionally read-only against Oracle data/model state; it only persists sanitized source-validation evidence.

Validation is not yet considered passed until a real workflow execution produces the 50-league result artifact and exact board reconciliation is completed.


## Major milestone — 50-league fixture board reconciliation control added — 2026-11-07
The live 50-league source validator now has a deterministic identity-reconciliation control between raw provider evidence and any future downstream scope decision.

- Reconciliation script: `scripts/reconcile_oracle_50_league_fixture_source_validation.py`
- Required controls:
  - exactly 50 governed registry rows
  - exactly 50 validation rows
  - exact governed league-ID set equality
  - zero missing IDs
  - zero unexpected IDs
  - zero duplicate IDs
- Output: `artifacts/oracle_50_league_fixture_source_reconciliation.json`
- The default-branch scheduled validation workflow now runs the reconciliation immediately after live source validation and persists both sanitized artifacts.
- Reconciliation commit: `0e03534b44dd0b6eaca56f19a3a61528ed1d5a01`
- Workflow integration commit: `21363c4da6a336a542a0e44b9e9f279a6cb63228`
- Checkpoint: `docs/checkpoints/2026-11-07-50-league-fixture-board-reconciliation-control.md`

Important: this is a control-plane/research milestone only. The live source-validation gate is still **NOT PASSED** until a genuine scheduled/manual workflow execution produces the validation artifact and the reconciliation returns PASS. Do not expand the private production 27-league allow-list before that evidence exists. Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance remain unchanged.


## Major milestone — 50-league code namespace reconciliation audit — 2026-11-07
A live inspection of the private prediction engine confirmed that the canonical 50-league source registry and the legacy prediction-engine league-code namespace are not directly interchangeable.

- Production engine file: `scripts/oracle_four_model_predict.py`
- Legacy ACTIVE namespace: 27 codes.
- Canonical governed source registry: 50 source codes.
- Direct code-string intersection: only `CRO`.
- 49/50 governed source identities therefore require an explicit evidence-backed identity bridge before downstream production scope can be safely advanced.
- Research audit: `reports/oracle-50-league-code-namespace-reconciliation-audit-2026-11-07.md`
- Checkpoint: `docs/checkpoints/2026-11-07-50-league-code-namespace-reconciliation.md`
- Audit commit: `3bc236c84261462da5e47add2779b050d7d1e56a`

This is a data/universe configuration control, not a model-logic change. Do not blindly substitute canonical source codes for legacy engine codes. The next implementation step is to derive and validate an exact one-to-one identity bridge from existing fixture/database metadata and governed source identities. Unmapped identities must remain explicitly fail-closed.

## Major milestone — 50-league internal identity bridge research — 2026-11-07
A research-only 50-row bridge now maps the canonical governed 50-league source registry toward the existing Oracle internal league-code namespace without changing production code.

- Bridge: `data/prospective/oracle_50_league_internal_identity_bridge_research.csv`
- Exactly 50/50 governed identities represented once.
- 15 mappings have direct, unique evidence from the existing internal `LEAGUE_NAME_TO_CODE` mapping.
- 26 remain UNMAPPED and fail-closed.
- 4 are CROSS-NAMESPACE_NAME_VARIANT and remain fail-closed.
- 2 are CODE_COLLISION (including D1 used by both Bundesliga and Denmark Superliga) and remain fail-closed.
- 1 is CODE_NAMESPACE_UNVERIFIED (Germany 2. Bundesliga) and remains fail-closed.
- 1 is NAME_VARIANT_UNVERIFIED (Croatia) and remains fail-closed.
- 1 is UNVERIFIED (Greece) and remains fail-closed.
- Research checkpoint: `docs/checkpoints/2026-11-07-50-league-internal-identity-bridge-research.md`
- Bridge creation commit: `044fc3e7e153d79305b3fdc103c14071bf1d0225`
- Checkpoint commit: `9799bc1dd3e1cc2ed4b1fb0c94cfc28e5aac4712`

Finding → Evidence → Root Cause → Impact → Fix → Validation:
- Finding: canonical 50-league identities cannot safely be substituted directly for legacy Oracle internal codes.
- Evidence: live production mapping contains only a subset of identities and includes a D1 collision; bridge preserves all 50.
- Root Cause: source/provider and legacy internal namespaces are distinct.
- Impact: downstream 50-league scope expansion remains blocked until exact fixture identity and one-to-one mapping are proven.
- Fix: research-only bridge with explicit fail-closed statuses.
- Validation: 50 rows re-read from live branch; all governed identities represented exactly once; production `ACTIVE` list unchanged.

The live 50-league fixture-source validation gate remains NOT PASSED because the scheduled validator artifact has not yet been produced. Do not expand the private 27-league prediction allow-list before that evidence exists.



## Governance control — immediate operator blocker escalation — 2026-11-07
Nolan explicitly requires immediate notification whenever a blocker exists or the assistant cannot execute a required workflow; do not wait for another prompt. Every continuation lane must state the exact blocker and operator action as soon as it is known, distinguish assistant-executed actions from operator-required actions, and never claim a workflow is running without live run evidence. When a workflow is already running, inspect its live status/jobs/logs/artifacts and report actionable findings without asking for unnecessary reruns.
- Checkpoint: `docs/checkpoints/2026-11-07-operator-escalation-and-immediate-blocker-reporting.md`
- Checkpoint commit: `b8bcf660f8973b80422f68b4daa406ee21984057`
- Validation: workflow run `42361333640` independently inspected; at inspection it was in progress with source validation step running and reconciliation/persistence pending. Oracle V1.6 untouched.


## Major milestone — first genuine 50-league live source validation completed, persistence race remains — 2026-11-07
Run 42361333640 completed the live 50-league OpenFoot validation and exact reconciliation: 50 governed leagues, 26 READY, 24 DATA_GATED, 0 SOURCE_ERROR, 299 fixtures in window; reconciliation PASS with zero missing, unexpected or duplicate league IDs. The run then failed only when persisting the two sanitized artifacts because the governed research branch had advanced concurrently and rejected the direct push.

Finding → Evidence → Root Cause → Impact → Fix → Validation:
- Finding: live source validation itself and board reconciliation pass; canonical evidence persistence failed.
- Evidence: workflow logs show validator COMPLETE and reconciliation PASS; both artifact files were created locally before the push rejection.
- Root Cause: moving research branch was concurrently updated by Oracle control-plane automation; old workflow used a direct push without fetch/rebase.
- Impact: source-validation gate remains fail-closed because canonical artifacts are not yet persisted/re-read from GitHub.
- Fix: hardened workflow persistence in commit b5987ca1194469e65e61296157cf1f2b75acaf89 with fetch/rebase and three bounded push retries, never force-pushing.
- Validation: workflow definition committed on main; checkpoint docs/checkpoints/2026-11-07-50-league-live-source-validation-persistence-race.md commit 6b23180a5edcc7c6b6ad21754caa2da7df8925cd. A new execution using the hardened workflow is required; the failed run must not be rerun as-is.

Immediate operator blocker: the current GitHub toolset does not expose workflow dispatch. If immediate execution is required before the next scheduled run, Nolan must manually use Actions → Oracle 50-League Live Fixture Source Validation → Run workflow → main. The next scheduled execution is at minute 07 of the next hour. This limitation must be surfaced immediately rather than waiting for another prompt.


## Major milestone — 50-league live source gate PASSED — 2026-11-07
Workflow run `42361725224` completed successfully using hardened workflow commit `b5987ca1194469e65e61296157cf1f2b75acaf89`.

Finding → Evidence → Root Cause → Impact → Fix → Validation:
- Finding: canonical live 50-league source validation and exact board reconciliation now have persisted evidence.
- Evidence: validator artifact and reconciliation artifact are both readable from `research/oracle-50-league-readiness-audit`; 50 registry rows = 50 validation rows; missing IDs 0; unexpected IDs 0; duplicate IDs 0; classification 26 READY / 24 DATA_GATED; 299 fixtures in governed window; 0 SOURCE_ERROR.
- Root Cause of prior failure: branch race during direct evidence push. Hardened persistence fixed it through fetch/rebase and bounded retry.
- Impact: the live 50-league fixture-source gate is now PASSED. This does NOT by itself make the 50-league universe production-eligible, because downstream internal identity mapping, feature evidence, settlement evidence, freshness and sample gates remain open.
- Fix: hardened workflow is now validated in a successful production-like execution.
- Validation: run `42361725224` status SUCCESS; both artifacts re-read successfully from the governed research branch; `production_model_changed=false`, `production_eligible=false`, `betting_eligible=false`.

Next highest-value blocker: exact one-to-one mapping from the canonical 50-league source namespace into the Oracle internal league-code namespace, followed by downstream 50-league fixture/prediction scope validation. Do not change the production `ACTIVE` allow-list until mapping and fixture identity gates are proven.


## Identity bridge refinement — config-backed exact mappings — 2026-11-07
Research-only bridge was refined using the live production repository config/data_config.json, without changing production code or model logic.
- Belgium Pro League -> B1: exact unique mapping from config season_leagues.
- Germany Bundesliga -> D1: exact unique mapping from config season_leagues; the prior false collision was caused by a stale/incorrect assumption that Denmark Superliga also owned D1. Denmark Superliga has no unique internal code in the current production config and remains UNMAPPED/fail-closed.
- Germany 2. Bundesliga -> D2: exact unique mapping from config season_leagues.
- Greece Super League -> G1: exact unique mapping from config season_leagues. This resolves internal namespace identity only; current live source-season readiness remains governed by the separate 50-league source validation artifact.
Bridge commit: dac3eaddea19988f75bbc04972d5cd776b4cc3bc.
Next: continue evidence-based mapping for remaining governed leagues from explicit production configuration/source mappings or leave them fail-closed; do not infer codes from name similarity. Production ACTIVE scope remains unchanged.


## Major milestone — OMI live-source evidence consumed — 2026-11-07 12:01 SAST
The OMI lane consumed the canonically persisted 50-league live fixture-source validation and reconciliation artifacts without rerunning acquisition, repair or provider recovery.

Finding → Evidence → Root Cause → Impact → Fix → Validation:
- Finding: the live 50-league source gate is now closed, but downstream OMI production scope remains gated by internal identity mapping and evidence-chain controls.
- Evidence: 50/50 registry rows reconciled to 50/50 validation rows; zero missing/unexpected/duplicate IDs; 26 leagues READY with 299 verified fixtures in the 2026-11-07 to 2026-11-21 window; 24 leagues DATA_GATED. The research identity bridge contains 19 exact unique mappings, 4 cross-namespace name variants, 1 unverified name variant and 26 unmapped identities.
- Root Cause: source/provider namespace and Oracle internal namespace remain only partially reconciled; feature snapshot, production probability, xG/odds provenance and verified settlement gates are separate controls.
- Impact: OMI may use the live source artifact as freshness/source evidence, but must not admit the 299 fixtures as a production Oracle V1.6 universe or expand the production ACTIVE allow-list.
- Fix: updated reports/oracle-omi-release-gate-register-2026-11-07.md to consume the new source gate and explicitly classify live identity/freshness status without promoting evidence.
- Validation: report was re-read from live GitHub after commit; source reconciliation artifact remains PASS; production_model_changed=false, production_eligible=false, betting_eligible=false.

Current OMI release posture:
- Historical Selected-50 OMI baseline #360 remains unchanged and is not rerun.
- Live 50-league source validation: PASS.
- Internal identity bridge: 19/50 exact, 31/50 fail-closed/non-exact.
- Production probability bridge: BLOCKED.
- Immutable feature snapshot: BLOCKED until a genuinely new eligible prediction produces non-empty snapshot artifacts.
- Point-in-time xG: BLOCKED.
- Timestamped odds: BLOCKED.
- Verified settlement/prediction-to-feature-to-settlement chain: BLOCKED.
- Per-market production sample/freshness/confidence: not yet admissible.
- 80 HTTP-417 tasks remain quarantined and excluded.

Highest-value next OMI action: consume the next validated downstream fixture/prediction evidence only after exact identity/scope reconciliation, then join exact fixture ID + market key + model-engine revision + feature snapshot into the existing readiness matrix. Do not infer mappings or production probabilities.


## Major blocker — internal league-code namespace conflict discovered — 2026-11-07
N1 is not a deterministic internal league identity across the live production repository. build_27_league_dna_lab.py assigns N1 to Norway Eliteserien, while restore_historical_match_spine.py and ingest_upcoming_fixtures.py assign N1 to Netherlands Eredivisie; readiness artifacts also conflict in their labeling. The research bridge has quarantined Netherlands Eredivisie -> N1 as CODE_NAMESPACE_CONFLICT/fail-closed in commit e0c7bdcc0eb8951d8b1b5bffe2a392ae42496797. Checkpoint: docs/checkpoints/2026-11-07-internal-namespace-conflict-n1.md, commit 99125d6ba0c2da7812d06e6cdfb0f8a0d1c4fd02. This is research-only; Oracle V1.6 and production ACTIVE scope remain unchanged. Next action: audit all internal codes for cross-file namespace conflicts before any 50-league expansion.


## Control-plane update — 2026-11-07 12:20 SAST

### Finding
Live HEAD has advanced to `209fa8c03faff8e2da09447a5a9b4ba798415d02` (`Add config-backed Serbia internal identity`). The latest branch already contains the effective Market Intelligence archive-consent repair from `f084491b95be1df95d0d59b8d2d08d16ab6dbfbc`; the repair commit itself is not an ancestor, but its workflow content is present at live HEAD. No duplicate merge/cherry-pick is required.

### Evidence
- Selected-50 contract run `42362869527`: SUCCESS on exact HEAD.
- Selected-50 dry-run planner run `42362869495`: SUCCESS on exact HEAD.
- The 50-row internal identity bridge now has 20 `EVIDENCE_EXACT_UNIQUE` mappings after the Serbia repair.
- Remaining bridge states are 26 `UNMAPPED`, 1 `NAME_VARIANT_UNVERIFIED`, 2 `CROSS-NAMESPACE_NAME_VARIANT`, and 1 `CODE_NAMESPACE_CONFLICT`; all remain fail-closed.
- Live 50-league source validation remains passed from prior evidence: 50/50 registry reconciliation, 26 READY, 24 DATA_GATED, 0 SOURCE_ERROR.
- No new provider/API acquisition was performed in this control run.
- The 80 HTTP-417 tasks remain quarantined after the confirmed account entitlement/selected-league access gap.
- Prospective evidence remains challenger/shadow only; immutable feature snapshot materialization, point-in-time xG, timestamped odds and verified settlement linkage remain open gates.

### Root Cause
The remaining blockers are evidence-chain and namespace-reconciliation controls, not Oracle V1.6 model logic. The production engine still has a legacy 27-league namespace and cannot safely consume the 50-league source namespace without exact evidence-backed mapping.

### Impact
Production and betting eligibility remain fail-closed. No production prediction scope expansion, probability change, calibration change or threshold change is justified.

### Fix
Integration/build-control performed no model or provider changes. The safe control action was to reconcile live branch content, validate the exact HEAD with the existing contract/planner runs, and preserve unresolved identities as explicit fail-closed states.

### Validation
Exact HEAD contract and dry-run workflows both passed. The current workflow configuration contains the repaired boolean archive-consent control and remains guarded against unapproved provider-result calls.

### Remaining blockers
1. 30/50 internal identity mappings remain non-admissible.
2. Downstream 50-league prediction scope is still blocked behind exact identity/scope evidence.
3. Immutable prediction-to-feature-snapshot capture is still incomplete.
4. Point-in-time xG provenance is blocked.
5. Timestamped odds provenance is blocked.6. Verified settlement provenance/immutable prediction-to-settlement chain is incomplete.
7. No Oracle V1.6 production prediction cohort is available for production scoreability.
8. 80 provider tasks remain quarantined pending account-side entitlement correction; do not repeat the exhausted transport experiment.

### Single highest-value next action
On the next genuinely new governed prospective fixture cohort, verify non-empty immutable feature snapshots, exact prediction-to-snapshot linkage, prediction-engine code attribution, pre-kickoff chronology and corrected settlement provenance. Continue evidence-backed identity reconciliation in parallel; do not assign any unproven internal codes.



## Control-plane update — 2026-11-07 12:38 SAST

### Finding
A live evidence-control audit after the Serbia identity repair found no additional identity mapping that could be promoted safely from the currently admissible evidence. The exact source gate remains passed; downstream production scope remains fail-closed.

### Evidence
- Live HEAD inspected: `209fa8c03faff8e2da09447a5a9b4ba798415d02`.
- 50-row internal identity bridge re-read from live GitHub: 20 `EVIDENCE_EXACT_UNIQUE`; 26 `UNMAPPED`; 1 `NAME_VARIANT_UNVERIFIED`; 2 `CROSS-NAMESPACE_NAME_VARIANT`; 1 `CODE_NAMESPACE_CONFLICT`.
- Live source validation remains 50/50 reconciled, 26 READY, 24 DATA_GATED, 0 SOURCE_ERROR, 299 governed-window fixtures.
- The 80 HTTP-417 tasks remain quarantined; no provider/API acquisition or recovery was attempted.
- Prospective evidence remains challenger/shadow; immutable feature snapshot, verified settlement, xG/odds provenance and production scoreability remain open.

### Root Cause
Additional mappings cannot be inferred from league-name similarity because the production namespace has demonstrated cross-file code conflicts (including N1). Only explicit authoritative configuration or a verified bridge can close a mapping.

### Impact
No safe production universe expansion or probability bridge is justified. Production and betting eligibility remain fail-closed.

### Fix
No model, production, provider or workflow change was made. Existing evidence was audited and unresolved identities were preserved as explicit fail-closed states. A non-essential GitHub search for further mapping evidence encountered HTTP 429 rate limiting; no retry was made.

### Validation
Checkpoint: `docs/checkpoints/2026-11-07-evidence-validation-control-1238.md`.
Checkpoint commit: `04de4fc25ca914646adb2c405e2731e887172cc2`.
Current bridge and HEAD were re-read directly from GitHub after the audit. No workflow was launched and no provider/API calls were consumed.

### Remaining blockers
1. 30/50 internal identity mappings remain non-admissible.
2. Immutable prediction-to-feature-snapshot capture/linkage remains incomplete.
3. Verified settlement provenance/linkage remains incomplete.
4. Point-in-time xG provenance remains blocked.
5. Timestamped odds provenance remains blocked.
6. No Oracle V1.6 production prediction cohort is scoreable.
7. 80 provider tasks remain quarantined by confirmed account entitlement gap.

### Single highest-value next action
On the next genuinely new governed prospective fixture cohort, verify non-empty immutable feature snapshots, exact prediction-to-snapshot linkage, actual model-engine revision, pre-kickoff chronology and corrected settlement provenance; continue identity reconciliation only from explicit authoritative evidence.


## Control-plane update — 2026-11-07 12:57 SAST — OMI identity-bridge count reconciliation

### Finding
The OMI release-gate register and the continuation state had stale internal identity-bridge counts after the Serbia exact mapping repair. The live research bridge was re-read and independently reconciled before correction.

### Evidence
- Live bridge contains 50/50 governed identities exactly once.
- Current mapping states: 20 EVIDENCE_EXACT_UNIQUE; 24 UNMAPPED; 4 CROSS-NAMESPACE_NAME_VARIANT; 1 NAME_VARIANT_UNVERIFIED; 1 CODE_NAMESPACE_CONFLICT.
- Live 50-league source reconciliation remains PASS: 50/50 validation rows, zero missing/unexpected/duplicate IDs, 26 READY, 24 DATA_GATED, 299 fixtures in the governed window.
- Corrected OMI report commit: 1543e95d0d8c29a73d7c858cf20cdb2778a86145.
- Dated checkpoint: docs/checkpoints/2026-11-07-omi-identity-bridge-count-reconciliation-1257.md.
- No provider/API acquisition, recovery, prediction-engine or Oracle V1.6 model change was performed.

### Root Cause
The report had retained the pre-Serbia-repair count of 19 exact / 26 unmapped while the live bridge had already advanced to 20 exact / 24 unmapped. The remaining unresolved mappings are still explicitly fail-closed.

### Impact
OMI release reporting now reflects the live evidence accurately. Production and betting eligibility remain false; no production scope expansion or probability reconstruction is justified.

### Fix
Updated the OMI release-gate register to 20 exact / 24 unmapped and documented the reconciliation in the dated checkpoint. No mapping was inferred or promoted.

### Validation
The corrected report and checkpoint were re-read from the live governed branch after their commits. The bridge counts were independently derived from the live 50-row bridge. Source reconciliation remains PASS. Oracle V1.6 production logic, probabilities, thresholds, calibration and governance remain unchanged.

### Remaining blockers
1. 30/50 internal identity mappings remain non-admissible.
2. Downstream 50-league production scope remains blocked.
3. Immutable prediction-to-feature snapshot capture remains incomplete.
4. Production probability bridge remains blocked.
5. Point-in-time xG and timestamped odds provenance remain blocked.
6. Verified settlement/prediction-to-feature-to-settlement linkage remains incomplete.
7. Current-feed candidate freshness and per-market sample gates remain open.
8. 80 HTTP-417 provider tasks remain quarantined pending account-side entitlement correction; exhausted transport experiments must not be repeated.

### Single highest-value next action
Consume the next genuinely new governed prospective fixture/prediction evidence and reconcile it by exact fixture ID + market key + model-engine revision + immutable feature snapshot; do not infer missing identity mappings or production probabilities.


## 2026-11-07 — Leagues Revision v4 team identity evidence
- User-provided source workbook: `Leagues Revision v4.0(1).xlsx`.
- Parsed and persisted research lookup: `data/prospective/oracle_leagues_revision_v4_team_league_lookup.csv` (872 team records; 45 distinct competition tables).
- Reconciled against live 50-league fixture crosswalk: `data/prospective/oracle_50_league_team_pair_workbook_reconciliation.csv`.
- 299 live fixtures classified: 185 existing Oracle internal identity; 29 workbook team-pair confirmed; 37 one-team workbook match; 46 no workbook team match; 2 workbook teams found in different competitions.
- This workbook is now a retained identity evidence source and must be referenced before repeating team→league discovery work.
- Research-only: do not promote workbook matches directly into production internal namespaces; production admission remains fail-closed until governed identity/provenance gates are satisfied.


## 2026-11-07 — Continuous Build Control: 50-league integration admission handoff

### Finding
The source-validation gate is closed, but downstream integration still lacked one canonical control artifact combining source readiness, internal identity status, live fixture count and retained workbook identity evidence. Creating this control prevents the validation and evidence/OMI lanes from operating on different league-admission interpretations.

### Evidence
- Live source reconciliation: 50/50 governed leagues, 26 READY, 24 DATA_GATED, 299 fixtures, production_eligible=false, betting_eligible=false.
- Live internal identity bridge: 20 EVIDENCE_EXACT_UNIQUE; 24 UNMAPPED; 4 CROSS-NAMESPACE_NAME_VARIANT; 1 NAME_VARIANT_UNVERIFIED; 1 CODE_NAMESPACE_CONFLICT.
- Retained Leagues Revision v4 evidence: 872 team records across 45 competition tables; 299 live fixtures reconciled into 185 existing internal identities, 29 workbook team-pair confirmations, 37 one-team matches, 46 no workbook matches and 2 workbook competition conflicts.
- New research/control artifact: data/prospective/oracle_50_league_integration_admission_matrix.csv.
- New dated checkpoint: docs/checkpoints/2026-11-07-50-league-integration-admission-control.md.

### Root Cause
The source namespace and internal Oracle namespace are separate evidence layers. Previous downstream work had the necessary components, but no single controlled handoff matrix prevented inconsistent admission decisions. Cross-file namespace conflicts such as N1 make implicit promotion unsafe.

### Impact
The 50-league universe can now be handed from source validation to downstream evidence/OMI using explicit states without changing Oracle V1.6 or silently dropping governed leagues. Production admission remains fail-closed.

### Fix
Added the research-only 50-league integration admission matrix and documented the controlled admission sequence: source identity → internal namespace → fixture/team identity → immutable pre-kickoff feature snapshot → engine revision → xG/odds provenance → settlement linkage → sample/freshness gates → OMI release evidence. No production code, probabilities, thresholds, calibration or betting governance changed.

### Validation
Both new artifacts were created on the governed research branch. The matrix was generated from the live 50-league bridge, live fixture/source reconciliation and retained workbook reconciliation. Exact internal codes are only carried where the bridge already marks them evidence-backed; unresolved/conflicted mappings remain FALSE for production admission.

### Remaining blockers
1. 30/50 internal identity mappings remain non-admissible.
2. Downstream prediction scope remains blocked for unresolved/conflicted identities.
3. Immutable prediction-to-feature snapshot evidence remains incomplete until a fresh eligible cohort produces non-empty snapshot artifacts.
4. Point-in-time xG provenance remains blocked.
5. Timestamped odds provenance remains blocked.
6. Verified settlement/prediction-to-feature-to-settlement linkage remains incomplete for a fresh cohort.
7. Prospective sample/freshness gates remain open.
8. 80 HTTP-417 tasks remain quarantined by confirmed provider entitlement gap.

### Single highest-value next action
Hand the new admission matrix to the evidence/OMI lane and, on the next genuinely new eligible prospective cohort, verify non-empty immutable feature snapshots plus exact fixture/market/model-engine linkage and settlement provenance. Do not expand production scope from the matrix alone.


## Major milestone — 50-league identity admission candidate board — 2026-11-07
- Live 50-league source gate remains PASS: 50/50 reconciled, 299 live fixtures, 26 READY / 24 DATA_GATED.
- Built `data/prospective/oracle_50_league_identity_admission_matrix.csv`: 19 PRODUCTION_READY_IDENTITY; 7 IDENTITY_CONFIRMED_NO_INTERNAL_CODE; 5 CONFLICT; 19 UNRESOLVED.
- Built `data/prospective/oracle_50_league_fixture_admission_candidates.csv`: 299 fixtures represented exactly once; 158 CANDIDATE_FIXTURE_ADMISSION; 66 awaiting internal namespace; 62 unresolved; 13 conflicted.
- Workbook `Leagues Revision v4.0(1).xlsx` remains retained identity evidence and must be referenced before repeating team-to-league discovery.
- This is research/admission evidence only. Oracle V1.6 production logic, ACTIVE scope, probabilities, thresholds, calibration and betting governance remain unchanged. Production admission remains FAIL-CLOSED.
- Checkpoint: `docs/checkpoints/2026-11-07-50-league-identity-admission-candidate-milestone.md`.
- Next controlled action: use only the 158 candidate fixtures to validate immutable pre-kickoff feature snapshots and exact prediction-engine revision linkage; do not broaden production scope until evidence gates pass.


## Major milestone — exact fixture/private feed bridge — 2026-11-07
- Research-only artifact `data/prospective/oracle_50_league_fixture_private_feed_bridge.csv` created.
- 115 of 158 candidate production-identity fixtures have an exact home+away+date bridge into the private `data/fixtures/oracle_upcoming_fixtures.csv` feed.
- 115/115 private internal league codes match the proven internal Oracle namespace; 0 ambiguous matches.
- This does not expand production ACTIVE scope or change Oracle V1.6 logic/governance.
- Checkpoint: `docs/checkpoints/2026-11-07-exact-fixture-private-feed-bridge.md`.
- Next controlled action: establish genuine pre-kickoff feature-state availability and immutable snapshot capture for this 115-fixture evidence cohort. Do not synthesize snapshots from historical aggregates.


## Major milestone — 115-fixture pre-match state readiness — 2026-11-07
- Exact private-feed bridge: 115 fixtures.
- Existing engine status: 80 CONTROLLED, 10 WATCH, 25 NO_BET.
- Engine-accepted pre-match state: 90/115; 25/115 fail-closed for missing/rejected state.
- Raw four-market values: 450 across the 90 state-ready fixtures.
- Research artifact: `data/prospective/oracle_50_league_pre_match_state_readiness.csv`.
- No synthetic feature snapshots created; feature snapshot status remains NOT_YET_MATERIALIZED.
- Checkpoint: `docs/checkpoints/2026-11-07-115-fixture-pre-match-state-readiness.md`.
- Next critical action: on a genuinely future-kickoff cycle, persist the actual accepted pre-match inputs into immutable FEATURE_SNAPSHOT_MANIFEST/VALUES evidence with source hashes and engine commit attribution.


## Major milestone — pre-match state compatibility control — 2026-11-07
- Identified and repaired a concrete schema/path gap: current staging produced `database/current_prematch_team_state.csv`, while the governed prediction engine and prospective snapshot publisher require `database/prematch_team_state.csv`.
- Added production-repo data-only adapter `scripts/build_prediction_team_state_compatibility.py` (commit `4eb000e5f0a652cab5f1a469387081d319e9105e`). It preserves existing feature values and only maps the existing state spine into the engine's expected schema.
- Current-data workflow now persists the compatibility view (commit `fdd448526b379952dcb6f43844ad2eb1dfdc8048`).
- Prospective learning workflow now refreshes the pre-match state spine and compatibility view before prediction (commit `8a744c2e24a335f84aebbd2dee1e697abd5bc4cf`).
- Checkpoint: `docs/checkpoints/2026-11-07-pre-match-state-compatibility-control.md`.
- Live workflow execution has NOT been claimed as passed; the available GitHub control interface cannot dispatch workflows. Next scheduled/manual cycle must be inspected for non-empty immutable snapshot artifacts and exact engine attribution.
- Oracle V1.6 logic, ACTIVE scope, probabilities, calibration, thresholds and betting governance remain unchanged; production remains FAIL-CLOSED.

## Control-plane update — 2026-11-07 13:43 SAST — prospective snapshot gate re-audit

### Finding
The latest private prospective-workflow hardening is present, but no completed governed cycle has yet produced admissible immutable feature-snapshot artifacts. The feature-snapshot gate therefore remains OPEN and no duplicate workflow was launched.

### Evidence
- Public governed branch live HEAD at start of this control run: `dd66dfae62affbbfdda49d2c1abba13014e3084f`.
- New research checkpoint: `docs/checkpoints/2026-11-07-evidence-validation-control-1343.md`, commit `8196177d353c093a5c4244a54e7b69e1482b80a1`.
- Private prospective workflow hardening: `8a744c2e24a335f84aebbd2dee1e697abd5bc4cf`.
- Private current-data HEAD: `54844dc3598584c106bf16be0c8fec010917a141`; pre-match state is persisted with 13,108 rows and current source/feed state is refreshed.
- Private `FEATURE_SNAPSHOT_MANIFEST.csv` remains header-only and `FEATURE_SNAPSHOT_VALUES.csv` is absent.
- Commit status for `8a744c2e...` is pending with no completed status records; no completed prospective evidence can be attributed to that revision.
- No provider/API acquisition or recovery call was made; 80 HTTP-417 tasks remain quarantined.

### Root Cause
The schema/path compatibility defect has been repaired in code, but code presence is not evidence closure. A genuinely executed governed prospective cycle must materialize the actual accepted pre-match inputs and bind them to prediction rows.

### Impact
Production prediction scoreability, production calibration/accuracy metrics, market/league/risk-band evidence and final readiness remain fail-closed. Existing challenger/shadow evidence remains research-only.

### Fix
No production model, probability, threshold, calibration, governance or provider data was changed. Existing artifacts were re-read and the absence of admissible snapshots was recorded without fabrication.

### Validation
- Live public HEAD inspected before writing.
- Continuation state, lessons and latest dated checkpoints read.
- Private workflow revision and current main state inspected.
- Snapshot manifest/value artifacts inspected directly.
- No duplicate workflow launched.
- No provider/API calls made.

### Remaining blockers
1. Immutable feature snapshot manifest/values remain non-admissible.
2. Exact prediction-to-feature linkage remains unproven for a fresh cohort.
3. Verified settlement provenance/linkage remains incomplete for a fresh cohort.
4. Production probability bridge and production scoreability remain blocked.
5. Point-in-time xG and timestamped odds remain blocked.
6. 30/50 internal identity mappings remain fail-closed.
7. 80 provider tasks remain quarantined by confirmed account entitlement gap.

### Single highest-value next action
Inspect the first genuinely completed prospective cycle after `8a744c2...`; if completed, validate non-empty snapshot manifest/values, exact prediction linkage, actual engine revision, pre-kickoff chronology and corrected settlement provenance. If no such cycle exists, manual dispatch of the already-corrected prospective cycle is the only gated action; no new provider acquisition is justified.


## Major milestone — OMI prospective pre-match readiness consumption — 2026-11-07 14:00 SAST

### Finding
OMI consumed the latest validated 115-fixture pre-match state readiness cohort without duplicating upstream acquisition, settlement or backtest work. The cohort is useful for readiness reporting but does not constitute immutable feature-snapshot evidence.

### Evidence
- Exact private-feed bridge: 115 fixtures.
- Engine status: 80 CONTROLLED, 10 WATCH, 25 NO_BET.
- Engine-accepted pre-match state: 90/115; 25/115 rejected/missing state.
- Four-market raw values: 450 across the 90 state-ready fixtures.
- Feature snapshot status: 115/115 NOT_YET_MATERIALIZED.
- No synthetic feature snapshots were created.
- Current cohort extends to 2026-11-21 and is therefore a readiness cohort, not a settled-performance cohort.
- OMI report updated: `reports/oracle-omi-market-readiness-2026-11-07.md`.
- Checkpoint: `docs/checkpoints/2026-11-07-omi-prospective-pre-match-readiness-1400.md`.

### Root Cause
The prospective workflow compatibility repair exists, but no completed governed cycle has yet produced admissible FEATURE_SNAPSHOT_MANIFEST/VALUES artifacts bound to prediction rows.

### Impact
The 90 accepted fixtures cannot be promoted to Oracle V1.6 production evidence. Raw challenger/research market values remain non-production. The 25 rejected fixtures remain fail-closed.

### Fix
OMI integrated the validated readiness cohort into the release report only. No production logic, probability, threshold, calibration, governance, provider data or quarantined evidence was changed.

### Validation
- Live OMI report was read before modification.
- Updated OMI report was re-read from the governed branch.
- New dated checkpoint was created on the governed branch.
- No provider/API calls or duplicate workflows were launched.

### Remaining blockers
1. Immutable feature snapshot manifest/values.
2. Exact prediction-to-feature linkage.
3. Separate model-engine revision attribution.
4. Point-in-time xG provenance.
5. Timestamped odds provenance.
6. Verified settlement provenance/linkage.
7. 30/50 non-admissible internal identity mappings.
8. Prospective freshness/sample gates.

### Single highest-value next action
Inspect the first completed governed prospective cycle after `8a744c2...`. If immutable snapshots exist, join them to OMI by exact fixture ID + market key + model-engine revision. If not, no additional OMI reconstruction is justified; the gated prospective execution is the only meaningful next step.

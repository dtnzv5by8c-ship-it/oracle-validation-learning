# PROJECT ORACLE — CANONICAL CONTINUATION STATE

Last updated: 2026-11-07 — settlement provenance control corrected; prospective evidence remains fail-closed
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
- Current private prediction archive contains 885 CHALLENGER rows across 177 fixtures; 25 rows across 5 fixtures now have SETTLED status, but remain research/shadow because settlement provenance is incomplete.
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
A direct audit of the current private `oracle-football-data/main` canonical archive found that `archive/PREDICTION_LEDGER.csv` is **not header-only**.

Current evidence:
- 555 prediction rows
- 555 unique prediction IDs
- 111 unique fixtures
- 5 model/market rows per fixture
- fixture dates 2026-10-09 through 2026-11-15
- 555/555 model status = CHALLENGER
- 320 CHALLENGER_OUTPUT + 235 NO_BET
- 555/555 prediction timestamps present
- 555/555 feature snapshot IDs present
- 555/555 source manifest hashes present
- 555/555 pre-match state hashes present
- 555/555 model code SHAs present
- 555/555 calibration IDs present
- 555/555 chronology checks pass: prediction timestamp < kickoff
- 555 unique feature snapshots
- 2 source manifest hashes
- canonical `archive/SETTLEMENT_LEDGER.csv` remains header-only

This corrects older validation snapshots that described the current prediction ledger as header-only or 210 rows. Those were earlier-state observations and must not be repeated as the current state.

The 555 rows are **CHALLENGER-only** and therefore do not establish Oracle V1.6 production performance. The current highest-value evidence blocker is now verified settlement provenance and production scoreability, not absence of prospective prediction capture.

The private repository already contains the governed prospective chain:
`prepare_prospective_four_market_publication.py` -> `publish_prediction_run.py` -> `build_prospective_settlement_truth.py` -> `settle_prediction_run.py` -> `feed_learning_ledgers.py`, orchestrated by `.github/workflows/oracle_prospective_learning.yml`.

Checkpoint:
`docs/checkpoints/2026-11-07-current-private-prediction-archive-audit.md`
Commit: `ed1aed7daf31773dbca72db18d6d3a1c12b2d142`.

Next evidence work: determine why 555 prospective prediction rows have not produced canonical settlement rows, using current workflow/result evidence and exact prediction IDs. Do not modify Oracle V1.6 or promote challenger evidence.

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

## Current prospective evidence after run 428
- Private prediction archive: 885 CHALLENGER rows.
- Canonical settlement ledger: 25 settled rows across 5 fixtures.
- Prospective shadow gate: COLLECTING; 5 settled observations per governed model, below the 100-row / 8-day minimum.
- Production readiness: HOLD_PROSPECTIVE_AND_RESEARCH_EVIDENCE.
- No automatic promotion; production models remain on the existing governed benchmark.

## Remaining release blockers
1. 80 HTTP-417 tasks remain quarantined across 20 provider-season partitions because the FootyStats account diagnostic confirmed an entitlement/league-selection gap. Do not repeat the exhausted transport experiment until entitlement changes.
2. Historical 2026-10-09 through 2026-10-17 prediction fixtures still require independently verified result truth; do not infer them from current/future snapshots.
3. xG numeric values exist but point-in-time capture timestamps are not verified.
4. Timestamped odds provenance is not verified.
5. Immutable prediction → fixture → pre-kickoff feature snapshot → verified settlement linkage must be demonstrated for production-admissible evidence.
6. Per-market prospective sample and observation-window gates remain open.
7. OMI/Visual Intelligence production readiness remains blocked until the canonical probability bridge, point-in-time features, verified settlement and current-feed freshness gates are satisfied.

## Resource-control rule
Private `oracle-football-data` Actions are scarce (3,000 minutes/month). Use the public `oracle-validation-learning` repository for research, validation, reconciliation, reporting and non-sensitive computation whenever private credentials/provider access are not required. Do not launch duplicate private workflows.

## Definition of done
Production prediction readiness requires genuinely satisfied identity, chronology, point-in-time feature provenance, prediction/settlement linkage and required market/league gates. Missing/quarantined evidence remains excluded. Fail-closed remains active until gates pass.

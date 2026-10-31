# Project Oracle — Master Operating Runbook & Recovery Pack
**Reviewed:** 31 October 2026 (SAST)  
**Scope:** Selected-50 research lane; Oracle production logic remains protected.  
**Canonical branch:** `research/oracle-50-league-readiness-audit`  
**Recovery branches:** initial baseline `backup/oracle-50-readiness-2026-10-30-98af1f7`; latest validated `backup/oracle-50-qa58-final-2026-10-30`

## 1. Operating objective
Make Project Oracle repeatable: preserve the existing model and archive, refresh the fixture feed, run the governed research runtime, produce the safe fixture report, validate evidence and export the report. Do not restart prior work, rebuild the model, or relax release gates to obtain a prediction.

## 2. Protected governance
- Production benchmark remains Oracle V1.6; V1.6.3 remains the master development benchmark.
- No new model, redesign, production model logic changes, probability/calibration/threshold changes, or production writes are authorised by this runbook.
- Selected-50 work stays isolated on the research branch until every identity, chronology, settlement, feature, market-validation and release gate is satisfied.
- No fabricated IDs, fixtures, probabilities, xG, odds, outcomes, joins or missing-value imputations.
- Never expose API keys, connector tokens or private raw provider payloads in the public repository.
- Research outputs must be labelled research-only; production_eligible and betting_eligible remain false until approved.

## 3. Durable assets and recovery points

### Public research repository
- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Active branch: `research/oracle-50-league-readiness-audit`
- Initial recovery branch: `backup/oracle-50-readiness-2026-10-30-98af1f7` (pre-improvement baseline).
- QA #58 recovery branch: `backup/oracle-50-qa58-2026-10-30` (snapshot before final watchlist documentation).
- Latest final recovery branch: `backup/oracle-50-qa58-v4-2026-10-30` (full research branch snapshot including the exact calendar-year audit, league-level quality watchlist, workbook references and Recovery Pack v4; commit `055133ef322a5b7aec3f28c362a3da7246fe94da`).
- Recovery Pack v4 and the human-readable 2024–2027 coverage workbook are saved in the persistent ChatGPT Library folder `/Project Oracle/2026-10-30 Recovery Pack/`.
- Workbook: `Oracle_Selected50_2024-2027_Coverage_and_Feature_Audit_30Oct2026.xlsx`; five tabs: Executive Summary, League-Year Coverage (200 rows), Season-Year Coverage (800 rows), Quality Watchlist, Definitions & Controls.
- Recovery Pack v4 SHA-256: `02ac0e814edd481c20c853e88fbe47ee680df24b718087cd84bbfd0edd371c87`.
- Backup commit: `98af1f79d3e79b4d9b7e177d21eb778233cf3bcd`
- Current follow-up commit after archive pin correction: `0d4135bdbde6558ce9237e6cce8f5f6510f5970b`
- Open research PR: [#31 — Research-only: FootyStats-first dynamic identity resolver for selected 50](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/31). It is a draft; do not merge to production without governance approval.

### Private historical archive
- Repository: `dtnzv5by8c-ship-it/oracle-football-data`
- Release: [research-selected50-footystats-history-40375285207](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/releases/tag/research-selected50-footystats-history-40375285207)
- Verified archive package SHA-256 recorded in the 30 Oct ingestion reconciliation: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- Ingestion ledger: 200 season folders (4 per selected group), 50/50 selected season IDs exact, 0 failed seasons, 59,049 match rows, 3,366 team-season roster memberships.
- This proves archive structure/ingestion counts, not canonical fixture/team identity, official settlement truth, point-in-time feature validity or predictive performance.
- The public repository stores sanitized ledgers and QA only. Raw licensed provider data remains in the private archive.

### Probe #6 evidence
- Workflow run: [41106377807](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41106377807)
- Commit: `98af1f79d3e79b4d9b7e177d21eb778233cf3bcd`
- Artifact: `13000514278`, name `footystats-selected50-bounded-endpoint-probe`, SHA-256 `f151803669223eeae53483018199c90b086378e2681a82cc0fcdc14bcaefe578`.
- Result: 201/201 HTTP 200 requests (1 catalogue + 4 endpoints × 50 selected seasons); all 50 selected season IDs found exactly in the live catalogue; all four endpoints succeeded for all 50; match endpoint sampled one match per season only.
- Endpoint schema evidence includes team IDs, fixture date/status, xG/pre-match xG fields and BTTS/Double Chance odds field names in each sampled league response. Field presence is not a completeness, validity, historical-availability or PIT proof.
- Existing crosswalk classifications were preserved: 22 candidate mappings requiring human review; 28 unresolved. Probe #6 did not approve canonical mappings.
- Last observed request_remaining: 1,599. This is not proof of monthly subscription credits.
- Artifact expiry: 6 November 2026. Its results are recorded here; keep the artifact downloaded separately if a long-term copy is needed.

## 4. Current known data position
- Exact 2024–2026 calendar-year coverage is now complete for the pinned 200-season archive: 50/50 groups have provider rows in each of 2024, 2025 and 2026 through 30 Oct 2026; 42,012 rows have kickoff dates on/before the audit date. A further 2,383 rows in 2026 and 4,452 rows in 2027 are future fixtures and are excluded from historical backtests. See `docs/PROJECT_ORACLE_SELECTED50_CALENDAR_YEAR_COVERAGE_2024_2027_2026-10-30.md`.
- The annual complete-status audit flags Belgium Pro League 2026 BTTS and Double Chance odds: 89/233 zero rows (38.20%) in each field, versus zero BTTS zeros in 2024/2025. India 2026 home/away prematch xG zeros are 23/107 (21.50%); Japan 2026 home/away prematch xG zeros are 20/120 (16.67%). Treat Belgium as a P0 odds-market quarantine candidate and India/Japan as P1 xG investigations. See the annual coverage report's league-level watchlist.
- QA #58: run `41115501513`, artifact `13004648723`, SHA-256 `b10eefaca601782e1083374d7f9836926a953f35f039274806149bac83cd9fc0`. It verified 200/200 season folders, 800 league/season-year output rows, zero undated rows and zero unmatched/missing season folders. No provider API calls were made.

- Selected-50 historical archive ledger: 200 seasons / 59,049 match rows; latest Private Archive QA #44 passed checksum and structural checks.
- Primary validation window 2025-03-20 to 2026-09-20 contains 22,291 unique provider match IDs (11,648 in 2025 and 10,643 in 2026); no duplicates detected within the primary window.
- QA #44 flagged 116 past-kickoff rows still marked incomplete, 7,066 parseable score pairs on non-complete rows (all 0-0), and 4,006 complete-status 0-0 rows. Preserve status-based quarantine; official settlement truth remains unverified.
- Prematch xG zero rates are elevated in current-season scopes versus historical scopes (home 13.26% vs 3.54%; away 13.30% vs 3.52%; total 11.91% vs 3.16%); 11 league groups crossed the 30% descriptive screen. Odds fields also show market/league-specific zero anomalies, including Belgium BTTS/DC fields. See the Run #44 QA report; do not recode zeros or assume semantics.
- Current fixture snapshot and safe report artifacts exist from earlier runs, but each new weekly cycle must use a fresh snapshot and a runtime built against the correct archive release.
- The earlier safe report was research-only: 344 clean exact-join rows, 320 raw uncalibrated research probability rows and 24 feature-blocked rows. It must not be presented as a current prediction slate.
- Canonical competition/team/fixture identity, official settlement truth, point-in-time xG/odds provenance and market-specific calibration remain open gates.
- Historical season availability from 2024 onward must be explicitly reconciled per league and season. Preserve the prior primary validation window (2025-03-20 to 2026-09-20) as a comparable benchmark; treat 2024 as an extension unless explicitly governed otherwise.

## 5. Weekly prediction-cycle operating procedure
Use the existing workflows and exact run artifacts; never manually recreate their outputs.

### Step A — Fresh fixture snapshot
Workflow: [Oracle Selected-50 Current Fixture Snapshot](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-current-fixture-snapshot.yml)
1. Select branch `research/oracle-50-league-readiness-audit`.
2. Check the current FootyStats plan tier and monthly credit allowance before dispatch. The snapshot has a 50-request hard cap and requires both provider-credit and monthly-budget confirmations.
3. The current script uses 2.1-second request spacing, performs no retries, stops on the first failed request, records any Retry-After header and marks remaining seasons NOT_ATTEMPTED_AFTER_STOP. The validator fails closed on rate limits, incomplete pagination, missing pagination metadata or partial coverage. A sanitized diagnostic artifact is uploaded even when validation fails.
4. Run once. Record run ID, artifact ID, artifact digest, retrieval time and coverage window. Do not repeat a successful run merely to refresh a screen.
4. Do not repeat a successful run merely to refresh a screen or because another workflow is still running.

### Step B — Research runtime
Workflow: [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)
1. Select the same research branch.
2. Confirm private archive read when prompted.
3. Use archive tag `research-selected50-footystats-history-40375285207`.
4. For a current prediction cycle, enable current snapshot overlay and enter the exact successful snapshot run ID. For historical-only work, leave the overlay disabled.
5. The workflow must verify the private archive checksum and snapshot artifact provenance. A failure is a stop condition; do not bypass it.
6. Record runtime run ID, artifact ID/digest, code SHA and runtime start time.

### Step C — Safe current report
Workflow file: [Oracle Selected-50 Safe Current Fixture Report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-safe-current-report.yml)

**Registration warning:** this workflow file exists on the governed research branch but was not found on the default main branch during the 31 October audit. Do not assume it is available in the Actions workflow picker until it is registered on main. Registering it on main is a separate change and has not been authorised.

1. Enter the successful snapshot run ID and successful runtime run ID.
2. Use the governed 7-day report horizon and 15-minute minimum lead unless a reviewed policy change is committed.
3. Verify both source runs are successful, on the research branch, artifacts unexpired and digests valid.
4. Review the fixture report, feature-blocked list, quarantine reasons, identity/market gates and audit summary.
5. Export and retain the report plus its provenance metadata. Do not call raw uncalibrated values production predictions.

### Step D — Release and evidence checks
- Run existing contract tests, dry-run planner, private archive QA and relevant identity/cross-provider audits when code or archive inputs change.
- Compare the new report to the previous run: fixture count, league coverage, missingness, quarantine, data freshness, feature availability and market-specific eligibility.
- Do not close a blocker without the required evidence and a regression test.
- Never promote to production merely because GitHub Actions is green.

## 6. Current technical configuration correction
Private Archive QA #44 [run 41112970245](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41112970245) completed successfully against the refreshed archive. It produced artifact 13003309729 (SHA-256 `6dc7288826bcd384b469ea9ed53b46c66221f85a4292d2c52f9f5ca3f7be7ea9`) and is documented in `docs/PROJECT_ORACLE_SELECTED50_ARCHIVE_QA_RUN44_2026-10-30.md`. The research runtime and private-archive-QA workflows previously defaulted to stale archive tag `research-selected50-footystats-history-40447419806` and stale pinned SHA. On 30 October, both were corrected on the research branch to default to the verified 200-season archive release `research-selected50-footystats-history-40375285207` and SHA `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`. The xG temporal-shift audit's internal archive SHA guard was also updated to this verified package checksum and covered by a regression test. The safety contract tests and dry-run planner passed on commit `2c489d5c9c0aa0be3f6e0e297b7074d4c2be8f68` (runs `41112970222` and `41112970242`). Private Archive QA run `41112970245` subsequently completed successfully; see artifact 13003309729 above. The workflows must pass their checksum guards before use.

## 7. Provider field semantics now verified
- FootyStats Match Details documentation defines `no_home_away=1` as a fixture with no home/away distinction (neutral/no standard home-away assignment). The snapshot overlay already records this documented semantic and keeps flagged rows quarantined from standard home/away-dependent markets. Do not clear the flag merely because both team IDs are present. The current safe policy remains conservative until a neutral-fixture feature/market contract is tested; BTTS eligibility is not automatically granted by this clarification. Source: [FootyStats Match Details API documentation](https://footystats.org/api/documentations/match-details).
- The same documentation defines match `competition_id` as the league season ID, not the parent competition ID. The separate `comp_master_id` field was returned in the identity probe for 50/50 season IDs, but the public material reviewed does not define its semantics or stability. Preserve it as provider evidence only; do not promote it to Oracle canonical competition ID. See `docs/PROJECT_ORACLE_SELECTED50_COMPMaster_ID_EVIDENCE_2026-10-30.md`.

## 8. What is not yet seamless / gates still open
The following are not yet certified complete:
1. End-to-end weekly snapshot → runtime → safe-report cycle on the latest archive pin.
2. Current Actions secret availability was verified on 31 October for FOOTYSTATS_API_KEY and ORACLE_PRIVATE_REPO_TOKEN without printing values. The FootyStats plan tier, monthly credit balance and actual API-key validity remain unverified.
3. 50/50 canonical competition mappings; current crosswalk has 22 human-review candidates and 28 unresolved.
4. Canonical team and fixture identity joins.
5. Official outcome/settlement truth for each governed market.
6. Historical point-in-time provenance and availability for xG, odds, standings and team features.
7. 2024–2026 per-league/per-season coverage and missingness reconciliation against the private archive.
8. Leakage-safe chronological backtesting, calibration and market-level performance on held-out data.
9. Production parity and human release approval.
10. The Safe Current Fixture Report workflow is not registered on main; default-branch registration is still required if that separate workflow is to be dispatched.
11. Two snapshot-runtime bridge provenance tests remain failing in the latest contract-test run; see the 31 October FootyStats readiness audit.

The 201-call probe validates endpoint access and sampled response schemas. It is not the historical archive ingestion workflow. The legacy `oracle-selected50-footystats-live-ingestion.yml` workflow is intentionally disabled because its old raw-data write path is prohibited. Do not reactivate it. A separate, reviewed, credit-bounded, private-destination ingestion path is required if additional history is missing.

## 9. Stop conditions
Stop and report the exact blocker if:
- archive tag or SHA verification fails;
- private archive token/permission is missing;
- snapshot artifact is stale, expired, incomplete or from the wrong branch;
- any API budget guard fails or monthly credits are uncertain;
- selected league/season/team IDs do not exact-match;
- fixture kickoff, team order or status conflicts are unresolved;
- required feature values are absent or lack pre-kickoff provenance;
- settlement specification or market semantics are ambiguous;
- any workflow proposes production writes or model/probability changes.

Never work around a failed gate by guessing, fuzzy matching, imputing, disabling validation or creating a second competing model.

## 10. Backup and recovery procedure
- Restore the research code baseline from branch `backup/oracle-50-readiness-2026-10-30-98af1f7` if the active research branch is damaged. Inspect/compare first; do not force-reset or merge blindly.
- Restore historical data only from the private release above after verifying its package checksum against the matching `private-package.sha256` file.
- Keep all new research commits on the research branch and preserve the backup branch. Create a new dated backup branch before material refactors.
- Retain workflow artifacts externally before their expiry; GitHub Actions artifacts are temporary and are not a substitute for a durable archive.
- Keep a dated checkpoint and update this runbook after every material milestone. Record run IDs, artifact IDs, digests, code SHA, archive tag/SHA, data window, API request count and outstanding gates.

## 11. User action / automation limitation
The connected GitHub capability can inspect repository files, branches, pull requests, runs and artifacts, but cannot dispatch the workflows in this setup. The operator must start the manual workflow in GitHub Actions when a new weekly cycle is due. The weekly cycle is therefore documented and repeatable, but it is **not yet a proven unattended scheduled automation**. Do not promise that no future difficulties can occur; the safeguards are designed to fail closed and surface issues early.

## 12. Authoritative companion records
- `PROJECT_ORACLE_CANONICAL_HANDOVER.md` — detailed historical decision and run log.
- `docs/PROJECT_ORACLE_SELECTED50_200_SEASON_INGESTION_RECONCILIATION_2026-10-30.md` — 200-season ingestion evidence and reconciliation.
- `docs/PROJECT_ORACLE_SELECTED50_CALENDAR_YEAR_COVERAGE_2024_2027_2026-10-30.md` — exact 2024–2027 provider-row coverage and feature-quality roll-up.
- `docs/PROJECT_ORACLE_SELECTED50_ARCHIVE_QA_RUN44_2026-10-30.md` — latest private archive QA, xG/odds quality and event-status findings.
- `docs/PROJECT_ORACLE_SELECTED50_COMPMaster_ID_EVIDENCE_2026-10-30.md` — exact 50/50 provider `comp_master_id` field observations, held unapproved pending semantic confirmation.
- `docs/PROJECT_ORACLE_CANONICAL_PREDICTION_ARCHIVE_TEAM_EXPOSURE_AUDIT_2026-10-30.md` — canonical prediction archive exposure limitations.
- `reports/oracle-selected50-integration-release-gate-register-2026-10-30-1237-sast.md` — release gate checkpoint.
- docs/PROJECT_ORACLE_FOOTYSTATS_READINESS_AUDIT_2026-10-31.md — current FootyStats credential, plan, endpoint, rate-limit, chronology and workflow-wiring audit.
- This runbook is the operating entry point; update it rather than starting another handover from scratch.


## 13. FootyStats Selected-50 readiness checkpoint — 31 October 2026

### Credential and workflow reference verification
- The governed research branch references FOOTYSTATS_API_KEY in the bounded endpoint probe, current fixture snapshot and provider schema diagnostic workflows.
- The contract workflow ran a no-network presence check. Run 41208617886, job 124558743771, commit 5e80999c9d9b899a20e2b7e6d1631e681ff58096: FOOTYSTATS_API_KEY=PRESENT and ORACLE_PRIVATE_REPO_TOKEN=PRESENT. Only names and presence states were logged; no secret values were read back or printed.
- This confirms non-empty secret availability in that Actions context. It does not validate the FootyStats key with the provider, establish the subscription tier or prove the monthly credit balance.

### Provider limits and request controls
- The official plan table lists Hobby at 50 leagues and 1,800 requests/hour, Serious at 150 leagues and 3,600 requests/hour, and Everything at 1,500+ leagues and 4,500 requests/hour. A 50-league universe therefore sits exactly at the Hobby league cap. The account's current tier is not visible to this audit.
- Official API overview material separately states a general 60–90 requests/minute rate limit. The implementation uses the stricter Hobby hourly ceiling: 2.1 seconds between requests (approximately 1,714 requests/hour), with no automatic retries.
- The 201-call endpoint probe remains hard-capped at 201 and checks provider request_remaining before its 200 endpoint calls. That field is a request-window indicator, not monthly credit evidence.
- The current fixture snapshot is hard-capped at 50 requests. It stops on the first failed request, records a returned Retry-After header for HTTP 429, marks remaining seasons NOT_ATTEMPTED_AFTER_STOP and uploads the sanitized diagnostic even if validation fails. The validator rejects rate limits, retries, skipped requests, early stops, insufficient pacing, incomplete 50/50 success and unverified pagination metadata.

### Endpoint coverage interpretation
- Historical Probe #6 remains the last verified broad endpoint-access result: 201/201 HTTP 200; 50/50 exact selected season IDs found in the live catalogue; all four tested endpoints succeeded for all 50 seasons. Its evidence and artifact digest are recorded in Section 3.
- The 201 calls were one league-list?chosen_leagues_only=true request plus four endpoint checks per selected season: league-matches, league-teams?include=stats, league-tables and league-season.
- The match endpoint sampled one row per season only. This is not full-season pagination, full historical ingestion, proof that every field is populated for all leagues or proof that a supported market is complete in every league. The current 50-call snapshot checks one league-matches page per selected season and marks pagination gaps for rejection.
- Provider season IDs remain exact provider-native IDs. The existing 22 human-review candidates and 28 unresolved crosswalk rows remain unapproved; no canonical mapping was inferred.

### Event time and source revision provenance
- The documented date_unix field is the match kickoff timestamp. The snapshot retrieved_utc field is our capture time, not the provider's per-fixture or per-field update time.
- The documented max_time query parameter can request statistics as of a UNIX timestamp for supported endpoints, but the reviewed schema does not provide an immutable per-fixture revision identifier or a full historical revision log. A timestamped retrieval and file hash prove which response Oracle captured, not which historical version the provider served before a past kickoff.
- FootyStats documents a roughly 20-minute data-update cadence and post-match statistics availability around 20 minutes after full time. That cadence is not a substitute for point-in-time feature provenance.
- xG, odds, standings and other mutable provider fields remain audit-only/quarantined until timestamped pre-kickoff capture and revision provenance are independently demonstrated.

### Workflow wiring
- Registered on main and manually dispatched: bounded Selected-50 endpoint probe, current fixture snapshot, provider schema diagnostic, research runtime and Market Intelligence repair.
- The three provider-call workflows reference FOOTYSTATS_API_KEY and require explicit provider-credit and monthly-budget confirmations. Runtime/report archive workflows use the separate ORACLE_PRIVATE_REPO_TOKEN.
- oracle-selected50-footystats-live-ingestion.yml remains disabled. Do not reactivate its prohibited raw-data write path.
- oracle-selected50-safe-current-report.yml exists on the research branch but not on main; it is not a proven default-branch dispatch option. No default-branch change was made.

### Code and test evidence
- Request pacing, fail-fast handling, secret-presence verification and regression tests were committed in 834841796905e46744682bcd399628f8b43d445a.
- Missing/invalid pagination metadata was then changed to UNVERIFIED_PAGINATION and made validator-blocking in follow-up commit 5e80999c9d9b899a20e2b7e6d1631e681ff58096.
- On commit 5e80999c9d9b899a20e2b7e6d1631e681ff58096, the GitHub Actions contract job ran the secret-presence check successfully, passed the 16 offline FootyStats safety-contract tests, compiled the current fixture probe and validator, and passed all 22 current-fixture validator tests.
- The overall contract job 41208617886 did not finish green: step 20, snapshot-runtime bridge provenance tests, failed 2 of 19 tests: test_exact_hashes_and_run_ids_verify and test_snapshot_artifact_branch_must_match_snapshot_workflow_branch. The first returned verified=false where the test expected true; the second returned verified=true where the test expected false. This is a separate unresolved bridge/provenance test issue; no changes were made to that subsystem in this FootyStats audit.

### Nolan action required before any live provider run
1. Confirm the current FootyStats subscription tier supports the governed 50 leagues (at least Hobby under the published plan table) and check the actual monthly credit balance in the FootyStats account.
2. Explicitly authorise the next current-fixture snapshot, capped at 50 requests, before dispatch. Both workflow confirmation inputs must then confirm provider-credit usage and that the monthly budget was checked. No live provider calls or credits were used in this audit.
3. If the separate Safe Current Fixture Report workflow is required in the weekly sequence, approve registering that workflow on main. This audit did not modify the default branch.
4. Keep the snapshot-runtime bridge provenance test failures open until their evidence/branch mismatch is corrected and regression-tested.

No Oracle V1.6 production logic, model probabilities, calibration, thresholds or production eligibility flags were changed.


## 14. Market Intelligence report generator hardening — 31 October 2026

### Current implementation
The governed branch now carries the persistent report-template correction. Fixture Date, League and Fixture are the first three columns on every fixture-level supporting tab:
- xG Evidence Audit
- H2H Intelligence
- Team Form Evidence
- Data Quality & Risk
- Goal Intelligence
- Goal Market Research

A new Schedule Reconciliation tab and companion CSV are generated. Each conflict is explicitly marked REVIEW_REQUIRED and exposes:
- exact provider season ID, fixture ID and ordered home/away team IDs, plus a readable composite fixture identity;
- league and Home vs Away fixture label;
- runtime kickoff and archive kickoff;
- signed archive-minus-runtime delta in minutes;
- archive source file and source row;
- exact join status and manual authoritative-time review instruction.

Data Quality & Risk repeats the schedule status, both kickoff timestamps and the signed delta. The aggregate Market Data Coverage and Archive Field Coverage tabs are unchanged and do not receive fixture-context fields.

The canonical report contract is now template v1.2 with 12 tabs. Oracle V1.6 Output remains exactly 38 columns and Market Intelligence remains exactly 83 columns. All new work is report-only: production model logic/probabilities are unchanged, production_eligible=false and betting_eligible=false remain enforced, exact identity and strict pre-kickoff chronology gates remain in place, and no schedule value is auto-corrected.

### Governed branch commits
- bd32ca3d430364d91bcfd5286cfd41838154f277 — report generator fixture context, exact trace/goal research mapping and schedule queue.
- f4f5235fa4dcb0497f786aa4739e44e4f5d1c826 — retain Goal Market Research headers when the research input has zero rows.
- e8b3ac86f4eed6d8094c0262a54d6183ea366672 — focused workbook-context, exact-identity and schedule-queue tests.
- 0fa0293644489c30f62e8c4d9ba3077e47ceee28 — lock Market Intelligence template v1.2 and 12-tab contract.
- 056ffd29c898c60ef24cb6e15275ed8ffce0fe84 — include the queue CSV in successful and blocked workflow artifacts.
- 0297ecb3ea226792bdb20922d549b5877bdd789d — align the template's tab order with the generator.
- e6c1e42a841d1ab36b08463427e82f40e35314b1 — record this hardening checkpoint in the execution protocol.
- 9a778d46dbf6addb3aaa6aa22ab392ed956a83f5 — include the v1.2 template contract in the report regression workflow's push path filter.
- 5f99de18751f0a25271fd080a8f984d0598a706d — assert the empty Goal Market Research tab retains its context and base headers.

### Test evidence and limits
- The report regression file now contains 20 test methods. Two new focused tests verify that the schedule queue exposes all required conflict fields and that Goal Market Research context is attached only through the exact four-part composite identity. The workbook test checks all six fixture-level supporting tabs, context values, unchanged aggregate coverage headers and exact 38/83-column schemas.
- The Goal Market Research engine test file remains at 6 test methods.
- The governed push workflow contains the two test commands:
  - python -m unittest discover -s tests -p 'test_selected50_market_intelligence_report.py' -v
  - python -m unittest discover -s tests -p 'test_goal_market_research_engine.py' -v
- The source and test commits are on the governed branch. CI was subsequently verified: report workflow run [41211050502](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41211050502) completed successfully on commit `f5eb67788c9cae27781ba0f12d28362c70df166c`; the `market-intelligence-repair` job ran the report regression suite (20/20 passed) and Goal Market Research engine suite (6/6 passed). This was a push-triggered test run only; the archive/runtime download, full workbook rebuild and artifact upload steps were correctly skipped because no `workflow_dispatch` inputs were supplied.

### Full workbook and reconciliation status
- The last full report run remains 41205672854, artifact 13044203808, with 434 runtime fixtures, 50 governed league groups, 19 schedule discordances and PARTIAL_RESEARCH_ONLY status. It predates the v1.2 generator changes and must not be cited as verification of the new layout.
- No new full 434-fixture workbook or artifact was generated in this checkpoint. The full Market Intelligence workflow still requires manual workflow_dispatch on the governed branch; the connected GitHub workflow interface here cannot dispatch it.
- The next full report run must verify: 12 workbook tabs; 38-column Oracle V1.6 Output; 83-column Market Intelligence; context fields on the six fixture-level supporting tabs; aggregate coverage tabs without context columns; and exactly the currently known 19 conflicts in the Schedule Reconciliation tab/CSV, each REVIEW_REQUIRED with complete provenance.
- The 19 schedule conflicts remain open. No timestamp is selected or corrected by this implementation. Require authoritative fixture-time evidence and retain REVIEW_REQUIRED until resolved.

### Remaining blockers
1. Inspect the push-triggered report and goal-engine regression workflow results; test status is not yet verified.
2. Run the full manual report workflow and inspect the new workbook/CSV artifacts against the checks above.
3. Resolve the 19 schedule conflicts from authoritative event-time evidence.
4. Keep xG quarantined until capture time and revision provenance are established; last verified evidence was 0/434 verified capture timestamps.
5. Obtain contemporaneous odds and verified settlement/outcome data before calibration or performance claims.
6. Complete the separate FootyStats plan/credit and snapshot-runtime bridge provenance gates recorded in Section 13 and the companion readiness audit.

No FootyStats provider requests, credits, subscriptions, archive writes, Oracle V1.6 production logic changes or probability changes were made during this report-hardening work.


## 15. Bounded endpoint probe dispatch safety clarification — 31 October 2026

A static comparison of the default-branch and governed-branch workflow files found a material pacing difference that must be respected before any future manual dispatch:

- Default-branch workflow file: `.github/workflows/footystats-selected50-bounded-endpoint-probe.yml`, blob SHA `1c6948771af5e9dd198478a646d3c0ff3c03cff0`. Its inline request loop contains `time.sleep(0.35)` after endpoint requests. This is approximately 171 requests/minute (about 10,286/hour), above the documented general 60–90 requests/minute guidance and above the 1,800/hour Hobby allowance.
- Governed research-branch workflow file: same path, blob SHA `d51fa47be8f58cbf4f3a4109b38f0db18f4fb652`. It defines `REQUEST_INTERVAL_SECONDS = 2.1`, records that value in its sanitized summary and sleeps at that interval between requests (approximately 28.6/minute or 1,714/hour). It also retains the 201-call hard cap and zero automatic retries.
- Therefore, if the bounded endpoint probe is ever needed again, select `research/oracle-50-league-readiness-audit` in the GitHub Actions branch selector. Do not dispatch the `main` copy. This is a dispatch instruction, not approval to run the probe; it remains unnecessary unless the endpoint contract or selected-league configuration changes.
- The default-branch current-fixture snapshot workflow is a separate implementation: its YAML checks out the governed branch into `research-source` and runs `scripts/oracle_selected50_current_fixture_probe.py`. That branch script defines the 2.1-second interval, stops on the first provider failure, records Retry-After for HTTP 429 and performs no retries. The script blob inspected was `55efcfbe97cdad84d9fe4fd1e21a87f73e39d86d`.
- No provider API requests were made during this static comparison. No credits were consumed and no production code, probabilities or default-branch files were changed.

### Verification record
- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`.
- Governed branch head inspected before this documentation update: `38aea5b38ec023c47a8f4791c174b3eeaf96e40d`.
- Current-fixture snapshot branch script: 2.1-second interval; HTTP 429 capture; no retries; fail-fast; pagination validation remains fail-closed.
- Existing contract run `41208617886` remains overall failed because two of 19 snapshot-runtime bridge provenance tests failed. The FootyStats offline safety contract suite passed 16/16 and current snapshot validator suite passed 22/22. The two bridge failures remain open and must not be bypassed.
- This checkpoint changes documentation only. No new code tests were required or claimed as run for this update.
- Dispatch-safety documentation commit: `b25b29b5ffb243a2aed7ed4786573cd35e19aeb7` (this commit adds the default-branch versus governed-branch pacing comparison and the mandatory branch-selection warning).

### Operator gates unchanged
1. Nolan must confirm the FootyStats subscription tier supports all 50 selected leagues and check the actual monthly credit balance.
2. Nolan must explicitly authorise up to 50 requests before the next current-fixture snapshot; both workflow confirmation inputs must remain false until that approval and budget check are complete.
3. The separate Safe Current Fixture Report workflow remains on the research branch only; registering it on `main` requires separate approval if it is still needed.
4. Resolve the two snapshot-runtime bridge provenance test failures before treating the runtime/snapshot bridge as validated.
5. Preserve the existing 22 human-review candidate and 28 unresolved competition crosswalk classifications; no canonical mappings are approved by this audit.

Oracle V1.6 production logic and probabilities remain unchanged. Research outputs remain `production_eligible=false` and `betting_eligible=false`.


## 16. Market Intelligence hardening — CI confirmation and full-data inspection checkpoint — 31 October 2026

### Governed state and verified tests
- Governed branch: `research/oracle-50-league-readiness-audit`.
- Branch head inspected before this runbook update: `f0917fe24c0b7a8e3adf7b6842f391ff7485ceb6`. This includes the report hardening, v1.2 template contract, regression tests, artifact wiring, execution protocol update and endpoint-dispatch documentation. No code changes were necessary in this checkpoint.
- Latest report-specific push test: [GitHub Actions run 41211050502](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41211050502), triggered by commit `f5eb67788c9cae27781ba0f12d28362c70df166c`, conclusion `success`.
- Its `market-intelligence-repair` job passed the test step. Exact results from the job log:
  - `test_selected50_market_intelligence_report.py`: 20 tests, all passed.
  - `test_goal_market_research_engine.py`: 6 tests, all passed.
  - The 20-test suite includes workbook assertions for all six fixture-level supporting tabs, first-three context fields and fixture values; the unchanged 38-column Oracle V1.6 Output; the unchanged 83-column Market Intelligence view; aggregate coverage tabs without fixture context; exact-identity Goal Market Research context; and the Schedule Reconciliation conflict fields and delta.
- The earlier push run [41211032643](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41211032643) also passed the same report and goal-engine test step. The latest run 41211050502 is the primary evidence reference.
- Important: these were `push` event test runs. The workflow's private archive download, runtime-artifact verification, full report generation and artifact-upload steps were skipped by design. A green push test job is not a full-data workbook certification and produced no report artifact.

### Full-data baseline and 19 kickoff conflicts inspected
- The last available full-data report remains workflow run `41205672854`, artifact `13044203808`, generated before template v1.2.
- Its QA file confirms 434 runtime fixtures, 50 governed league groups, 434 exact archive joins, zero unmatched/quarantined identity rows, 19 schedule discordances, schedule gate `REVIEW_REQUIRED`, and both production and betting eligibility false.
- I downloaded and inspected that artifact. It contains 11 tabs and predates the new Schedule Reconciliation tab and fixture-context additions; it must not be presented as validation of the v1.2 workbook.
- The prior QA `join_failure_examples` contains all 19 schedule-conflict records with exact composite identity, runtime kickoff, archive kickoff, fixture names and archive source file/row. I independently mapped all 19 records to the successful runtime artifact from run `41175230838` using the exact four-part key, recovering the runtime league labels and confirming 19/19 identity matches. Calculated archive-minus-runtime differences range from -3,285 to +2,940 minutes: 12 archive times precede the runtime time and 7 follow it. Nine of the 19 archive timestamps are exactly 00:00:00 UTC, a possible date-only/default-time signature, but not proof of the provider's storage semantics. These differences are diagnostic only; no cause or authoritative kickoff can be assumed from this evidence.
- The new generator's trace/queue path now carries the runtime league and fixture context, exact identity, both timestamps, signed delta, source file/row, exact join status and `REVIEW_REQUIRED`. The focused synthetic regression test confirms the output mapping. The 19 real rows have not yet been regenerated through the v1.2 workbook; do not claim that the full-data queue has been inspected until the new manual report run completes.

#### Prior-run 19-conflict inventory — diagnostic baseline only
Source: QA examples from full report run `41205672854` / artifact `13044203808`, mapped to runtime prediction artifact from run `41175230838` by exact provider-season/fixture/ordered-team identity. Delta is archive kickoff minus runtime kickoff. This table preserves the discrepancy evidence; it is not a corrected schedule and is not a substitute for the new v1.2 generated queue.

| League | Fixture | Exact fixture identity (season\|fixture\|home\|away) | Runtime kickoff UTC | Archive kickoff UTC | Delta (minutes) | Archive source file:row |
|---|---|---|---|---|---:|---|
| Primera División | O'Higgins vs Ñublense | 16615\|8432240\|2191\|2201 | 2026-10-31T21:00:00Z | 2026-10-31T23:00:00Z | +120 | private-package/seasons/16615/matches.json:46 |
| Ukrainian Premier League | Veres vs Chornomorets | 17191\|8568431\|1675\|1674 | 2026-10-31T11:00:00Z | 2026-10-31T13:30:00Z | +150 | private-package/seasons/17191/matches.json:25 |
| MLS | Vancouver Whitecaps vs Seattle Sounders | 16504\|8390931\|5\|18 | 2026-11-01T20:30:00Z | 2026-11-01T21:30:00Z | +60 | private-package/seasons/16504/matches.json:326 |
| Ligue 1 | Olympique Lyonnais vs Angers SCO | 17102\|8548602\|57\|444 | 2026-11-01T16:15:00Z | 2026-10-31T19:45:00Z | -1230 | private-package/seasons/17102/matches.json:171 |
| LigaPro | CD Tondela vs Felgueiras 1932 | 17215\|8573971\|169\|4821 | 2026-11-01T14:00:00Z | 2026-10-30T18:00:00Z | -2640 | private-package/seasons/17215/matches.json:175 |
| LigaPro | Lusitania Lourosa vs Farense | 17215\|8574019\|4894\|4866 | 2026-11-01T15:30:00Z | 2026-11-01T14:00:00Z | -90 | private-package/seasons/17215/matches.json:223 |
| Super League | Panathinaikos vs AEK Athens | 17356\|8604046\|960\|1101 | 2026-11-01T17:30:00Z | 2026-11-01T17:00:00Z | -30 | private-package/seasons/17356/matches.json:172 |
| Ligue 1 | Lorient vs Brest | 17102\|8548603\|448\|491 | 2026-11-02T19:45:00Z | 2026-10-31T19:45:00Z | -2880 | private-package/seasons/17102/matches.json:172 |
| Ligue 2 | Reims vs Sochaux | 17117\|8551239\|451\|454 | 2026-11-02T19:45:00Z | 2026-10-31T13:00:00Z | -3285 | private-package/seasons/17117/matches.json:28 |
| Primera División | Univ. Concepción vs O'Higgins | 16615\|8432236\|2196\|2191 | 2026-11-05T23:00:00Z | 2026-11-08T00:00:00Z | +2940 | private-package/seasons/16615/matches.json:42 |
| Professional League | Al Kholood vs Al Khaleej | 17426\|8620554\|5125\|5077 | 2026-11-05T13:25:00Z | 2026-11-05T00:00:00Z | -805 | private-package/seasons/17426/matches.json:65 |
| Professional League | Abha vs Al Shabab | 17426\|8620615\|5093\|5067 | 2026-11-05T15:10:00Z | 2026-11-05T00:00:00Z | -910 | private-package/seasons/17426/matches.json:126 |
| Professional League | Al Quadisiya vs Al Feiha | 17426\|8620606\|5068\|5071 | 2026-11-05T17:30:00Z | 2026-11-05T00:00:00Z | -1050 | private-package/seasons/17426/matches.json:117 |
| Ligue 2 | Montpellier vs Metz | 17117\|8551236\|435\|438 | 2026-11-06T19:00:00Z | 2026-11-07T13:00:00Z | +1080 | private-package/seasons/17117/matches.json:25 |
| Liga I | UTA Arad vs Petrolul 52 | 17247\|8579504\|6653\|10307 | 2026-11-06T15:30:00Z | 2026-11-07T00:00:00Z | +510 | private-package/seasons/17247/matches.json:116 |
| Liga I | Argeș vs Dinamo Bucureşti | 17247\|8579523\|6644\|5400 | 2026-11-06T18:30:00Z | 2026-11-07T00:00:00Z | +330 | private-package/seasons/17247/matches.json:135 |
| Professional League | Al Fateh vs Al Riyadh | 17426\|8620610\|5064\|5088 | 2026-11-06T14:30:00Z | 2026-11-05T00:00:00Z | -2310 | private-package/seasons/17426/matches.json:121 |
| Professional League | Al Hazm vs Al Nassr | 17426\|8620666\|5089\|5069 | 2026-11-06T14:55:00Z | 2026-11-05T00:00:00Z | -2335 | private-package/seasons/17426/matches.json:177 |
| Professional League | Al Ittihad vs Neom SC | 17426\|8620553\|5070\|5097 | 2026-11-06T17:30:00Z | 2026-11-05T00:00:00Z | -2490 | private-package/seasons/17426/matches.json:64 |

No row in this baseline is resolved. Preserve every entry as `REVIEW_REQUIRED` in the next generated v1.2 workbook until authoritative event-time evidence supports a documented resolution.

- No timestamp has been auto-corrected. All 19 conflicts remain open for authoritative event-time review.

### Separate contract-test failure — not part of report generator
- Safety Contract Tests run [41211032556](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41211032556) failed at the separate snapshot-runtime bridge provenance test step: 2 of 19 tests failed:
  - `test_exact_hashes_and_run_ids_verify`
  - `test_snapshot_artifact_branch_must_match_snapshot_workflow_branch`
- The other preceding contract checks in that job passed, including FootyStats offline safety, research score/settlement, H2H chronology, current-feed identity, snapshot validator and runtime provenance tests. These bridge failures are outside the Market Intelligence report generator. They remain open and must not be bypassed or weakened by this task.

### Required next action and release gates
1. Nolan must manually dispatch [Oracle Selected-50 Market Intelligence Report Repair](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-market-intelligence-repair.yml) from the governed branch, confirming read-only private archive access and using the pinned archive release tag `research-selected50-footystats-history-40375285207` and runtime run `41175230838`. The connected GitHub interface used for this checkpoint exposes read/inspection and commit operations but no workflow-dispatch action.
2. Inspect the resulting workbook and CSV queue: exactly 12 tabs; 38 source columns; 83 decision-view columns; context on the six fixture-level tabs and Schedule Reconciliation; no context fields on the two aggregate coverage tabs; all 19 known conflicts present with complete league/fixture/identity/timestamp/delta/source provenance and `REVIEW_REQUIRED`.
3. Keep the 19 schedule records unresolved until authoritative kickoff evidence is obtained. Do not infer a correction from a large delta or date-only archive time.
4. Keep xG quarantined until capture-time and revision provenance are established. The prior full report recorded 0/434 verified capture timestamps.
5. Do not make accuracy/calibration claims until contemporaneous odds, chronological out-of-fold predictions and verified settlements are available.
6. Resolve the two snapshot-runtime bridge provenance test failures independently; do not relax exact artifact/run/branch/hash checks.
7. Confirm FootyStats subscription tier and remaining monthly credits, and obtain explicit approval before any live API requests or credit consumption.

No live FootyStats calls, credits, subscriptions or paid services were used in this checkpoint. Oracle V1.6 production logic, probabilities and thresholds remain unchanged. All report/research outputs remain `production_eligible=false` and `betting_eligible=false`.



## 17. FootyStats Selected-50 follow-up — 31 October 2026

### 17.1 Verified governed code state

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`.
- Governed branch: `research/oracle-50-league-readiness-audit`.
- Code/test head before this documentation update: `14e6152b2d9fe815a31ffbc0051fe42590f52b76`.
- Research workflow branch guard + immutable checkout commit: `f3c8ecf2809e11f6ac4c2b07f6b56486ecb09535`.
- Bridge provenance fixture correction: `a42d015f18d91716e85b273bf9078d27fb8a8947`.
- Branch-guard regression test: `14e6152b2d9fe815a31ffbc0051fe42590f52b76`.
- Companion readiness audit update: `69b19e942197e2c688091d0b70870fa2ffe3673e`.
- PR #31 remains an open draft against `main`; it is not merged and must not be merged without governance review.

### 17.2 Latest test evidence

The latest full Selected-50 Safety Contract Tests run is [41217808497](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41217808497), on code/test commit `14e6152b2d9fe815a31ffbc0051fe42590f52b76`, conclusion `success`.

- Presence-only secret check passed: `FOOTYSTATS_API_KEY=PRESENT`; `ORACLE_PRIVATE_REPO_TOKEN=PRESENT`. The values were not printed, hashed, transmitted to a provider or persisted.
- FootyStats offline safety contract: 16/16 passed.
- Current fixture snapshot validator/workflow contract: 23/23 passed, including the branch guard and immutable checkout test.
- Snapshot-runtime bridge provenance: 19/19 passed.
- All other steps in the contract job completed successfully.
- Related Identity & Settlement Evidence run `41217808555` and Dry-Run Planner run `41217808488` also completed successfully.

The earlier bridge failures were caused by inconsistent test fixtures: the positive fixture used a `main` snapshot artifact branch even though the bridge implementation requires the governed research branch. The positive fixture now uses the research branch; a negative test asserts that `main` is rejected. The branch requirement was not weakened.

### 17.3 Secret and workflow reference inventory

Static workflow inspection on the governed branch confirms:
- `FOOTYSTATS_API_KEY` is referenced by the bounded endpoint probe, current-fixture snapshot and provider-schema diagnostic workflows.
- `ORACLE_PRIVATE_REPO_TOKEN` is referenced by the private-archive research runtime and Market Intelligence repair workflows.
- The presence-only contract job confirms both names are non-empty in that Actions context. This does not establish provider-side key validity, account tier or monthly credits.
- No Secrets API was queried and no secret value was accessed or exposed.

### 17.4 Current workflow dispatch safety

The governed research-branch `oracle-selected50-current-fixture-snapshot.yml` now:
1. Rejects any dispatch unless `GITHUB_REF` is exactly `refs/heads/research/oracle-50-league-readiness-audit`, before the provider request step.
2. Checks out the workflow revision and research script using the same immutable `${{ github.sha }}`, avoiding a moving-branch race.
3. Retains explicit provider-credit and monthly-budget confirmations, a 50-request hard cap, 2.1-second pacing, no retries, stop-on-first-failure and fail-closed pagination validation.

**Do not dispatch the default-branch copy.** The `main` version has not been changed: it lacks the new branch guard and still checks out the moving research branch for its script. Use the governed research branch in the Actions branch selector.

The bounded endpoint probe also differs by branch:
- `main`: 0.35-second inline pacing; unsafe relative to the documented hourly/minute limits.
- Governed research branch: 2.1-second pacing, 201-call hard cap and no automatic retries.
- Do not dispatch the `main` copy. The existing 201/201 endpoint sample does not need to be repeated unless the endpoint contract or selected-league configuration changes.

The Safe Current Fixture Report workflow remains research-branch-only; it is still not registered on `main`.

### 17.5 Selected-50 provider and market readiness

The latest inspected per-league file is `reports/oracle-selected50-per-league-market-readiness-2026-10-25-run16.csv`, blob SHA `43826a40c53ce9bdd9257128fddf7d8dab01c02e`, cutoff `2026-10-25T10:10:42Z`. It contains 50 rows and 50 distinct FootyStats provider season IDs. Its evidence is stale and must not be treated as a current refresh.

The file records 22 human-review candidates and 28 unresolved canonical-code candidates; all 50 have unverified canonical team identity and unverified Oracle current-fixture joins. All 50 have unverified xG point-in-time provenance and unverified odds point-in-time provenance. All 50 are marked stale (source 8 October, reconciliation 7 October, schedule ends 17 October), and all 50 remain `production_eligibility=NOT_GRANTED`. BTTS Yes and Double Chance remain unverified/not production-ready; M-1UP remains blocked.

The last inspected successful live current-fixture snapshot is from 28 October 2026 (50/50 requests successful, 871 future-window rows). No fresh snapshot was generated in this follow-up. Do not use that snapshot as a 31 October current slate.

The current fixture probe retains fixture/team identity, kickoff/status, score, PPG and BTTS/over-2.5 potential fields. It does not currently retain xG, bookmaker odds, lineups, lineup publication times, injury or suspension data. The 201-call endpoint probe was a schema sample (one match per season) plus teams/tables/season endpoint access; it is not a full per-league field-completeness certification.

### 17.6 Plan, freshness and historical provenance

The English FootyStats API plans page currently lists Hobby at 50 selected leagues and 1,800 requests/hour. Official localized pages have conflicting Hobby capacity (40 leagues). The public API overview states 60–90 requests/minute and 20-minute result-update frequency; the FAQ says post-match stats are usually available within 20 minutes and historical coverage varies by league. These are public descriptions, not account entitlement, a freshness SLA or proof of pre-kickoff publication.

The match endpoint documents:
- `date_unix`: fixture kickoff timestamp.
- `max_time`: request statistics as of a UNIX timestamp.
- `page` and `max_per_page`: paginated match retrieval, with maximum page size 1,000.

Oracle's `retrieved_utc` is its capture time. Neither `date_unix`, `retrieved_utc` nor `max_time` proves immutable provider revisions or the exact publication time of a historical xG/odds/standings value. Keep mutable historical features quarantined until Oracle has timestamped pre-kickoff captures and verified revision provenance. Do not infer a point-in-time backtest from a current historical response.

### 17.7 Required Nolan action and stop conditions

Before a live fixture snapshot, Nolan must:
1. Check the FootyStats account dashboard and confirm the actual plan tier and the exact selected 50 leagues. The English and localized public plan pages conflict.
2. Check the current monthly credit balance.
3. Explicitly approve up to 50 provider requests for the next snapshot.

Until those steps are complete, both workflow confirmation inputs must remain false and no provider workflow may be dispatched.

Other blockers remain: full per-league non-null feature coverage; 22 candidate and 28 unresolved canonical-code mappings; canonical team/current-fixture joins; xG/odds pre-kickoff revision provenance; verified lineup/injury/suspension coverage; and current schedule freshness. The two snapshot-runtime bridge test failures are now resolved by the test-fixture correction and verified green run above.

No live FootyStats API calls, credits, subscription changes or costs occurred in this follow-up. Oracle V1.6 production logic, probabilities, thresholds and production registry were not changed. All research outputs remain `production_eligible=false` and `betting_eligible=false`.


## 18. Pagination fail-fast hardening and live-state recheck — 31 October 2026 (18:59 SAST)

### 18.1 Governed code change

The current-fixture snapshot was previously fail-closed at validation time, but the request loop could continue through the remaining leagues after the first response showed that pagination was required or pagination metadata was missing. That would consume unnecessary provider requests even though the final snapshot could not pass validation.

Commit `92710c5dc2de4c022d6949d0df204cc4ad0e8a16` hardens the research-only snapshot path:

- Every successful `league-matches` response must prove `pager.max_page=1` and `pager.current_page=1`.
- Missing, malformed, non-positive or inconsistent pager values are classified `UNVERIFIED_PAGINATION`.
- A valid `max_page>1` is classified `REQUIRES_PAGINATION`.
- On either condition, the script stops immediately after that response, sets `UNVERIFIED_PAGINATION_METADATA` or `PAGINATION_REQUIRED_ONE_PAGE_CAP`, and marks all remaining selected seasons `NOT_ATTEMPTED_AFTER_STOP`.
- No further provider requests are made after the first pagination blocker.
- The offline validator independently requires `max_page=1` and `current_page=1` for each of the 50 season records.
- The existing 50-request ceiling, 2.1-second pacing, no-retry policy, exact selected-season IDs, sanitized output, and research-only eligibility remain unchanged.

This is a request-cost and data-completeness safeguard. It does not alter Oracle V1.6 logic, probabilities, calibration, thresholds or production eligibility.

### 18.2 CI evidence

The following runs were triggered by the governed branch commit above. They made no FootyStats requests:

- [Selected-50 Safety Contract Tests — run 41222551988](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41222551988): completed successfully. The snapshot validator/workflow suite ran 25 tests; both new regression tests passed:
  - `test_pagination_metadata_requires_page_one_of_one`
  - `test_probe_stops_after_first_pagination_or_unverified_pager`
  The probe and validator compilation step passed. The presence-only Actions secret availability step also passed.
- [Identity & Settlement Evidence Tests — run 41222551893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41222551893): completed successfully.
- [Selected-50 Dry-Run Planner — run 41222551965](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41222551965): completed successfully.

The contract workflow's secret check prints only each required variable name and PRESENT/MISSING status. Its workflow definition does not print, hash, transmit or persist either secret value. No Secrets API was queried.

### 18.3 Selected-50 manifest and readiness evidence rechecked

Static reads on the governed branch confirm:

- Selected manifest `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`: 50 rows, 50 distinct provider season IDs; blob SHA `f6f9069b692b79a7595d1513a3413e8660763632`.
- Snapshot identity crosswalk `reports/oracle-selected50-provider-identity-reconciliation-2026-10-27.csv`: 50 rows, 50 distinct selected-manifest IDs; blob SHA `f78e9f371e2f566f148497d9a12ede56ad26bff4`.
- Canonical crosswalk readiness `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv`: 50 rows, 50 distinct FootyStats season IDs; blob SHA `2c23ac9d42f0b8cf85111ea5e431b234cc164ab4`.
- Per-league market readiness `reports/oracle-selected50-per-league-market-readiness-2026-10-25-run16.csv`: 50 rows, 50 distinct provider IDs; blob SHA `43826a40c53ce9bdd9257128fddf7d8dab01c02e`; evidence cutoff `2026-10-25T10:10:42Z`.

The readiness matrix still records 22 candidate canonical-code mappings requiring human review and 28 unresolved mappings. All 50 have unverified xG point-in-time provenance, unverified odds point-in-time provenance, stale freshness evidence, unverified canonical team identity bridges and unverified current-fixture joins. These files are evidence of the governed 50-ID universe and its unresolved gates, not a current schedule refresh.

### 18.4 Credential references and workflow wiring rechecked

Static workflow references on the governed branch:

- `FOOTYSTATS_API_KEY`: `footystats-selected50-bounded-endpoint-probe.yml`, `oracle-selected50-current-fixture-snapshot.yml`, and `oracle-selected50-provider-schema-diagnostic.yml`.
- `ORACLE_PRIVATE_REPO_TOKEN`: `oracle-selected50-research-runtime.yml` and `oracle-selected50-market-intelligence-repair.yml`.

The presence-only check in contract run `41222551988` succeeded. This proves non-empty values were available in that Actions job context at that time; it does not prove provider-side API-key validity, subscription tier, selected-league entitlement or monthly credits. No secret values were read or exposed in this audit.

The governed research-branch current-fixture workflow retains its pre-provider branch guard, immutable `github.sha` checkout for both workflow and script, explicit credit/budget confirmations, and research-only output. The `main` copy remains unguarded and checks out a moving research branch; do not dispatch the `main` copy. The bounded endpoint probe on `main` still uses 0.35-second pacing, while the governed research-branch version uses 2.1 seconds. Do not dispatch the `main` probe.

### 18.5 Provider plan, coverage and chronology assumptions

The current English FootyStats API page lists Hobby at 50 selected leagues and 1,800 requests/hour; the Dutch localized page displays 40 Hobby leagues. The actual account tier and selected 50 remain unverified. Public rate guidance is 60–90 requests/minute; the governed 2.1-second interval is approximately 28.6 requests/minute (about 1,714/hour), below the published 1,800/hour Hobby ceiling. See [English plans](https://footystats.org/api) and [Dutch plans](https://footystats.org/nl/api).

The prior bounded endpoint probe remains the only broad live endpoint sample: run `41106377807`, 201/201 HTTP 200, exact selected season IDs found for 50/50, and four tested endpoints successful for all 50. Its `league-matches` request sampled one match per season only. It is not full pagination, full-season ingestion, non-null feature coverage or market-readiness certification. No new probe was run.

The current-fixture snapshot last succeeded on 28 October 2026 (50/50 requests; 871 future-window fixtures). It is stale for a new prediction cycle. The current snapshot field whitelist does not include xG, bookmaker odds, confirmed lineup publication times, injuries or suspensions.

FootyStats documentation states that match retrieval is paginated, supports `page` and `max_per_page` up to 1,000, and accepts `max_time` for statistics as of a UNIX timestamp. The FAQ states feature coverage varies by league, post-match statistics are usually available within about 20 minutes, and historical coverage varies by competition. The match-details endpoint documents lineups, bench and odds-comparison fields, but does not establish immutable historical publication timestamps. See [Match Schedule & Stats](https://footystats.org/api/documentations/match-schedule-and-stats), [API FAQ](https://footystats.org/api/documentations/faq), and [Match Details](https://footystats.org/api/documentations/match-details).

`date_unix` remains event kickoff time; `retrieved_utc` remains Oracle capture time; `max_time` is a query cutoff, not an immutable revision identifier. Mutable historical xG, odds, standings and other features remain quarantined until pre-kickoff capture and revision provenance are independently demonstrated.

### 18.6 Remaining blockers and required Nolan action

Before the next live current-fixture snapshot, Nolan must:

1. Confirm in the FootyStats account dashboard that the actual plan tier and selected-league list cover the exact governed 50.
2. Check the current monthly API credit balance.
3. Explicitly approve up to 50 provider requests for one current-fixture snapshot. The workflow confirmation inputs must remain false until approval and budget confirmation.

No provider calls, API credits, subscription changes or costs were incurred in this checkpoint. Do not dispatch a live provider workflow before those actions.

Remaining technical blockers: per-league non-null feature coverage; 22 candidate and 28 unresolved canonical mappings; canonical team and Oracle current-fixture joins; timestamped pre-kickoff xG/odds/standings provenance; verified lineup/injury/suspension coverage; and fresh schedule evidence. The snapshot-runtime bridge provenance tests are green on the latest contract run.

No production model logic, probabilities, calibration, thresholds or release flags were changed. Oracle V1.6 remains the protected production benchmark; research outputs remain `production_eligible=false` and `betting_eligible=false`.

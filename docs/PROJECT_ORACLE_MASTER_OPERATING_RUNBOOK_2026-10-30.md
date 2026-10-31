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

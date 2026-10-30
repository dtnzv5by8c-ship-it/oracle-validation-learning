# Project Oracle — Master Operating Runbook & Recovery Pack
**Reviewed:** 30 October 2026 (SAST)  
**Scope:** Selected-50 research lane; Oracle production logic remains protected.  
**Canonical branch:** `research/oracle-50-league-readiness-audit`  
**Recovery branch:** `backup/oracle-50-readiness-2026-10-30-98af1f7` (snapshot of commit `98af1f79d3e79b4d9b7e177d21eb778233cf3bcd`)

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
- Backup branch: `backup/oracle-50-readiness-2026-10-30-98af1f7`
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
2. Check provider monthly credit allowance and current request limits before dispatch. The snapshot historically used up to 50 requests; obey its configured cap and fail-closed budget checks.
3. Run once. Record run ID, artifact ID, artifact digest, retrieval time and coverage window.
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
Workflow: [Oracle Selected-50 Safe Current Fixture Report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-safe-current-report.yml)
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
Private Archive QA #44 [run 41112970245](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41112970245) completed successfully against the refreshed archive. It produced artifact 13003309729 (SHA-256 `6dc7288826bcd384b469ea9ed53b46c66221f85a4292d2c52f9f5ca3f7be7ea9`) and is documented in `docs/PROJECT_ORACLE_SELECTED50_ARCHIVE_QA_RUN44_2026-10-30.md`. The research runtime and private-archive-QA workflows previously defaulted to stale archive tag `research-selected50-footystats-history-40447419806` and stale pinned SHA. On 30 October, both were corrected on the research branch to default to the verified 200-season archive release `research-selected50-footystats-history-40375285207` and SHA `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`. The xG temporal-shift audit's internal archive SHA guard was also updated to this verified package checksum and covered by a regression test. The safety contract tests and dry-run planner passed on commit `2c489d5c9c0aa0be3f6e0e297b7074d4c2be8f68` (runs `41112970222` and `41112970242`). Private Archive QA run `41112970245` was still running when this runbook revision was prepared; check its final conclusion before treating the latest QA as passed. The workflows must pass their checksum guards before use.

## 7. Provider field semantics now verified
- FootyStats Match Details documentation defines `no_home_away=1` as a fixture with no home/away distinction (neutral/no standard home-away assignment). The snapshot overlay already records this documented semantic and keeps flagged rows quarantined from standard home/away-dependent markets. Do not clear the flag merely because both team IDs are present. The current safe policy remains conservative until a neutral-fixture feature/market contract is tested; BTTS eligibility is not automatically granted by this clarification. Source: [FootyStats Match Details API documentation](https://footystats.org/api/documentations/match-details).
- The same documentation defines match `competition_id` as the league season ID, not the parent competition ID. The separate `comp_master_id` field was returned in the identity probe for 50/50 season IDs, but the public material reviewed does not define its semantics or stability. Preserve it as provider evidence only; do not promote it to Oracle canonical competition ID. See `docs/PROJECT_ORACLE_SELECTED50_COMPMaster_ID_EVIDENCE_2026-10-30.md`.

## 8. What is not yet seamless / gates still open
The following are not yet certified complete:
1. End-to-end weekly snapshot → runtime → safe-report cycle on the latest archive pin.
2. Secret availability and permission scope at the time of each run (never inspect secret values).
3. 50/50 canonical competition mappings; current crosswalk has 22 human-review candidates and 28 unresolved.
4. Canonical team and fixture identity joins.
5. Official outcome/settlement truth for each governed market.
6. Historical point-in-time provenance and availability for xG, odds, standings and team features.
7. 2024–2026 per-league/per-season coverage and missingness reconciliation against the private archive.
8. Leakage-safe chronological backtesting, calibration and market-level performance on held-out data.
9. Production parity and human release approval.

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
- `docs/PROJECT_ORACLE_SELECTED50_ARCHIVE_QA_RUN44_2026-10-30.md` — latest private archive QA, xG/odds quality and event-status findings.
- `docs/PROJECT_ORACLE_SELECTED50_COMPMaster_ID_EVIDENCE_2026-10-30.md` — exact 50/50 provider `comp_master_id` field observations, held unapproved pending semantic confirmation.
- `docs/PROJECT_ORACLE_CANONICAL_PREDICTION_ARCHIVE_TEAM_EXPOSURE_AUDIT_2026-10-30.md` — canonical prediction archive exposure limitations.
- `reports/oracle-selected50-integration-release-gate-register-2026-10-30-1237-sast.md` — release gate checkpoint.
- This runbook is the operating entry point; update it rather than starting another handover from scratch.

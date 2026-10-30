# Project Oracle — Latest Verified Checkpoint
**Date:** 30 October 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Purpose:** Fast recovery and continuation pointer. Read this first, then the Master Operating Runbook.

## Current recovery point
- Latest verified code/test commit: `2c489d5c9c0aa0be3f6e0e297b7074d4c2be8f68`.
- Safety Contract Tests run #487: PASS (run `41112970222`).
- Dry-Run Planner run #767: PASS (run `41112970242`).
- Private Archive QA run #44 (`41112970245`): PASS; artifact `13003309729`, SHA-256 `6dc7288826bcd384b469ea9ed53b46c66221f85a4292d2c52f9f5ca3f7be7ea9`.
- Safety Contract Tests run #487: PASS (run `41112970222`).
- Dry-Run Planner run #767: PASS (run `41112970242`).
- The QA workflow's first attempt against the refreshed archive failed on a stale hard-coded SHA in the xG temporal-shift audit. That pin and a regression test were updated to the verified current archive checksum; run #44 passed against the corrected checksum.
- Initial backup branch: `backup/oracle-50-readiness-2026-10-30-98af1f7`.
- QA #58 recovery branch: `backup/oracle-50-qa58-2026-10-30`.
- Latest final recovery branch: `backup/oracle-50-qa58-v4-2026-10-30`, snapshot commit `055133ef322a5b7aec3f28c362a3da7246fe94da` (includes exact calendar-year audit, league-level quality watchlist and Recovery Pack v4 references).
- Backup points to pre-documentation commit: `98af1f79d3e79b4d9b7e177d21eb778233cf3bcd`
- Runtime archive pin correction commit: `0d4135bdbde6558ce9237e6cce8f5f6510f5970b`
- Runbook commit: `23fa143407cb746f17be18f568f4f99abb0de677`
- Open draft PR #31 remains research-only; do not merge without approval.

## Verified archive
Private repository `dtnzv5by8c-ship-it/oracle-football-data`, release `research-selected50-footystats-history-40375285207`.
- Archive SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`
- 200 season folders (4 per selected league group), 50/50 selected season IDs exact, zero failed seasons.
- 59,049 match rows; 3,366 team-season roster memberships.
- This is archive ingestion/structure evidence only, not production-readiness proof.

## Latest completed live provider probe
- Workflow: [FootyStats Selected-50 Bounded Endpoint Coverage Probe #6](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41106377807)
- Status: completed successfully; job `selected50-endpoint-probe` success.
- Commit: `98af1f79d3e79b4d9b7e177d21eb778233cf3bcd`
- Artifact ID: `13000514278`; SHA-256: `f151803669223eeae53483018199c90b086378e2681a82cc0fcdc14bcaefe578`; expiry: 6 Nov 2026.
- 201/201 HTTP 200 calls: one live catalogue plus 50 each for league-matches, league-teams, league-tables and league-season.
- All 50 selected season IDs found exactly in live catalogue; each of four endpoints succeeded 50/50.
- One match row per season was sampled for schema only. This was not a full-season ingestion.
- Existing crosswalk state remains 22 candidate mappings requiring human review and 28 unresolved. No canonical identity was approved.
- Sample match field names include team xG/pre-match xG and BTTS/Double Chance odds fields in 50/50 league samples. Presence does not prove values, provenance, completeness or point-in-time validity.
- Last observed request_remaining was 1,599; it is not monthly-credit evidence.

## Workflow correction
The research runtime's stale default private archive tag and SHA were corrected on the research branch to the verified 200-season archive tag and checksum above. The correction must pass its checksum guard during the next runtime run.

## Weekly cycle
1. Run the fresh Selected-50 current fixture snapshot on the research branch after checking provider credit limits.
2. Run the Selected-50 research runtime with explicit private archive read confirmation, current archive tag and the successful snapshot run ID.
3. Run the Safe Current Fixture Report with those exact snapshot/runtime run IDs, 7-day horizon and 15-minute minimum lead.
4. Retain run IDs, artifact IDs/digests, code SHA, archive tag/SHA, as-of time and the exported report. Inspect all quarantine and gate outcomes.
5. Do not represent research-only, uncalibrated outputs as production predictions.

## Open release gates
- 22 candidate and 28 unresolved canonical competition mappings.
- Canonical team and fixture joins not fully verified.
- Official settlement truth and market specifications remain open.
- Historical PIT provenance for xG, odds, standings and features remains open.
- 2024 onward coverage needs league/season/value-level reconciliation.
- Market-specific chronological backtest/calibration and production parity are not yet cleared.
- Weekly end-to-end cycle has not yet been re-proven against the corrected archive pin.
- GitHub Actions dispatch is not available through the connected assistant interface; the operator still needs to trigger manual workflows. It is not yet an unattended scheduled weekly service.

## Canonical operating documentation
- [Master Operating Runbook & Recovery Pack](PROJECT_ORACLE_MASTER_OPERATING_RUNBOOK_2026-10-30.md)
- [200-Season Ingestion Reconciliation](PROJECT_ORACLE_SELECTED50_200_SEASON_INGESTION_RECONCILIATION_2026-10-30.md)
- [Canonical Prediction Archive & Team Exposure Audit](PROJECT_ORACLE_CANONICAL_PREDICTION_ARCHIVE_TEAM_EXPOSURE_AUDIT_2026-10-30.md)
- Detailed historical decisions and workflow log: `PROJECT_ORACLE_CANONICAL_HANDOVER.md`

**Rule:** continue from this checkpoint and the active research branch. Do not recreate prior audits or re-run completed provider probes unless a specific evidence gap requires it.

## Durable ChatGPT Library recovery copy
The following run outputs and workbook were copied into the persistent ChatGPT Library folder `/Project Oracle/2026-10-30 Recovery Pack/`: Probe #6 artifact, Visual Intelligence workbook v2, safe current report #5, research runtime #174, current fixture snapshot, private archive QA #40, identity probe #3, dry-run planner #760, cross-provider join audit #18, and FootyStats archive feature audit #64. These are copies of the artifacts available in this session; the canonical private historical archive remains in the private GitHub release listed above.

Latest documentation refresh commit: `92188350b8bd5a0841063a2e03271a17c5db34cd`.

## Latest archive QA findings
- Exact 2024–2026 calendar-year coverage audit: QA #58, run `41115501513`, artifact `13004648723`, SHA-256 `b10eefaca601782e1083374d7f9836926a953f35f039274806149bac83cd9fc0`.
- 200/200 archive season folders exact, 50/50 selected groups, 800 season-year output rows, zero undated rows and zero missing/unmatched season folders.
- Provider match rows: 2024 14,761 (50/50 groups); 2025 15,029 (50/50); 2026 14,605 total, of which 12,222 are on/before 30 Oct and 2,383 are future; 2027 4,452 future-only (32/50 groups).
- Historical rows on/before 30 Oct: 42,012, including 41,781 provider-complete and 231 non-complete rows. Provider-complete status is not independent official settlement truth.
- Full coverage and complete-status xG/odds field-zero rates: `docs/PROJECT_ORACLE_SELECTED50_CALENDAR_YEAR_COVERAGE_2024_2027_2026-10-30.md`.
- 200/200 season folders present; 59,049 match rows; 3,366 team-season roster memberships; 22,291 unique provider match IDs in the primary validation window; no duplicate IDs in that window.
- 116 past-kickoff rows remain `incomplete`; 7,066 non-complete rows have parseable 0-0 score pairs; official settlement truth remains unverified.
- Current vs historical prematch-xG zero rates: home 13.26% vs 3.54%; away 13.30% vs 3.52%; total 11.91% vs 3.16%. Eleven groups cross the descriptive 30% zero-rate screen. Odds zero-mask anomalies remain under investigation.
- Full findings: `docs/PROJECT_ORACLE_SELECTED50_ARCHIVE_QA_RUN44_2026-10-30.md`.
- Recovery bundle v2 and individual QA #44 artifact are saved in ChatGPT Library at `/Project Oracle/2026-10-30 Recovery Pack/`.

Latest QA report commit: `711045e3f8620c72ce01b87e67c4711995dd2fc3`.
Latest runbook refresh commit: `25d3272a93fa32f8f9b70c2a05c1c3c919ca7fe3`.

Latest exact annual coverage report commit: `b2b7c09418c685d2fc00a20447a3fcaf6a9e4d64`.
Latest runbook refresh commit: `f59af9fad3b11e49895298f560cb6d5547986b57`.

Latest runbook commit after recovery-branch record: `a4d7a79f536aa686182ead10607f3927b795b1f6`.

## Latest annual quality exceptions
- Belgium Pro League 2026: BTTS Yes/No and Double Chance 1X/X2 odds each have 89/233 zero values (38.20%), compared with no BTTS zero values in 2024 and 2025. P0 odds-market quarantine candidate pending provider confirmation.
- India 2026 prematch home/away xG zeros: 23/107 (21.50%); Japan 2026: 20/120 (16.67%). P1 xG source investigations.
- Detailed annual coverage and complete-status field quality: `docs/PROJECT_ORACLE_SELECTED50_CALENDAR_YEAR_COVERAGE_2024_2027_2026-10-30.md`.

Latest runbook pointer update commit: `3ab7558b28e34bbae3b62419f5d7652efde2af0a`.

## Latest Library backup
- Recovery Pack v4 saved at `/Project Oracle/2026-10-30 Recovery Pack/Project_Oracle_Recovery_Pack_2026-10-30_v4.zip`.
- Recovery Pack v4 SHA-256: `02ac0e814edd481c20c853e88fbe47ee680df24b718087cd84bbfd0edd371c87`.
- Added human-readable workbook `Oracle_Selected50_2024-2027_Coverage_and_Feature_Audit_30Oct2026.xlsx` (200 league-year rows, 800 season-year rows, quality watchlist and definitions).

Latest runbook recovery-branch pointer commit: `cbb850d61c125975dbe4d7b8e64750937551c80a`.

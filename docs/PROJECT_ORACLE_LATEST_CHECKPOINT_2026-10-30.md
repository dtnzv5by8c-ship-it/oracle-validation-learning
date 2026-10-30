# Project Oracle — Latest Verified Checkpoint
**Date:** 30 October 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Purpose:** Fast recovery and continuation pointer. Read this first, then the Master Operating Runbook.

## Current recovery point
- Backup branch created: `backup/oracle-50-readiness-2026-10-30-98af1f7`
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

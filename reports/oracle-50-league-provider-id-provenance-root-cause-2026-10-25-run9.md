# Project Oracle — Selected-50 Provider ID Provenance Root-Cause Report
Date: 2026-10-25 04:49 UTC
Branch: `research/oracle-50-league-readiness-audit`
Decision: **BLOCKED — production eligibility NOT GRANTED**

## Executive finding
The new exact-scope guard now runs in the research-only archive feature workflow. Runs #54, #55 and #56 all completed successfully, but the guard correctly blocked selected-50 readiness. The workflow green status means the diagnostic completed, not that the scope passed.

## Verified artifact evidence
- Run #54: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155615819
  - Artifact ID: `12584008833`
  - 97 unit tests passed.
  - `selected50_scope_guard.json`: `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`.
- Run #55: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155717694
  - Artifact ID: `12584253631`
  - 97 unit tests passed.
  - Catalogue schema diagnostics established three columns: `provider_league_id`, `provider_league_name`, `season_count`; 43 rows and no populated provider IDs.
- Run #56: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155799320
  - Artifact ID: `12583524862`
  - Artifact SHA-256: `a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`
  - 98 unit tests passed, including the test for a present-but-blank ID column.
  - Guard result remains `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`.

Run #56 archive summary:
- 35,819 match rows and 35,819 chronological feature rows.
- 126 season folders/manifest rows.
- 28,491 rows had accepted settled status and complete score.
- Zero parse errors; zero duplicate nonempty fixture IDs; no missing team IDs or team names in the archive integrity summary.
- Archive release freshness gate passed at 3.92 days old against a 14-day maximum.
- Production readiness explicitly `NOT_ASSESSED`.

These counts describe the archive package, not exact selected-50 coverage or current fixture freshness.

## Exact-scope guard findings
1. Owner-selected manifest: 50 rows / 50 unique provider IDs.
2. Research crosswalk: 50 rows / 50 unique IDs; exact ID-set equality with the selected manifest.
3. Acquired provider catalogue: 43 rows; columns `provider_league_id`, `provider_league_name`, `season_count`; all 43 `provider_league_id` values blank.
4. Archive manifest: 126 rows; all 126 `provider_league_id` values blank.
5. Therefore no exact selected provider ID -> archive fixture -> canonical team join can be certified from this package. A season ID must not be substituted for a provider competition ID.

## Source-code review: verified risk, exact producer not yet attributed
The public research feature builder `scripts/build_footystats_archive_features.py` derives `provider_league_id` from match-payload fields `competition_id`, `league_id`, or `leagueID`, while it separately reads `season_id`/`seasonID`. The audited archive payloads yielded blank provider IDs.

A separate private workflow, `.github/workflows/footystats-private-historical-ingestion.yml`, calls the FootyStats `league-list` endpoint. Its current mapping code stores a name-to-season-list mapping and writes `oracle_code`, `provider_name`, `season_start_year`, `season_year`, `season_id`, and status, but does not preserve the parent league object's top-level `id` in the mapping rows. This is a verified ID-preservation gap in that workflow. However, the reviewed files do not establish that this private workflow generated the specific 43-row `selected_leagues.csv` in the public audit artifact. The precise upstream producer of that CSV remains unidentified; do not claim a proven single root cause.

## Other live-state blockers
- Protected canonical registry remains the 27-entry registry, not the scope for this audit.
- The legacy readiness matrix last refreshed 2026-10-01.
- Current-source manifest is dated 2026-10-08; reconciliation is dated 2026-10-07 and reports 108 unverified rows; current team state is dated 2026-10-07.
- The upcoming fixture manifest covers only the legacy 27 leagues and ends 2026-10-22.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv` has zero data rows.
- Latest private expansion run #208 (40149882862) still failed in `prepare`; no artifacts and job-log retrieval returns `BlobNotFound`. No newer private run appeared in the latest eight-run listing at this checkpoint.
- Canonical candidates remain 22 review-only; 28 selected leagues remain `UNRESOLVED`. No mappings are approved. M-1UP remains blocked; BTTS Yes, Double Chance and DC Under 4.5 remain unverified for the selected IDs.

## Required remediation
1. Identify the actual producer of the 43-row selected catalogue and preserve the source league/competition ID as a nonblank `provider_league_id`.
2. Preserve `season_id` in its own field; never repurpose it as the provider league ID.
3. Enforce exact set equality between the 50 selected IDs and the provider catalogue before admitting any rows to the selected-50 package. Fail closed on missing, duplicate, extra, or blank IDs.
4. Preserve parent competition IDs in archive manifests even when match payloads omit them, using an explicit, source-backed season-to-competition relation. Do not infer the relation from numeric equality alone.
5. Only after exact IDs exist, join fixture IDs and canonical home/away team IDs; then verify current fixtures, recent form, standings, xG/odds point-in-time provenance, immutable feature snapshots, and each supported market independently.

## Governance
The updated crosswalk is `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r9.csv` (50 rows, 50 unique provider IDs, 154 columns). It records run #56 and the verified blockers. The run-8 checkpoint has been updated with artifact results.

No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry or canonical ledgers were changed. No draft PR was merged, no quality gate bypassed, and no paid provider change was made.

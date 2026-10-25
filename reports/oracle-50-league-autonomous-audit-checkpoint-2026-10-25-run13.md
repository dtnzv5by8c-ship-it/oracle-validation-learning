# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 13)

Audit date: 2026-10-25
Branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**
Scope: exact 50 owner-selected IDs from `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`. Research/reporting only.

## New research-only deliverable

- Crosswalk revision 14: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r14.csv`.
- Commit: `c0deaeb57df164f7242037b7ef183c28a6302be7`.
- Revision 14 retains all 50 manifest IDs and the existing review-only candidate/unresolved classifications. It adds a verified archive season-level join status, locked-window historical counts, feature availability counts, and the current-data consistency failures observed directly in repository artifacts.
- Structural validation of the generated CSV: 50 rows, 50 unique IDs, exact 50-ID scope retained, 22 review-only candidates, 28 unresolved, 0 approved mappings, 31 exact archive season-level joins, 19 IDs without an exact archive join.

## Identifier semantics — improved, not fully closed

Official FootyStats documentation:
- League List: https://footystats.org/api/documentations/league-list — says each season of a competition has a unique ID and describes `season > id` as the season ID.
- League Matches: https://footystats.org/api/documentations/match-schedule-and-stats — takes `season_id` as the ID of the league season.
- Player Individual: https://footystats.org/api/documentations/player-individual — describes `competition_id` as the ID of the season and league.

In the downloaded Run 56 archive artifact, 31 selected IDs match a 2026 season-folder ID, the exact country/competition name corroborates the folder, and every fixture in that matched folder carries the same ID in its `competition_id` field. This is exact **season-level historical archive evidence**. It does not establish a separate parent-competition ID, does not prove a current-feed join, and does not resolve the 19 IDs absent from the archive.

The account-specific selected-catalogue diagnostic has not run. The existing catalogue artifact has 43 competition-name rows and a blank `provider_league_id` column in all 43 rows; the archive manifest has 126 rows and blank `provider_league_id` values throughout. The saved checkbox control's precise semantics and the 19 unmatched IDs therefore still need live account catalogue evidence.

## Locked historical window coverage (2025-03-20 through 2026-09-20)

Denominator: 15,016 archive fixture rows across the 31 exact season-level joins. The other 19 selected IDs remain UNVERIFIED for this archive window.

| Evidence | Rows | Coverage |
|---|---:|---:|
| Settled-status and score-complete rows | 15,003 / 15,016 | 99.91% |
| Team IDs present for both sides | 15,016 / 15,016 | 100.00% |
| Parseable kickoff timestamps | 15,016 / 15,016 | 100.00% |
| Home recent form, at least 5 prior matches | 14,612 / 15,016 | 97.31% |
| Away recent form, at least 5 prior matches | 14,591 / 15,016 | 97.17% |
| Provisional standings for both teams | 14,467 / 15,016 | 96.34% |
| Numeric fields labelled pre-match xG present | 15,016 / 15,016 | 100.00% |
| At least one odds field name present | 15,016 / 15,016 | 100.00% |
| Odds timestamps present | 0 / 15,016 | 0.00% |
| Verified point-in-time xG provenance | 0 / 15,016 | 0.00% |
| Verified point-in-time odds provenance | 0 / 15,016 | 0.00% |

These are archive availability counts, not proof that xG or odds were available before kickoff. The audit policy excludes numeric fields from model features until point-in-time provenance is verified. Provisional standings also remain research-only because competition-specific formats, deductions, splits, playoffs, and tie-break rules have not been validated.

## Current-feed and snapshot integrity — newly confirmed blockers

The private repository files are internally inconsistent:

- `database/current_matches.csv`: 241 data rows, dates 2026-10-01 to 2026-10-10, 13 legacy league labels.
- `database/current_source_reconciliation.csv`: 108 rows, dates 2026-09-30 to 2026-10-09.
- `database/current_reconciliation_status.json`: generated 2026-10-07; reports 108 current match rows, 128 goal-event rows, and `EVENT_TRUTH_STALE`.
- `database/current_goal_events.csv`: 137 data rows; the status file reports 128.
- `database/current_prematch_team_state.csv`: empty (0 data rows), although `data/current_team_state_manifest.json` claims 12,883 rows generated 2026-10-07.
- `data/fixtures/oracle_upcoming_fixtures.csv`: 80 rows, dates 2026-10-09 through 2026-10-17, using 13 legacy Oracle codes rather than the selected-50 provider IDs.
- `data/current_source_manifest.json`: generated 2026-10-08; requested dates 2026-10-01 through 2026-10-10.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv`: header only, 0 data rows.

The current files cannot be reconciled to a single trustworthy freshness state. The 27-row legacy readiness matrix was last refreshed 2026-10-01 (22 `PRODUCTION-READY`, 5 `PARTIAL`); it does not establish selected-50 readiness. The protected canonical registry remains at 27 entries (13 `CONTROLLED`, 14 `NOT_INGESTED`) and is unchanged.

## Workflow and artifact inspection

- Public research Run 56 (`40155799320`) completed successfully with 98 tests passed. Artifact `12583524862`, digest `sha256:a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`, was downloaded and inspected. Its selected-50 scope guard remains `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`; this is diagnostic success, not readiness.
- Private Expansion run `40149882862`: `prepare` failed; downstream jobs skipped; no artifacts.
- Private Current Staging run `40135966324`: `current` failed; no artifacts.
- Requests for the two private failed-job log blobs returned `BlobNotFound` / HTTP 404, so the root causes are not established from logs.
- The new read-only selected-50 schema diagnostic workflow is present on the research branch and the research repository default branch. The connected GitHub tools do not expose workflow dispatch, and no run/artifact for this diagnostic is present in the inspected evidence. No provider API request was made in this audit.

## Market readiness

All 50 remain ineligible for production predictions.

- **M-1UP:** blocked by stale event truth and no current selected-50 fixture/team bridge. Exact historical season-level joins exist for 31 only.
- **BTTS Yes:** not verified for selected-50 production use; current feed/team identity, point-in-time feature provenance, and market walk-forward gates remain open.
- **Double Chance:** not verified for selected-50 production use for the same reasons.
- **Double Chance + Under 4.5:** not verified for selected-50 production use for the same reasons.

## Next safe actions

1. Manually run the research-only schema diagnostic once in GitHub Actions with the existing `FOOTYSTATS_API_KEY` secret, if present. It makes one read-only catalogue request and emits only sanitized schema/match metadata.
2. Use that output to confirm which field the account's 50 checkbox IDs represent; do not infer parent IDs from season IDs.
3. Resolve the 19 IDs with exact provider evidence; preserve `UNRESOLVED` where evidence is absent.
4. Reconcile the current match/event/team-state files and their manifests; do not run predictions while the counts and freshness gates disagree.
5. Rebuild current selected-50 fixture/team joins, establish point-in-time feature provenance, and rerun market-specific validation before any readiness claim.

No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry, or canonical ledgers were modified. No draft PR was merged, no gate was bypassed, no paid provider change was made, and no readiness pass is claimed.

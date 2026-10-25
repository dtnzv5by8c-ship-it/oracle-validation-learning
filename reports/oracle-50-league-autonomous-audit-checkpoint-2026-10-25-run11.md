# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 11)

Audit date: 2026-10-25
Branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**
Scope: exactly the 50 owner-selected FootyStats checkbox IDs in `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`. Research/reporting only.

## Research commits and artifacts

- Crosswalk revision 12: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r12.csv`
- Schema diagnostic workflow: `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml` (present on this research branch and on the research repository's default branch so it can be manually dispatched).
- Diagnostic workflow commit on research branch: `9145f626e22018e7e991b4d907af4128afed9f66`.
- Diagnostic workflow commit on research repository default branch: `1cd654e6824b2e30ba9a2ed7e420235557e9e668`.
- Crosswalk revision 12 commit: `ec08673cf0cdf6c37beb76bdf577f40f51bf8d8e`.

## Exact-scope and canonical crosswalk status

- Selected manifest: 50 rows, 50 unique IDs.
- Crosswalk revision 12: 50 rows, 50 unique IDs; exact ID-set equality with the manifest.
- Canonical candidates: 22, explicitly marked `CANDIDATE_REQUIRES_HUMAN_REVIEW_NOT_APPROVED`.
- Canonical unresolved: 28, explicitly marked `UNRESOLVED`.
- Approved mappings: 0.
- Exact selected ID to protected parent-competition ID to API fixture/canonical team joins: 0/50 verified. The protected registry remains unchanged at 27 leagues; it is not the selected-50 scope.

## New evidence from the actual Run 56 artifact

Run 56 (workflow run ID `40155799320`) completed successfully; 98 tests passed. Artifact ID `12583524862`, digest `sha256:a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`. The downloaded artifact was inspected, not just its metadata.

- Archive integrity summary: 35,819 match rows and 35,819 chronological feature rows across 126 season folders; zero duplicate non-empty fixture IDs, zero duplicate feature fixture IDs, zero rows missing team IDs, and zero rows missing team names. Production readiness was not assessed by this archive audit.
- The artifact's `league_season_mapping.csv` contains an exact `season_id` match for 31/50 selected IDs. All 31 matched archive season IDs have season start year 2026.
- The same 31 rows have exact country/competition corroboration after Unicode diacritic normalization in the archive. The remaining 19 selected IDs have no exact `season_id` match in the 126-row archive mapping and no exact country/competition match in the audited archive snapshot.
- For the 31 exact season-ID matches, the corresponding 2026 archive season folders contain 9,708 records in total: 3,488 rows with settled-status labels and 6,220 rows with non-settled-status labels. The 31 name-matched competitions also contain 20,549 prior-two-season records, for 30,257 archive records in total across those matched seasons.
- These are archive/season-level joins, **not** proof that the checkbox values represent parent competition IDs. The source account's raw checkbox/API response was not retained. Revision 12 now distinguishes exact selected-ID-to-archive-season evidence from the still-unverified parent competition ID and live API fixture join. No canonical mapping was promoted as approved.

## Current feed and feature readiness

- Existing readiness matrix: 27 rows, 22 labelled `PRODUCTION-READY` and 5 `PARTIAL`; last successful refresh `2026-10-01T17:25:35.759116Z`. This is a stale legacy snapshot and does not prove selected-50 readiness.
- Protected canonical registry: 27 entries (13 `CONTROLLED`, 14 `NOT_INGESTED`); untouched.
- Current source manifest generated `2026-10-08T04:32:49Z`; requested window `2026-10-01` through `2026-10-10`.
- Current reconciliation generated `2026-10-07T04:33:52Z`, status `EVENT_TRUTH_STALE`, 108 match rows, 128 goal-event rows, and four completed matches missing goal-event chronology.
- Current team-state manifest generated `2026-10-07T04:33:53Z`, 12,883 rows, history window 5.
- Immutable feature snapshot manifest `archive/FEATURE_SNAPSHOT_MANIFEST.csv` remains header-only with zero rows.
- Independent current-source reconciliation remains 108 unverified, zero matched, with eight HTTP 403 errors. Existing current fixtures only extend through 2026-10-17 and use legacy league codes.

## Market readiness (selected-50 scope)

- **M-1UP:** blocked for all 50 by stale event truth and lack of verified selected-ID-to-parent-provider/fixture joins.
- **BTTS Yes:** not verified for all 50; selected-ID fixture joins and point-in-time feature provenance are not established.
- **Double Chance:** not verified for all 50 for the same reasons.
- **Double Chance + Under 4.5:** not verified for all 50 for the same reasons.
- Verified pre-match xG provenance: 0 rows.
- Verified pre-match odds provenance: 0 rows; odds timestamp fields: 0 rows.
- H2H chronology and team identity are not cleared for selected-50 use.

## Diagnostic workflow prepared; not yet run

The new workflow `oracle-selected50-provider-schema-diagnostic.yml` is a one-call, read-only `league-list` schema diagnostic. It reads the exact 50-row manifest, verifies 50 unique IDs before calling the provider, reports only schema keys and selected-ID matches against direct league/season ID fields, suppresses request errors and response bodies, does not save the raw payload or API key, performs no match ingestion, and uploads only a sanitized summary artifact with seven-day retention.

The connected GitHub tools in this run do not expose workflow dispatch, so the diagnostic has **not** been triggered and no provider API call was made. It requires the existing `FOOTYSTATS_API_KEY` repository secret. Manual dispatch from the research repository's Actions page is the next action; do not rerun the older catalogue-transfer workflow unchanged.

## Required blockers before completion

1. Run the new schema diagnostic and verify whether selected checkbox IDs correspond to season-level IDs, another documented field, or remain unmatched. Preserve parent competition ID and season ID as separate fields.
2. Resolve the 19 selected IDs with no archive season-ID match using exact provider evidence; do not fuzzy-map.
3. Repair/rebuild the catalogue/archive mapping so the exact selected IDs survive ingestion and can join to the correct season and fixture rows.
4. Refresh current fixture/event truth and team state for the selected-50 scope; establish exact canonical team IDs, recent form and standings coverage per league.
5. Create immutable feature snapshots and prove as-of-kickoff xG and odds provenance/timestamps.
6. Re-run independent validation and market gates for each of the 50 leagues and four supported markets. Do not infer market readiness from archive volume alone.

## Governance

No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry or canonical ledgers were changed. No draft PR was merged, no gate was bypassed, no paid provider change was made, and no readiness pass is claimed.

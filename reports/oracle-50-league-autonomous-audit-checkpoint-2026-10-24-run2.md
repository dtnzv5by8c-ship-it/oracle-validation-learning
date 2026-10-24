# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 2)

- **Checkpoint date:** 2026-10-24 (SAST)
- **Research branch:** `research/oracle-50-league-readiness-audit`
- **Mode:** research-only; no production writes
- **Outcome:** **NOT COMPLETE** — exact selected-provider-ID joins and current readiness gates remain unverified.

## Work completed this run

1. Re-read the owner-approved 50-entry FootyStats manifest and addendum.
2. Read the live protected registry at `config/oracle_major_league_registry_v1.json` on private `oracle-football-data@main` (blob SHA `81d6db487e498fc84a87a7457b0de7215537f15c`), plus `config/data_config.json`, the separate `league_intelligence_matrix.csv`, and `data/league_readiness_matrix.csv`.
3. Read current-source, upcoming-fixture, historical-spine, prematch-state, current-team-state, FootyStats and Sofascore manifests, and the M-1UP event-truth manifest.
4. Built a stricter second-pass 50-row CSV. It accepts only (a) exact country + competition-name matches or (b) explicit country-scoped aliases already declared in `scripts/build_oracle_competition_crosswalk.py`. All candidates remain review-only. Prior candidates not supported by the protected registry and explicit alias evidence were demoted to `UNRESOLVED` rather than silently retained.
5. Validated the generated register in memory: 50 rows, 50 unique provider IDs, every row retained, and no provider-ID-to-API-fixture join represented as verified.

## Crosswalk result

| Measure | Result |
|---|---:|
| Owner-selected entries preserved | 50/50 |
| Exact country + competition-name candidates | 13 |
| Explicit country-scoped alias candidates | 9 |
| Unresolved against protected 27-entry registry | 28 |
| Exact FootyStats ID → API fixture → canonical fixture/team joins verified | 0/50 |
| Selected-league market readiness passes verified | 0/50 |

The 22 codes are **candidates only**, not approved mappings. The 28 unresolved rows remain in the CSV. Prior crosswalk snapshot candidates now unresolved under the stricter protected-registry rule: Greece — Super League (prior GRC_G1); Romania — Liga I (prior ROU_R1); Serbia — SuperLiga (prior SRB_SR1); Switzerland — Super League (prior CHE_S1).

## Existing data evidence — correct scope and freshness

| Artifact | Actual persisted evidence | Limitation for the selected 50 |
|---|---|---|
| Protected registry | 27 entries; active-universe count 27; blob `81d6db487e498fc84a87a7457b0de7215537f15c` | It is the protected 27-entry registry, not a 50-entry provider-ID map. Membership/readiness does not approve provider joins. |
| Separate league intelligence matrix | 22 candidate rows have a distinct research-code row in this strict pass, totalling 10305 fixture rows; matrix dates are generally 2025-03-20/21 through 2026-09-20 | These are separate research-code counts, not counts joined to the selected FootyStats IDs. |
| Existing canonical readiness matrix | 27 rows; last successful refresh shown as 2026-10-01T17:25:35.759116Z | Stale. 7 candidate rows conflict as registry `NOT_INGESTED` versus matrix `PRODUCTION-READY`; 4 more are registry `NOT_INGESTED` versus matrix `PARTIAL`. 11 candidate rows say `PRODUCTION-READY` while the same snapshot has zero fixture rows. Do not use these statuses as 50-league readiness. |
| Current fixture manifest | Generated 2026-10-08T04:30:39.615849+00:00; 27-league target list; window 2026-10-08–2026-10-22 | Stale on 2026-10-24; 28 selected entries have no target in this 27-target manifest. Of the 22 candidate rows, 10 have any non-zero primary/fallback rows in the old snapshot; not a selected-ID join. |
| Current-source manifest | Generated 2026-10-08T04:32:49.356196+00:00; dates requested 20261001–20261010 | No fresh 50-ID refresh verified. |
| Historical match spine | Generated 2026-10-02T12:40:25.476309+00:00; 12836 admitted rows, window 2025-03-20–2026-09-20, 27 active leagues | Aggregate controlled spine; not joined to selected FootyStats IDs. |
| Prematch/team state | Historical prematch state 12836 rows; current team-state 12883 rows generated 2026-10-07T04:33:53.351088+00:00 | Aggregate row counts only; no selected-ID identity bridge verified. |
| Base controlled manifest | Built 2026-10-01T17:25:35.759116Z; 11364 match rows, 6012 goal-event rows, 2179 1UP truth rows | Separate artifact/window; not evidence of 50-league completeness. |
| FootyStats dataset-page acquisition | Generated 2026-10-01T17:25:59.043705+00:00; 0 rows retrieved, 0 new controlled rows, 8 recorded errors | The existing page-acquisition path failed to add data; errors include HTTP 403. This does not prove every FootyStats API endpoint is unavailable. |
| Sofascore acquisition | Generated 2026-10-01T17:26:15.368574+00:00; 0 rows retrieved, 14 errors | Existing source path yielded no new rows; errors include HTTP 403. |
| M-1UP event truth | 2179 matches across 5 leagues (Bundesliga, La Liga, Ligue 1, Premier League, Serie A), window 2025-03-27–2026-05-24 | Last event-truth date is 2026-05-24; stale for current use and not joined to selected provider IDs. M-1UP remains blocked for the 50-league target. |

## Workflow and execution status

- Latest private workflow: [Oracle Autonomous League Expansion #206](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40125710200) — **FAILURE** at 2026-10-24T19:31:48Z. Its `prepare` job failed, downstream jobs were skipped, and no artifacts were attached. A log retrieval attempt returned GitHub storage `BlobNotFound`, so the root cause is not verified. The preceding expansion runs #205 and #204 also failed.
- Latest visible public runs are [H2H Reporting #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720) and [H2H Exact-ID Join Tests #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716), both successful; these are H2H jobs, **not** the 50-league audit.
- No dedicated 50-league workflow run was found in the latest accessible public run listing for this checkpoint. The connected GitHub tool set has no workflow-dispatch operation, so this run could not safely trigger a new Actions workflow. No production workflow was modified.

## Market gates

The protected registry declares these four market families: M-1UP, BTTS Yes, Double Chance, and DC Under 4.5. For all 50 rows, the CSV marks readiness **NOT VERIFIED FOR SELECTED PROVIDER ID**. The old readiness matrix's BTTS/DC/COMBO labels are included only as stale canonical-code snapshots. M-1UP remains blocked by stale/incomplete event truth and missing selected-ID joins. Pre-match xG and odds point-in-time provenance remain unestablished.

## Next safe actions

1. Obtain a fresh provider response that includes exact selected FootyStats league ID, season ID, fixture ID, home/away team IDs, kickoff, and retrieval/source timestamps.
2. Persist sanitized request/response status per provider ID, including explicit 403/empty/error states; do not replace failures with name-based assumptions.
3. Join each selected provider ID to the exact fixture and canonical team IDs; review all candidate codes, and leave unresolved rows untouched until evidence is available.
4. Refresh the current fixture and team-state snapshots for the 50 target, then rebuild per-league recent-form/standings coverage and market-specific gates.
5. Resolve the readiness-matrix status conflicts and prove pre-kickoff xG/odds provenance before any prediction evaluation.

## Governance

Research only. No production model logic, weights, probabilities, thresholds, calibration, version, protected registry, or canonical ledger was changed. No draft PR was merged, no gate bypassed, and no paid provider change made. Completion is **not declared**.

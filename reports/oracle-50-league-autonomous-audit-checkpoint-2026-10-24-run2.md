# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 2, corrected)

- **Checkpoint date:** 2026-10-24 (SAST)
- **Research branch:** `research/oracle-50-league-readiness-audit`
- **Mode:** research-only; no production writes
- **Outcome:** **NOT COMPLETE** — exact selected-provider-ID joins and current readiness gates remain unverified.

## Work completed

1. Re-read the owner-approved 50-entry FootyStats manifest and recovery addendum.
2. Read the protected registry at `config/oracle_major_league_registry_v1.json` on private `oracle-football-data@main` (blob SHA `81d6db487e498fc84a87a7457b0de7215537f15c`), plus `config/data_config.json`, the separate `league_intelligence_matrix.csv`, and `data/league_readiness_matrix.csv`.
3. Inspected current-source, upcoming-fixture, historical-spine, prematch-state, current-team-state, FootyStats and Sofascore manifests, and the M-1UP event-truth manifest.
4. Produced a stricter 50-row crosswalk snapshot. A canonical candidate is only shown when the country and competition name match exactly after case/diacritic/punctuation normalization, or when an explicit country-scoped alias already exists in `scripts/build_oracle_competition_crosswalk.py`. Candidates still require human review; no candidate is an approved provider mapping.
5. Validated 50 rows, 50 unique provider IDs, all selected leagues retained, and zero verified selected-ID-to-API-fixture joins.

## Crosswalk result

| Measure | Result |
|---|---:|
| Owner-selected entries preserved | 50/50 |
| Exact country + competition-name candidates | 13 |
| Explicit country-scoped alias candidates | 9 |
| Unresolved against an exact/explicit-alias rule | 28 |
| Exact FootyStats ID → API fixture → canonical fixture/team joins verified | 0/50 |
| Selected-league market readiness passes verified | 0/50 |

The 22 canonical codes are candidates only. 28 rows remain unresolved. Four candidates in the previous snapshot were demoted under this stricter rule: Greece — Super League (prior GRC_G1); Romania — Liga I (prior ROU_R1); Serbia — SuperLiga (prior SRB_SR1); Switzerland — Super League (prior CHE_S1). The distinction is important: Greece (`GRC_G1`) and Serbia (`SRB_SR1`) are explicitly listed as excluded from the active universe and are not entries in the protected `leagues` array; Romania (`ROU_R1`) and Switzerland (`CHE_S1`) do have same-country registry entries, but the saved provider names `Liga I` and `Super League` have no exact-name match or explicit alias in the reviewed alias table. Those two remain unresolved until explicit mapping evidence/review exists.

## Existing evidence and limits

| Artifact | Persisted evidence | Limitation for the selected 50 |
|---|---|---|
| Protected registry | 27 entries; active-universe count 27; blob `81d6db487e498fc84a87a7457b0de7215537f15c` | This is the protected 27-entry registry, not a 50-provider-ID map. Registry readiness is not provider-ID join approval. |
| Separate league intelligence matrix | 22 candidate rows have separate research-code records, totalling 10305 fixture rows | These are separate research-code counts; none is joined to the selected FootyStats ID. |
| Canonical readiness matrix | 27 rows; last refresh shown as 2026-10-01T17:25:35.759116Z | Stale. 7 rows conflict as registry `NOT_INGESTED` vs matrix `PRODUCTION-READY`; 4 more are registry `NOT_INGESTED` vs matrix `PARTIAL`. 11 candidate rows say `PRODUCTION-READY` while the same snapshot shows zero fixture rows. These labels do not establish 50-league readiness. |
| Upcoming-fixture manifest | Generated 2026-10-08T04:30:39.615849+00:00; 27-league targets; window 2026-10-08–2026-10-22 | Stale as of 2026-10-24. 28 selected entries are not mapped to an existing target in this strict pass; 10 candidate rows have any non-zero primary/fallback rows in the old snapshot. None is an exact selected-ID join. |
| Current-source manifest | Generated 2026-10-08T04:32:49.356196+00:00; source dates 20261001–20261010 | No fresh 50-ID refresh verified. |
| Historical match spine | Generated 2026-10-02T12:40:25.476309+00:00; 12836 admitted rows, 2025-03-20–2026-09-20, 27 active leagues | Aggregate controlled spine, not a 50-league selected-ID join. |
| Prematch/team state | Historical prematch state 12836 rows; current team-state 12883 rows generated 2026-10-07T04:33:53.351088+00:00 | Aggregate counts only; no selected-ID team bridge verified. |
| Base controlled manifest | Built 2026-10-01T17:25:35.759116Z; 11364 match rows, 6012 goal-event rows, 2179 1UP truth rows | Separate artifact/window; not evidence of 50-league completeness. |
| FootyStats dataset-page acquisition | Generated 2026-10-01T17:25:59.043705+00:00; 0 rows retrieved, 0 new controlled rows, 8 errors | Existing page-acquisition path added no rows; errors include HTTP 403. This does not prove all FootyStats API endpoints are unavailable. |
| Sofascore acquisition | Generated 2026-10-01T17:26:15.368574+00:00; 0 rows retrieved, 14 errors | Existing source path yielded no new rows; errors include HTTP 403. |
| M-1UP event truth | 2179 matches across 5 leagues (Bundesliga, La Liga, Ligue 1, Premier League, Serie A), window 2025-03-27–2026-05-24 | Latest event-truth date 2026-05-24; stale and not joined to selected IDs. M-1UP remains blocked for the 50-league target. |

## Workflow / execution status

- Latest private workflow: [Oracle Autonomous League Expansion #206](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40125710200) failed at `prepare`; downstream jobs were skipped and no artifacts were attached. Fetching its job log returned GitHub storage `BlobNotFound`, so the root cause remains unverified. Runs #205 and #204 also failed.
- Latest visible public runs: [H2H Reporting #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720) and [H2H Exact-ID Join Tests #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716) succeeded, but they are H2H jobs, not 50-league audit runs.
- No dedicated 50-league run was found in the latest accessible public run listing. The connected GitHub tools expose no workflow-dispatch operation, so a new Actions run could not be triggered from this execution. No production workflow was modified.

## Market gates

The protected registry declares four supported market families: M-1UP, BTTS Yes, Double Chance, and DC Under 4.5. Every CSV row marks readiness as **not verified for the selected provider ID**. The old readiness matrix's BTTS/DC/COMBO values are included only as stale canonical-code snapshots. M-1UP is blocked by stale/incomplete event truth and missing selected-ID joins. Pre-match xG and odds provenance remain unestablished.

## Next safe actions

1. Obtain a fresh provider response containing exact selected FootyStats league ID, season ID, fixture ID, home/away team IDs, kickoff, and source/retrieval timestamps.
2. Persist sanitized request/response status per provider ID, including explicit 403/empty/error outcomes.
3. Join each provider ID to exact fixture and canonical team IDs; review candidates and leave unresolved rows untouched until evidence is available.
4. Refresh current fixtures/team state for the 50 target and rebuild per-league form, standings, and market gates.
5. Resolve registry/readiness-matrix status conflicts and verify point-in-time xG/odds provenance before evaluation.

## Governance

Research only. No production logic, weights, probabilities, thresholds, calibration, model version, protected registry, or canonical ledger was changed. No draft PR was merged, no gate bypassed, and no paid provider change made. Completion is **not declared**.

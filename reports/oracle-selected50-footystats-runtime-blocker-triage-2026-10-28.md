# Selected-50 FootyStats Runtime Blocker Triage — 2026-10-28

## Evidence inspected

- Existing FootyStats identity probe: 50/50 selected seasons returned HTTP 200; 1,744 fixture rows in the saved snapshot.
- Existing isolated research runtime artifact timestamp: 2026-10-28 06:52 UTC.
- Current seven-day FootyStats join output: 373 fixtures; 345 raw research outputs, 25 blocked for required-feature gaps, 3 with no runtime output.
- Runtime QA explicitly says production/betting eligibility NOT_GRANTED and combo probabilities masked.

## Root cause of the 25 missing-feature fixtures

This is not primarily a FotMob ID/crosswalk issue. The research runtime report names the missing feature fields. Across these fixtures, the absent fields are primarily the selected side's last-five team-state inputs:
- `home_gf5`, `home_ga5`, `home_btts5`, `home_fts5`, `home_cs5`, `home_shots5`, `home_sot5`, or the corresponding `away_*` fields.
- Pair-derived features `pair_btts_mean`, `pair_fts_mean`, `pair_cs_mean`, plus `score_environment`, `shot_environment`, and `score_gap5`.

Twenty-four of the 25 blocked rows show 35% input coverage (65% missing); one row, Troyes–Le Mans in Ligue 1, shows 0% coverage. The missing fields cluster around a team's recent history on the correct home/away side. This suggests a team-history join / historical-team-support gap or a team/competition label mismatch, not a blanket FootyStats season-ID failure. Do not fill these with zero, future data, league averages, or another provider's similarly named team without a validated join.

## Three fixtures without runtime output

The three rows are Universidad Católica–Audax Italiano (Chile, Primera División) and two Serbia SuperLiga fixtures: Radnički Kragujevac–Železničar Pančevo and Radnički Niš–Partizan. They appear in the current seven-day FootyStats window but not the prior runtime output. They require checking the runtime horizon, minimum lead time, source snapshot cutoff, selected-season coverage and join keys before classifying them as source failures. No probability should be synthesized for them.

## Priority fixes

1. Add an offline diagnostics script/report that groups missing features by fixture, team, league, historical row count and normalized team key; preserve strict pre-kickoff filtering.
2. For each missing side, compare exact provider team IDs and selected season against the historical training lake's team/league keys. Generate candidates only; do not auto-map from display names alone.
3. Determine whether each gap is (a) no historical matches, (b) wrong home/away split, (c) name/alias mismatch, or (d) feature generation bug. Fix only the demonstrated root cause.
4. Inspect the three no-runtime fixtures against the exact runtime report horizon and minimum lead-time gate.
5. Refresh the FootyStats snapshot and run the isolated research runtime again only after the runtime entrypoint is identified and the adapter integration is wired and tested.

## Governance

No production model logic, probabilities, thresholds, calibration, registries, or ledgers were changed. No blocked feature is imputed. The new FootyStats adapter is research-only and does not yet execute the existing Oracle runtime end-to-end. Production and betting release remain blocked pending the existing gates, including canonical identity, official settlement truth, point-in-time provenance, calibration and resolved combo settlement definition.

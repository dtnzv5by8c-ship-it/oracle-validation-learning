# Oracle 50-League FootyStats Catalogue Reconciliation — 2026-10-25

## Result

**The uploaded live catalogue resolves the immediate identifier ambiguity for all 50 selected entries.** The 50 numbers recovered from the saved FootyStats page match the nested `season_id` field in the live `league-list?chosen_leagues_only=true` catalogue—not a demonstrated parent-competition ID field.

- Catalogue status: `API_CATALOGUE_RETRIEVED`
- Distinct selected competition names: **50**
- Catalogue rows (competition-season entries): **766**
- Selected IDs matched to catalogue season IDs: **50/50**
- Selected ID/name disagreements: **0**
- Blank catalogue season IDs: **0**
- Duplicate season IDs in catalogue: **0**
- Production mappings approved by this check: **0**

The match was exact by numeric ID and the corresponding country/competition name from the recovered 50-entry manifest. Examples include Argentina Primera División, season 2026, ID 16571; England Premier League, season 2026/27, ID 17146; and South Africa Premier Soccer League, season 2026/27, ID 17444.

## What this establishes

1. The 50 selected numbers are valid **season identifiers** present in the live selected-league catalogue.
2. The previous catalogue-transfer assumption that read a parent competition ID from `league.get('id')` was not suitable evidence for these selected IDs. The reliable identifier for season-level ingestion is the nested `season[].id`.
3. The catalogue contains 766 season entries across the 50 selected competition names. This is catalogue coverage only; it does not prove that historical match data, current fixtures, standings, xG, odds, H2H, or each betting market are complete or production-ready.

## Required next steps — research only

1. Correct or replace the research-only catalogue generator to preserve both competition name and nested season ID explicitly. Do not relabel season IDs as parent competition IDs.
2. Join the 50 selected season IDs to historical archive records and fixture records using verified provider IDs, then separately verify canonical Oracle league/team/fixture identity.
3. Build the per-league and per-market readiness matrix using observed coverage, freshness, identity joins, and pre-match provenance.
4. Keep unresolved or stale inputs blocked. Do not infer xG/odds provenance from field presence alone.
5. Keep the production registry at its existing governed scope. This report does **not** authorize production changes or grant production eligibility.

## Evidence and limits

Source artifact supplied by the user: `footystats-selected-league-catalogue.zip`, containing `footystats-selected-leagues.csv` and `footystats-catalogue-summary.json`. The summary reports `chosen_leagues_only=true`, 50 unique league names, 766 league-season entries, and `secret_value_logged=false`.

This is a live catalogue reconciliation, not a historical-results audit. No paid ingestion workflow was run, no API key is reproduced here, and no production model logic, probabilities, thresholds, registry, or ledgers were changed.

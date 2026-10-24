# Oracle unmatched competition review — 2026-10-24

## Fresh catalogue run
- Workflow: [Oracle 44-League Research Catalogue Discovery](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038416001)
- Result: success
- Catalogue size: 1,737 provider competition entries
- Exact-alias candidates: 41 of 44 targets
- Fuzzy-only candidates: CRO, CO and EC
- Crosswalk structural validation: 0 errors; 19 warnings; mapping approval NOT GRANTED
- Source artifact: `oracle-44-league-broader-catalogue-discovery`

## Candidate review (not approved mappings)
- **CRO — Croatia HNL:** leading candidate is `Croatia Prva HNL` (similarity 0.8519), followed by `Croatia Druga HNL` (0.8286), with lower-tier Croatia competitions also returned. The presence of second-/third-tier candidates makes a fuzzy auto-map unsafe. Keep CRO parked pending independent identity confirmation.
- **CO — Colombia Primera A:** the discovery process returned fuzzy candidates only. Candidate rows include multiple Colombian competition names, but the current evidence does not establish the intended top-flight competition and season. Keep CO parked pending independent identity confirmation.
- **EC — Ecuador Serie A:** the discovery process returned fuzzy candidates only. Candidate rows include multiple Ecuadorian competition names, but the current evidence does not establish the intended top-flight competition and season. Keep EC parked pending independent identity confirmation.

## Important catalogue limitations
The latest crosswalk reports no provider season start/end dates for any candidate. Its `provider_league_id` field is blank in the artifact, so it cannot be used as an independently verified provider competition-ID mapping. Season IDs are listed, but season IDs alone do not prove competition identity or target-season alignment.

Therefore, the three unmatched targets are explicitly **PARKED_UNVERIFIED** for fixture ingestion. Do not fetch or merge them under fuzzy mappings without an independent identifier/source. The 41 exact-alias entries are still candidates, not independent proof of full-season completeness or prediction readiness.

## Next pipeline step
The full-season audit workflow has been updated to emit `oracle_44_league_readiness.csv` and `oracle_44_league_readiness_summary.json` with its sanitized audit artifact. The triggered run is in progress; its output must be checked before calling this integration complete.

## Governance
Research-only. No production model logic, weights, probabilities, thresholds, calibration, markets or governed 27-league registry changed. Odds validation remains parked. No prediction-readiness claims are made.


## User-supplied FootyStats display names — 2026-10-24
The user confirmed these exact display names from their selected-league screen. These are useful identity evidence and should be preferred over prior guessed aliases:
- Colombia target CO: `Colombia - Categoria Primera A` (provider display name likely `Colombia Categoria Primera A`); this is a stronger exact-name candidate for the intended top-flight than the earlier generic `Primera A` target label.
- Croatia target CRO: `Croatia - Prva HNL`; this appears to be the intended top-flight competition and should be added as an exact alias, subject to checking the current provider catalogue spelling.
- Ecuador target EC: `Ecuador - Primera Categoría Serie A`; add accent/diacritic-normalised exact alias variants, subject to checking the current provider catalogue spelling.
- Russia display name is `Russia - Russian Premier League`, consistent with the intended target.
- Ukraine display name is `Ukraine - Ukrainian Premier League`, consistent with the intended target.
- Portugal is shown as `Portugal - LigaPro`. Do **not** map this to the Oracle Portugal Primeira Liga target without verification: LigaPro may denote a different division than the intended top flight.
- User has now explicitly requested a research-catalogue scope change: exclude Qatar Stars League; include Saudi Arabia Professional League plus Spain Segunda División, Germany 2. Bundesliga, England EFL League One, Italy Serie B, and France Ligue 2. The research catalogue now has 50 target competitions. This is a research-only catalogue expansion and does not alter the protected production 27-league registry. These new competition identities and seasons still require validation against the live provider catalogue before ingestion; adding them to the research list does not certify data coverage or prediction readiness.
The current extraction run was already in progress when these names were supplied, so it cannot validate the new exact aliases. Apply the alias updates after that run completes, then run the lightweight catalogue discovery before any targeted match extraction.


## Research scope change — 2026-10-24
- Updated `scripts/oracle_44_catalogue_discovery.py` to expand the research catalogue from 44 to 50 competitions on branch `research/oracle-crosswalk-isolation-2026-10-22`.
- Added Saudi Arabia Professional League, Spain Segunda División, Germany 2. Bundesliga, England EFL League One, Italy Serie B, and France Ligue 2; Qatar is excluded.
- Added exact-name alias candidates for Croatia Prva HNL, Colombia Categoria Primera A, and Ecuador Primera Categoría Serie A. These aliases remain candidates until the next live catalogue output verifies exact matches.
- Portugal LigaPro remains unmapped to Primeira Liga pending independent identity confirmation.
- No production model logic or protected 27-league registry changed. Historical ingestion and prediction readiness remain blocked on validation/completeness gates.

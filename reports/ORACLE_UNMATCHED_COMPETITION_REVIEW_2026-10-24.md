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

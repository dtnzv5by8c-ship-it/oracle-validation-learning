# FootyStats catalogue run #4 — provider-led league configuration

**Retrieved:** 2026-11-04 14:34 UTC  
**Repository:** dtnzv5by8c-ship-it/oracle-validation-learning  
**Research branch base inspected:** 11c8dce37019a94486d6776d35279bf1226da004  
**Catalogue workflow run:** 41848820573 (main, commit c197c999eeb894adcb5eb1c01acaacf1baae2e13)  
**Artifact:** footystats-selected-league-catalogue (ID 13332511451)  
**Artifact SHA-256:** 6ae5ff7c575d5d7517d25600047d4e342454514ed996324c81685c1204a870fe

## Verified provider response

The approved `league-list?chosen_leagues_only=true` request completed successfully. The response contained:
- 49 unique provider league names;
- 756 league-season records;
- provider season IDs and season labels in the CSV;
- no API key in logs or artifacts.

The catalogue includes the following provider league names:

- Argentina Primera División
- Australia A-League
- Austria Bundesliga
- Belgium Pro League
- Brazil Serie A
- Bulgaria First League
- Canada Canadian Premier League
- Chile Primera División
- China Chinese Super League
- Colombia Categoria Primera A
- Croatia Prva HNL
- Czech Republic First League
- Denmark Superliga
- Ecuador Primera Categoría Serie A
- Egypt Egyptian Premier League
- England Championship
- England EFL League One
- England Premier League
- France Ligue 1
- France Ligue 2
- Germany 2. Bundesliga
- Germany Bundesliga
- Greece Super League
- Italy Serie A
- Italy Serie B
- Japan J1 League
- Mexico Liga MX
- Netherlands Eredivisie
- Norway Eliteserien
- Paraguay Division Profesional
- Peru Primera División
- Poland Ekstraklasa
- Portugal Liga NOS
- Portugal LigaPro
- Qatar Stars League
- Romania Liga I
- Saudi Arabia Professional League
- Scotland Premiership
- Serbia SuperLiga
- South Africa Premier Soccer League
- Spain La Liga
- Spain Segunda División
- Sweden Allsvenskan
- Switzerland Super League
- Turkey Süper Lig
- USA MLS
- Ukraine Ukrainian Premier League
- Uruguay Primera División
- Wales Welsh Premier League

## Configuration decision

FootyStats is the authoritative provider catalogue for the enabled FootyStats league-season universe. Oracle's provider configuration must be derived from the latest successful catalogue response, not constrained by the legacy fixed 50-row season manifest.

The returned season ID is the provider-native season key. It must not be relabelled as a permanent competition ID. Preserve the raw provider league name, season label, season ID, retrieval timestamp, source artifact digest and selection status. Any separate Oracle canonical label is an optional downstream bridge and must never override provider identity.

This run used `chosen_leagues_only=true`. It therefore proves the leagues currently selected/returned by the account, not the full universe FootyStats could offer. Qatar Stars League is present in the provider response and must remain in the provider catalogue even though it was not in the previous Oracle manifest. Slovenia PravLiga and Finland Veikkausliiga were not returned; their absence means they are not currently visible in this selected catalogue, not that FootyStats does not support them.

## Implementation requirements

1. Treat the provider catalogue as the source of truth for provider league and season membership.
2. Replace fixed-count assumptions in the research ingestion/configuration path with catalogue-driven iteration over unique provider season IDs.
3. Retain exact provider season IDs as the partition key for fixtures, results, team identities, H2H and form retrieval.
4. Build each market's feature availability from actual endpoint evidence per league-season. A league being listed does not imply every market field is populated.
5. Maintain explicit field-level coverage, source timestamps, pagination/completeness checks and fail-closed missing-data diagnostics.
6. Do not fuzzy-join provider IDs, infer season IDs from names, or silently drop leagues.
7. Keep Oracle V1.6 production logic, probabilities, thresholds, calibration and ledgers unchanged. New ingestion/configuration and market-readiness outputs remain research-only until independently validated and released.

## Credit and execution boundary

This run made exactly one catalogue API request. No fixture, match, team, H2H, standings, xG or historical endpoint was called. No bulk ingestion was run. Further authenticated provider calls must remain bounded and require an explicit request budget/approval before dispatch.

## Current state

Catalogue retrieval: PASS. Provider season catalogue: 49 leagues / 756 league-season records. Dynamic provider-led configuration: implementation required; not yet declared complete. Full market data readiness: not yet established.

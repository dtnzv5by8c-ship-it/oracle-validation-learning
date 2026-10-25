# Oracle Selected-50 Archive Reconciliation — 2026-10-25

## Decision

**31/50 exact selected season IDs are present in the Run 56 archive; 19/50 are absent.** This is an archive inventory result only. It is not a parent-competition join, a current fixture freshness check, or market readiness approval.

## Evidence examined

- Selected source: `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md` (50 unique selected IDs).
- Live schema diagnostic: [run #1](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40171490082), artifact `oracle-selected50-schema-diagnostic`. It found 50/50 IDs in nested season-level `id` fields and 0/50 in league-level ID fields.
- Historical archive: Run 56 artifact `12583524862`, mapping file `audit-output/extracted/private-package/league_season_mapping.csv` (126 season rows). Its `provider_league_id` field is blank in all 126 rows; `season_id` is populated.
- Archive integrity summary: 35,819 match rows, 35,819 feature rows, 126 season rows; no duplicate nonempty fixture IDs, no duplicate feature fixture IDs, no missing team IDs/names. The artifact explicitly says production readiness was not assessed.

## Exact season-ID matches present (31)

| Selected ID | Country | Selected competition | Archive label | Archive season rows | Rows with settled status allowed |
|---:|---|---|---|---:|---:|
| 16571 | Argentina | Primera División | Argentina Primera División | 495 | 450 |
| 17181 | Austria | Bundesliga | Austria Bundesliga | 132 | 54 |
| 17171 | Belgium | Pro League | Belgium Pro League | 306 | 72 |
| 16544 | Brazil | Serie A | Brazil Serie A | 380 | 309 |
| 17087 | Croatia | Prva HNL | Croatia Prva HNL | 180 | 49 |
| 17157 | Czech Republic | First League | Czech Republic First League | 240 | 87 |
| 17146 | England | Premier League | England Premier League | 380 | 70 |
| 17184 | England | Championship | England Championship | 552 | 132 |
| 17180 | England | EFL League One | England EFL League One | 552 | 125 |
| 17102 | France | Ligue 1 | France Ligue 1 | 306 | 63 |
| 17117 | France | Ligue 2 | France Ligue 2 | 306 | 81 |
| 17210 | Germany | Bundesliga | Germany Bundesliga | 306 | 54 |
| 17212 | Germany | 2. Bundesliga | Germany 2. Bundesliga | 306 | 72 |
| 17356 | Greece | Super League | Greece Super League | 182 | 48 |
| 17084 | Italy | Serie A | Italy Serie A | 380 | 70 |
| 17404 | Italy | Serie B | Italy Serie B | 380 | 70 |
| 17099 | Mexico | Liga MX | Mexico Liga MX | 153 | 109 |
| 17097 | Netherlands | Eredivisie | Netherlands Eredivisie | 306 | 81 |
| 16558 | Norway | Eliteserien | Norway Eliteserien | 240 | 184 |
| 17112 | Poland | Ekstraklasa | Poland Ekstraklasa | 306 | 97 |
| 17215 | Portugal | LigaPro | Portugal LigaPro | 306 | 63 |
| 17247 | Romania | Liga I | Romania Liga I | 240 | 96 |
| 17426 | Saudi Arabia | Professional League | Saudi Arabia Professional League | 306 | 85 |
| 17148 | Scotland | Premiership | Scotland Premiership | 198 | 54 |
| 17444 | South Africa | Premier Soccer League | South Africa Premier Soccer League | 240 | 65 |
| 17199 | Spain | La Liga | Spain La Liga | 380 | 88 |
| 17269 | Spain | Segunda División | Spain Segunda División | 462 | 110 |
| 17129 | Switzerland | Super League | Switzerland Super League | 132 | 60 |
| 17265 | Turkey | Süper Lig | Turkey Süper Lig | 306 | 72 |
| 16504 | USA | MLS | USA MLS | 510 | 450 |
| 17191 | Ukraine | Ukrainian Premier League | Ukraine Ukrainian Premier League | 240 | 68 |

The row counts above describe the matching season folder in the archived artifact; they are not the number of winning predictions. “Settled status allowed” is an archive status/eligibility field, not proof that all these rows have complete scores or are valid backtest selections.

## IDs absent from the 126-season archive mapping (19)

| Selected ID | Country | Selected competition |
|---:|---|---|
| 17326 | Australia | A-League |
| 16741 | Canada | Canadian Premier League |
| 16615 | Chile | Primera División |
| 16789 | China | Chinese Super League |
| 16614 | Colombia | Categoria Primera A |
| 17091 | Denmark | Superliga |
| 16714 | Ecuador | Primera Categoría Serie A |
| 16572 | Finland | Veikkausliiga |
| 17964 | India | Indian Super League |
| 17115 | Japan | J1 League |
| 16533 | Paraguay | Division Profesional |
| 16905 | Peru | Primera División |
| 16537 | Republic of Ireland | Premier Division |
| 17178 | Russia | Russian Premier League |
| 17119 | Serbia | SuperLiga |
| 16627 | South Korea | K League 1 |
| 16576 | Sweden | Allsvenskan |
| 16708 | Uruguay | Primera División |
| 16617 | Venezuela | Primera División |

“Absent” means no exact selected ID was found in the inspected archive mapping. It does not prove the provider has no historical data for that competition.

## Root cause and safe correction direction

1. The live schema diagnostic confirms selected IDs are **season IDs** (`season[].id`), not parent league IDs. No direct league-level ID field appeared in the inspected live catalogue response.
2. The archive transfer workflow currently writes `league.get('id')` into `provider_league_id`. That field is blank in the saved archive mapping. The expression does not match the observed league-object schema.
3. Do not fill `provider_league_id` with season IDs. Keep `provider_season_id` and `provider_competition_id` separate. Leave parent competition ID blank unless the provider explicitly supplies it.
4. The selected 19 missing IDs need a separate exact archive-coverage investigation. Do not substitute same-name seasons or fuzzy-map competitions.
5. Before editing the transfer workflow, inspect its consumers and the private target's expected schema. No workflow schema change, ingestion, API spend, canonical registry update, or production change is made by this report.

## Next actions

- Build a research-only catalogue reconciliation output with distinct season-ID and parent-competition-ID columns.
- Investigate the 19 absent season IDs against the saved ingestion manifest/error records and existing archive package; distinguish “not requested”, “request failed”, and “not present” only when direct evidence supports it.
- Add regression tests to prevent a season ID being written into a parent league ID column.
- Rerun research tests and exact-scope guard. Production eligibility remains **NOT GRANTED** until selected-ID-to-fixture/team joins, freshness, point-in-time xG/odds provenance, and per-market gates pass.

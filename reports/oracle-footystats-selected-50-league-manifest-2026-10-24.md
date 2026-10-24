# Project Oracle — FootyStats Selected League Manifest
Date recovered: 2026-10-24
Source: user-supplied saved browser page `Profile _ Football Stats API.mhtml`
Source page: `https://footystats.org/api/u/api-settings?area=3&status=1`
Verification method: parsed saved HTML checkbox inputs; 1,737 checkboxes were present and exactly 50 league checkboxes were checked.
Scope: research/registry reconciliation only. This is not a production registry update and does not imply data readiness.

| # | Provider league ID | Country | Provider competition name (as saved) |
|---:|---:|---|---|
| 1 | 16571 | Argentina | Primera División |
| 2 | 17326 | Australia | A-League |
| 3 | 17181 | Austria | Bundesliga |
| 4 | 17171 | Belgium | Pro League |
| 5 | 16544 | Brazil | Serie A |
| 6 | 16741 | Canada | Canadian Premier League |
| 7 | 16615 | Chile | Primera División |
| 8 | 16789 | China | Chinese Super League |
| 9 | 16614 | Colombia | Categoria Primera A |
| 10 | 17087 | Croatia | Prva HNL |
| 11 | 17157 | Czech Republic | First League |
| 12 | 17091 | Denmark | Superliga |
| 13 | 16714 | Ecuador | Primera Categoría Serie A |
| 14 | 17146 | England | Premier League |
| 15 | 17184 | England | Championship |
| 16 | 17180 | England | EFL League One |
| 17 | 16572 | Finland | Veikkausliiga |
| 18 | 17102 | France | Ligue 1 |
| 19 | 17117 | France | Ligue 2 |
| 20 | 17210 | Germany | Bundesliga |
| 21 | 17212 | Germany | 2. Bundesliga |
| 22 | 17356 | Greece | Super League |
| 23 | 17964 | India | Indian Super League |
| 24 | 17084 | Italy | Serie A |
| 25 | 17404 | Italy | Serie B |
| 26 | 17115 | Japan | J1 League |
| 27 | 17099 | Mexico | Liga MX |
| 28 | 17097 | Netherlands | Eredivisie |
| 29 | 16558 | Norway | Eliteserien |
| 30 | 16533 | Paraguay | Division Profesional |
| 31 | 16905 | Peru | Primera División |
| 32 | 17112 | Poland | Ekstraklasa |
| 33 | 17215 | Portugal | LigaPro |
| 34 | 16537 | Republic of Ireland | Premier Division |
| 35 | 17247 | Romania | Liga I |
| 36 | 17178 | Russia | Russian Premier League |
| 37 | 17426 | Saudi Arabia | Professional League |
| 38 | 17148 | Scotland | Premiership |
| 39 | 17119 | Serbia | SuperLiga |
| 40 | 17444 | South Africa | Premier Soccer League |
| 41 | 16627 | South Korea | K League 1 |
| 42 | 17199 | Spain | La Liga |
| 43 | 17269 | Spain | Segunda División |
| 44 | 16576 | Sweden | Allsvenskan |
| 45 | 17129 | Switzerland | Super League |
| 46 | 17265 | Turkey | Süper Lig |
| 47 | 16504 | USA | MLS |
| 48 | 17191 | Ukraine | Ukrainian Premier League |
| 49 | 16708 | Uruguay | Primera División |
| 50 | 16617 | Venezuela | Primera División |

## Reconciliation rules
1. Treat provider IDs as the primary identifiers for the selected FootyStats competitions.
2. Reconcile each provider ID/name to Oracle's canonical league code only after confirming the match against existing Oracle config and source data.
3. Preserve the user's exact 50-league scope even where data is absent; mark such leagues gated or missing rather than silently dropping them.
4. Do not add cups, infer substitute competitions, or map by fuzzy country/name matching alone.
5. Do not modify production model logic, production probabilities, canonical production registry, calibration, or promotion gates as part of this research manifest.
6. Next deliverable: a 50-row provider-to-canonical crosswalk with historical/current fixture coverage, team identity, recent form, standings, xG/odds provenance, and per-supported-market readiness. Mark unresolved mappings and missing evidence explicitly.

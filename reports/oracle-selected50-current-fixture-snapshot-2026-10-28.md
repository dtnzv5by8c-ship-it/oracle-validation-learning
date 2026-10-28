# Selected-50 Current Fixture Snapshot — 2026-10-28

## Result

**The bounded FootyStats fixture-schedule probe completed successfully: 50/50 requests returned HTTP 200 with provider success.** It made one sequential `league-matches` request per selected season, with no retries. Retrieval time: `2026-10-28T06:11:51.985177+00:00` UTC. The window covers 14 days before and after retrieval.

| Metric | Result |
|---|---:|
| Selected seasons queried | 50 |
| Successful requests | 50/50 |
| Seasons with fixtures in next 14 days | 50/50 |
| Upcoming fixture rows in window | 871 |
| Recent completed match rows in window | 871 |
| Seasons requiring additional pagination | 0 |
| Production/betting eligibility | NOT GRANTED |

**Source boundary:** This is a fresh FootyStats-native schedule snapshot. It does not refresh the FotMob `current_matches.csv` file and does not create a FotMob/Oracle canonical identity bridge. Match/team IDs remain FootyStats provider IDs.

## Per-season schedule coverage

| Country | Competition | FootyStats season ID | Observed master ID | HTTP | Matches returned | Future 14d | Recent completed 14d | Pages | Response state |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Argentina | Primera División | 16571 | 27 | 200 | 495 | 30 | 31 | 1 | ONE_PAGE_RESPONSE |
| Australia | A-League | 17326 | 34 | 200 | 156 | 12 | 11 | 1 | ONE_PAGE_RESPONSE |
| Austria | Bundesliga | 17181 | 40 | 200 | 132 | 12 | 12 | 1 | ONE_PAGE_RESPONSE |
| Belgium | Pro League | 17171 | 1 | 200 | 306 | 19 | 8 | 1 | ONE_PAGE_RESPONSE |
| Brazil | Serie A | 16544 | 64 | 200 | 380 | 20 | 20 | 1 | ONE_PAGE_RESPONSE |
| Canada | Canadian Premier League | 16741 | 524 | 200 | 116 | 4 | 8 | 1 | ONE_PAGE_RESPONSE |
| Chile | Primera División | 16615 | 72 | 200 | 240 | 17 | 8 | 1 | ONE_PAGE_RESPONSE |
| China | Chinese Super League | 16789 | 2 | 200 | 240 | 8 | 16 | 1 | ONE_PAGE_RESPONSE |
| Colombia | Categoria Primera A | 16614 | 76 | 200 | 394 | 25 | 28 | 1 | ONE_PAGE_RESPONSE |
| Croatia | Prva HNL | 17087 | 82 | 200 | 180 | 10 | 10 | 1 | ONE_PAGE_RESPONSE |
| Czech Republic | First League | 17157 | 88 | 200 | 240 | 17 | 15 | 1 | ONE_PAGE_RESPONSE |
| Denmark | Superliga | 17091 | 95 | 200 | 132 | 12 | 12 | 1 | ONE_PAGE_RESPONSE |
| Ecuador | Primera Categoría Serie A | 16714 | 99 | 200 | 312 | 16 | 16 | 1 | ONE_PAGE_RESPONSE |
| England | Premier League | 17146 | 9 | 200 | 380 | 20 | 20 | 1 | ONE_PAGE_RESPONSE |
| England | Championship | 17184 | 103 | 200 | 552 | 36 | 29 | 1 | ONE_PAGE_RESPONSE |
| England | EFL League One | 17180 | 6 | 200 | 552 | 15 | 41 | 1 | ONE_PAGE_RESPONSE |
| Finland | Veikkausliiga | 16572 | 125 | 200 | 177 | 9 | 9 | 1 | ONE_PAGE_RESPONSE |
| France | Ligue 1 | 17102 | 130 | 200 | 306 | 18 | 18 | 1 | ONE_PAGE_RESPONSE |
| France | Ligue 2 | 17117 | 132 | 200 | 306 | 18 | 18 | 1 | ONE_PAGE_RESPONSE |
| Germany | Bundesliga | 17210 | 143 | 200 | 306 | 18 | 18 | 1 | ONE_PAGE_RESPONSE |
| Germany | 2. Bundesliga | 17212 | 140 | 200 | 306 | 18 | 18 | 1 | ONE_PAGE_RESPONSE |
| Greece | Super League | 17356 | 152 | 200 | 182 | 14 | 13 | 1 | ONE_PAGE_RESPONSE |
| India | Indian Super League | 17964 | 169 | 200 | 78 | 11 | 12 | 1 | ONE_PAGE_RESPONSE |
| Italy | Serie A | 17084 | 193 | 200 | 380 | 27 | 23 | 1 | ONE_PAGE_RESPONSE |
| Italy | Serie B | 17404 | 194 | 200 | 380 | 23 | 27 | 1 | ONE_PAGE_RESPONSE |
| Japan | J1 League | 17115 | 198 | 200 | 380 | 20 | 30 | 1 | ONE_PAGE_RESPONSE |
| Mexico | Liga MX | 17099 | 225 | 200 | 153 | 19 | 27 | 1 | ONE_PAGE_RESPONSE |
| Netherlands | Eredivisie | 17097 | 234 | 200 | 306 | 18 | 18 | 1 | ONE_PAGE_RESPONSE |
| Norway | Eliteserien | 16558 | 247 | 200 | 240 | 16 | 16 | 1 | ONE_PAGE_RESPONSE |
| Paraguay | Division Profesional | 16533 | 444 | 200 | 264 | 16 | 8 | 1 | ONE_PAGE_RESPONSE |
| Peru | Primera División | 16905 | 253 | 200 | 306 | 26 | 19 | 1 | ONE_PAGE_RESPONSE |
| Poland | Ekstraklasa | 17112 | 259 | 200 | 306 | 18 | 18 | 1 | ONE_PAGE_RESPONSE |
| Portugal | LigaPro | 17215 | 5 | 200 | 306 | 18 | 9 | 1 | ONE_PAGE_RESPONSE |
| Republic of Ireland | Premier Division | 16537 | 264 | 200 | 180 | 5 | 12 | 1 | ONE_PAGE_RESPONSE |
| Romania | Liga I | 17247 | 265 | 200 | 240 | 16 | 16 | 1 | ONE_PAGE_RESPONSE |
| Russia | Russian Premier League | 17178 | 268 | 200 | 240 | 16 | 16 | 1 | ONE_PAGE_RESPONSE |
| Saudi Arabia | Professional League | 17426 | 272 | 200 | 306 | 18 | 24 | 1 | ONE_PAGE_RESPONSE |
| Scotland | Premiership | 17148 | 278 | 200 | 198 | 16 | 12 | 1 | ONE_PAGE_RESPONSE |
| Serbia | SuperLiga | 17119 | 283 | 200 | 182 | 16 | 14 | 1 | ONE_PAGE_RESPONSE |
| South Africa | Premier Soccer League | 17444 | 290 | 200 | 240 | 15 | 4 | 1 | ONE_PAGE_RESPONSE |
| South Korea | K League 1 | 16627 | 294 | 200 | 228 | 12 | 12 | 1 | ONE_PAGE_RESPONSE |
| Spain | La Liga | 17199 | 3 | 200 | 380 | 20 | 21 | 1 | ONE_PAGE_RESPONSE |
| Spain | Segunda División | 17269 | 299 | 200 | 462 | 22 | 22 | 1 | ONE_PAGE_RESPONSE |
| Sweden | Allsvenskan | 16576 | 303 | 200 | 240 | 23 | 17 | 1 | ONE_PAGE_RESPONSE |
| Switzerland | Super League | 17129 | 312 | 200 | 132 | 12 | 6 | 1 | ONE_PAGE_RESPONSE |
| Turkey | Süper Lig | 17265 | 8 | 200 | 306 | 18 | 18 | 1 | ONE_PAGE_RESPONSE |
| USA | MLS | 16504 | 334 | 200 | 510 | 44 | 46 | 1 | ONE_PAGE_RESPONSE |
| Ukraine | Ukrainian Premier League | 17191 | 328 | 200 | 240 | 16 | 16 | 1 | ONE_PAGE_RESPONSE |
| Uruguay | Primera División | 16708 | 331 | 200 | 281 | 8 | 16 | 1 | ONE_PAGE_RESPONSE |
| Venezuela | Primera División | 16617 | 339 | 200 | 231 | 14 | 13 | 1 | ONE_PAGE_RESPONSE |

## Execution evidence

- [FootyStats probe workflow run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790) — attempt 5.
- Sanitized schedule artifact: [artifact 12796425175](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796425175).
- API documentation: [League Matches](https://footystats.org/api/documentations/match-schedule-and-stats) documents the season-specific fixture endpoint and match fields; [League Season](https://footystats.org/api/documentations/league-season-stats-teams) documents season metadata.
- The artifact contains filtered fixtures in the 28-day window and per-season request metadata, not raw full provider payloads or the API key.

## Identity reconciliation finding

The separate 50-request `league-season` probe succeeded for all selected seasons: 50/50 returned IDs, countries and competition names matched the manifest; 50/50 returned a non-null `comp_master_id`, and all 50 observed values were distinct. These provider master IDs are now appended to the research crosswalk with response status and run provenance.

The public FootyStats API overview lists `comp_master_id` among its league data fields ([official documentation](https://footystats.org/api)), but the accessible field list does not precisely define how it maps to Oracle canonical competition codes or FotMob league IDs. Therefore all values remain labelled `REVIEW_REQUIRED_NOT_CANONICAL`.

## Remaining release blockers

1. **FotMob current-feed freshness:** the checked-in production `data/current_source_manifest.json` is generated on 6 October and covers through 8 October. This new FootyStats snapshot is a different source and cannot be presented as a refresh of that file.
2. **Cross-provider identity:** 0/50 approved FootyStats-to-FotMob bridges; do not infer from names or use provider master IDs as FotMob IDs.
3. **Fixture/team joins:** canonical fixture/team identity and kickoff reconciliation remain unverified.
4. **Settlement:** official score/status provenance and the Combo predictor/settlement disagreement remain unresolved. Combo probabilities stay masked.
5. **Production release:** no production registry, ledger, model logic or probabilities were changed. Production and betting eligibility remain NO-GO.

## Next actions

- Use the fresh provider-native snapshot to build a research-only fixture candidate list keyed by selected season ID and provider master ID.
- Confirm `comp_master_id` semantics from authoritative provider documentation/support.
- Locate a permitted current-feed staging snapshot and its manifest; do not reactivate the unsafe name-only FotMob ingestion path.
- Reconcile fixture/team IDs and official settlement truth before final release assessment.

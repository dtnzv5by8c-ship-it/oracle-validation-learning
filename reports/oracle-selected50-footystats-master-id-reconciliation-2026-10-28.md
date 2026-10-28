# Selected-50 FootyStats Identity Reconciliation — 2026-10-28

## Executive result

**Bounded provider probe: PASS (50/50 HTTP 200 provider-success responses).** The probe made exactly one `league-season` request for each of the 50 selected season IDs, sequentially, with no retries. The sanitized output was captured in GitHub Actions run [40562430790, attempt 4](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790).

| Check | Result |
|---|---:|
| Selected seasons requested | 50 |
| Successful HTTP 200 responses | 50/50 |
| Returned season IDs matching requested IDs | 50/50 |
| Country and competition-name checks matching the manifest | 50/50 |
| Responses containing provider field `comp_master_id` | 50/50 |
| Distinct observed `comp_master_id` values | 50 |
| Country mismatches | 0 |
| Retries | 0 |

The user confirmed FootyStats capacity of 1,800 requests/hour and explicitly authorized bounded use. This run used 50 requests, approximately 2.8% of that hourly ceiling. The hourly ceiling is not a confirmation of remaining monthly credits; no credit dashboard was accessed.

## Critical interpretation

The response exposes two distinct identifiers: `id` (the requested season ID) and `comp_master_id` (a provider-supplied field). For all 50 records, the requested season ID matched the returned `id`, and the returned country/name aligned with the selected manifest row. All 50 had a non-null, distinct `comp_master_id`.

The official FootyStats API overview lists `comp_master_id` among its league data fields ([official API documentation](https://footystats.org/api)); the public field listing available to this audit does not provide a precise definition sufficient to equate it with an Oracle canonical ID. Therefore the 50 values are now **provider master-ID evidence**, not yet approved canonical mappings. They must not be copied into the protected Oracle registry or used to promote production eligibility until the provider's identifier semantics and crosswalk are confirmed.

## Sanitized 50-row evidence

| Country | Selected competition | FootyStats season ID | Observed `comp_master_id` | Season | ISO | HTTP | Assessment |
|---|---|---:|---:|---|---|---:|---|
| Argentina | Primera División | 16571 | 27 | 2026 | ar | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Australia | A-League | 17326 | 34 | 2026/2027 | au | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Austria | Bundesliga | 17181 | 40 | 2026/2027 | at | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Belgium | Pro League | 17171 | 1 | 2026/2027 | be | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Brazil | Serie A | 16544 | 64 | 2026 | br | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Canada | Canadian Premier League | 16741 | 524 | 2026 | ca | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Chile | Primera División | 16615 | 72 | 2026 | cl | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| China | Chinese Super League | 16789 | 2 | 2026 | cn | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Colombia | Categoria Primera A | 16614 | 76 | 2026 | co | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Croatia | Prva HNL | 17087 | 82 | 2026/2027 | hr | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Czech Republic | First League | 17157 | 88 | 2026/2027 | cz | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Denmark | Superliga | 17091 | 95 | 2026/2027 | dk | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Ecuador | Primera Categoría Serie A | 16714 | 99 | 2026 | ec | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| England | Premier League | 17146 | 9 | 2026/2027 | gb-eng | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| England | Championship | 17184 | 103 | 2026/2027 | gb-eng | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| England | EFL League One | 17180 | 6 | 2026/2027 | gb-eng | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Finland | Veikkausliiga | 16572 | 125 | 2026 | fi | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| France | Ligue 1 | 17102 | 130 | 2026/2027 | fr | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| France | Ligue 2 | 17117 | 132 | 2026/2027 | fr | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Germany | Bundesliga | 17210 | 143 | 2026/2027 | de | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Germany | 2. Bundesliga | 17212 | 140 | 2026/2027 | de | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Greece | Super League | 17356 | 152 | 2026/2027 | gr | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| India | Indian Super League | 17964 | 169 | 2026/2027 | in | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Italy | Serie A | 17084 | 193 | 2026/2027 | it | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Italy | Serie B | 17404 | 194 | 2026/2027 | it | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Japan | J1 League | 17115 | 198 | 2026/2027 | jp | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Mexico | Liga MX | 17099 | 225 | 2026/2027 | mx | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Netherlands | Eredivisie | 17097 | 234 | 2026/2027 | nl | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Norway | Eliteserien | 16558 | 247 | 2026 | no | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Paraguay | Division Profesional | 16533 | 444 | 2026 | py | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Peru | Primera División | 16905 | 253 | 2026 | pe | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Poland | Ekstraklasa | 17112 | 259 | 2026/2027 | pl | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Portugal | LigaPro | 17215 | 5 | 2026/2027 | pt | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Republic of Ireland | Premier Division | 16537 | 264 | 2026 | ie | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Romania | Liga I | 17247 | 265 | 2026/2027 | ro | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Russia | Russian Premier League | 17178 | 268 | 2026/2027 | ru | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Saudi Arabia | Professional League | 17426 | 272 | 2026/2027 | sa | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Scotland | Premiership | 17148 | 278 | 2026/2027 | gb-sct | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Serbia | SuperLiga | 17119 | 283 | 2026/2027 | rs | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| South Africa | Premier Soccer League | 17444 | 290 | 2026/2027 | za | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| South Korea | K League 1 | 16627 | 294 | 2026 | kr | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Spain | La Liga | 17199 | 3 | 2026/2027 | es | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Spain | Segunda División | 17269 | 299 | 2026/2027 | es | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Sweden | Allsvenskan | 16576 | 303 | 2026 | se | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Switzerland | Super League | 17129 | 312 | 2026/2027 | ch | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Turkey | Süper Lig | 17265 | 8 | 2026/2027 | tr | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| USA | MLS | 16504 | 334 | 2026 | us | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Ukraine | Ukrainian Premier League | 17191 | 328 | 2026/2027 | ua | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Uruguay | Primera División | 16708 | 331 | 2026 | uy | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |
| Venezuela | Primera División | 16617 | 339 | 2026 | ve | 200 | SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW |

## What this resolves

- Confirms all 50 selected IDs are recognized by the FootyStats `league-season` endpoint at the time of the probe.
- Establishes one observed provider `comp_master_id` for each selected season; values are distinct across this 50-row sample.
- Adds the observed master IDs, HTTP result, match assessment and run provenance to the existing research identity reconciliation CSV.
- Enables the next exact crosswalk step without guessing from display names or season IDs.

## What remains unresolved

1. **Provider master-ID semantics:** obtain a precise definition from provider documentation/support before treating `comp_master_id` as a parent competition ID or canonical key.
2. **FotMob/current-feed bridge:** the 50 FootyStats master IDs do not establish the corresponding FotMob league IDs. The approved FootyStats-to-FotMob bridge remains 0/50.
3. **Current-feed freshness:** the accessible production manifest remains generated on 6 October and no newer authoritative current-feed manifest/run was found in the audited evidence.
4. **Fixture/team identity and settlement:** exact canonical fixture/team joins and official settlement truth are still not verified; Combo probabilities remain masked.
5. **Production governance:** no IDs are promoted to the protected canonical registry. Production/betting eligibility remains NOT GRANTED.

## Next actions

1. Request/locate authoritative documentation for the `comp_master_id` field semantics.
2. Use these 50 observed IDs as a research-only identity bridge candidate, not a canonical approval.
3. Find a permitted current-feed staging snapshot and its run manifest; do not reactivate the unsafe name-only ingestion path.
4. Build exact FotMob ID + country/category evidence for each selected competition, quarantine unknown/ambiguous IDs, and then reconcile exact fixtures, teams and settlement outcomes.
5. Publish the final 50-league readiness matrix with archive coverage, provider identity, current-feed freshness, market support and release eligibility as separate gates.

## Governance

This was a bounded provider lookup and sanitized research-only update. No raw provider payload or API key was retained in the report. No production repository code, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers or governance were changed.

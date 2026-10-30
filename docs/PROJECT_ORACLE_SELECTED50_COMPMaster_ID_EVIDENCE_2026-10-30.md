# Selected-50 FootyStats `comp_master_id` Evidence Register
**Probe:** Identity probe #3, workflow run `41064739646`  
**Artifact:** `12982202358`  
**Artifact SHA-256:** `76f6c8bc1dbe54d7204c33abac0a0dfd124aadcc79c0bea5265af939fb33799e`  
**Probe date:** 30 October 2026, 13:37:36 UTC  
**Classification:** Provider identity evidence only; no canonical approval.

## Probe outcome
- Requests: 50 planned / 50 attempted.
- HTTP 200: 50/50.
- Exact selected season ID match: 50/50.
- Country/name match: 50/50; country mismatches: 0.
- `comp_master_id` returned: 50/50.
- Unique returned `comp_master_id` values: 50.
- API key persisted: no; raw provider payload persisted: no; production ledger writes: no.
- Every row's assessment remains `SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW`.

## Exact observed season-to-provider-parent-field pairs
| Selected FootyStats season ID | Returned `comp_master_id` | Country | Competition |
|---:|---:|---|---|
| 16504 | 334 | USA | MLS |
| 16533 | 444 | Paraguay | Division Profesional |
| 16537 | 264 | Republic of Ireland | Premier Division |
| 16544 | 64 | Brazil | Serie A |
| 16558 | 247 | Norway | Eliteserien |
| 16571 | 27 | Argentina | Primera División |
| 16572 | 125 | Finland | Veikkausliiga |
| 16576 | 303 | Sweden | Allsvenskan |
| 16614 | 76 | Colombia | Categoria Primera A |
| 16615 | 72 | Chile | Primera División |
| 16617 | 339 | Venezuela | Primera División |
| 16627 | 294 | South Korea | K League 1 |
| 16708 | 331 | Uruguay | Primera División |
| 16714 | 99 | Ecuador | Primera Categoría Serie A |
| 16741 | 524 | Canada | Canadian Premier League |
| 16789 | 2 | China | Chinese Super League |
| 16905 | 253 | Peru | Primera División |
| 17084 | 193 | Italy | Serie A |
| 17087 | 82 | Croatia | Prva HNL |
| 17091 | 95 | Denmark | Superliga |
| 17097 | 234 | Netherlands | Eredivisie |
| 17099 | 225 | Mexico | Liga MX |
| 17102 | 130 | France | Ligue 1 |
| 17112 | 259 | Poland | Ekstraklasa |
| 17115 | 198 | Japan | J1 League |
| 17117 | 132 | France | Ligue 2 |
| 17119 | 283 | Serbia | SuperLiga |
| 17129 | 312 | Switzerland | Super League |
| 17146 | 9 | England | Premier League |
| 17148 | 278 | Scotland | Premiership |
| 17157 | 88 | Czech Republic | First League |
| 17171 | 1 | Belgium | Pro League |
| 17178 | 268 | Russia | Russian Premier League |
| 17180 | 6 | England | EFL League One |
| 17181 | 40 | Austria | Bundesliga |
| 17184 | 103 | England | Championship |
| 17191 | 328 | Ukraine | Ukrainian Premier League |
| 17199 | 3 | Spain | La Liga |
| 17210 | 143 | Germany | Bundesliga |
| 17212 | 140 | Germany | 2. Bundesliga |
| 17215 | 5 | Portugal | LigaPro |
| 17247 | 265 | Romania | Liga I |
| 17265 | 8 | Turkey | Süper Lig |
| 17269 | 299 | Spain | Segunda División |
| 17326 | 34 | Australia | A-League |
| 17356 | 152 | Greece | Super League |
| 17404 | 194 | Italy | Serie B |
| 17426 | 272 | Saudi Arabia | Professional League |
| 17444 | 290 | South Africa | Premier Soccer League |
| 17964 | 169 | India | Indian Super League |

## Interpretation and release controls
The `league-season` response exposes both the selected season `id` and a separate `comp_master_id` field. The provider's public API variable catalogue lists `comp_master_id` among league data points, but the material reviewed does not define its referential semantics, stability guarantees or whether it is the competition key used by all other endpoints. Therefore:
- Preserve these values as exact provider-returned parent-field candidates.
- Do not substitute them into Oracle's canonical competition registry.
- Do not alter the existing 22 candidate / 28 unresolved canonical crosswalk classifications.
- Require provider confirmation or a documented endpoint contract plus a second independent exact endpoint reconciliation before promoting the field's semantics.
- This does not establish canonical team/fixture identity, settlement truth, or market eligibility.

## Next verification
1. Obtain provider documentation or written confirmation defining `comp_master_id`, its lifecycle/stability and relationship to season `id`.
2. Verify that each returned value is stable across at least one additional season of the same competition without relying on name-only joins.
3. Reconcile with the Oracle canonical competition registry using an explicit approved crosswalk; retain human review for ambiguous or unmapped rows.
4. Keep all production and betting eligibility flags false until the independent identity and settlement gates pass.

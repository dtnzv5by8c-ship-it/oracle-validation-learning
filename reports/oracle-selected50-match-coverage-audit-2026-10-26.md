# Selected-50 FootyStats Match-Coverage Audit — 2026-10-26

## Verified run

- Workflow: [40391540391 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40391540391)
- Branch: `research/oracle-50-league-readiness-audit`
- Workflow/code commit used for the audit: `af143fcd42f3f320027e67dbd0f7d5184b85f938`
- Sanitized artifact: [12684045977](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40391540391#artifacts)
- Artifact ZIP SHA-256: `47392a7986e43d35bc9ada442e157d52fa945b51175d7f1e632bd03c34e67f6e`
- API requests: 50, hard cap 50, no retries; all 50 responses returned HTTP 200 and provider `success=true`.
- Last provider request-window metadata observed: 1,750 remaining. **Monthly credit/billing balance was not exposed or verified**; do not interpret the request-window value as monthly credit proof.
- Raw provider payloads and API keys were not saved in the artifact. No production code/probabilities were changed.

## Aggregate result

| Measure | Observed result |
|---|---:|
| Selected leagues queried | 50/50 |
| Match rows returned on page 1 | 14,051 |
| Unique fixture IDs within the queried league pages | 14,051 |
| Duplicate fixture-ID rows within a queried league page | 0 |
| Leagues with provider pager max_page = 1 | 50/50 |
| Rows with a status field | 14,051/14,051 |
| Rows with both provider team IDs | 14,051/14,051 |
| Rows with both score fields present | 14,051/14,051 |
| Rows with Unix kickoff field | 14,051/14,051 |
| Provider status `complete` | 7,040 |
| Provider status `incomplete` | 6,958 |
| Provider status `suspended` | 53 |
| Match-record rows with a non-empty `season_id` field | 0 |
| Match-record `competition_id` matches the selected ID | 50/50 groups |

Observed Unix kickoff range: **2026-01-16 23:20:00 UTC to 2027-06-06 00:00:00 UTC**.

### Important interpretation limits

- The query used the provider's `league-matches` endpoint with the selected ID as the `season_id` parameter and `max_per_page=1000`. The response rows exposed `competition_id` and `season`; no non-empty `season_id` values were observed. Therefore, equality between the selected ID and `competition_id` is an observed provider-field relationship, **not proof of parent-competition semantics or an Oracle canonical ID bridge**.
- All pages reported `pager.max_page=1`; this establishes that this endpoint response was not paginated beyond page 1 for this query. It does not establish complete historical coverage across the 2025-03-20–2026-09-20 primary modeling window or across every season.
- The fact that a score field exists is not proof the score is final. Incomplete and suspended rows can contain placeholder/partial scores; no row from this audit is admitted as official settlement truth on this evidence alone.
- Unique provider fixture IDs within each selected group do not prove canonical fixture joins or that IDs are globally unique across all provider competitions.
- Odds and xG fields are not approved for modeling until their point-in-time provenance, semantics and exact fixture joins are verified.

## League-by-league first-page coverage

Counts below describe provider rows returned by this bounded query. Status labels are preserved exactly; no status is converted to a settlement outcome. Duplicate counts are within each returned page.

| Country | Provider competition | Selected ID | Rows | Complete | Incomplete | Suspended | Unique fixture IDs | Duplicate rows | Pager max page |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Argentina | Primera División | 16571 | 495 | 462 | 33 | 0 | 495 | 0 | 1 |
| Australia | A-League | 17326 | 156 | 11 | 145 | 0 | 156 | 0 | 1 |
| Austria | Bundesliga | 17181 | 132 | 60 | 72 | 0 | 132 | 0 | 1 |
| Belgium | Pro League | 17171 | 306 | 80 | 225 | 1 | 306 | 0 | 1 |
| Brazil | Serie A | 16544 | 380 | 317 | 62 | 1 | 380 | 0 | 1 |
| Canada | Canadian Premier League | 16741 | 112 | 112 | 0 | 0 | 112 | 0 | 1 |
| Chile | Primera División | 16615 | 240 | 197 | 42 | 1 | 240 | 0 | 1 |
| China | Chinese Super League | 16789 | 240 | 232 | 8 | 0 | 240 | 0 | 1 |
| Colombia | Categoria Primera A | 16614 | 394 | 355 | 32 | 7 | 394 | 0 | 1 |
| Croatia | Prva HNL | 17087 | 180 | 52 | 127 | 1 | 180 | 0 | 1 |
| Czech Republic | First League | 17157 | 240 | 94 | 144 | 2 | 240 | 0 | 1 |
| Denmark | Superliga | 17091 | 132 | 71 | 61 | 0 | 132 | 0 | 1 |
| Ecuador | Primera Categoría Serie A | 16714 | 312 | 270 | 41 | 1 | 312 | 0 | 1 |
| England | Premier League | 17146 | 380 | 80 | 299 | 1 | 380 | 0 | 1 |
| England | Championship | 17184 | 552 | 144 | 408 | 0 | 552 | 0 | 1 |
| England | EFL League One | 17180 | 552 | 138 | 407 | 7 | 552 | 0 | 1 |
| Finland | Veikkausliiga | 16572 | 177 | 168 | 9 | 0 | 177 | 0 | 1 |
| France | Ligue 1 | 17102 | 306 | 71 | 235 | 0 | 306 | 0 | 1 |
| France | Ligue 2 | 17117 | 306 | 88 | 218 | 0 | 306 | 0 | 1 |
| Germany | Bundesliga | 17210 | 306 | 63 | 243 | 0 | 306 | 0 | 1 |
| Germany | 2. Bundesliga | 17212 | 306 | 81 | 225 | 0 | 306 | 0 | 1 |
| Greece | Super League | 17356 | 182 | 55 | 126 | 1 | 182 | 0 | 1 |
| India | Indian Super League | 17964 | 78 | 16 | 62 | 0 | 78 | 0 | 1 |
| Italy | Serie A | 17084 | 380 | 80 | 300 | 0 | 380 | 0 | 1 |
| Italy | Serie B | 17404 | 380 | 80 | 300 | 0 | 380 | 0 | 1 |
| Japan | J1 League | 17115 | 380 | 120 | 238 | 22 | 380 | 0 | 1 |
| Mexico | Liga MX | 17099 | 153 | 124 | 29 | 0 | 153 | 0 | 1 |
| Netherlands | Eredivisie | 17097 | 306 | 90 | 216 | 0 | 306 | 0 | 1 |
| Norway | Eliteserien | 16558 | 240 | 192 | 48 | 0 | 240 | 0 | 1 |
| Paraguay | Division Profesional | 16533 | 264 | 222 | 42 | 0 | 264 | 0 | 1 |
| Peru | Primera División | 16905 | 306 | 270 | 36 | 0 | 306 | 0 | 1 |
| Poland | Ekstraklasa | 17112 | 306 | 106 | 198 | 2 | 306 | 0 | 1 |
| Portugal | LigaPro | 17215 | 306 | 71 | 235 | 0 | 306 | 0 | 1 |
| Republic of Ireland | Premier Division | 16537 | 180 | 175 | 5 | 0 | 180 | 0 | 1 |
| Romania | Liga I | 17247 | 240 | 103 | 137 | 0 | 240 | 0 | 1 |
| Russia | Russian Premier League | 17178 | 240 | 96 | 144 | 0 | 240 | 0 | 1 |
| Saudi Arabia | Professional League | 17426 | 306 | 94 | 211 | 1 | 306 | 0 | 1 |
| Scotland | Premiership | 17148 | 198 | 60 | 137 | 1 | 198 | 0 | 1 |
| Serbia | SuperLiga | 17119 | 182 | 89 | 91 | 2 | 182 | 0 | 1 |
| South Africa | Premier Soccer League | 17444 | 240 | 65 | 175 | 0 | 240 | 0 | 1 |
| South Korea | K League 1 | 16627 | 198 | 198 | 0 | 0 | 198 | 0 | 1 |
| Spain | La Liga | 17199 | 380 | 98 | 282 | 0 | 380 | 0 | 1 |
| Spain | Segunda División | 17269 | 462 | 120 | 342 | 0 | 462 | 0 | 1 |
| Sweden | Allsvenskan | 16576 | 240 | 200 | 40 | 0 | 240 | 0 | 1 |
| Switzerland | Super League | 17129 | 132 | 66 | 66 | 0 | 132 | 0 | 1 |
| Turkey | Süper Lig | 17265 | 306 | 78 | 228 | 0 | 306 | 0 | 1 |
| USA | MLS | 16504 | 510 | 466 | 44 | 0 | 510 | 0 | 1 |
| Ukraine | Ukrainian Premier League | 17191 | 240 | 76 | 162 | 2 | 240 | 0 | 1 |
| Uruguay | Primera División | 16708 | 281 | 273 | 8 | 0 | 281 | 0 | 1 |
| Venezuela | Primera División | 16617 | 231 | 211 | 20 | 0 | 231 | 0 | 1 |

## Executive disposition

The audit materially improves provider-layer coverage evidence and identifies no duplicate fixture IDs or pagination truncation in these 50 first pages. It does **not** close the canonical identity or settlement gates. The 50 provider `competition_id` values match their selected IDs, but the response schema does not establish that these are authoritative parent IDs for Oracle's canonical registry. Keep all rows quarantined from production/betting use until authoritative provider-to-canonical league, fixture and team bridges and official settlement truth are evidenced. Combo remains blocked by its unresolved predictor-versus-ledger definition mismatch.

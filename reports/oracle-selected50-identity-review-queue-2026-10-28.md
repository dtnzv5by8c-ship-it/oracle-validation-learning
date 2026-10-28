# Selected-50 Identity Review Queue — 2026-10-28

## New evidence available

The bounded FootyStats identity probe returned HTTP 200 for all 50 selected seasons, matched the requested season ID/country/name in 50/50 cases, and returned 50 distinct `comp_master_id` values. These values are appended to the candidate crosswalk. They are provider-side identity evidence only; they are not approved Oracle canonical IDs or FotMob IDs.

## Review workload

| Queue | Count | Handling |
|---|---:|---|
| Candidate matches to current 27-league registry | 22 | Human review of canonical candidate, country, competition semantics and provider master ID |
| No match in current 27-league registry | 28 | Requires a supported new canonical identity proposal or explicit out-of-scope disposition; do not force-map |
| Total selected seasons | 50 | Every row has observed FootyStats `comp_master_id` and successful response status |
| Approved canonical bridges | 0 | No automatic promotion |

## Full review queue

| Country | Selected competition | FootyStats season ID | Provider master ID observed | Canonical candidate | Candidate name | Current match state | Registry readiness |
|---|---|---:|---:|---|---|---|---|
| Argentina | Primera División | 16571 | 27 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Australia | A-League | 17326 | 34 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Austria | Bundesliga | 17181 | 40 | AUT_A1 | Austrian Bundesliga | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Belgium | Pro League | 17171 | 1 | BEL_B1 | Belgian Pro League | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| Brazil | Serie A | 16544 | 64 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Canada | Canadian Premier League | 16741 | 524 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Chile | Primera División | 16615 | 72 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| China | Chinese Super League | 16789 | 2 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Colombia | Categoria Primera A | 16614 | 76 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Croatia | Prva HNL | 17087 | 82 | HRV_HR1 | Croatian HNL | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Czech Republic | First League | 17157 | 88 | CZE_CZ1 | Czech First League | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Denmark | Superliga | 17091 | 95 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Ecuador | Primera Categoría Serie A | 16714 | 99 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| England | Premier League | 17146 | 9 | ENG_E0 | Premier League | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| England | Championship | 17184 | 103 | ENG_E1 | Championship | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| England | EFL League One | 17180 | 6 | ENG_E2 | League One | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| Finland | Veikkausliiga | 16572 | 125 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| France | Ligue 1 | 17102 | 130 | FRA_F1 | Ligue 1 | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| France | Ligue 2 | 17117 | 132 | FRA_F2 | Ligue 2 | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Germany | Bundesliga | 17210 | 143 | DEU_D1 | Bundesliga | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| Germany | 2. Bundesliga | 17212 | 140 | DEU_D2 | 2. Bundesliga | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Greece | Super League | 17356 | 152 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| India | Indian Super League | 17964 | 169 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Italy | Serie A | 17084 | 193 | ITA_I1 | Serie A | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| Italy | Serie B | 17404 | 194 | ITA_I2 | Serie B | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Japan | J1 League | 17115 | 198 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Mexico | Liga MX | 17099 | 225 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Netherlands | Eredivisie | 17097 | 234 | NLD_N1 | Eredivisie | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| Norway | Eliteserien | 16558 | 247 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Paraguay | Division Profesional | 16533 | 444 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Peru | Primera División | 16905 | 253 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Poland | Ekstraklasa | 17112 | 259 | POL_P1 | Ekstraklasa | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Portugal | LigaPro | 17215 | 5 | PRT_P2 | Liga Portugal 2 | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Republic of Ireland | Premier Division | 16537 | 264 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Romania | Liga I | 17247 | 265 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Russia | Russian Premier League | 17178 | 268 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Saudi Arabia | Professional League | 17426 | 272 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Scotland | Premiership | 17148 | 278 | SCO_SC0 | Scottish Premiership | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| Serbia | SuperLiga | 17119 | 283 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| South Africa | Premier Soccer League | 17444 | 290 | ZAF_PSL | South African PSL | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| South Korea | K League 1 | 16627 | 294 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Spain | La Liga | 17199 | 3 | ESP_SP1 | La Liga | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| Spain | Segunda División | 17269 | 299 | ESP_SP2 | Segunda División | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Sweden | Allsvenskan | 16576 | 303 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Switzerland | Super League | 17129 | 312 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Turkey | Süper Lig | 17265 | 8 | TUR_T1 | Turkish Super Lig | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | CONTROLLED |
| USA | MLS | 16504 | 334 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Ukraine | Ukrainian Premier League | 17191 | 328 | UKR_UA1 | Ukrainian Premier League | CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW | NOT_INGESTED |
| Uruguay | Primera División | 16708 | 331 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |
| Venezuela | Primera División | 16617 | 339 | — | — | NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY | — |

## Newly prioritized exact-overlap evidence

Eight exact fixture joins now support two strong bridge candidates:
- Canada CPL: FootyStats season 16741 / master ID 524 ↔ FotMob league ID 1000001192; four joins, one score/status conflict.
- England EFL League One: season 17180 / master ID 6 ↔ FotMob league ID 938219; four joins, no score/status conflicts, three postponed matches.

Both remain human-review candidates. The Canadian conflict shows that stale source records cannot be treated as settlement truth. Full evidence: [overlap join audit](oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md).

## Approval checklist for each row

1. Confirm the FootyStats `comp_master_id` field semantics with authoritative documentation or written provider confirmation.
2. Verify that the candidate competition code refers to the same competition and gender/competition type, not merely a similar display name.
3. Verify the corresponding FotMob league ID and country/category independently; FootyStats IDs cannot be used as FotMob IDs.
4. Record reviewer, evidence source, decision timestamp and reason.
5. Keep rejected, unknown, ambiguous or non-equivalent candidates quarantined.
6. Do not update the protected canonical registry or production model configuration from this research queue.

## Release disposition

- FootyStats provider identity: observed for 50/50 selected seasons.
- Provider master ID semantics: pending authoritative confirmation.
- FootyStats-to-FotMob bridges: 0/50 approved.
- Fixture/team canonical joins: not verified.
- Production/betting eligibility: NO-GO.

Source crosswalk: [Selected-50 canonical candidate crosswalk](oracle-selected50-canonical-candidate-crosswalk-2026-10-27.csv).

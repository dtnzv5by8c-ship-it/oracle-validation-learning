# Oracle Selected-50 Identity Review Queue — 2026-10-27

**Branch:** `research/oracle-50-league-readiness-audit`  
**Source:** candidate crosswalk CSV (read-only input), generated from schema diagnostic run `40548721202`.  
**Purpose:** organize human review; this is not an approval record or a production change.

## Gate summary

- Selected provider season IDs: **50**
- Current-registry candidate matches requiring human review: **22**
- No match in the current 27-league registry: **28**
- Verified provider parent competition IDs: **0**
- Approved mappings / production eligibility: **0 / NOT_GRANTED**

## Review rules

1. Confirm country and competition identity, including division/tier, before marking any candidate approved.
2. Keep provider season IDs in the season-ID field only. Do not populate parent competition IDs from the season ID, display name, or season year.
3. A candidate may only be approved after the identity evidence is recorded and a human reviewer explicitly signs off.
4. Rows with no current registry match remain research-only expansion candidates. Do not create canonical IDs in this pass.
5. Do not change the protected production registry, model logic, probabilities, calibration, thresholds, or prediction gates.

## Queue A — Candidate matches against existing registry (22)

| Provider season ID | Country | Provider catalogue name | Season | Candidate canonical ID | Canonical competition | Current registry status | Review action |
|---:|---|---|---|---|---|---|---|
| 17181 | Austria | Austria Bundesliga | 20262027 | AUT_A1 | Austrian Bundesliga | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17171 | Belgium | Belgium Pro League | 20262027 | BEL_B1 | Belgian Pro League | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17087 | Croatia | Croatia Prva HNL | 20262027 | HRV_HR1 | Croatian HNL | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17157 | Czech Republic | Czech Republic First League | 20262027 | CZE_CZ1 | Czech First League | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17146 | England | England Premier League | 20262027 | ENG_E0 | Premier League | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17184 | England | England Championship | 20262027 | ENG_E1 | Championship | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17180 | England | England EFL League One | 20262027 | ENG_E2 | League One | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17102 | France | France Ligue 1 | 20262027 | FRA_F1 | Ligue 1 | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17117 | France | France Ligue 2 | 20262027 | FRA_F2 | Ligue 2 | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17210 | Germany | Germany Bundesliga | 20262027 | DEU_D1 | Bundesliga | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17212 | Germany | Germany 2. Bundesliga | 20262027 | DEU_D2 | 2. Bundesliga | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17084 | Italy | Italy Serie A | 20262027 | ITA_I1 | Serie A | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17404 | Italy | Italy Serie B | 20262027 | ITA_I2 | Serie B | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17097 | Netherlands | Netherlands Eredivisie | 20262027 | NLD_N1 | Eredivisie | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17112 | Poland | Poland Ekstraklasa | 20262027 | POL_P1 | Ekstraklasa | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17215 | Portugal | Portugal LigaPro | 20262027 | PRT_P2 | Liga Portugal 2 | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17148 | Scotland | Scotland Premiership | 20262027 | SCO_SC0 | Scottish Premiership | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17444 | South Africa | South Africa Premier Soccer League | 20262027 | ZAF_PSL | South African PSL | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17199 | Spain | Spain La Liga | 20262027 | ESP_SP1 | La Liga | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17269 | Spain | Spain Segunda División | 20262027 | ESP_SP2 | Segunda División | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17265 | Turkey | Turkey Süper Lig | 20262027 | TUR_T1 | Turkish Super Lig | CONTROLLED | Confirm same competition and correct tier; verify stable parent ID separately |
| 17191 | Ukraine | Ukraine Ukrainian Premier League | 20262027 | UKR_UA1 | Ukrainian Premier League | NOT_INGESTED | Confirm same competition and correct tier; verify stable parent ID separately |

## Queue B — No match in current 27-league registry (28)

| Provider season ID | Country | Provider catalogue name | Season | Candidate canonical ID | Canonical competition | Current registry status | Review action |
|---:|---|---|---|---|---|---|---|
| 16571 | Argentina | Argentina Primera División | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17326 | Australia | Australia A-League | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16544 | Brazil | Brazil Serie A | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16741 | Canada | Canada Canadian Premier League | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16615 | Chile | Chile Primera División | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16789 | China | China Chinese Super League | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16614 | Colombia | Colombia Categoria Primera A | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17091 | Denmark | Denmark Superliga | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16714 | Ecuador | Ecuador Primera Categoría Serie A | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16572 | Finland | Finland Veikkausliiga | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17356 | Greece | Greece Super League | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17964 | India | India Indian Super League | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17115 | Japan | Japan J1 League | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17099 | Mexico | Mexico Liga MX | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16558 | Norway | Norway Eliteserien | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16533 | Paraguay | Paraguay Division Profesional | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16905 | Peru | Peru Primera División | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16537 | Republic of Ireland | Republic of Ireland Premier Division | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17247 | Romania | Romania Liga I | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17178 | Russia | Russia Russian Premier League | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17426 | Saudi Arabia | Saudi Arabia Professional League | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17119 | Serbia | Serbia SuperLiga | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16627 | South Korea | South Korea K League 1 | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16576 | Sweden | Sweden Allsvenskan | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 17129 | Switzerland | Switzerland Super League | 20262027 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16504 | USA | USA MLS | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16708 | Uruguay | Uruguay Primera División | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |
| 16617 | Venezuela | Venezuela Primera División | 2026 |  |  |  | Research-only expansion candidate; do not assign canonical ID |

## Required evidence before identity closure

- Provider evidence that explicitly links the selected season ID to a stable competition/parent ID, or written provider clarification that the season ID is the only supported identifier.
- Canonical registry evidence for any proposed existing mapping; expansion proposals need a separate governed research review.
- Reviewer, review date, evidence URL/artifact, and disposition for every row.
- After competition identity is settled, separately validate team IDs, fixture IDs, kickoff/schedule freshness, match status and final-score settlement evidence.

## Executive disposition

**Identity reconciliation remains OPEN.** This queue makes the human-review workload explicit but does not promote any mapping. Production and betting eligibility remain **NOT_GRANTED**. No provider API calls were made to generate this queue; no production files were changed.

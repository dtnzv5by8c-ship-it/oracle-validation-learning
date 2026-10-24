# Project Oracle — 50-League Crosswalk Evidence Addendum

- Date: 2026-10-25 (SAST)
- Scope: research-only reconciliation of the recovered 50 selected FootyStats competitions against the live private canonical registry and its existing readiness matrix.
- Production status: unchanged; no registry/model/ledger writes.

## Important interpretation

This pass accessed the live private repository successfully and inspected `config/oracle_major_league_registry_v1.json`, `data/league_readiness_matrix.csv`, and `data/oracle_four_model_readiness_v1.2.json`. The canonical registry contains 27 active-universe entries and the readiness matrix is dated 2026-10-01. That matrix provides useful evidence for a subset of selected competitions, but it is dated and its league names are not the same thing as provider-ID proof. Therefore the table below records **candidate canonical codes only**, never approved mappings. A selected FootyStats provider ID must still be checked against provider/archive metadata before final acceptance.

## Candidate crosswalk and available canonical-matrix evidence

| Country | Selected FootyStats competition | Provider ID | Candidate Oracle code | Canonical readiness | Matrix status | Historical results rows | Current fixtures | Historical window | BTTS / DC / Combo / M1UP |
|---|---|---:|---|---|---|---:|---:|---|---|
| Australia | A-League | 17326 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Argentina | Primera División | 16571 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Austria | Bundesliga | 17181 | AUT_A1 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Belgium | Pro League | 17171 | BEL_B1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Brazil | Serie A | 16544 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Canada | Canadian Premier League | 16741 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Chile | Primera División | 16615 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| China | Chinese Super League | 16789 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Colombia | Categoria Primera A | 16614 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Croatia | Prva HNL | 17087 | HRV_HR1 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Czech Republic | First League | 17157 | CZE_CZ1 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Denmark | Superliga | 17091 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Ecuador | Primera Categoría Serie A | 16714 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| England | Premier League | 17146 | ENG_E0 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| England | Championship | 17184 | ENG_E1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| England | EFL League One | 17180 | ENG_E2 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Finland | Veikkausliiga | 16572 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| France | Ligue 1 | 17102 | FRA_F1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| France | Ligue 2 | 17117 | FRA_F2 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Germany | Bundesliga | 17210 | DEU_D1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Germany | 2. Bundesliga | 17212 | DEU_D2 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Greece | Super League | 17356 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| India | Indian Super League | 17964 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Italy | Serie A | 17084 | ITA_I1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Italy | Serie B | 17404 | ITA_I2 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Japan | J1 League | 17115 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Mexico | Liga MX | 17099 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Netherlands | Eredivisie | 17097 | NLD_N1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Norway | Eliteserien | 16558 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Paraguay | Division Profesional | 16533 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Peru | Primera División | 16905 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Poland | Ekstraklasa | 17112 | POL_P1 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Portugal | LigaPro | 17215 | PRT_P2 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Republic of Ireland | Premier Division | 16537 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Romania | Liga I | 17247 | ROU_R1 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Russia | Russian Premier League | 17178 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Saudi Arabia | Professional League | 17426 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Scotland | Premiership | 17148 | SCO_SC0 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Serbia | SuperLiga | 17119 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| South Africa | Premier Soccer League | 17444 | ZAF_PSL | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| South Korea | K League 1 | 16627 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Spain | La Liga | 17199 | ESP_SP1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Spain | Segunda División | 17269 | ESP_SP2 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Sweden | Allsvenskan | 16576 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Switzerland | Super League | 17129 | CHE_S1 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Turkey | Süper Lig | 17265 | TUR_T1 | CONTROLLED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| USA | MLS | 16504 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Ukraine | Ukrainian Premier League | 17191 | UKR_UA1 | NOT_INGESTED | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Uruguay | Primera División | 16708 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |
| Venezuela | Primera División | 16617 | UNRESOLVED | N/A | NO_CANONICAL_MATRIX_ROW | N/A | N/A | N/A | NOT ASSESSED |

## Evidence summary

- Owner-selected competitions: 50.
- Candidate canonical codes surfaced by exact country + competition relation against the registry: 24.
- Remaining entries: 26 UNRESOLVED against the current 27-league canonical registry.
- Candidate codes are **not approvals**; exact FootyStats provider ID to archive/canonical competition linkage remains a required validation step.
- The registry's 27 active league count is preserved. This research audit does not expand or modify production scope.
- Existing readiness JSON (effective 2026-10-01) reports 11,364 controlled rows, 27 leagues present, historical data max date 2026-09-20, 22 leagues with full BTTS/DC/combo controlled paths and 5 partial current-season leagues (CRO, NED2, POR2, RSA, UKR). M1UP is event-truth-gated and controlled event truth was reported for 5 leagues only. These are existing aggregate registry metrics, not evidence of readiness for all 50 selected competitions.

## Main gaps that remain

1. **Provider ID join:** the selected FootyStats IDs need exact linkage to provider archive folder/season metadata. Competition-name similarity alone is not enough for final approval.
2. **Current data:** the readiness matrix is dated 2026-10-01 and has a maximum controlled match date of 2026-09-20; it does not establish live current-fixture freshness on 2026-10-25.
3. **50-league coverage:** 23 selected competitions are not represented as distinct entries in the 27-row canonical registry by this candidate mapping pass; they remain unresolved, not silently excluded.
4. **Feature provenance:** recent form and standings must be computed strictly before kickoff; xG/odds field presence is not sufficient without timestamped pre-match snapshots.
5. **Market readiness:** existing market status applies only to current canonical registry entries and existing controlled data. It cannot be copied to unresolved leagues or treated as proof of 50-league production readiness.
6. **Model performance:** production prediction accuracy remains unverified until immutable pre-kickoff predictions are joined to exact, independently verified fixture/market settlements.

## Source evidence

- Canonical registry: `config/oracle_major_league_registry_v1.json` in private repository `oracle-football-data` (main, blob SHA `81d6db487e498fc84a87a7457b0de7215537f15c`).
- Existing readiness matrix: `data/league_readiness_matrix.csv` (main, blob SHA `602061ebe0bbecdd3c11876307cebe45b0ed2ffd`; last refresh shown as 2026-10-01).
- Readiness summary: `data/oracle_four_model_readiness_v1.2.json` (main, blob SHA `d91b6359187c646571022d99a14754485959201c`; effective date 2026-10-01).
- Selected provider IDs: [owner-selected FootyStats manifest](oracle-footystats-selected-50-league-manifest-2026-10-24.md).

## Governance

Research only. Candidate mappings require evidence and review. No production logic, probabilities, thresholds, calibration, model version, canonical registry, or canonical ledgers were changed. No paid provider change or workflow gate bypass was made.

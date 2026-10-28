# Oracle 50-League Identity, Settlement Truth and Provenance Audit — 2026-10-28

**Scope:** research-only audit on the live branch; no provider API calls.  
**Audit input head:** [`9566103e8d1ad4cf9d2e4cb56f70de1e57167043`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9566103e8d1ad4cf9d2e4cb56f70de1e57167043)  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** identity candidate inventory reconciled; settlement placeholder exclusion regression coverage added; production and betting release remain **BLOCKED**.

## 1. Executive decision

- Selected manifest: **50 rows / 50 unique season IDs**.
- Candidate canonical correspondences against the current 27-league registry: **22**, all requiring human review.
- No unique current-registry match: **28**, all retained as research-only expansion candidates.
- Parent competition IDs verified: **0/50**; provider-to-canonical bridges verified: **0/50**.
- Human-approved mappings: **0**; production/betting eligibility: **NOT_GRANTED**.
- Existing archive evidence accounts for all 50 selected groups across two distinct evidence layers: 31 Run 56 manifest matches and 19 retained private-package QA gap reconciliations. This is inventory evidence, not canonical identity.
- Existing archive QA records **59,049** historical rows: 51,983 marked complete and 7,066 non-complete records, every one of the latter carrying a numeric 0–0 pair. Non-complete 0–0 rows must remain excluded from settled truth.
- Production registry (27 leagues), Oracle V1.6/V1.6.3 logic, probabilities, thresholds, calibration, ledgers and governance remain unchanged.

## 2. Live GitHub state and exact evidence links

- Audit input head: [commit 9566103e8d1ad4cf9d2e4cb56f70de1e57167043](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9566103e8d1ad4cf9d2e4cb56f70de1e57167043).
- Prior live-state checkpoint: [commit 9566103e8d1ad4cf9d2e4cb56f70de1e57167043](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9566103e8d1ad4cf9d2e4cb56f70de1e57167043).
- Approved one-call identity probe: [workflow run 40562430790 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790); sanitized artifact [12760832880](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12760832880), SHA-256 `54b25732953cae74b59963613e4c2948c643612dc86dafa11b038a58ffdb7015`.
- Existing archive status/score QA: [run 40423922693](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693), artifact [12698682583](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693/artifacts/12698682583).
- Existing selected-50 research runtime: [run 40554064150](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150), artifact [12757295232](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232).
- Existing latest Run 120 research runtime audit: [run 40608511893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893), artifact [12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212), SHA-256 `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`.
- Most recent observed safety-contract tests: [run 40620012826 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012826).
- Most recent observed dry-run planner: [run 40620012759 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012759). It is a no-provider-call planner run, not evidence of production readiness.

The probe result is recorded in [the sanitized result report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-footystats-one-call-identity-probe-result-2026-10-27.md). It returned `data.id=16571`, Argentina, Primera División, season 2026; this establishes only the sampled season record. **Do not repeat the request.**

## 3. Official FootyStats documentation — identifier semantics

1. [League List](https://footystats.org/api/documentations/league-list): says each season of a competition has a unique ID; the named fields are `season.id` and `season.year`.
2. [League Stats / Get Season Stats and Teams](https://footystats.org/api/documentations/league-season-stats-teams): the query parameter is `season_id`; its field description calls `id` the season ID. The published example has an apparent mismatch (`season_id=2012` versus sample `data.id="161"` and season `2017/2018`).
3. [League Matches](https://footystats.org/api/documentations/match-schedule-and-stats): `season_id` is described as the league-season ID; the match-level `competition_id` field is also described as the **season ID of the league**. That field name must not be interpreted as proof of a stable parent competition ID.
4. [API Overview / support route](https://footystats.org/api/documentations): explicitly invites API questions and requests at **admin@footystats.org**.

**Conclusion:** public docs support season-scoped interpretation and show a `competition_id` naming ambiguity, but do not establish a distinct, stable parent competition identifier or provider-to-Oracle canonical bridge. The one approved sample does not change that conclusion. No further provider API request is authorized without fresh explicit approval and a verified credit budget.

## 4. Full 50-row identity candidate audit

Inputs: [selected 50-season manifest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/data/oracle-footystats-selected-50-season-id-manifest.csv), [canonical candidate crosswalk](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-canonical-candidate-crosswalk-2026-10-27.csv), and [independent identity evidence register](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-independent-identity-evidence-register-2026-10-27.csv).

Provider catalogue labels below come from the previously retained sanitized catalogue/schema audit; only ID `16571` has the separately approved one-call season-record sample. Candidate codes are drawn from the existing country-constrained, explicit alias crosswalk. Official FootyStats docs establish field semantics, **not** each individual country/name/code mapping. Every candidate remains unapproved. No fuzzy matching, generic country-prefix stripping, or season-ID-as-parent-ID inference is used.

| Season ID | Manifest country | Manifest competition | Provider catalogue label / season | Candidate canonical code/name | Research-only grouping alias | Existing archive evidence | Identity evidence | Disposition |
|---:|---|---|---|---|---|---|---|---|
| 16571 | Argentina | Primera División | Argentina Primera División (2026) | — (no current-27 candidate) | R50_ARG_PRIMERA_DIVISION | Run 56 exact manifest; 495 rows | one-call season record only | UNMATCHED — RESEARCH ONLY |
| 17326 | Australia | A-League | Australia A-League (20262027) | — (no current-27 candidate) | R50_AUS_A_LEAGUE | retained QA; 156 rows; primary-window 0 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17181 | Austria | Bundesliga | Austria Bundesliga (20262027) | AUT_A1 — Austrian Bundesliga | R50_AUT_BUNDESLIGA | Run 56 exact manifest; 132 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17171 | Belgium | Pro League | Belgium Pro League (20262027) | BEL_B1 — Belgian Pro League | R50_BEL_PRO_LEAGUE | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16544 | Brazil | Serie A | Brazil Serie A (2026) | — (no current-27 candidate) | R50_BRA_SERIE_A | Run 56 exact manifest; 380 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16741 | Canada | Canadian Premier League | Canada Canadian Premier League (2026) | — (no current-27 candidate) | R50_CAN_CANADIAN_PREMIER_LEAGUE | retained QA; 112 rows; primary-window 89 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16615 | Chile | Primera División | Chile Primera División (2026) | — (no current-27 candidate) | R50_CHL_PRIMERA_DIVISION | retained QA; 240 rows; primary-window 183 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16789 | China | Chinese Super League | China Chinese Super League (2026) | — (no current-27 candidate) | R50_CHN_CHINESE_SUPER_LEAGUE | retained QA; 240 rows; primary-window 208 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16614 | Colombia | Categoria Primera A | Colombia Categoria Primera A (2026) | — (no current-27 candidate) | R50_COL_CATEGORIA_PRIMERA_A | retained QA; 394 rows; primary-window 296 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17087 | Croatia | Prva HNL | Croatia Prva HNL (20262027) | HRV_HR1 — Croatian HNL | R50_HRV_PRVA_HNL | Run 56 exact manifest; 180 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17157 | Czech Republic | First League | Czech Republic First League (20262027) | CZE_CZ1 — Czech First League | R50_CZE_FIRST_LEAGUE | Run 56 exact manifest; 240 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17091 | Denmark | Superliga | Denmark Superliga (20262027) | — (no current-27 candidate) | R50_DNK_SUPERLIGA | retained QA; 132 rows; primary-window 54 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16714 | Ecuador | Primera Categoría Serie A | Ecuador Primera Categoría Serie A (2026) | — (no current-27 candidate) | R50_ECU_PRIMERA_CATEGORIA_SERIE_A | retained QA; 312 rows; primary-window 246 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17146 | England | Premier League | England Premier League (20262027) | ENG_E0 — Premier League | R50_ENG_PREMIER_LEAGUE | Run 56 exact manifest; 380 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17184 | England | Championship | England Championship (20262027) | ENG_E1 — Championship | R50_ENG_CHAMPIONSHIP | Run 56 exact manifest; 552 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17180 | England | EFL League One | England EFL League One (20262027) | ENG_E2 — League One | R50_ENG_EFL_LEAGUE_ONE | Run 56 exact manifest; 552 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16572 | Finland | Veikkausliiga | Finland Veikkausliiga (2026) | — (no current-27 candidate) | R50_FIN_VEIKKAUSLIIGA | retained QA; 177 rows; primary-window 150 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17102 | France | Ligue 1 | France Ligue 1 (20262027) | FRA_F1 — Ligue 1 | R50_FRA_LIGUE_1 | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17117 | France | Ligue 2 | France Ligue 2 (20262027) | FRA_F2 — Ligue 2 | R50_FRA_LIGUE_2 | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17210 | Germany | Bundesliga | Germany Bundesliga (20262027) | DEU_D1 — Bundesliga | R50_DEU_BUNDESLIGA | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17212 | Germany | 2. Bundesliga | Germany 2. Bundesliga (20262027) | DEU_D2 — 2. Bundesliga | R50_DEU_2_BUNDESLIGA | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17356 | Greece | Super League | Greece Super League (20262027) | — (no current-27 candidate) | R50_GRC_SUPER_LEAGUE | Run 56 exact manifest; 182 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17964 | India | Indian Super League | India Indian Super League (20262027) | — (no current-27 candidate) | R50_IND_INDIAN_SUPER_LEAGUE | retained QA; 78 rows; primary-window 0 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17084 | Italy | Serie A | Italy Serie A (20262027) | ITA_I1 — Serie A | R50_ITA_SERIE_A | Run 56 exact manifest; 380 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17404 | Italy | Serie B | Italy Serie B (20262027) | ITA_I2 — Serie B | R50_ITA_SERIE_B | Run 56 exact manifest; 380 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17115 | Japan | J1 League | Japan J1 League (20262027) | — (no current-27 candidate) | R50_JPN_J1_LEAGUE | retained QA; 380 rows; primary-window 80 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17099 | Mexico | Liga MX | Mexico Liga MX (20262027) | — (no current-27 candidate) | R50_MEX_LIGA_MX | Run 56 exact manifest; 153 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17097 | Netherlands | Eredivisie | Netherlands Eredivisie (20262027) | NLD_N1 — Eredivisie | R50_NLD_EREDIVISIE | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16558 | Norway | Eliteserien | Norway Eliteserien (2026) | — (no current-27 candidate) | R50_NOR_ELITESERIEN | Run 56 exact manifest; 240 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16533 | Paraguay | Division Profesional | Paraguay Division Profesional (2026) | — (no current-27 candidate) | R50_PRY_DIVISION_PROFESIONAL | retained QA; 264 rows; primary-window 198 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16905 | Peru | Primera División | Peru Primera División (2026) | — (no current-27 candidate) | R50_PER_PRIMERA_DIVISION | retained QA; 306 rows; primary-window 241 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17112 | Poland | Ekstraklasa | Poland Ekstraklasa (20262027) | POL_P1 — Ekstraklasa | R50_POL_EKSTRAKLASA | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17215 | Portugal | LigaPro | Portugal LigaPro (20262027) | PRT_P2 — Liga Portugal 2 | R50_PRT_LIGAPRO | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16537 | Republic of Ireland | Premier Division | Republic of Ireland Premier Division (2026) | — (no current-27 candidate) | R50_IRL_PREMIER_DIVISION | retained QA; 180 rows; primary-window 158 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17247 | Romania | Liga I | Romania Liga I (20262027) | — (no current-27 candidate) | R50_ROU_LIGA_I | Run 56 exact manifest; 240 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17178 | Russia | Russian Premier League | Russia Russian Premier League (20262027) | — (no current-27 candidate) | R50_RUS_RUSSIAN_PREMIER_LEAGUE | retained QA; 240 rows; primary-window 72 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17426 | Saudi Arabia | Professional League | Saudi Arabia Professional League (20262027) | — (no current-27 candidate) | R50_SAU_PROFESSIONAL_LEAGUE | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17148 | Scotland | Premiership | Scotland Premiership (20262027) | SCO_SC0 — Scottish Premiership | R50_SCO_PREMIERSHIP | Run 56 exact manifest; 198 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17119 | Serbia | SuperLiga | Serbia SuperLiga (20262027) | — (no current-27 candidate) | R50_SRB_SUPERLIGA | retained QA; 182 rows; primary-window 68 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17444 | South Africa | Premier Soccer League | South Africa Premier Soccer League (20262027) | ZAF_PSL — South African PSL | R50_ZAF_PREMIER_SOCCER_LEAGUE | Run 56 exact manifest; 240 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16627 | South Korea | K League 1 | South Korea K League 1 (2026) | — (no current-27 candidate) | R50_KOR_K_LEAGUE_1 | retained QA; 198 rows; primary-window 179 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17199 | Spain | La Liga | Spain La Liga (20262027) | ESP_SP1 — La Liga | R50_ESP_LA_LIGA | Run 56 exact manifest; 380 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 17269 | Spain | Segunda División | Spain Segunda División (20262027) | ESP_SP2 — Segunda División | R50_ESP_SEGUNDA_DIVISION | Run 56 exact manifest; 462 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16576 | Sweden | Allsvenskan | Sweden Allsvenskan (2026) | — (no current-27 candidate) | R50_SWE_ALLSVENSKAN | retained QA; 240 rows; primary-window 176 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17129 | Switzerland | Super League | Switzerland Super League (20262027) | — (no current-27 candidate) | R50_CHE_SUPER_LEAGUE | Run 56 exact manifest; 132 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17265 | Turkey | Süper Lig | Turkey Süper Lig (20262027) | TUR_T1 — Turkish Super Lig | R50_TUR_SUPER_LIG | Run 56 exact manifest; 306 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16504 | USA | MLS | USA MLS (2026) | — (no current-27 candidate) | R50_USA_MLS | Run 56 exact manifest; 510 rows | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 17191 | Ukraine | Ukrainian Premier League | Ukraine Ukrainian Premier League (20262027) | UKR_UA1 — Ukrainian Premier League | R50_UKR_UKRAINIAN_PREMIER_LEAGUE | Run 56 exact manifest; 240 rows | prior catalogue: season.id match only | HUMAN REVIEW — NOT APPROVED |
| 16708 | Uruguay | Primera División | Uruguay Primera División (2026) | — (no current-27 candidate) | R50_URY_PRIMERA_DIVISION | retained QA; 281 rows; primary-window 231 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |
| 16617 | Venezuela | Primera División | Venezuela Primera División (2026) | — (no current-27 candidate) | R50_VEN_PRIMERA_DIVISION | retained QA; 231 rows; primary-window 193 | prior catalogue: season.id match only | UNMATCHED — RESEARCH ONLY |

### Candidate audit interpretation

- The **22 candidate rows** have a populated candidate code/name from the existing explicit crosswalk, but require a human reviewer to confirm competition and tier against the protected registry and then separately verify provider identity semantics. A name/country match is not a canonical ID join.
- The **28 unmatched rows** have no current-27 candidate. Their `R50_...` values are source-label grouping aliases only; they are not provider IDs, canonical IDs, or approval to expand production scope.
- Archive presence, season year, match counts, and country/name similarity cannot prove a parent competition ID, canonical team ID, or fixture join.
- Two legacy manifest gaps — Australia A-League (`17326`) and India Indian Super League (`17964`) — have zero retained primary-window rows in the cited gap-triage evidence. Do not fabricate or infer those historical samples; quarantine markets requiring the missing history until authoritative prior-season evidence is available.

## 5. Existing archive reconciliation — scoped evidence

- The archive reconciliation accounts for **50/50 selected groups**: 31 exact Run 56 manifest matches (reported 9,708 rows) and 19 rows absent from that older manifest but reconciled to retained private-package row-level QA (reported 4,343 rows).
- The private-archive audit reports 14,051 current-season fixture rows across the selected 50 groups. The 31-row and 19-row figures refer to separate evidence layers; do not treat them as a new deduplicated lifetime total or add unrelated archive totals.
- Run 56 feature-coverage CSV has rows for the 31 manifest-present groups only. Empty entries for the 19 older manifest gaps must not be read as “no archive data”; use the separate retained package QA for those rows.
- Archive feature presence proves structural availability only. It does not prove source authenticity, canonical fixture/team identity, kickoff-time correctness, or that historical values were available before the relevant kickoff.

## 6. Settlement truth — non-complete 0–0 placeholders stay excluded

Evidence sources: [status/score QA report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-data-quality-settlement-audit-2026-10-27.md), [settlement/provenance review](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-settlement-truth-provenance-review-2026-10-27.md), [research-only source trust policy](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/docs/oracle-result-source-trust-policy-research-only-2026-10-21.md), and [archive feature builder](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/scripts/build_footystats_archive_features.py).

| Source status | Rows | Observed score pattern | Required treatment |
|---|---:|---|---|
| `complete` | 51,983 | Numeric pairs; includes 4,006 0–0 | Research candidate truth only, pending identity and provenance gates |
| `incomplete` | 6,962 | All 0–0 | Exclude from settled truth |
| `suspended` | 57 | All 0–0 | Exclude from settled truth |
| `canceled` | 47 | All 0–0 | Exclude from settled truth |
| **Non-complete total** | **7,066** | **All numeric 0–0** | **Never settle as 0–0 or use as a market label** |

The archive builder can parse numeric zero score fields before status is considered. The controlling safeguard is the status gate: history/training candidates require parseable kickoff, allowed settled status, complete score and both team IDs. Unknown and non-complete statuses fail closed. This pass adds research-only regression coverage for `incomplete`, `suspended`, `canceled/cancelled`, `postponed`, and `abandoned` rows whose numeric scores are 0–0, while retaining the existing check that a `complete` 0–0 is only a candidate. The test change does not alter production or runtime logic.

Official provider documentation lists `complete`, `suspended`, `canceled`, and `incomplete` as status values and documents goal-count fields separately. A valid score pair cannot override a non-complete status.

### Limited official-score corroboration

Existing shadow rows point to two official Bundesliga reports:
- [Borussia Dortmund 2–2 Werder Bremen, 9 October 2026](https://www.bundesliga.com/en/bundesliga/news/borussia-dortmund-werder-bremen-match-report-highlights-matchday-5-39473).
- [Mainz 3–4 Bayer Leverkusen, 10 October 2026](https://www.bundesliga.com/en/bundesliga/news/mainz-bayer-leverkusen-match-report-highlights-matchday-5-39489).

These pages corroborate score/date only. The retained two-row shadow CSV lacks stable fixture IDs, canonical competition/team IDs, scheduled kickoff UTC, raw snapshot hash, acquisition timestamp, allowlist hash/version and a reproducible exact-identity join. They remain manual corroborations, not production settlement rows.

## 7. Point-in-time source-provenance gate

The existing [source trust policy](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/docs/oracle-result-source-trust-policy-research-only-2026-10-21.md) and [snapshot validator](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/scripts/validate_result_snapshot_provenance.py) require an independently pinned allowlist; raw snapshot hash and acquisition/run metadata; exact fixture/competition/kickoff/team identity; final status and score; result-observed time after kickoff; versioned score-derived settlement; rejected-row reasons; and point-in-time feature/odds/xG evidence. The validator explicitly reports `provider_authenticity_independently_proven=false`. A hash proves byte identity, not truth or authority.

The current official-source spot checks are insufficient to close these gates. Canonical production settlement and scorecard ledgers remain unpopulated; no production hit rate or betting edge can be claimed.

## 8. FootyStats clarification request — improved but not sent

The [clarification draft](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-footystats-identity-clarification-request-2026-10-27.md) now asks about the published `league-season` example mismatch and the ambiguous match-level `competition_id` label, in addition to stable-parent-ID and cross-season-key questions. The official API Overview confirms **admin@footystats.org** is an appropriate first contact route; the official About page also directs support to its Contact Us page.

**Status remains `DRAFT — NOT SENT`.** No email or support message has been sent. Do not send without separate explicit approval. No provider API call was made during this audit.

## 9. Controls and release decision

1. Keep all 50 parent competition IDs blank/unverified and all 50 canonical bridges unverified.
2. Have a human reviewer disposition the 22 candidate codes against the protected registry; retain all 28 unmatched rows as research-only expansion candidates.
3. Obtain written provider clarification or a documented identity contract before closing the parent-ID blocker.
4. Preserve exclusion of all 7,066 non-complete 0–0 placeholders; keep complete-score archive rows as research candidates until source, identity and point-in-time provenance are satisfied.
5. Expand official-score shadow reconciliation only with stable fixture identity and full provenance; do not create production ledger rows from score/date corroboration alone.
6. Keep Combo blocked under the existing settlement-spec mismatch. Keep raw metrics uncalibrated and odds/ROI claims unapproved.
7. Keep production registry, Oracle V1.6/V1.6.3, probabilities, thresholds, calibration, ledgers and governance unchanged.

**Final disposition: RESEARCH-ONLY PROGRESS; PRODUCTION AND BETTING RELEASE NOT GRANTED.** No further provider request is authorized. No production files were changed.

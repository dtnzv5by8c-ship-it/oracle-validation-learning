# Project Oracle — Exact-Name Candidate Crosswalk Addendum
- Date: 2026-10-24 (SAST)
- Branch: `research/oracle-50-league-readiness-audit`
- Status: Research only; production eligibility **NOT GRANTED**
- Purpose: Improve the 50-row crosswalk without approving any mapping or altering production.

## Method and limitations
The exact 50-row FootyStats manifest was joined to the live protected canonical registry and existing readiness matrix using exact country + exact competition-name equality only. No fuzzy matching, country-prefix stripping, or alias inference was used. Where both country and competition name matched, the canonical code is listed as a **candidate requiring review**, not an approved provider-ID mapping. The archive-level provider ID-to-season-manifest linkage was not available in the evidence fetched for this pass, so even exact-name matches are not approved mappings. Rows without an exact country/name match remain `UNRESOLVED`.

The canonical registry has 27 active entries. The matrix was last refreshed at `2026-10-01T17:25:35.759116Z`; its figures are historical evidence, not proof of current freshness. Matrix counts below are not attributed to the FootyStats provider ID until exact archive linkage is verified. A row's registry readiness state and matrix market labels are separate and may appear inconsistent; preserve that discrepancy for investigation rather than reconciling by assumption.

## 50 selected competitions — candidates and evidence
| # | FootyStats ID | Country | Exact provider competition | Canonical code | Mapping state | Existing matrix counts (not provider-ID-verified) | Matrix period / refresh | Matrix market states BTTS / DC / Combo / M1UP |
|---:|---:|---|---|---|---|---|---|---|
| 1 | 16571 | Argentina | Primera División | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 2 | 17326 | Australia | A-League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 3 | 17181 | Austria | Bundesliga | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 4 | 17171 | Belgium | Pro League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 5 | 16544 | Brazil | Serie A | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 6 | 16741 | Canada | Canadian Premier League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 7 | 16615 | Chile | Primera División | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 8 | 16789 | China | Chinese Super League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 9 | 16614 | Colombia | Categoria Primera A | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 10 | 17087 | Croatia | Prva HNL | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 11 | 17157 | Czech Republic | First League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 12 | 17091 | Denmark | Superliga | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 13 | 16714 | Ecuador | Primera Categoría Serie A | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 14 | 17146 | England | Premier League | ENG_E0 | CANDIDATE — REVIEW REQUIRED | 521 results; 6 fixtures; 50 current-season matches | 2025-04-01 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 15 | 17184 | England | Championship | ENG_E1 | CANDIDATE — REVIEW REQUIRED | 743 results; 0 fixtures; 95 current-season matches | 2025-03-28 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 16 | 17180 | England | EFL League One | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 17 | 16572 | Finland | Veikkausliiga | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 18 | 17102 | France | Ligue 1 | FRA_F1 | CANDIDATE — REVIEW REQUIRED | 423 results; 5 fixtures; 45 current-season matches | 2025-03-28 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 19 | 17117 | France | Ligue 2 | FRA_F2 | CANDIDATE — REVIEW REQUIRED | 431 results; 0 fixtures; 63 current-season matches | 2025-03-28 to 2026-09-19; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 20 | 17210 | Germany | Bundesliga | DEU_D1 | CANDIDATE — REVIEW REQUIRED | 414 results; 5 fixtures; 36 current-season matches | 2025-03-28 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 21 | 17212 | Germany | 2. Bundesliga | DEU_D2 | CANDIDATE — REVIEW REQUIRED | 432 results; 5 fixtures; 54 current-season matches | 2025-03-28 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 22 | 17356 | Greece | Super League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 23 | 17964 | India | Indian Super League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 24 | 17084 | Italy | Serie A | ITA_I1 | CANDIDATE — REVIEW REQUIRED | 520 results; 5 fixtures; 50 current-season matches | 2025-03-29 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 25 | 17404 | Italy | Serie B | ITA_I2 | CANDIDATE — REVIEW REQUIRED | 510 results; 0 fixtures; 50 current-season matches | 2025-03-28 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 26 | 17115 | Japan | J1 League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 27 | 17099 | Mexico | Liga MX | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 28 | 17097 | Netherlands | Eredivisie | NLD_N1 | CANDIDATE — REVIEW REQUIRED | 443 results; 0 fixtures; 63 current-season matches | 2025-03-29 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 29 | 16558 | Norway | Eliteserien | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 30 | 16533 | Paraguay | Division Profesional | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 31 | 16905 | Peru | Primera División | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 32 | 17112 | Poland | Ekstraklasa | POL_P1 | CANDIDATE — REVIEW REQUIRED | 465 results; 0 fixtures; 67 current-season matches | 2025-03-28 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 33 | 17215 | Portugal | LigaPro | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 34 | 16537 | Republic of Ireland | Premier Division | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 35 | 17247 | Romania | Liga I | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 36 | 17178 | Russia | Russian Premier League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 37 | 17426 | Saudi Arabia | Professional League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 38 | 17148 | Scotland | Premiership | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 39 | 17119 | Serbia | SuperLiga | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 40 | 17444 | South Africa | Premier Soccer League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 41 | 16627 | South Korea | K League 1 | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 42 | 17199 | Spain | La Liga | ESP_SP1 | CANDIDATE — REVIEW REQUIRED | 551 results; 5 fixtures; 69 current-season matches | 2025-03-27 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 43 | 17269 | Spain | Segunda División | ESP_SP2 | CANDIDATE — REVIEW REQUIRED | 649 results; 12 fixtures; 66 current-season matches | 2025-03-21 to 2026-09-20; refresh 2026-10-01T17:25:35.759116Z | CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / CONTROLLED_DATA_PATH / EVENT-TRUTH-GATED |
| 44 | 16576 | Sweden | Allsvenskan | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 45 | 17129 | Switzerland | Super League | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 46 | 17265 | Turkey | Süper Lig | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 47 | 16504 | USA | MLS | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 48 | 17191 | Ukraine | Ukrainian Premier League | UKR_UA1 | CANDIDATE — REVIEW REQUIRED | 85 results; 5 fixtures; 4 current-season matches | 2025-03-28 to 2026-08-02; refresh 2026-10-01T17:25:35.759116Z | PARTIAL_CURRENT_SEASON / PARTIAL_CURRENT_SEASON / PARTIAL_CURRENT_SEASON / EVENT-TRUTH-GATED |
| 49 | 16708 | Uruguay | Primera División | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |
| 50 | 16617 | Venezuela | Primera División | UNRESOLVED | UNRESOLVED | NOT ALLOCATED | UNVERIFIED | NOT ASSESSED |

## Findings from exact-name join
- Selected manifest rows: 50.
- Exact country + exact competition-name candidates: 13; all require human review and exact provider/archive ID linkage before acceptance.
- Unresolved: 37.
- These candidates are not approved mappings. Exact display-name equality is a useful candidate-generation rule but is not sufficient identity proof.
- The existing matrix has 27 rows and a refresh timestamp of 1 October 2026. Its historical/current fixture counts and market statuses must not be treated as current until refreshed and linked to exact FootyStats IDs.

## Market gates
- BTTS Yes, Double Chance, and Combo/DC Under 4.5 are assessed only as existing matrix labels at this checkpoint; those labels do not prove 50-league readiness or validated prediction performance.
- M1UP remains `EVENT-TRUTH-GATED` in the existing matrix. Production-quality M1UP requires chronological goal events and pre-match team state.
- xG/odds pre-kickoff provenance remains unverified; field presence alone is not enough.
- OOS evidence is not league-partitioned in the existing matrix. No 50-league per-market calibration/stability or production accuracy claim is supported.

## Blockers to completion
1. Obtain/read the exact archive `ingestion_manifest.csv` and per-competition `matches.json` records from a supported existing artifact; link each provider ID to season and fixture records.
2. Resolve the 42-versus-43 provider competition catalogue discrepancy.
3. Calculate per-ID historical/current fixtures, team-ID coverage, recent-form and standings availability, field missingness and source freshness from the actual archive.
4. Verify point-in-time xG/odds provenance.
5. Run the existing research-only crosswalk and readiness workflow only when its input artifact can be safely supplied and the workflow can be dispatched; inspect resulting artifact and tests.
6. Verify chronological OOS, calibration, stability and governance gates before any production decision.

## Governance
No production logic, weights, probabilities, thresholds, calibration, model version, protected registry, or canonical ledger was changed. No PR was merged, no gates were bypassed, and no provider purchase/change was made.

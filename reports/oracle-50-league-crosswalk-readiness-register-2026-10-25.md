# Project Oracle — 50-League Crosswalk & Readiness Register

- **As of:** 2026-10-25 (SAST)
- **Branch:** `research/oracle-50-league-readiness-audit`
- **Status:** Research-only inventory; production eligibility **NOT GRANTED**
- **Purpose:** Convert the recovered owner-selected FootyStats 50 into an explicit reconciliation register without altering production.

## Executive checkpoint

The source selection is established: the saved FootyStats settings page contained 1,737 checkbox inputs and exactly 50 checked league entries. This report carries all 50 into a row-level register. At this checkpoint, I have **not verified an authoritative provider-ID-to-Oracle-canonical-code mapping for any row from the evidence inspected in this pass**. Accordingly, each canonical mapping remains `UNRESOLVED`; historical/current fixture coverage, team identity, recent form, standings, xG/odds chronology, and market readiness are `UNVERIFIED / NOT ASSESSED`. These are honest statuses, not claims that the underlying data is absent.

The prior research audit reports 35,819 archive match records across 126 season groups, 28,491 settled rows with complete scores, provisional standings populated for 34,083 rows (95.2%), and historical xG/odds fields whose pre-kickoff provenance is unverified. Those are aggregate results from earlier runs and **must not be allocated to individual leagues** without a league-level artifact. The prior prediction evaluation path had 210 staged/challenger rows, zero verified fixture identities, and zero rows eligible for scoring; no production accuracy claim is supported.

## 50-row provider-to-canonical crosswalk

| # | Provider ID | Country | Provider competition (source exact) | Oracle canonical code | Competition-type verification | Historical/current fixtures | Team IDs / recent form | Standings | xG/odds pre-kickoff provenance | Per-market readiness |
|---:|---:|---|---|---|---|---|---|---|---|---|
| 1 | 16571 | Argentina | Primera División | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 2 | 17326 | Australia | A-League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 3 | 17181 | Austria | Bundesliga | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 4 | 17171 | Belgium | Pro League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 5 | 16544 | Brazil | Serie A | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 6 | 16741 | Canada | Canadian Premier League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 7 | 16615 | Chile | Primera División | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 8 | 16789 | China | Chinese Super League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 9 | 16614 | Colombia | Categoria Primera A | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 10 | 17087 | Croatia | Prva HNL | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 11 | 17157 | Czech Republic | First League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 12 | 17091 | Denmark | Superliga | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 13 | 16714 | Ecuador | Primera Categoría Serie A | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 14 | 17146 | England | Premier League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 15 | 17184 | England | Championship | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 16 | 17180 | England | EFL League One | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 17 | 16572 | Finland | Veikkausliiga | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 18 | 17102 | France | Ligue 1 | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 19 | 17117 | France | Ligue 2 | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 20 | 17210 | Germany | Bundesliga | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 21 | 17212 | Germany | 2. Bundesliga | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 22 | 17356 | Greece | Super League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 23 | 17964 | India | Indian Super League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 24 | 17084 | Italy | Serie A | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 25 | 17404 | Italy | Serie B | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 26 | 17115 | Japan | J1 League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 27 | 17099 | Mexico | Liga MX | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 28 | 17097 | Netherlands | Eredivisie | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 29 | 16558 | Norway | Eliteserien | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 30 | 16533 | Paraguay | Division Profesional | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 31 | 16905 | Peru | Primera División | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 32 | 17112 | Poland | Ekstraklasa | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 33 | 17215 | Portugal | LigaPro | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 34 | 16537 | Republic of Ireland | Premier Division | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 35 | 17247 | Romania | Liga I | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 36 | 17178 | Russia | Russian Premier League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 37 | 17426 | Saudi Arabia | Professional League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 38 | 17148 | Scotland | Premiership | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 39 | 17119 | Serbia | SuperLiga | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 40 | 17444 | South Africa | Premier Soccer League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 41 | 16627 | South Korea | K League 1 | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 42 | 17199 | Spain | La Liga | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 43 | 17269 | Spain | Segunda División | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 44 | 16576 | Sweden | Allsvenskan | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 45 | 17129 | Switzerland | Super League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 46 | 17265 | Turkey | Süper Lig | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 47 | 16504 | USA | MLS | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 48 | 17191 | Ukraine | Ukrainian Premier League | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 49 | 16708 | Uruguay | Primera División | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |
| 50 | 16617 | Venezuela | Primera División | UNRESOLVED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | NOT ASSESSED |

## Market readiness status (applies to all 50 until per-league evidence is attached)

| Market / family | Current readiness for the 50-league target | Evidence required before a PASS |
|---|---|---|
| M-1UP / early lead | NOT ASSESSED | Exact fixture identity; chronological goal events or equivalent trusted lead-event truth; pre-kickoff feature cutoff; market-specific settled outcomes |
| BTTS Yes / No | NOT ASSESSED | Verified fixture and team IDs; strict pre-kickoff inputs; exact settled score; market-specific chronological evaluation |
| Double Chance (1X / X2 / 12) | NOT ASSESSED | Verified fixture IDs and score settlement; market mapping and selection rules |
| Goal totals (Over/Under) | NOT ASSESSED | Verified score settlement; market/line mapping; pre-match data cutoff |
| Team goals | NOT ASSESSED | Verified home/away identity, scores, market line and pre-match feature provenance |
| Combination markets (including DC + totals) | NOT ASSESSED | All component markets verified plus joint-event settlement and dependence/combination rules |
| Other markets present in canonical prediction records | NOT ASSESSED | Inventory of canonical market codes and market-specific required-input contract; do not assume coverage from the list above |

## Root-cause / next-action register

1. **Canonical mapping is the first hard blocker.** Read the protected canonical registry and ingestion/archive manifests; match by provider ID and exact source evidence. Do not infer a canonical code from similar competition names. Preserve unresolved rows.
2. **Coverage must be measured per provider ID and season.** For each selected ID, record request result/status, season groups, fixture count, earliest/latest kickoff, score/settlement completeness, and explicit errors. Aggregate archive totals cannot substitute for this.
3. **Identity joins must be exact and league-aware.** Record canonical home/away team IDs and fixture ID coverage. No fuzzy joins may be treated as verified.
4. **Recent form and standings must be temporal.** Calculate only from matches before each target kickoff; validate each competition's season format and tie-break rules before marking standings verified.
5. **xG and odds require point-in-time provenance.** Field presence is insufficient: retain provider, source timestamp, retrieval timestamp, and immutable pre-kickoff snapshot or mark UNVERIFIED.
6. **Market readiness is a separate gate.** Define required inputs and settled outcomes for each supported market; score only exact verified fixture/market pairs with chronological separation.
7. **Production remains frozen.** Do not modify model logic, weights, probabilities, thresholds, calibration, version, canonical registry, or canonical ledgers. Do not merge draft PRs or bypass quality gates.

## Workflow observation at checkpoint

The latest ten repository workflow runs visible during this check were headed by H2H reporting PR runs, including H2H Reporting run #47 (ID 40124388720, completed successfully). That run is an H2H branch check and is **not evidence that the 50-league audit or a provider extraction completed**. I did not find verified output from a dedicated 50-league reconciliation run in the inspected latest-run page. No new data coverage or production readiness is claimed here.

## Acceptance criteria for the next checkpoint

- All 50 rows retained with evidence-backed canonical code or explicit UNRESOLVED.
- Every league has per-season historical and current fixture counts, coverage dates, request errors, score completeness, and exact team/fixture identity coverage.
- Recent form and standings carry strict as-of cutoffs; standings rules validated by competition.
- xG/odds provenance states are explicit for each feature and match window.
- Each supported market has required-input, settled-label, eligible-row count, and readiness status by league.
- Any performance metrics use verified exact fixture/market matches, chronological out-of-sample splits, and report sample size/uncertainty.
- Production gates remain closed unless independently evidenced and approved.

## Source references

- [Recovered owner-selected FootyStats manifest](oracle-footystats-selected-50-league-manifest-2026-10-24.md)
- [Initial readiness audit](oracle-50-league-readiness-audit-initial-2026-10-24.md)
- [Manifest recovery addendum](oracle-50-league-manifest-recovery-addendum-2026-10-24.md)
- [Latest observed H2H reporting run #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720)

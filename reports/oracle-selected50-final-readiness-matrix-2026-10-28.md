# Oracle Selected-50 Final Readiness Matrix — 2026-10-28

**Scope:** 50 selected FootyStats seasons.  
**Evidence timestamp:** FootyStats current schedule snapshot retrieved 2026-10-28 06:11:51 UTC.  
**Decision:** Research data coverage and provider schedule retrieval are available; **production and betting release remain NO-GO** because cross-provider identity, current FotMob freshness, canonical fixture/team joins, official settlement and market controls are not approved.

## Gate summary

| Gate | Status | Evidence |
|---|---|---|
| Research workflow/test QA | PASS | Safety contract, archive audit, dry-run planner and runtime workflows passed in cited runs |
| FootyStats season identity probe | PASS as provider evidence | 50/50 HTTP 200, returned season ID/country/name matched selected manifest; 50 distinct `comp_master_id` values |
| FootyStats current fixture retrieval | PASS as source retrieval | 50/50 `league-matches` calls succeeded; one page per season; 871 fixtures in next 14 days and 871 recent completed matches in prior 14 days |
| Historical archive coverage | OBSERVED, not completeness proof | 59,049 deduplicated match rows; 51,983 explicitly completed across 50 selected groups |
| FotMob current-feed freshness | FAIL / STALE | Accessible manifest generated 6 Oct 2026 and requested dates only through 8 Oct; no newer authoritative FotMob manifest verified |
| FootyStats-to-FotMob bridge | NOT APPROVED | 0/50 reviewed bridges; provider master ID semantics not sufficient to equate with FotMob league IDs |
| Canonical fixture/team joins | NOT VERIFIED | Exact kickoff/team joins and official settlement truth remain unverified |
| Combo settlement | BLOCKED | Predictor/settlement definition disagreement remains; Combo probabilities masked |
| Production/betting eligibility | NO-GO | No mapping promotions or production model changes authorized |

## Full per-league matrix

Historical columns are preserved from the 27 October archive readiness report. The new columns reflect the live FootyStats API retrieval, not the stale FotMob feed. Provider `comp_master_id` is an observed source field, not an approved Oracle canonical ID.

| Country | Competition | Season ID | Provider master ID observed | Archive rows | Completed archive | Primary-window completed | Full 20-feature rows | Archive fixtures next 7d | FootyStats schedule request | Provider matches returned | FootyStats fixtures next 14d | Recent completed next 14d lookback | FotMob bridge approved | Production eligible |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| USA | MLS | 16504 | 334 | 2,093 | 2,049 | 867 | 1,928 | 29 | PASS | 510 | 44 | 46 | NOT APPROVED | NO |
| Paraguay | Division Profesional | 16533 | 444 | 1,056 | 1,014 | 407 | 938 | 11 | PASS | 264 | 16 | 8 | NOT APPROVED | NO |
| Republic of Ireland | Premier Division | 16537 | 264 | 721 | 716 | 310 | 650 | 5 | PASS | 180 | 5 | 12 | NOT APPROVED | NO |
| Brazil | Serie A | 16544 | 64 | 1,520 | 1,457 | 657 | 1,331 | 11 | PASS | 380 | 20 | 20 | NOT APPROVED | NO |
| Norway | Eliteserien | 16558 | 247 | 960 | 912 | 408 | 826 | 8 | PASS | 240 | 16 | 16 | NOT APPROVED | NO |
| Argentina | Primera División | 16571 | 27 | 1,965 | 1,932 | 763 | 1,663 | 16 | PASS | 495 | 30 | 31 | NOT APPROVED | NO |
| Finland | Veikkausliiga | 16572 | 125 | 688 | 678 | 327 | 582 | 6 | PASS | 177 | 9 | 9 | NOT APPROVED | NO |
| Sweden | Allsvenskan | 16576 | 303 | 960 | 920 | 416 | 836 | 14 | PASS | 240 | 23 | 17 | NOT APPROVED | NO |
| Colombia | Categoria Primera A | 16614 | 76 | 1,730 | 1,690 | 660 | 1,585 | 7 | PASS | 394 | 25 | 28 | NOT APPROVED | NO |
| Chile | Primera División | 16615 | 72 | 960 | 917 | 384 | 817 | 8 | PASS | 240 | 17 | 8 | NOT APPROVED | NO |
| Venezuela | Primera División | 16617 | 339 | 922 | 901 | 370 | 810 | 8 | PASS | 231 | 14 | 13 | NOT APPROVED | NO |
| South Korea | K League 1 | 16627 | 294 | 882 | 882 | 378 | 789 | 0 | PASS | 228 | 12 | 12 | NOT APPROVED | NO |
| Uruguay | Primera División | 16708 | 331 | 1,178 | 1,170 | 483 | 1,036 | 8 | PASS | 281 | 8 | 16 | NOT APPROVED | NO |
| Ecuador | Primera Categoría Serie A | 16714 | 99 | 1,108 | 1,065 | 517 | 976 | 8 | PASS | 312 | 16 | 16 | NOT APPROVED | NO |
| Canada | Canadian Premier League | 16741 | 524 | 463 | 463 | 206 | 410 | 0 | PASS | 116 | 4 | 8 | NOT APPROVED | NO |
| China | Chinese Super League | 16789 | 2 | 960 | 952 | 432 | 814 | 0 | PASS | 240 | 8 | 16 | NOT APPROVED | NO |
| Peru | Primera División | 16905 | 253 | 1,302 | 1,249 | 528 | 1,122 | 16 | PASS | 306 | 26 | 19 | NOT APPROVED | NO |
| Italy | Serie A | 17084 | 193 | 1,520 | 1,220 | 520 | 1,365 | 19 | PASS | 380 | 27 | 23 | NOT APPROVED | NO |
| Croatia | Prva HNL | 17087 | 82 | 720 | 592 | 269 | 647 | 5 | PASS | 180 | 10 | 10 | NOT APPROVED | NO |
| Denmark | Superliga | 17091 | 95 | 711 | 650 | 308 | 609 | 6 | PASS | 132 | 12 | 12 | NOT APPROVED | NO |
| Netherlands | Eredivisie | 17097 | 234 | 1,233 | 1,017 | 449 | 1,081 | 9 | PASS | 306 | 18 | 18 | NOT APPROVED | NO |
| Mexico | Liga MX | 17099 | 225 | 1,170 | 1,141 | 475 | 1,062 | 10 | PASS | 153 | 19 | 27 | NOT APPROVED | NO |
| France | Ligue 1 | 17102 | 130 | 1,224 | 988 | 422 | 1,026 | 9 | PASS | 306 | 18 | 18 | NOT APPROVED | NO |
| Poland | Ekstraklasa | 17112 | 259 | 1,224 | 1,024 | 465 | 1,041 | 9 | PASS | 306 | 18 | 18 | NOT APPROVED | NO |
| Japan | J1 League | 17115 | 198 | 1,446 | 1,186 | 402 | 1,274 | 10 | PASS | 380 | 20 | 30 | NOT APPROVED | NO |
| France | Ligue 2 | 17117 | 132 | 1,302 | 1,084 | 434 | 1,082 | 9 | PASS | 306 | 18 | 18 | NOT APPROVED | NO |
| Serbia | SuperLiga | 17119 | 283 | 1,070 | 977 | 436 | 930 | 7 | PASS | 182 | 16 | 14 | NOT APPROVED | NO |
| Switzerland | Super League | 17129 | 312 | 816 | 750 | 342 | 724 | 6 | PASS | 132 | 12 | 6 | NOT APPROVED | NO |
| England | Premier League | 17146 | 9 | 1,520 | 1,220 | 521 | 1,294 | 10 | PASS | 380 | 20 | 20 | NOT APPROVED | NO |
| Scotland | Premiership | 17148 | 278 | 882 | 744 | 318 | 799 | 9 | PASS | 198 | 16 | 12 | NOT APPROVED | NO |
| Czech Republic | First League | 17157 | 88 | 1,069 | 923 | 416 | 957 | 8 | PASS | 240 | 17 | 15 | NOT APPROVED | NO |
| Belgium | Pro League | 17171 | 1 | 1,244 | 1,018 | 448 | 1,083 | 9 | PASS | 306 | 19 | 8 | NOT APPROVED | NO |
| Russia | Russian Premier League | 17178 | 268 | 960 | 816 | 384 | 834 | 8 | PASS | 240 | 16 | 16 | NOT APPROVED | NO |
| England | EFL League One | 17180 | 6 | 2,223 | 1,809 | 755 | 1,933 | 17 | PASS | 552 | 15 | 41 | NOT APPROVED | NO |
| Austria | Bundesliga | 17181 | 40 | 717 | 645 | 300 | 634 | 6 | PASS | 132 | 12 | 12 | NOT APPROVED | NO |
| England | Championship | 17184 | 103 | 2,224 | 1,815 | 753 | 1,996 | 12 | PASS | 552 | 36 | 29 | NOT APPROVED | NO |
| Ukraine | Ukrainian Premier League | 17191 | 328 | 960 | 796 | 367 | 783 | 8 | PASS | 240 | 16 | 16 | NOT APPROVED | NO |
| Spain | La Liga | 17199 | 3 | 1,520 | 1,238 | 551 | 1,330 | 10 | PASS | 380 | 20 | 21 | NOT APPROVED | NO |
| Germany | Bundesliga | 17210 | 143 | 1,224 | 981 | 414 | 1,006 | 9 | PASS | 306 | 18 | 18 | NOT APPROVED | NO |
| Germany | 2. Bundesliga | 17212 | 140 | 1,224 | 999 | 432 | 991 | 9 | PASS | 306 | 18 | 18 | NOT APPROVED | NO |
| Portugal | LigaPro | 17215 | 5 | 1,224 | 989 | 431 | 988 | 9 | PASS | 306 | 18 | 9 | NOT APPROVED | NO |
| Romania | Liga I | 17247 | 265 | 1,189 | 1,052 | 461 | 1,045 | 8 | PASS | 240 | 16 | 16 | NOT APPROVED | NO |
| Turkey | Süper Lig | 17265 | 8 | 1,334 | 1,106 | 450 | 1,117 | 9 | PASS | 306 | 18 | 18 | NOT APPROVED | NO |
| Spain | Segunda División | 17269 | 299 | 1,866 | 1,524 | 661 | 1,597 | 11 | PASS | 462 | 22 | 22 | NOT APPROVED | NO |
| Australia | A-League | 17326 | 34 | 664 | 519 | 207 | 590 | 6 | PASS | 156 | 12 | 11 | NOT APPROVED | NO |
| Greece | Super League | 17356 | 152 | 894 | 767 | 325 | 748 | 7 | PASS | 182 | 14 | 13 | NOT APPROVED | NO |
| Italy | Serie B | 17404 | 194 | 1,552 | 1,249 | 529 | 1,232 | 19 | PASS | 380 | 23 | 27 | NOT APPROVED | NO |
| Saudi Arabia | Professional League | 17426 | 272 | 1,224 | 1,012 | 450 | 1,049 | 9 | PASS | 306 | 18 | 24 | NOT APPROVED | NO |
| South Africa | Premier Soccer League | 17444 | 290 | 960 | 756 | 350 | 774 | 8 | PASS | 240 | 15 | 4 | NOT APPROVED | NO |
| India | Indian Super League | 17964 | 169 | 471 | 409 | 98 | 361 | 6 | PASS | 78 | 11 | 12 | NOT APPROVED | NO |

## What is now unblocked

- The selected 50 FootyStats season IDs have direct provider responses rather than name-only inference.
- A current, timestamped FootyStats schedule response exists for all 50 selected seasons.
- The new schedule artifact provides filtered upcoming fixtures and recent completed matches with provider-native match/team IDs.
- A repaired research identity crosswalk records all 50 observed `comp_master_id` values and the request provenance.

## Snapshot data quality

The retrieved FootyStats snapshot has 1,744 rows in the 28-day audit window: 871 future fixtures and 871 recent completed results, plus 2 recent suspended rows. Across the window, 354 rows have `no_home_away=1` (181 future and 173 recent); 14 future rows are suspended. Quarantine suspended fixtures and all no-home/away fixtures from standard home/away markets. All rows have team names, team IDs and kickoff timestamps; no duplicate match IDs were detected. There are 47 recent rows with status `complete` and a 0–0 score; retain the source status but reconcile settlement truth before use.

[Read the detailed fixture snapshot data-quality audit](oracle-selected50-fixture-snapshot-data-quality-2026-10-28.md).

## New cross-provider overlap evidence

A read-only overlap audit found 8 exact home/away-team + UTC-kickoff joins across two selected leagues. Canada Canadian Premier League (FootyStats season 16741 / observed master ID 524) maps as a strong candidate to FotMob league ID 1000001192 with four exact joins, three completed scores agreeing and one score/status conflict. England EFL League One (season 17180 / master ID 6) maps as a strong candidate to FotMob league ID 938219 with four exact joins, one completed score agreeing and three postponed/suspended matches. These are **research candidates only**, not approved canonical bridges. [Full join evidence and conflict details](oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md).

## Expanded overlap snapshot and validator

A second, expanded FootyStats snapshot (30-day lookback + 14-day future window) was retrieved at `2026-10-28T06:19:09.645973+00:00` UTC. The offline snapshot validator passed: 50/50 requests succeeded, 2,250 rows, 871 future fixtures, 1,372 recent completed results, zero duplicate match IDs and no missing team IDs/names/kickoff timestamps. It found 19 suspended rows and 486 `no_home_away=1` rows (181 future, 305 recent), which must be quarantined from unsupported markets. The [overlap join audit](oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md) documents the eight exact joins and one score/status conflict.

## Historical ledger crosswalk progress

The read-only cross-provider audit now finds **24 strong research-only historical ledger league-code candidates** across 24 selected seasons, supported by 577 ordered home/away team + UTC calendar-date joins. The observed historical scores agree across these joins. The historical ledger does not provide kickoff precision in the matched file, so these are candidates for human review—not approved canonical mappings. A further 2 FotMob league-ID candidates are supported by 10 exact team/kickoff joins; England overlaps with the 24-code list, while Canada has one score/status conflict. Overall, 25 of 50 selected seasons have at least one evidence-backed identity candidate; 25 remain without a supported join in the current audit. **Approved canonical bridges remain 0/50.** [Full join evidence](oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md).

## Current-feed incident

The latest three visible production `Oracle Current Data Staging` workflow runs (26–27 October) failed. The exact failure cause remains unverified because the connected log read did not expose the job logs. Do not infer a quota or code cause without the failure step. [Incident evidence and safe remediation](oracle-selected50-production-current-feed-incident-2026-10-28.md).

## Market release readiness

The latest historical walk-forward diagnostics remain research-only: across 50 leagues, positive Brier skill was stable across all available folds for 3 BTTS leagues, 17 DC_HOME, 19 DC_AWAY, 15 Home Combo and 17 Away Combo; 20 leagues per market have insufficient fold sample/metric. **Production-eligible leagues remain 0/50 for every market.** Combo probabilities remain masked pending canonical fixture/team joins and official settlement truth. The new FootyStats schedule rows are not model predictions. [Full market release readiness](oracle-selected50-market-release-readiness-2026-10-28.md).

## Latest runtime and Combo QA

Latest research runtime [run 40644996653](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644996653), [artifact 12797455274](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644996653/artifacts/12797455274), passed the research output contract. It produced 463 seven-day fixture candidates across 40 competitions; 25 were blocked by minimum recent home/away history requirements. QA reports 9,335 Home Combo and 8,017 Away Combo predictor-versus-ledger disagreement rows. The governed report masks all 438 available Combo probabilities on each side because the predictor target (Double Chance AND 2–4 goals) differs from the settlement helper (Double Chance AND total goals <5, including 0–1 goals). Combo remains blocked; do not silently change either definition.

## What is not unblocked

1. The FootyStats snapshot is not the same feed as production's FotMob `database/current_matches.csv`. It must not be substituted silently into production.
2. The public FootyStats docs list `comp_master_id` but do not establish a sufficiently precise semantic mapping to Oracle canonical codes or FotMob league IDs.
3. 50 successful source requests do not guarantee full schedule completeness beyond one page; the current probe shows one page per season, and no season required pagination in this result.
4. Provider team IDs cannot be assumed to equal FotMob team IDs.
5. Historical archive and current fixture availability do not establish calibrated betting performance. Combo remains blocked; other markets remain research-only until canonical joins, settlement truth, point-in-time features and calibration gates pass.

## Next actions

1. Confirm the exact semantics of `comp_master_id` from authoritative FootyStats documentation/support.
2. Build a research-only candidate crosswalk from provider master IDs to the existing canonical registry and separately to FotMob league IDs; require source evidence for both sides.
3. Inspect the production current-data workflow failures through a supported run/log path and establish why the FotMob manifest is stale. Do not rerun the unsafe name-only ingestion as a shortcut.
4. If an identity-safe staging destination is available, use the current FootyStats schedule artifact as a source candidate only; do not promote rows into production until IDs, kickoff, teams and settlement are verified.
5. Publish the final release decision after all mandatory gates are checked. If evidence remains absent at noon, keep release NO-GO and record the blocker.

## Evidence links

- [FootyStats identity reconciliation report](oracle-selected50-footystats-master-id-reconciliation-2026-10-28.md)
- [FootyStats current fixture snapshot report](oracle-selected50-current-fixture-snapshot-2026-10-28.md)
- [Sanitized current fixture artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796425175)
- [FootyStats League Matches API documentation](https://footystats.org/api/documentations/match-schedule-and-stats)
- [FootyStats League Season API documentation](https://footystats.org/api/documentations/league-season-stats-teams)

## Governance

Research-only updates. No changes to production Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers or governance. No canonical mapping was approved automatically. Production/betting eligibility remains NO-GO.

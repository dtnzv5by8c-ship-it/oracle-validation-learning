# Oracle Selected-50 League Readiness Matrix — 2026-10-27

**Evidence basis:** Run #112, [GitHub Actions run 40554064150](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150), [artifact 12757295232](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232). This table is derived from the sanitized runtime artifact. It describes observed archive coverage, not proof of provider completeness.

## Executive interpretation

- 50 selected season groups; four provider season-year labels (2023–2026) observed for each group in this archive.
- 59,049 deduplicated match rows, 51,983 explicitly completed rows across the 50 groups.
- Primary-window completed rows below count only archive records falling in 2025-03-20 through 2026-09-20; they are not a guarantee of complete historical coverage.
- 461 future-fixture candidates in the seven-day horizon. Three groups have no fixture in that horizon and require schedule-freshness checks.
- Parent competition IDs verified: 0/50. Provider-to-Oracle canonical bridges approved: 0.
- Canonical fixture/team joins and official settlement truth are not verified. Combo probabilities remain masked.
- All groups remain production-ineligible and betting-ineligible. Raw walk-forward results are uncalibrated; odds/ROI evidence is not approved.
- The detailed per-market walk-forward folds and scores remain in the source artifact: `oracle_selected50_league_market_readiness.csv` and `oracle_selected50_league_walk_forward_metrics.csv`.

## Per-league coverage and release gates

| Country | Competition | Selected season ID | Observed years | Seasons | Archive rows | Completed rows | Primary-window completed | Full 20-feature rows | Fixtures next 7d | Schedule status | Identity gate | Production eligible |
|---|---|---:|---|---:|---:|---:|---:|---:|---|---|---|---|
| Argentina | Primera División | 16571 | 2023;2024;2025;2026 | 4 | 1,965 | 1,932 | 763 | 1,663 | 16 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Australia | A-League | 17326 | 2023;2024;2025;2026 | 4 | 664 | 519 | 207 | 590 | 6 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Austria | Bundesliga | 17181 | 2023;2024;2025;2026 | 4 | 717 | 645 | 300 | 634 | 6 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Belgium | Pro League | 17171 | 2023;2024;2025;2026 | 4 | 1,244 | 1,018 | 448 | 1,083 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Brazil | Serie A | 16544 | 2023;2024;2025;2026 | 4 | 1,520 | 1,457 | 657 | 1,331 | 11 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Canada | Canadian Premier League | 16741 | 2023;2024;2025;2026 | 4 | 463 | 463 | 206 | 410 | 0 | NO_FIXTURE_IN_7D_HORIZON_CHECK_SCHEDULE_FRESHNESS | Parent/canonical unverified | NO |
| Chile | Primera División | 16615 | 2023;2024;2025;2026 | 4 | 960 | 917 | 384 | 817 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| China | Chinese Super League | 16789 | 2023;2024;2025;2026 | 4 | 960 | 952 | 432 | 814 | 0 | NO_FIXTURE_IN_7D_HORIZON_CHECK_SCHEDULE_FRESHNESS | Parent/canonical unverified | NO |
| Colombia | Categoria Primera A | 16614 | 2023;2024;2025;2026 | 4 | 1,730 | 1,690 | 660 | 1,585 | 7 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Croatia | Prva HNL | 17087 | 2023;2024;2025;2026 | 4 | 720 | 592 | 269 | 647 | 5 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Czech Republic | First League | 17157 | 2023;2024;2025;2026 | 4 | 1,069 | 923 | 416 | 957 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Denmark | Superliga | 17091 | 2023;2024;2025;2026 | 4 | 711 | 650 | 308 | 609 | 6 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Ecuador | Primera Categoría Serie A | 16714 | 2023;2024;2025;2026 | 4 | 1,108 | 1,065 | 517 | 976 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| England | Championship | 17184 | 2023;2024;2025;2026 | 4 | 2,224 | 1,815 | 753 | 1,996 | 12 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| England | EFL League One | 17180 | 2023;2024;2025;2026 | 4 | 2,223 | 1,809 | 755 | 1,933 | 17 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| England | Premier League | 17146 | 2023;2024;2025;2026 | 4 | 1,520 | 1,220 | 521 | 1,294 | 10 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Finland | Veikkausliiga | 16572 | 2023;2024;2025;2026 | 4 | 688 | 678 | 327 | 582 | 6 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| France | Ligue 1 | 17102 | 2023;2024;2025;2026 | 4 | 1,224 | 988 | 422 | 1,026 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| France | Ligue 2 | 17117 | 2023;2024;2025;2026 | 4 | 1,302 | 1,084 | 434 | 1,082 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Germany | 2. Bundesliga | 17212 | 2023;2024;2025;2026 | 4 | 1,224 | 999 | 432 | 991 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Germany | Bundesliga | 17210 | 2023;2024;2025;2026 | 4 | 1,224 | 981 | 414 | 1,006 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Greece | Super League | 17356 | 2023;2024;2025;2026 | 4 | 894 | 767 | 325 | 748 | 7 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| India | Indian Super League | 17964 | 2023;2024;2025;2026 | 4 | 471 | 409 | 98 | 361 | 6 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Italy | Serie A | 17084 | 2023;2024;2025;2026 | 4 | 1,520 | 1,220 | 520 | 1,365 | 19 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Italy | Serie B | 17404 | 2023;2024;2025;2026 | 4 | 1,552 | 1,249 | 529 | 1,232 | 19 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Japan | J1 League | 17115 | 2023;2024;2025;2026 | 4 | 1,446 | 1,186 | 402 | 1,274 | 10 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Mexico | Liga MX | 17099 | 2023;2024;2025;2026 | 4 | 1,170 | 1,141 | 475 | 1,062 | 10 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Netherlands | Eredivisie | 17097 | 2023;2024;2025;2026 | 4 | 1,233 | 1,017 | 449 | 1,081 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Norway | Eliteserien | 16558 | 2023;2024;2025;2026 | 4 | 960 | 912 | 408 | 826 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Paraguay | Division Profesional | 16533 | 2023;2024;2025;2026 | 4 | 1,056 | 1,014 | 407 | 938 | 11 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Peru | Primera División | 16905 | 2023;2024;2025;2026 | 4 | 1,302 | 1,249 | 528 | 1,122 | 16 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Poland | Ekstraklasa | 17112 | 2023;2024;2025;2026 | 4 | 1,224 | 1,024 | 465 | 1,041 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Portugal | LigaPro | 17215 | 2023;2024;2025;2026 | 4 | 1,224 | 989 | 431 | 988 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Republic of Ireland | Premier Division | 16537 | 2023;2024;2025;2026 | 4 | 721 | 716 | 310 | 650 | 5 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Romania | Liga I | 17247 | 2023;2024;2025;2026 | 4 | 1,189 | 1,052 | 461 | 1,045 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Russia | Russian Premier League | 17178 | 2023;2024;2025;2026 | 4 | 960 | 816 | 384 | 834 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Saudi Arabia | Professional League | 17426 | 2023;2024;2025;2026 | 4 | 1,224 | 1,012 | 450 | 1,049 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Scotland | Premiership | 17148 | 2023;2024;2025;2026 | 4 | 882 | 744 | 318 | 799 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Serbia | SuperLiga | 17119 | 2023;2024;2025;2026 | 4 | 1,070 | 977 | 436 | 930 | 7 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| South Africa | Premier Soccer League | 17444 | 2023;2024;2025;2026 | 4 | 960 | 756 | 350 | 774 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| South Korea | K League 1 | 16627 | 2023;2024;2025;2026 | 4 | 882 | 882 | 378 | 789 | 0 | NO_FIXTURE_IN_7D_HORIZON_CHECK_SCHEDULE_FRESHNESS | Parent/canonical unverified | NO |
| Spain | La Liga | 17199 | 2023;2024;2025;2026 | 4 | 1,520 | 1,238 | 551 | 1,330 | 10 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Spain | Segunda División | 17269 | 2023;2024;2025;2026 | 4 | 1,866 | 1,524 | 661 | 1,597 | 11 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Sweden | Allsvenskan | 16576 | 2023;2024;2025;2026 | 4 | 960 | 920 | 416 | 836 | 14 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Switzerland | Super League | 17129 | 2023;2024;2025;2026 | 4 | 816 | 750 | 342 | 724 | 6 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Turkey | Süper Lig | 17265 | 2023;2024;2025;2026 | 4 | 1,334 | 1,106 | 450 | 1,117 | 9 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| USA | MLS | 16504 | 2023;2024;2025;2026 | 4 | 2,093 | 2,049 | 867 | 1,928 | 29 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Ukraine | Ukrainian Premier League | 17191 | 2023;2024;2025;2026 | 4 | 960 | 796 | 367 | 783 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Uruguay | Primera División | 16708 | 2023;2024;2025;2026 | 4 | 1,178 | 1,170 | 483 | 1,036 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |
| Venezuela | Primera División | 16617 | 2023;2024;2025;2026 | 4 | 922 | 901 | 370 | 810 | 8 | FIXTURES_FOUND | Parent/canonical unverified | NO |

## Required follow-up

1. Obtain documented provider identity semantics or an authoritative crosswalk for the selected season IDs. Do not infer parent IDs.
2. Review and approve canonical league/team/fixture joins with explicit evidence and human sign-off.
3. Verify final result/status truth against an authoritative source and preserve exclusion of non-complete 0–0 placeholders.
4. Investigate schedule freshness for Canada, China and South Korea, where no fixture appeared in the current seven-day horizon.
5. Resolve missing feature/training support for blocked fixture rows without inventing data.
6. Assess calibration, point-in-time provenance and odds/ROI only after identity and settlement gates are resolved.

## Production integrity

The Run #112 QA states `production_model_logic_changed=false` and `production_probabilities_changed=false`. This is a research readiness artifact, not production approval.

# Project Oracle — Selected-50 Per-League / Per-Season Numeric Missingness Audit

**Audit date:** 30 October 2026  
**Source private-archive QA:** run #30, 40994720108, artifact 12950667181  
**Source archive release:** research-selected50-footystats-history-40375285207  
**Archive SHA-256:** 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f  
**Research branch:** research/oracle-50-league-readiness-audit

## Executive finding

The new per-league and per-season numeric QA outputs reveal that zero-coded xG and odds fields are not uniformly distributed. The most material current-season issue is Belgium Pro League: 54 of 63 current-season completed rows (85.714%) have zero full-time BTTS odds and zero Double Chance 1X/X2 odds. The same season's full-time 1X2 odds have only 1 zero in 63 rows, so this appears market-specific rather than a blanket absence of all odds fields.

Prematch-xG-labelled fields also show high zero rates in several current-season league samples: Germany Bundesliga 18/36 (50%), England Premier League 20/50 (40%), France Ligue 1 18/45 (40%), Greece Super League 14/35 (40%), Italy Serie A 20/50 (40%) and Serie B 20/50 (40%). These are data-quality warnings, not evidence of team or model failure. Field names do not prove values were captured pre-kickoff, and zero values have not been semantically classified by the provider.

## 1. New scoped QA outputs

The private-archive QA generator now emits numeric xG/odds statistics at both scopes, without exporting raw provider records:

| Output | Rows | Scope |
|---|---:|---|
| selected50_numeric_feature_quality_by_league.csv | 7,400 | 50 league groups × 74 fields × 2 subsets |
| selected50_numeric_feature_quality_by_season.csv | 19,240 | 130 seasons with primary-window data × 74 fields × 2 subsets |

Subsets are the full primary window and provider-complete rows within that window. The outputs preserve denominators, numeric counts, zero counts, non-numeric counts, negative counts, min/max and means.

The downstream analysis script converts these into explicit per-league and per-season core-market quality rows. If a field is absent from a scope, it is marked FIELD_ABSENT_OR_UNOBSERVED rather than silently omitted.

## 2. Current-season coverage interpretation

There are 50 selected current-season rows in the 200-season archive, but only 48 have records inside the locked historical window ending 20 September 2026. The two selected seasons with no rows in that historical window are:

| Competition | Provider season ID | First archived kickoff | Interpretation |
|---|---:|---|---|
| Australia — A-League | 17326 | 16 October 2026 | Starts after the locked window |
| India — Indian Super League | 17964 | 10 October 2026 | Starts after the locked window |

These are not missing historical matches within the locked window. Their first archived kickoff dates are later than the window end. The 48 current-season scopes with in-window data contribute 5,633 provider-complete rows.

## 3. Prematch-xG zero rates by league

Across all 50 groups and the full primary window, the highest zero rates in the team-side prematch-xG fields are:

| League | Field | Zero rows / sample | Zero share |
|---|---|---:|---:|
| India — Indian Super League | team_a_xg_prematch | 14 / 98 | 14.286% |
| South Africa — Premier Soccer League | team_a_xg_prematch | 33 / 350 | 9.429% |
| Ukraine — Ukrainian Premier League | team_b_xg_prematch | 33 / 367 | 8.992% |
| Canada — Canadian Premier League | team_a_xg_prematch | 18 / 206 | 8.738% |
| Germany — Bundesliga | team_a_xg_prematch | 36 / 414 | 8.696% |

The full-window weighted zero shares are 6.066% for team A, 6.066% for team B and 5.423% for total prematch xG. In the 48 selected current seasons with in-window data, the weighted rates rise to 13.261%, 13.297% and 11.912%, respectively.

Current-season outliers include Germany Bundesliga (18/36, 50%), England Premier League (20/50, 40%), France Ligue 1 (18/45, 40%), Greece Super League (14/35, 40%), Italy Serie A (20/50, 40%) and Italy Serie B (20/50, 40%). Samples are modest, but the zero share is large enough to warrant field-provenance investigation before using these values as model inputs.

## 4. Odds quality by league and market

### Full-time BTTS odds

The highest full-window zero share is Belgium Pro League at 89/448 (19.866%), followed by Uruguay Primera División 36/483 (7.453%), Russia Premier League 26/384 (6.771%), Venezuela Primera División 16/370 (4.324%) and Paraguay División Profesional 14/407 (3.440%).

In the selected current-season sample, Belgium Pro League is a clear outlier: 54/63 (85.714%) zero values in both BTTS Yes and BTTS No. Ukraine Premier League is 3/52 (5.769%).

### Double Chance 1X / X2 odds

The highest full-window zero shares are Belgium Pro League 95/448 (21.205%), Uruguay Primera División 49/483 (10.145%), Portugal LigaPro 40/431 (9.281%), Turkey Süper Lig 35/450 (7.778%) and Ukraine Premier League 25/367 (6.812%).

In the selected current season, Belgium Pro League again has 54/63 (85.714%) zero values for both 1X and X2. This is an odds-source/market-coverage warning, not a reason to exclude Belgian teams from Oracle predictions where odds are not an input.

### Other odds fields

- Full-time 1X2 zero share is comparatively low: 96/22,256 (0.431%) per outcome field in the full window. Current-season weighted share is 0.462%.
- Full-time Over/Under 2.5 zero share is 61/22,256 (0.274%) per field; current-season weighted share is 0.018%.
- Double Chance 12 is a different market from 1X/X2. Its zero share is 13,584/22,256 (61.035%) overall, and 39/50 groups have more than 50% zeros. Do not use this field as a proxy for Double Chance Home/Away availability.
- Draw No Bet fields have 76.321% zeros overall; they are not suitable for price analysis without a separate data-quality gate.
- All four half-specific BTTS odds fields are 100% zero in all 50 league groups. Treat these odds fields as unavailable in this archive.

## 5. Cross-field zero-count signatures

Across the 50 league groups, aggregate zero counts are equal for BTTS Yes/No (50/50 groups), Double Chance 1X/X2 (50/50), full-time 1X/X/2 (50/50), and team A/B prematch xG (47/50). This parity suggests shared field-coverage behaviour, but aggregate counts do not prove that zeros occur on the same fixtures. Row-level co-occurrence and provider semantics must be checked before calling them a common sentinel or missingness mechanism.

## 6. Operational and governance cross-check

The same commit's validation runs passed:
- Safety contract tests #419: PASS.
- Selected-50 dry-run planner #704: PASS.
- Private archive QA #30: PASS.

The planner still emits zero current governed fixture rows and zero prediction rows. Canonical fixture/team joins, official settlement truth and point-in-time xG/odds provenance remain unverified. The schedule snapshot is stale (last fixture date 17 October 2026; manifest window ends 22 October 2026). No live or paid provider calls were made.

## 7. Decision and next action

1. Treat zero odds values as unusable decimal prices until provider semantics confirm otherwise.
2. Keep prematch-xG zero rates as explicit feature-quality flags; do not automatically convert zero to missing or impute values.
3. Prioritise a row-level audit of Belgium Pro League 2026/27 BTTS and DC 1X/X2 odds, and current-season prematch-xG in Germany, England, France, Greece and Italy.
4. Verify source timestamps and field semantics before using any *_prematch field as a pre-kickoff feature.
5. Continue the separate immutable pre-kickoff prediction/settlement ledger work. Do not infer team-market suitability, predictive advantage, ROI or exclusion recommendations from these aggregate QA results.

**Governance:** research-only; no provider API calls or credits; no raw provider payload exported; no H2H holdout used; no production logic, frozen probabilities, calibration or governance changed. Production and betting eligibility remain false.

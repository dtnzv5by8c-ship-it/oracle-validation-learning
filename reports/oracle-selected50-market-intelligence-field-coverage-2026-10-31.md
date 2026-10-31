# Project Oracle — Selected-50 Market Intelligence Field-Coverage Audit

**Evidence cutoff:** 31 October 2026 (SAST)  
**Source:** Selected-50 Run #124; runtime run `41175230838`, artifact `13032880970`  
**Runtime commit:** `ea3f46dab4e54b71a818ab8d8723f36426e36bef`  
**Pinned archive SHA-256:** `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`  
**Lane:** Reporting-only; no provider API calls, no production writes.

## Executive decision

The Selected-50 QA scope contains all **50** governed league-season groups, but the fixture-level workbook is **PARTIAL_RESEARCH_ONLY**, not a complete 50-league intelligence pack and not production- or betting-ready.

- 50 selected groups enumerated; 46 have fixtures in the seven-day horizon; 4 have none.
- 434 fixture rows across those 46 groups.
- 434/434 exact archive fixture/team-order joins; 415 kickoff matches and 19 kickoff mismatches requiring manual review across 9 groups.
- 410/434 raw research outputs each for BTTS, DC_HOME and DC_AWAY.
- 24 fixtures blocked by the research runtime's feature-support gate.
- 422 experimental goal-market estimates; 12 blocked by a league baseline below 20 settled matches (A-League 5; Indian Super League 7).
- 0/434 fixtures production-eligible or betting-eligible.

## Market and field coverage

The locked 38-column fixture summary contains three supported raw Oracle research markets (BTTS Yes, Home 1X, Away X2), each populated for 410/434 fixtures (94.47%). The other 14 forecast/market fields are explicitly unavailable from this runtime output; they must not be synthesized from historical empirical rates. Historical Accuracy is not validated and A+ Setup is not graded on all 434 fixtures. Evidence-risk fields are data-coverage indicators, not outcome probabilities or predictive confidence.

The workbook's additional evidence tabs contain:
- 868 team-side form records: 844 have five overall matches; 851 have at least three. Venue-split form has five matches in 610/868 and at least three in 845/868.
- 188 exact-scope H2H meeting rows across 144/434 fixtures; 290 fixtures have no prior meeting in the current competition scope. No cross-season H2H meeting is verified.
- 434/434 provisional conventional table positions; not independently verified official historical standings.
- 434/434 numeric pre-match-labelled home/away/total xG values, but 0/434 capture timestamps. All xG remains quarantined and excluded from prediction and betting.
- 0 verified provider parent-competition IDs and 0 provider-to-canonical bridges. Source IDs are present, but canonical fixture/team joins remain unverified.

## Root cause of 24 blocked research fixtures

The existing research runtime requires five prior completed, oriented matches for each team. If either side has fewer than five, its seven last-five features are withheld; the derived pair/environment features are then also unavailable.

The existing offline diagnostic applied to Run #124 identifies:
- 24 blocked fixtures and 25 blocked team-side histories (15 home, 10 away).
- 21 affected sides have four prior oriented matches; 4 have three.
- 23 fixtures have one side below the five-match minimum; one fixture has both sides below it.
- 23 blocked fixtures have 35% model-input coverage; one has 0%.

This is a history-support gate, not evidence that the raw shots fields are universally absent. No imputation or threshold relaxation was applied. Preserve the gate; reassess when eligible history accrues. Do not change Oracle V1.6.

## Groups with no fixture in the seven-day horizon

- Republic of Ireland — Premier Division (16537)
- South Korea — K League 1 (16627)
- Canada — Canadian Premier League (16741)
- China — Chinese Super League (16789)

These are not automatically data failures, but the recurring workbook should show all 50 groups in a league-level summary tab so no-fixture groups remain visible.

## FootyStats xG provenance decision

The official documentation describes a `max_time` parameter for requesting league/team statistics as of a UNIX timestamp, and states that match statistics are usually available around 20 minutes after full-time. The reviewed documentation does not define an immutable per-fixture xG revision history or establish that `*_xg_prematch` values were frozen and available before each historical kickoff. Consequently, the 434 values remain unverified for historical pre-match use.

No live provider API call was made. Existing readiness evidence confirms only that the GitHub secret reference was present; it does not verify current key validity, account tier or monthly credit balance. Those operator checks and an explicit request budget are still required before any live provider probe.

## Next actions

1. Keep all xG quarantined until point-in-time capture and revision provenance are demonstrated.
2. Preserve the five-match research feature gate; reassess the 24 blocked fixtures as eligible history grows.
3. Reconcile the 19 kickoff mismatches against authoritative event times.
4. Add a 50-row league summary tab to the recurring Market Intelligence workbook.
5. Keep unsupported market fields explicit until a governed market-specific output exists.
6. Keep accuracy and A+ grading blocked until exact pre-match predictions, canonical identities, official settlement truth, calibration and contemporaneous odds are verified.

**Governance:** Reporting-only evidence expansion. Oracle V1.6 production logic, thresholds, calibration, raw probabilities and market definitions were not changed. No provider API credits were used. All outputs remain non-production and non-betting eligible.

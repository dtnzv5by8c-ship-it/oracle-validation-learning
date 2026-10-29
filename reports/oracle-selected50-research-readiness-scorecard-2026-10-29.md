# Oracle Selected-50 Research Readiness Scorecard — 2026-10-29

## Decision
Continue research-only predictions for fixtures with validated required features. Do not let individually blocked fixtures prevent analysis of other eligible fixtures. This is not production or betting approval.

## Verified evidence
- Snapshot run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40867886151
- Research runtime #166: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40870100742
- Snapshot-to-runtime bridge audit: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40884431781
- Bridge artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40884431781/artifacts/12902485332
- Runtime output artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40870100742/artifacts/12895297494
- Exact ID/team join coverage within the seven-day bridge window: 353/354 = 99.72%; one unmatched fixture remains in QA.
- Snapshot and runtime provenance passed: exact run IDs, artifact digest and ZIP hash, metadata, snapshot file SHA-256, selected runtime archive SHA-256 before runtime and at archive open, consumption receipt, and runtime report SHA-256.
- Runtime report contains 436 fixtures: 411 raw research predictions and 25 rows blocked for missing required features. Prediction availability is 411/436 = 94.27%; do not describe this as 95%. The separate exact identity-bridge metric is 99.72%.
- The 25 blocked fixtures are tracked in [Issue #32](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/issues/32).

## Current report-horizon coverage by league

| Country | League | Fixtures | Research predictions | Blocked | Availability |
|---|---|---:|---:|---:|---:|
| Argentina | Primera División | 15 | 15 | 0 | 100.0% |
| Australia | A-League | 6 | 6 | 0 | 100.0% |
| Austria | Bundesliga | 6 | 6 | 0 | 100.0% |
| Belgium | Pro League | 10 | 8 | 2 | 80.0% |
| Brazil | Serie A | 12 | 12 | 0 | 100.0% |
| Chile | Primera División | 8 | 8 | 0 | 100.0% |
| Colombia | Categoria Primera A | 10 | 10 | 0 | 100.0% |
| Croatia | Prva HNL | 5 | 5 | 0 | 100.0% |
| Czech Republic | First League | 8 | 8 | 0 | 100.0% |
| Denmark | Superliga | 6 | 6 | 0 | 100.0% |
| Ecuador | Primera Categoría Serie A | 8 | 8 | 0 | 100.0% |
| England | Championship | 24 | 24 | 0 | 100.0% |
| England | EFL League One | 14 | 14 | 0 | 100.0% |
| England | Premier League | 10 | 8 | 2 | 80.0% |
| Finland | Veikkausliiga | 5 | 5 | 0 | 100.0% |
| France | Ligue 1 | 9 | 8 | 1 | 88.9% |
| France | Ligue 2 | 9 | 9 | 0 | 100.0% |
| Germany | 2. Bundesliga | 9 | 6 | 3 | 66.7% |
| Germany | Bundesliga | 9 | 6 | 3 | 66.7% |
| Greece | Super League | 7 | 6 | 1 | 85.7% |
| India | Indian Super League | 6 | 5 | 1 | 83.3% |
| Italy | Serie A | 12 | 12 | 0 | 100.0% |
| Italy | Serie B | 10 | 8 | 2 | 80.0% |
| Japan | J1 League | 10 | 10 | 0 | 100.0% |
| Mexico | Liga MX | 9 | 9 | 0 | 100.0% |
| Netherlands | Eredivisie | 9 | 9 | 0 | 100.0% |
| Norway | Eliteserien | 8 | 8 | 0 | 100.0% |
| Paraguay | Division Profesional | 11 | 11 | 0 | 100.0% |
| Peru | Primera División | 12 | 12 | 0 | 100.0% |
| Poland | Ekstraklasa | 9 | 8 | 1 | 88.9% |
| Portugal | LigaPro | 9 | 7 | 2 | 77.8% |
| Republic of Ireland | Premier Division | 5 | 5 | 0 | 100.0% |
| Romania | Liga I | 8 | 8 | 0 | 100.0% |
| Russia | Russian Premier League | 8 | 8 | 0 | 100.0% |
| Saudi Arabia | Professional League | 9 | 8 | 1 | 88.9% |
| Scotland | Premiership | 3 | 3 | 0 | 100.0% |
| Serbia | SuperLiga | 7 | 7 | 0 | 100.0% |
| South Africa | Premier Soccer League | 15 | 12 | 3 | 80.0% |
| Spain | La Liga | 10 | 10 | 0 | 100.0% |
| Spain | Segunda División | 11 | 10 | 1 | 90.9% |
| Sweden | Allsvenskan | 11 | 11 | 0 | 100.0% |
| Switzerland | Super League | 6 | 6 | 0 | 100.0% |
| Turkey | Süper Lig | 9 | 8 | 1 | 88.9% |
| USA | MLS | 15 | 15 | 0 | 100.0% |
| Ukraine | Ukrainian Premier League | 8 | 7 | 1 | 87.5% |
| Uruguay | Primera División | 8 | 8 | 0 | 100.0% |
| Venezuela | Primera División | 8 | 8 | 0 | 100.0% |

### Selected groups with no fixtures in the current seven-day horizon
- Canada — Canadian Premier League (selected ID 16741)
- China — Chinese Super League (selected ID 16789)
- South Korea — K League 1 (selected ID 16627)

These are schedule-horizon gaps, not evidence that those leagues are unsupported. Recheck them on the next snapshot.

## Market readiness and restrictions
- The 250 league-market diagnostics do not approve a market edge; all `edge_claim` fields remain `NOT_APPROVED`.
- BTTS raw holdout accuracy was 53.588% versus a 54.143% majority-class baseline; no demonstrated edge on that accuracy metric.
- Double Chance metrics are raw and uncalibrated; positive Brier-skill diagnostics are research evidence only, not proof of profitable betting performance.
- Combo probabilities remain masked due to an unresolved target-versus-settlement mismatch.
- Provider parent-competition IDs/canonical bridges remain unverified; canonical fixture/team join fields remain unverified in the runtime report.
- Point-in-time xG, standings and odds provenance remains unverified; xG/odds are excluded as model features. Official settlement truth is not established.
- All rows remain `production_eligible=NO`; betting eligibility remains false.

## Operating rules
1. Proceed with research predictions only for fixtures whose required features and source-safety checks pass.
2. Keep the 25 feature-blocked fixtures in Issue #32; do not impute missing data. Reassess on future runs and clear only when the real features pass validation.
3. Keep the one unmatched fixture and the 83 matched-but-source-quarantined rows in the bridge QA exception tracking; do not treat source-quarantined rows as eligible just because IDs match.
4. Use >=95% as the exact identity-bridge coverage target. Always report prediction availability separately.
5. Do not change production model logic, frozen probabilities, thresholds, calibration or production ledgers.
6. No production or betting release until the separate canonical identity, point-in-time integrity, official settlement truth, calibration and market readiness gates are explicitly approved.

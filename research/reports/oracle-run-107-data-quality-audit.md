# Oracle Completion Run #107 — Research-Only Data Quality Audit

**Date:** 2026-10-22  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning` (public research repository)  
**Run:** [Oracle Completion Run #107](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39772347617)  
**Classification:** Research/reporting only. No production model, weights, thresholds, calibration, or probabilities are changed by this report.

## Executive result

Run #107 completed successfully as a workflow, but the prediction reconciliation is **PARTIAL** and production promotion remains **BLOCKED**.

- 244 scheduled fixture rows; 234 fixtures reconciled with predictions (95.9016%); 10 excluded.
- 5,148 fixture-market prediction rows across 22 markets; all exported probability fields are populated for predicted rows.
- 165 scheduled fixtures have no verified kickoff timestamp in the run's audit; 79 have a timestamp.
- The schedule has fixtures in 26 leagues against 27 configured leagues. One configured league has no fixtures in the selected window.
- Historical baseline unchanged; calibration not applied; production promotion not allowed.

## Duplicate-run comparison (#106 versus #107)

The fixture schedule export and current pre-match team-state export were exactly equal between runs. Prediction outputs contained the same 5,148 rows and the same market/fixture structure; the generated timestamp changed and the numeric probabilities differed only at tiny floating-point precision. Run #107 therefore did not materially improve coverage over #106. Do not trigger another duplicate completion run to obtain another copy.

## Root cause analysis: 10 excluded fixtures

All 10 exclusions have the same gate reason: `MISSING_PREMATCH_TEAM_STATE`. This is not one single failure mode. The exported state/history snapshots show a mixture of (a) plausible label/alias mismatch candidates and (b) teams with no exact-name history in the exported snapshot. Similarity candidates are leads only, not approved mappings.

| Fixture | Missing state | Audit finding | Safe next action |
|---|---|---|---|
| Pau FC vs Grenoble (Ligue 2) | Home role history | No exact-name Pau FC rows or plausible alias in exported snapshots; Grenoble history exists | Verify source coverage/team ID; do not infer a mapping |
| Almere City vs Roda (Eerste Divisie) | Both roles | Candidate `Almere City FC` (similarity 0.909); no exact-name history for either scheduled label | Verify both official IDs and competition before mapping |
| Jong AZ vs Helmond (Eerste Divisie) | Both roles | No plausible exact/near history surfaced for these labels in exported snapshots | Verify provider/competition coverage and IDs |
| Oss vs Jong Ajax (Eerste Divisie) | Home role | No exact-name Oss history; Jong Ajax has state history | Verify whether the scheduled label maps to an approved canonical club |
| Westerlo vs Beveren (Belgian Pro League) | Away role | Candidate `SK Beveren` (similarity 0.875); Westerlo state history exists | Verify the club and competition ID; do not auto-map |
| Brno vs Bohemians (Czech First League) | Home role | No exact-name Brno history; `Bohemians 1905` appears as the likely full label, but identity still needs source-ID confirmation | Verify both team IDs and competition |
| Dordrecht vs Venlo (Eerste Divisie) | Both roles | Candidate `FC Dordrecht` (similarity 0.900); no exact-name history for either scheduled label | Verify official IDs and historical coverage |
| Wisla vs Rakow (Ekstraklasa) | Both roles | No plausible alias found for either short label in exported snapshots | Resolve full club names and IDs from an independent source |
| Braunschweig vs Hannover (2. Bundesliga) | Home role | No exact-name Braunschweig history; `Hannover 96` appears as a likely full label, but needs source-ID confirmation | Verify both official IDs and competition |
| PSV vs Feyenoord (Eredivisie) | Home role | No exact-name PSV rows in exported state snapshot; Feyenoord state history exists | Check why PSV's history is absent before any prediction is released |

**Interpretation:** some candidates point toward label mismatch, but similarity alone is not sufficient to safely repair a team mapping. For teams with no exact history, the next step is to establish whether the governed historical source lacks records or uses another verified identifier. The durable fix is a verified team/competition identity crosswalk plus coverage checks before rebuilding pre-match state—not fuzzy auto-mapping.

## Kickoff data quality

The workflow's fixture audit reports 165 fixtures without verified kickoff timestamps and 79 with timestamps. Missing kickoff counts by league code:

| League code | Missing kickoff fixtures |
|---|---:|
| AUT | 5 |
| B1 | 8 |
| CZE | 8 |
| D2 | 8 |
| E1 | 12 |
| E2 | 12 |
| E3 | 12 |
| F2 | 9 |
| I1 | 4 |
| I2 | 16 |
| N1 | 9 |
| NED2 | 7 |
| P1 | 8 |
| POL | 8 |
| POR2 | 8 |
| SC0 | 12 |
| SP1 | 3 |
| SP2 | 10 |
| T1 | 6 |

The fixture CSV contains only `league_code,date,home_team,away_team,kickoff_time`; many kickoff values are blank. The audit says kickoff is not required for eligibility, so a row can receive predictions without a verified kickoff. For betting use, this must be treated as a reporting/data-quality gate: independently verify kickoff time and fixture identity before a selection is called actionable. Do not fill missing times with assumptions.

## Historical benchmark / calibration

The run's expanding walk-forward benchmark is development-only (27 leagues, 22 markets, 214,464 prediction rows across the benchmark artifact). The report shows calibration worsened Brier score and log loss for reported markets. Example: BTTS Yes raw Brier 0.247863 versus calibrated 0.250422; raw log loss 0.688851 versus calibrated 0.712527. Calibration remains unapplied. These metrics are probability-quality metrics, not betting hit rate or proof of profitability.

## Required next actions

1. Build/verify official team-ID and competition-ID mappings for the 10 excluded fixtures. Never approve mappings from similarity alone.
2. Trace missing state records back to their source: separate absent historical match coverage from name/crosswalk mismatch; rebuild pre-match state only after verification.
3. Add a reporting-only readiness gate that flags fixtures without independently verified kickoff timestamps and identity, without changing model logic.
4. Reconcile the 27 configured leagues against the actual fixture universe and document the league with no fixtures in the selected window.
5. Complete historical hit-rate evaluation only from verified prediction-to-settlement joins with pre-kickoff timestamps and documented settlement definitions.
6. Keep production promotion blocked until these gates pass. Do not alter production model logic, weights, thresholds, calibration, or probabilities based on this audit.

## Evidence sources

- Run #107 completion report and fixture-level artifact, downloaded from the public workflow artifacts.
- `oracle_upcoming_fixtures.csv`, `four_model_live_predictions.csv`, `current_prematch_team_state.csv`, `matches.csv`, `tmp/oracle-fixture-audit.json`, and `tmp/oracle-live-reconciliation.json` from Run #107's fixture-level artifact.
- Comparison against Run #106's equivalent fixture-level artifact.

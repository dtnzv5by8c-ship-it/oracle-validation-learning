# Project Oracle — Team & H2H DNA Run 3: Market Reliability and Recency

**Timestamp:** 31 October 2026, 01:19 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** research-only; no production or betting eligibility

## Executive result

This incremental pass extends the saved Team/H2H DNA checkpoint. It does not repeat ingestion, snapshot, runtime or bridge workflows and uses no provider/API credits. It adds uncertainty and recency analysis to exact-ID Team/H2H profiles, preserves the latest ranking/lag workbook, and records a ranking-currentness warning.

- **Team profiles:** 732 exact composite keys across 31/50 governed groups.
- **H2H profiles:** 7188 exact pair keys and 23,328 chronological meetings.
- **Team market tendencies:** 2,120 team/window rows covering 10 outcomes and all-history, primary and recent365 windows; home-away deltas included.
- **H2H market reliability:** 7,188 exact-pair rows with Wilson intervals for BTTS, Over 1.5/2.5/3.5 and draw.
- **H2H recency:** 7,188 exact pair profiles with meeting gaps, recency share and last-five vs prior comparisons.
- **Identity key warning:** 58 provider team_id values recur across selected groups; `selected_id + team_id` is mandatory.

## 1. Exact data integrity and coverage

- Run64 archive SHA-256: `65aca16d0562745576f1499d25808498a560b5167cdf00bc86074f8e4c20211a`.
- Full archive ledger: 50/50 exact selected IDs, 200 seasons and 59,049 archived rows; raw provider payload is not publicly saved in the ledger (lineage SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`).
- Raw JSON is available for 31/50 selected groups; 19 remain unprofiled because their raw match JSON is not in the accessible Run64 extract. This is an access gap, not a zero-match finding.
- Included rows require complete status, numeric scores and UTC kickoff through 20 September 2026. Primary window remains 20 March 2025–20 September 2026.
- Exact ledger: 23,328 rows, 23,328 unique fixture IDs, zero duplicate fixture rows; both record-level hashes present for 100%.
- `no_home_away=1`: 2,603 matches; retained for overall team outcomes but excluded from venue splits. Venue-valid rows: 20,725.
- Team keys: 732 unique composite keys; 58 provider team IDs recur across selected groups. All profiles have one observed exact name variant within the selected group; canonical cross-provider identity remains unverified.

## 2. Team Market Tendencies

The new tab reports BTTS Yes, Over 1.5/2.5/3.5, team-to-score, clean sheet, failed-to-score, team win, draw and non-loss for all available history, the primary window and trailing 365 days. Each row includes sample size, rate, Wilson 95% interval, exact league baseline, deviation, fixture-set hash and provenance coverage; home-minus-away market deltas are included.

Wilson intervals are unadjusted descriptive intervals; multiple comparisons are not corrected. They are not forecast calibration intervals or fixture-level Oracle probabilities. HOME/AWAY samples are already represented in the existing Team Venue DNA tab and exclude `no_home_away=1`.

## 3. H2H Market Reliability and Recency

The H2H reliability tab adds Wilson intervals and league baselines for BTTS, Over 1.5/2.5/3.5 and draw. The recency tab adds first/last meeting dates, days since last meeting at archive cutoff, meeting-gap statistics, last-365/730 counts, chronological halves, last-five shifts and exact fixture-set hashes.

Only 159 of 7,188 pairs have at least eight meetings; 7,029 have fewer than eight. Eight meetings is a minimum descriptive split-screen threshold, not proof of predictive reliability. H2H outcomes are score-derived, not official settlement truth; squads and managers change over time.

## 4. Repeatable scoring screens carried forward

- Team scoring: 13 high and 7 low profiles persist across all-history, primary and recent365 overlapping windows.
- H2H scoring: 9 high and 6 low pairings pass the saved chronological stability screen.

Illustrative team profiles from the strict screen (all / primary / recent365 samples and Over 2.5 rates):

- High-scoring: PSV — n=75/49/36; mean total goals 4.29/4.37/4.31; Over 2.5 86.7%/87.8%/91.7%.
- High-scoring: Bayern München — n=72/46/34; mean total goals 4.24/4.48/4.50; Over 2.5 84.7%/91.3%/91.2%.
- High-scoring: Inter Miami — n=103/62/38; mean total goals 3.99/4.18/4.37; Over 2.5 78.6%/80.6%/81.6%.
- Low-scoring: Getafe CF — n=83/55/41; mean total goals 1.86/1.93/1.73; Over 2.5 28.9%/30.9%/22.0%.
- Low-scoring: Argeș — n=50/50/40; mean total goals 1.94/1.94/1.68; Over 2.5 28.0%/28.0%/22.5%.

Illustrative H2H patterns (all meetings; last five in parentheses): Dinamo Zagreb–Istra 1961, 9 meetings, 3.56 average total goals and 88.9% Over 2.5 (last five: 3.2 goals, 80% Over 2.5); Inter Miami–Nashville SC, 9 meetings, 4.11 goals and 100% Over 2.5 (last five: 4.0 goals, 100%); Osijek–Gorica, 9 meetings, 1.67 goals and 11.1% Over 2.5 (last five: 1.4 goals, 0%). H2H samples are only 8–9 matches in these examples and remain descriptive, not reliable betting signals.

These overlapping windows are not independent OOS confirmation. Existing H2H backtest evidence remains mixed (Brier improvement in 2/5 BTTS, 3/5 DC_HOME and 1/5 DC_AWAY folds); no H2H weighting increase is recommended.

## 5. Ranking-currentness QA

The newer 01:08 SAST research register reports **319 current rankable candidates per market**, 37 selected groups and **zero quarantined or kickoff-mismatched rows in each Top 50**. It excludes fixtures already started by 01:08 (`8409576`, `8432243`, `8432245`) and retains the Saudi kickoff-mismatch exclusions (`8620566`, `8620618`, `8620625`).

The older `oracle-selected50-top50-ranking-qa-2026-10-31.csv` still reports 3/2/9 quarantined rows, while the newer `repo_oracle_selected50_ranking_qa_2026-10-31-0108.csv` reports 0/0/0. The newer register is used for QA counts. Its row-level refreshed Top 50 fixture list is not attached, so existing workbook Top 50 tabs are marked **superseded / not current** rather than silently reused.

The candidate-level evidence is also saved as compact CSVs in the research branch: `reports/oracle_selected50_team_scoring_candidates_run3_2026-10-31.csv` and `reports/oracle_selected50_h2h_scoring_candidates_run3_2026-10-31.csv`. These preserve the exact team/pair keys and the sample windows behind the named examples.

## 6. Workbook and governance

- Workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v7_Team_H2H_Market_Reliability.xlsx`
- Workbook SHA-256: `75774dcf45d8228d4a3f403a2b6a7c6200631603830a4420897dd236be808df9`
- Base ranking workbook SHA-256: `e7471a7f7a82658d90aa293b27513383f72a18b6db1f01fb3c56cc3b117b7802`
- Detailed Team/H2H source workbook SHA-256: `caf389b64f8713d77b36c95da7ab4215358c6949238e4a47027d00b2f134ce13`
- Sheet count: 55
- Validation: `{"h2h_dna_rows": 7188, "h2h_market_rows": 7188, "h2h_meetings_rows": 23328, "h2h_recency_rows": 7188, "identity_rows": 732, "ranking_qa_rows": 3, "sheet_count": 55, "team_dna_rows": 732, "team_market_rows": 2120, "unprofiled_rows": 19}`

Provider/API credits used: **0**. Ingestion/snapshot/runtime/bridge workflows rerun: **none**. Oracle V1.6 logic/probabilities/calibration changed: **no**. `production_eligible=false`; `betting_eligible=false`.

## Next priority

1. Restore raw JSON for the remaining 19 selected groups from the existing archive through a read-only path.
2. Attach the exact 01:08 row-level Top 50 export before replacing superseded ranking tabs.
3. Continue only with verified point-in-time data; do not modify Oracle V1.6.
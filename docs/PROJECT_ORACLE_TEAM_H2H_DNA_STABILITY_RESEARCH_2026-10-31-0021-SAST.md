# Project Oracle — Team & H2H DNA Stability Research
**Date:** 31 October 2026, 00:21 SAST  
**Branch:** research/oracle-50-league-readiness-audit  
**Status:** Research-only; production_eligible=false; betting_eligible=false.

## Findings

- The full selected-50 archive ledger verifies 50/50 exact selected-ID matches, 200 seasons and 59,049 archived match rows. It also records that raw provider payload was not saved publicly.
- The accessible Run64 raw match extract contains 31/50 governed groups (93 season folders; 30,257 raw rows). It yields 23,328 complete, dated, numeric-score matches through 20 September 2026. The remaining 19 groups exist in the full archive ledger but their raw match JSON is absent from the accessible extract. This is a payload-access gap, not an ID-mapping failure or evidence of zero teams/matches.
- Team DNA: 732 exact provider-ID profiles across the 31 available groups, keyed by selected_id + team_id. 58 provider team IDs recur across groups, so team_id alone is not a safe key.
- H2H DNA: 7,188 exact pair profiles and 23,328 chronological meetings. Only 159 pairings have 8+ meetings; 3,273 have 1–2 meetings.
- Strict team scoring screen: 13 high and 7 low profiles persist across all-history, primary-window and trailing-365-day windows. Seven earlier two-window candidates fail the recent-365 confirmation. These windows overlap and are descriptive, not independent validation.
- Strict H2H screen: 9 high and 6 low pairings retain direction across the whole sample, chronological halves and last five meetings. Small samples are not treated as reliable.
- Venue integrity: 2,603 no_home_away=1 matches are retained for scoring and team-relative W/D/L, but excluded from home/away splits and league home/draw/away rates. 20,725 venue-valid matches remain.

## Model and fixture evidence

The governed primary validation window remains 20 March 2025–20 September 2026 (15,003 matches in the accessible extract). Calendar-year extract counts are 2024: 5,715 (partial for 27 of 31 groups), 2025: 10,307, and 2026 through 20 September: 7,306.

Existing runtime #176 H2H paired evidence covers 19,991 holdout fixtures at 95.75% feature coverage with chronology QA passing. H2H improved Brier in 2/5 BTTS folds, 3/5 DC_HOME folds and 1/5 DC_AWAY folds. Do not increase H2H weighting.

Runtime #176 contains 426 fixture rows, 403 raw predictions and 23 feature-blocked rows. The committed ranking checkpoint records 347 exact future candidates, 79 source-quarantined rows and 325 rankable candidates per core market across 33 league names / 37 country-league groups. Top-three-per-country/league output has 111 rows per market. Top-50 source-quarantine counts are BTTS 3, DC_HOME 2 and DC_AWAY 9. All probabilities are raw and uncalibrated; confidence score is not calculated and data-risk percentage is not quantified.

The committed three-fold feature-edge summary supports only two DC_HOME challenger candidates: RECENT_GOALS_STRENGTH and VENUE_SPLITS (Brier, log-loss and AUC improved in 3/3 folds; ECE in 2/3). No BTTS or DC_AWAY family passed the overall gate. xG, shots, standings and odds remain excluded pending point-in-time provenance; rest/travel was not tested. This is not Oracle V1.6 and does not authorise a production change.

## Corrections and controls

A previous note described 19 groups as lacking an exact selected-ID bridge. The full archive ledger now proves exact selected-ID mapping for all 50 groups. The actual limitation is raw match JSON access for 19 groups in the Run64 extract. Keep those groups unprofiled/unavailable; do not zero-fill or infer team identities.

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflows were rerun. Oracle V1.6 production logic and probabilities were not changed. The separately generated v5 workbook binary was not mounted in this run; this v6 workbook was rebuilt from the accessible v3 workbook and committed runtime/feature-edge artifacts. Aggregated feature summaries are included; unavailable per-fold feature metrics were not fabricated.

## Output and next step

Workbook: Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v6_Team_H2H_Stability.xlsx  
SHA-256: caf389b64f8713d77b36c95da7ab4215358c6949238e4a47027d00b2f134ce13  
Size: 10,211,909 bytes; 39 sheets.

Next priority: expose the existing raw match JSON for the remaining 19 selected groups through a read-only route from the private archive. Do not spend provider/API credits or rerun ingestion.

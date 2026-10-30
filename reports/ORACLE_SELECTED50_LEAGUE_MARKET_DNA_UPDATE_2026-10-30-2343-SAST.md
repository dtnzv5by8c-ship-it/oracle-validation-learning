# Project Oracle — Selected-50 League DNA & Market Suitability
**Date:** 30 October 2026, 23:43 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** Research-only; production logic and frozen probabilities unchanged.

## Findings
- Full selected-50 archive lineage: run 40375285207; 50 groups, 200 seasons, 59,049 raw rows; SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- The available supplementary score extract maps by exact selected season ID to 31/50 leagues and contains 23,328 completed, dated, numeric-score matches. The remaining 19 leagues have no exact-ID match in this extract; their rates are blank, not zero.
- Calendar-year scope: 2024 is complete for only 4/31 extract leagues (Argentina Primera División, Brazil Serie A, Norway Eliteserien, USA MLS); 27/31 are partial due to missing earlier season-folder rows. 2025 reconciles to full calendar-year completed-score counts for 31/31. 2026 covers the primary-window boundary through 20 September 2026 for 31/31, not the full calendar year.
- 1X2 rates exclude completed rows with `no_home_away=1`; scoring totals, BTTS, overs, clean sheets and failed-to-score rates use completed numeric scores.
- Three-fold walk-forward screen across 50 leagues × BTTS/DC_HOME/DC_AWAY: 26 repeatable positive-skill combinations (2 BTTS, 11 DC_HOME, 13 DC_AWAY), 13 positive-skill with calibration warning, 47 mixed, 60 insufficient sample/metric, 4 no positive skill. 17 leagues have at least one repeatable diagnostic candidate. These are not betting recommendations; labels remain provisional and raw probabilities uncalibrated.
- Current runtime #176 (run 41119141526) used snapshot 41117910952 / artifact 13005239530. Bridge audit #12 passed with release blockers: 426 exact snapshot-to-runtime fixture/team-ID matches, 347 future research candidates and 79 source-quarantined. This validates the bridge lineage only; canonical competition/fixture/team identity and official settlement truth remain unverified. The runtime has 403 raw predictions and 23 feature-blocked rows across 46/50 leagues.
- Top-50 raw rankings were added for BTTS, DC_HOME and DC_AWAY. Source-quarantined rows retained for visibility: BTTS 3/50, DC_HOME 2/50, DC_AWAY 9/50. All probabilities remain `RAW_ONLY_UNCALIBRATED`; canonical fixture/team joins and official settlement truth remain unverified.

## Repository-side 50-league summary
[oracle-selected50-league-market-dna-summary-2026-10-30.csv](oracle-selected50-league-market-dna-summary-2026-10-30.csv)

The consolidated Excel workbook with detailed year profiles, market suitability and three top-50 ranking tabs is provided as the run attachment.

## Next evidence required
Read-only raw match rows for the 19 unmatched leagues and missing early-2024 season segments; full 2026 score rows after 20 September; verified canonical competition/fixture/team identity; point-in-time xG/odds provenance; and authoritative market settlement definitions.

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. `production_eligible=false`; `betting_eligible=false`.

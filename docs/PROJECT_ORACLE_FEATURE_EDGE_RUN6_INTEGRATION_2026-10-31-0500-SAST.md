# Project Oracle — Feature Edge Run 6: Team/H2H Integration

**Run:** 31 October 2026, 05:00 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** research-only; `production_eligible=false`; `betting_eligible=false`

## Executive result

Integrated the completed Team/H2H Run 6 integrity checkpoint into the Feature Edge master. The 95-tab Run 5 Feature Edge workbook was extended to 106 tabs; all 95 existing worksheet XML parts remain byte-for-byte unchanged. The separate 101-tab Team/H2H workbook is a different v11-based consolidation; its verified evidence is integrated here without replacing the Feature Edge Run 4/Run 5 tabs.

No provider/API credits were used. No ingestion, snapshot, runtime, backtest or bridge workflow was rerun. Oracle V1.6 logic, probabilities and calibration were not changed.

## Team and H2H evidence

- 732 exact selected_id + provider team_id profiles across 31/50 raw-data groups. Team median Kish ESS: 62.54 (365d) and 70.73 (730d); 648/732 have ESS >=30 at 365d and 650/732 at 730d.
- 7,188 exact selected_id + ordered provider team-ID H2H pairs and 23,328 chronological completed-score meetings.
- Run 6 corrected the Run 5 H2H tier label: 318 is the 5 <= ESS <8 band at both half-lives, not the inclusive BOTH >=5 total. Correct inclusive ESS >=5 under both settings is 386 (=1+67+318).

| Corrected mutually exclusive H2H ESS screen | Pairs |
|---|---:|
| ESS >=8 at both 365d and 730d | 1 |
| ESS365 5–<8; ESS730 >=8 | 67 |
| ESS 5–<8 at both | 318 |
| ESS365 <5; ESS730 >=5 | 174 |
| ESS <5 at both | 6,628 |

Only one pair clears ESS >=8 at both half-lives: LASK Linz vs Hartberg (selected_id 17181; provider IDs 595/599), 10 meetings, ESS 8.3826/9.5365, five meetings in trailing 365 days. Fixture-ID-set SHA-256: `ee0caf57cddc938f7eeb060d811572d70e4febf67128c7c398b3d9c6f0b1d111`. Team A/B is provider-ID order, not home/away; canonical cross-provider identity and official settlement truth remain unverified.

Decision: do not increase H2H weighting. The 13 Run 5 team scoring candidates (9 high, 4 low) retained the required 0.50-goal and 10pp Over 2.5 directional margins under 365d/730d x k10/k20; this is sensitivity robustness, not independent OOS validation.

## Coverage and feature decisions

The full archive ledger has 50/50 exact selected IDs, 200 seasons and 59,049 raw match rows. The accessible Run64 extract has 31/50 groups, 93 season folders, 30,257 raw rows and 23,328 completed scored matches. The other 19 groups remain unavailable; do not zero-fill or substitute another provider's different 27-league scope.

No new pre-kickoff publication provenance became available, so no new feature-family ablation was run. Run 4's three-fold challenger results remain unchanged: DC_HOME recent goals/strength and venue splits remain research candidates; BTTS effects remain marginal; DC_AWAY effects remain rejected where calibration deteriorated. These are challengers versus smoothed league prevalence, not incremental tests against frozen Oracle V1.6. xG, shots, historical standings, bookmaker odds, rest/travel and isolated clean-sheet/failed-to-score effects remain blocked or descriptive pending immutable PIT provenance.

## Fixture rankings

Top 50 and Top 3 tabs are carried forward unchanged from 31 October 2026 03:02:03 SAST: 319 rankable candidates across 37/50 groups; 50/50 exact runtime/bridge matches per market; zero quarantined rows and zero kickoff mismatches in each Top 50; 111 Top-3-per-league rows and three Top-3-overall rows per market. Snapshot age at 05:00:33 SAST was 7.23 hours; earliest Top-50 kickoff was 07:00 SAST. No new snapshot/runtime/bridge artifact was available, so rankings were not refreshed.

Probabilities remain raw and uncalibrated. Rankings are not betting recommendations or production approvals.

## Workbook

- File: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v13_Run6_Feature_Edge_Team_H2H_0500SAST.xlsx`
- SHA-256: `0216ab9435190471d334cd5bf10630485e85d1a93abd7a353986b40dd0244d0c`
- 16,926,465 bytes; 106 tabs; 95 original worksheet XML parts byte-identical.
- Eleven new tabs: Run6 Executive Summary; Team Effective Sample; H2H Pair ESS Audit; H2H ESS Leaders; Team Robustness; Profile QA; 50-League Coverage; Source Lineage; H2H Correction; Feature Edge Update; Ranking Currentness.

Source Team/H2H checkpoint: `reports/oracle_selected50_team_h2h_run6_checkpoint_2026-10-31-0423-sast.json` (blob SHA `9bac5920c1cc0c5effa997e1b967a9052518631e`).

Governance: provider/API credits 0; workflow reruns 0; production logic/probabilities/calibration unchanged; production_eligible=false; betting_eligible=false.
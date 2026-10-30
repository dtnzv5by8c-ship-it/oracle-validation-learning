# Oracle Data & Team DNA — Cross-Scope Reconciliation Checkpoint

**Date:** 30 October 2026, 08:23 SAST  
**Branch:** research/oracle-50-league-readiness-audit  
**Source:** Private Archive QA #35, run 41012121829, artifact 12957738691  
**Pinned archive SHA-256:** af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875

## Verified findings

- Corrected the xG comparison to include all 48 current-selected league groups with primary-window rows. Team A prematch xG zeros: 747/5,633 (13.26%) current vs 577/16,318 (3.54%) non-current in the same groups; +9.72 pp. Team B +9.78 pp; total +8.75 pp.
- The 11-group threshold-selected subset remains separately reported; it is not a 50-league estimate.
- Across 48 groups, 2,160/2,167 prematch-zero field-pair observations (99.68%) co-occur with positive postmatch xG. These are pair observations, not unique fixtures.
- Four first/second-half BTTS odds fields are zero across all 59,049 archive rows. Current-scope DC 12, DNB and first-goal odds are >99% zero.
- Belgium BTTS Yes/No and DC 1X/X2 share an identical 54-zero/9-positive mask; other 47 groups show 0.52% BTTS Yes zeros and 0.57% DC 1X/X2 zeros.
- 48/50 current-season groups have primary-window rows; Australia A-League and India Indian Super League have none in this event window.

## New outputs

- scripts/audit_selected50_xg_odds_crossscope_reconciliation.py
- tests/test_selected50_xg_odds_crossscope_reconciliation.py — six local regression tests passed.
- docs/PROJECT_ORACLE_XG_ODDS_CROSSSCOPE_RECONCILIATION_2026-10-30.md
- The script generates a JSON summary and three sanitized CSVs for the next private-archive QA artifact.

## Blockers and next action

- Existing sanitized QA has no field retrieval/update timestamps, bookmaker/source IDs or quote timestamps. Manual review of existing archive ingestion metadata or archive-owner documentation is required to establish xG and odds semantics. No provider calls or credits.
- Official settlement truth remains unverified. The existing ledger adapter audit reported 210 rows missing home-team IDs and 210 missing away-team IDs, with zero rows eligible for scoring. Do not repeat the separate identity or H2H lane.
- Team-market accuracy/calibration remains blocked until a strictly pre-kickoff prediction ledger, canonical team/fixture joins and independently verified settlement truth exist.

## Governance

Research-only. No H2H holdout access, provider/API calls, production logic, frozen probability, calibration or governance changes. Keep all 50 leagues in the research universe; no exclusions from descriptive rates.

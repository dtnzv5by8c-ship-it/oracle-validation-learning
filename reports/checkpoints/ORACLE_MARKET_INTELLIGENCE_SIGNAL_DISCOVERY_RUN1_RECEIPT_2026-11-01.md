# Oracle Market Intelligence Signal Discovery — Run 1 Commit Receipt

Date: 1 November 2026
Research branch: research/oracle-50-league-readiness-audit

Analysis commit SHA: 2f19e822782a81d1a284616e16debb7302c44529
Parent commit SHA: 9c144f5b4230f502c90c84971c0a78a42e5fccb5

Committed:
- scripts/analyze_selected50_market_intelligence_actual_signals.py
- tests/test_selected50_market_intelligence_actual_signals.py
- reports/checkpoints/ORACLE_MARKET_INTELLIGENCE_SIGNAL_DISCOVERY_RUN1_2026-11-01.md

Validation:
- Eight dedicated unit tests passed locally against the committed code.
- Repository Safety Contract Tests workflow run 41341044529: all substantive test steps completed successfully; post-job cleanup was still in progress when checked.
- Selected-50 Dry-Run Planner workflow run 41341044552: all substantive planner and regression-test steps completed successfully; post-job cleanup was still in progress when checked.
- No Market Intelligence repair workflow was triggered by these research-only paths.
- No provider API calls or credits used.

Primary finding:
The five-match strict 204-fixture diagnostic identifies recent PPG differential, qualified venue form and the Home Strength × Away Weakness interaction as candidate home-result signals. No robust BTTS or goal-total feature signal was found. These remain research-only until the interactions pass the full chronological 18-month validation against league and frozen Oracle V1.6 baselines.

Blockers:
Provisional standings, unverified xG capture timestamps, 24 feature-field gaps, four schedule-review fixtures, and the existing goal-market engine's three-match minimum remain unresolved. Do not relax the five-match minimum.

Next:
Add the two prespecified interactions to the historical feature-edge ablation, enforce five observed matches overall and by venue, and evaluate fold-level Brier, log loss, AUC and ECE with confidence intervals. No production changes are authorized.

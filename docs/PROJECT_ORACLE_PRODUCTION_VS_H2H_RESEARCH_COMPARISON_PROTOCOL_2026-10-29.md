# Project Oracle — Production vs H2H Research Comparison Protocol
**Date:** 2026-10-29  
**Status:** Research plan; implementation and results pending  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Production protection:** No production model logic, frozen probabilities, thresholds, calibration, or governance may be changed by this experiment.

## Decision
Run a paired, leakage-controlled comparison between the frozen production benchmark (where its exact historical predictions and version can be recovered) and a research-only model that uses the existing multi-season FootyStats archive, including eligible 2024 history, and explicit H2H features. The existing primary holdout (2025-03-20 through 2026-09-20) remains unchanged for comparability. A separate chronological backtest can assess the broader archive without replacing the primary holdout.

## Important distinction
2024 is not itself a model. It is historical training/context data. The meaningful comparison is:
- Baseline: the existing frozen production model and/or exact reproducible baseline model.
- Candidate: a research model trained only on data available before each target kickoff, using the same test fixtures where possible and H2H features validated before kickoff.

If the exact production model version, historical predictions, or feature snapshot cannot be reconstructed, label the comparison “reproducible research baseline vs H2H candidate,” not “production vs research.” Never imply a model was production if it was reconstructed.

## Data and feature rules
1. Use the existing private FootyStats archive; no new provider API calls are needed merely to access the already ingested 2024 records.
2. Use only explicitly finished matches with valid non-negative integer scores as H2H outcomes.
3. Enforce strict kickoff chronology; exclude same-time/future matches, target fixture itself, invalid statuses, duplicate fixture IDs, and ambiguous team/competition joins.
4. Audit team ID stability across season files. H2H should be competition-scoped unless an explicitly validated cross-competition identity policy is approved.
5. H2H feature candidates: prior meeting count, last-five result sequence from target home-team perspective, last-five BTTS rate, last-five mean total goals, recency of last meeting, and optionally recency-weighted outcomes. No imputation for absent H2H; report coverage and compare on matched test subsets.
6. Current table snapshots, actual/post-match xG, untimestamped odds, and any feature whose point-in-time availability is unverified remain excluded from predictive inputs.
7. Preserve the current baseline feature set as a separate model; do not silently add H2H to its existing 20 features.

## Evaluation design
- Primary paired holdout: 2025-03-20 through 2026-09-20, unchanged.
- Additional chronological expanding-window or rolling-origin tests that include 2024 as training history where appropriate; every fold must train strictly before its test start.
- Evaluate the same fixtures for baseline and H2H candidate; report the H2H-available subset separately and report coverage loss from H2H gating.
- Markets: BTTS, Double Chance Home/Away and Combo only after settlement contract is resolved. Keep Combo masked while settlement truth differs.
- Metrics: sample size, accuracy at a declared threshold, Brier score, log loss, AUC where both labels occur, calibration/ECE, confidence intervals, prevalence baseline, and per-league/fold stability.
- Do not tune thresholds on the test set. Any model selection/calibration must use separate training/validation periods, then evaluate on untouched test data.
- Include ablation comparison: baseline inputs vs baseline + H2H, so the marginal value of H2H is isolated.
- No claim of superiority based on accuracy alone or a single fold. Report paired fixture deltas and uncertainty.

## Release gate
The research candidate remains non-production and non-betting-eligible until identity joins, feature point-in-time provenance, settlement truth, leakage-safe evaluation, calibration, market-specific readiness, and formal release review pass. Do not claim a 90% or any other target accuracy in advance.

## Current known facts
- Existing FootyStats archive has observed 2024 rows across 50/50 selected league groups: 14,761 rows; 14,749 with completed-like status and numeric scores; 13,526 with all current 20 baseline features.
- Existing runtime calculates H2H history but H2H fields are not in the current 20-feature model input list.
- Existing primary validation window remains 2025-03-20 through 2026-09-20.
- Production remains unchanged; research prediction/betting eligibility is not granted.

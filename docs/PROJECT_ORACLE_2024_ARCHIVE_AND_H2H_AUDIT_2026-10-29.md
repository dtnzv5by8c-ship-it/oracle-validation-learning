# Project Oracle — 2024 archive and H2H usage audit
**Date:** 2026-10-29  
**Scope:** Research branch only. No production model, probability, threshold, calibration, or governance changes.

## Executive decision
FootyStats historical data is already present in the private archive and the selected-50 research runtime can read it. The archive does not need to be re-downloaded merely to gain access to 2024. However, “data is present” is not the same as “the model uses it in training” or “H2H influences probabilities.”

## Verified archive coverage
The latest selected-50 research runtime artifact reports:
- 2024: 50/50 selected league groups have archive rows.
- 14,761 fixture rows in calendar year 2024.
- 14,749 rows with completed-like status and numeric scores.
- 14,749 rows with fixture ID and both team IDs.
- 13,526 rows with all 20 currently required research features.
- 2024 rows in the current primary evaluation window: 0, because the window is fixed to 2025-03-20 through 2026-09-20.
- Archive observations are not proof of complete provider coverage, official settlement truth, or point-in-time feature provenance.

## What the current research code actually does
File: `scripts/build_selected50_research_runtime.py`.
1. It maps archive season files to the selected league grouping and deduplicates records.
2. It builds team-form histories and head-to-head histories from explicitly finished matches with numeric scores.
3. For each target fixture, historical matches are cut off strictly before the target kickoff using `bisect_left`. Same-timestamp matches are excluded, which is conservative.
4. H2H is keyed by the normalized competition group plus the sorted pair of provider team IDs. This allows cross-season H2H only where the archive mapping and provider team IDs remain stable across seasons.
5. It calculates `h2h_prior_n`, last-five H2H result string from the target home team's perspective, last-five H2H BTTS rate, last-five average total goals, and the last prior H2H date.
6. **Important gap:** the active `FEATURES` list contains 20 team-form/score/shot features and does **not** include any H2H field. H2H is calculated and exported for diagnostics, but it does not currently affect fitted research probabilities. It is therefore not yet being used for prediction in the way intended.
7. The current backtest's training rows are restricted by the existing primary window/training cutoff. 2024 is not part of the reported primary holdout; earlier rows can still contribute to prior-history features for later fixtures if they pass data and chronology rules. Code review confirms the current runtime forms `train_pre` from all eligible completed rows strictly before 2025-03-20, so eligible 2024 outcome labels can and do enter the primary-window training pool when they pass the required 20-feature gate. The 2024 archive is therefore not wholly unused: it already contributes training history for the existing baseline where rows qualify. The separate gap is that H2H values are not part of the active 20-feature model inputs.
8. Current table position is explicitly marked as a current provider snapshot and is display-only; it must not be used as historical training data.

## H2H risks to resolve before relying on it
- Team IDs must be verified as stable across seasons and competition mappings. Team IDs that change or are reused can break H2H joins.
- H2H is currently restricted to the mapped competition group. Cross-competition meetings (e.g., cups) are excluded. This is acceptable if explicitly intended, but must be a documented policy.
- The current implementation includes prior records marked finished with numeric scores, but does not yet visibly enforce a minimum H2H sample, recency decay, or an explicit H2H reliability/confidence gate.
- The current H2H features are exported but not included in model input features.
- Duplicate fixture IDs and same-kickoff duplicates must be audited after normalization; simple timestamp cutoff alone does not resolve duplicate source records.
- Provider status/score fields are not official settlement truth. H2H result features must use only validated completed records.
- Point-in-time provenance for all other features remains a separate gate; current archive coverage does not prove that every input was available before kickoff.

## Safe implementation plan
1. Keep production untouched. Create a research-only H2H feature experiment behind an explicit experiment flag or separate feature set.
2. Add audit outputs per target fixture: number of valid prior H2H meetings; dates and age of the last five; same-team-ID and competition mapping status; duplicate/invalid-score exclusions; feature availability; H2H reliability tier. Do not silently impute missing H2H.
3. Validate H2H history chronologically: only prior kickoff times; finished status plus valid integer scores; no target fixture/self-match; deduplication; consistent home-team perspective; no future information.
4. Build a 2024-inclusive rolling-origin evaluation. Keep 2024 as historical training/context only where its records are eligible and strictly before each test kickoff. Compare (a) existing 20-feature baseline vs (b) H2H-augmented research model, using identical chronological folds and the same fixture set where possible.
5. Report sample counts, Brier score, log loss, calibration error, discrimination, market prevalence/baseline, league-by-league stability and confidence intervals. No claim of improvement unless the H2H version beats the baseline consistently out of sample.
6. Separately validate official settlement definitions and point-in-time data lineage before any release review.

## Configuration answer
Accessing the existing 2024 archive is operationally straightforward: the runtime already reads the multi-season archive. The current evaluation cutoff is a configuration boundary, but widening it blindly would change the experiment and could introduce leakage or non-comparable results. The safe change is a separate research-only 2024-inclusive rolling-origin evaluation, not a production cutoff change. Enabling H2H in the prediction model is also technically small, but it changes model inputs and must be treated as a new research experiment, evaluated against the frozen baseline before any production consideration.

## Status
- FootyStats archive accessible in research runtime: **YES**
- 2024 rows present for all selected 50 groups: **YES**
- 2024 included in current primary holdout: **NO**
- H2H features calculated and exported: **YES**
- H2H features included in current model's 20 inputs: **NO**
- Production changes made: **NO**
- Production/betting eligibility: **NOT GRANTED**

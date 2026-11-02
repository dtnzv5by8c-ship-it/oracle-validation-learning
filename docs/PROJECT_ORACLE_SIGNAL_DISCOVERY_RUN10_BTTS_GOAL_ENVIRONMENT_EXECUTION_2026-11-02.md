# Project Oracle — Run 10 BTTS Goal-Environment Execution Checkpoint

**Date:** 2 November 2026 (SAST)  
**Status:** Completed successfully; research-only.

## Repository safety and execution lineage

- Repository: dtnzv5by8c-ship-it/oracle-validation-learning
- Branch: research/oracle-50-league-readiness-audit
- Exact branch HEAD inspected before checkpoint write: f2e71aa03f2aaeca68a4892b0b299d60a255c7ab
- Run 10 implementation commit: a273588d890ca0dbc1ce52eced38c13dc40de650
- Training-window correction commit: f2e71aa03f2aaeca68a4892b0b299d60a255c7ab
- Target checkpoint path was confirmed absent before this write.
- This checkpoint is documentation-only. No production files, Oracle V1.6 logic/probabilities, canonical ledgers or existing production workflows were changed.

## Run 8 asset recovery and archive

A fresh exact-title Library search and repository inspection did not recover the original Feature Edge v18 workbook or Run 8 companion bundle.

| Asset | Expected SHA-256 | Status |
|---|---|---|
| Feature Edge v18 workbook | 66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7 | Not recovered |
| Run 8 companion bundle | b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f | Not recovered |

The checksum-pinned Selected-50 archive was downloaded read-only and verified:
- SHA-256: bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261
- 59,049 raw records; 200 season files; 50/50 exact selected-group mappings.
- Zero archive parse errors, missing identities or duplicate identity keys.
- Provider API credits used: 0.

This is a reproducible archive rebuild, not recovery of the original workbook.

## Execution attempts and correction

1. Workflow run 41387035675 passed all three contract tests and the pinned archive checksum, but failed during model execution because the target panel began at PRIMARY_START. This left FOLD_1 with zero training rows.
2. The event-time panel builder was corrected to start at TRAIN_START, matching the existing Run 6 expanding-fold convention.
3. Successful workflow run 41387143018 completed the archive rebuild, BTTS diagnostics and aggregate artifact upload.
4. The dedicated contract suite passed 3/3 tests. The Selected-50 Safety Contract Tests and Dry-Run Planner also completed successfully.

Successful workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41387143018  
Artifact ID: 13115886021  
Artifact SHA-256: cbe77ed39dd3a68929ee65d920bd9a44c68d1e7f6546cd9989799d70254632f5

## Population, gates and chronology

- Event-time panel: 31,265 rows.
- Primary settled, home/away-distinguished targets: 17,780.
- Overall five-observed-match eligible: 17,103.
- Venue five-observed-match eligible: 16,476 across 48 selected groups.
- H2H five-plus cohort within venue-eligible rows: 6,400 across 48 groups.

Folds:
- FOLD_1: train N=12,419; test N=5,824; 47 test groups.
- FOLD_2: train N=18,243; test N=6,004; 44 test groups.
- FOLD_3: train N=24,247; test N=4,648; 45 test groups.

Event-time construction is strictly earlier-than-kickoff; all targets sharing a kickoff timestamp are evaluated before any same-time result is appended. Overall form requires five actual settled score-complete prior matches per team. Venue features require five explicit home-role and away-role matches. H2H rates and H2H modelling require at least five actual prior pair meetings. League goal-environment rates require 50 actual prior league matches. No pseudo-counts are used.

## Main BTTS findings

Pooled out-of-sample cohort: 16,476 fixtures across 48 groups; BTTS prevalence 54.58%.

| Model | Brier | Log loss | AUC | ECE10 |
|---|---:|---:|---:|---:|
| League-only | 0.246814 | 0.686747 | 0.536459 | 0.009969 |
| Overall-form-only | 0.246432 | 0.685972 | 0.543337 | 0.009697 |
| Main effects (overall + venue) | 0.246624 | 0.686351 | 0.541203 | 0.010035 |
| Main + team goal environment | 0.246673 | 0.686452 | 0.540760 | 0.009833 |
| Main + venue goal environment | 0.246682 | 0.686474 | 0.540348 | 0.009864 |
| Main + league goal environment | 0.246989 | 0.687091 | 0.538100 | 0.011969 |
| Main + all goal-environment blocks | 0.247183 | 0.687487 | 0.535965 | 0.011886 |

Overall-form-only was the best principal model, but its AUC of 0.543337 remains weak. Its small improvement over league-only did not survive joint multiplicity correction.

Adding venue main effects did not help BTTS. Team and venue goal-rate blocks were neutral/slightly worse. League goal-environment rates worsened all four pooled metrics. Combining all goal-environment blocks worsened pooled Brier/log loss and reduced AUC.

## H2H and constituent-controlled tests

The H2H cohort had 6,400 pooled OOS fixtures. Main effects improved H2H-cohort AUC over league-only, but the proper-score improvement was small and ECE deteriorated. Adding H2H BTTS/O2.5 rates to main effects did not improve Brier, log loss or AUC.

Partial-Spearman tests controlled for all existing main-effect features and selected-league fixed effects. Candidate partial correlations ranged from -0.0127 to +0.0178; the smallest unadjusted p-value was 0.1025.

Joint multiplicity family: 166 tests. BH q<0.05: 0. BY q<0.05: 0. No feature block or partial-Spearman result passed the correction.

## Previously completed interactions not repeated

The two Run 6 candidate interactions were not rerun. Their nested ablations and constituent-controlled tests already failed to demonstrate independent incremental value. No raw-correlation-only claim is made.

## Blockers and provenance limits

- Frozen Oracle V1.6 comparison remains blocked: no matching historical fixture-level V1.6 BTTS probabilities, prediction timestamps and settlement truth are available. No challenger output was substituted.
- Original Run 8 workbook and companion bundle remain unavailable.
- Provider publication/capture timestamps are unverified; event-time chronology is not proof of source publication time.
- Archive settled status/scores are not independently verified official settlement.
- xG without verified capture timestamps and provisional standings remain quarantined.

## Next steps

1. Do not promote any new BTTS goal-environment feature block.
2. Test a bivariate Poisson or Dixon–Coles-style scoreline distribution using pre-kickoff attack/defence and league scoring parameters; derive BTTS from the joint score distribution.
3. Compare against league-only and overall-form logistic baselines on the same three chronological folds.
4. Preserve Brier, log loss, AUC, ECE/reliability, paired league-cluster intervals, joint BH/BY and the existing sample gates.
5. Obtain a matching frozen V1.6 historical BTTS probability/settlement ledger before attempting the production benchmark.

## Governance

- Provider API credits used: 0.
- Raw provider rows exported: false.
- Fixture-level predictions exported: false.
- Event-time feature panel exported: false.
- Oracle V1.6 production logic/probabilities changed: false.
- Canonical ledgers changed: false.
- Existing production workflows changed or dispatched: false.
- Production eligible: false.
- Betting eligible: false.

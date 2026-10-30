# Oracle Data & Team DNA — Research Checkpoint

**Checkpoint:** 30 October 2026, 04:25 SAST  
**Repository:** dtnzv5by8c-ship-it/oracle-validation-learning  
**Branch:** research/oracle-50-league-readiness-audit  
**Lane:** Global market/fold stability; separate from the primary H2H integrity task.

## Completed this pass

- Audited the sanitized Selected-50 aggregate walk-forward metrics: 15 market-fold rows covering five markets and three chronological folds.
- Added a reproducible standard-library analysis script with strict source, fold chronology, sample-partition, Brier arithmetic and governance checks.
- Added nine offline regression tests.
- Extended the existing research safety-contract workflow to compile and execute this audit.
- Committed a market-level summary and detailed report. No fixture-level or team-level outcomes were reconstructed.

## Verified aggregate findings

Each market has 20,878 test observations across three disjoint windows. Test sizes are 6,611 / 7,600 / 6,667; training sizes expand 22,427 / 29,038 / 36,638.

| Market | Aggregate Brier skill | Positive folds | Research interpretation |
|---|---:|---:|---|
| DC_AWAY | +0.05400 | 3/3 | Strongest global baseline signal |
| DC_HOME | +0.04943 | 3/3 | Positive probability-score signal; threshold accuracy is 0.29pp below majority-class baseline |
| BTTS | +0.00536 | 3/3 | Small positive signal; materially weaker than Double Chance |
| COMBO_AWAY | +0.01871 | 3/3 | Blocked; predictor/settlement semantics unresolved |
| COMBO_HOME | +0.01478 | 3/3 | Blocked; predictor/settlement semantics unresolved |

All outputs remain raw and uncalibrated. No profitability, team suitability or betting eligibility conclusion is supported.

## Related identity-lane evidence

Open draft PR #31 documents an offline FootyStats-first adapter/resolver smoke test: 50/50 selected seasons passed the source-success guard; 1,744 source rows were adapted with no duplicate season/match keys; 681 future fixtures remained after status/home-away quarantine; exact season-ID + match-ID joins found 370 runtime matches (345 raw research-only and 25 feature-blocked), with three additional candidates lacking runtime output. Zero production-eligible predictions remain. PR #31 is still draft; its body does not claim the isolated resolver CI has passed.

## Outstanding blockers

1. Canonical team/fixture identity is not approved merely by source-native FootyStats IDs.
2. Official settlement truth and market definitions remain incomplete.
3. There is no immutable team-attributed chronological prediction/outcome ledger to calculate team-specific accuracy, Brier, calibration, draw/upset/low-scoring risk or market suitability.
4. The current artifact is aggregate-only; exact fixture-level uncertainty intervals and team-level profiles cannot be recovered from it.
5. No Brier-skill confidence intervals or multiplicity-adjusted inference are supplied for the 150 non-Combo league-market screen.

## Next action

Keep DC_AWAY, DC_HOME and BTTS as research priorities only. Continue the source-neutral identity/settlement reconciliation in the existing draft research PR, then require a fresh untouched chronological prediction/settlement ledger before team-market suitability analysis. Do not access the locked H2H paired holdout, change production logic, calibrate, tune or approve betting eligibility.

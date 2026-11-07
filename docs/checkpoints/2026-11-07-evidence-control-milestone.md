# Project Oracle — Evidence-Control Milestone — 2026-11-07

## Scope
Governed universe: Oracle-50-League.
Branch: research/oracle-50-league-readiness-audit.
Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance are unchanged.

## Milestone
The evidence-control lane has completed the currently admissible archive/research reconciliation without any new provider/API acquisition.

### Verified evidence position
- Selected-50 Market Intelligence Report Repair: completed successfully; baseline run #360 / f084491.
- Challenger shadow settlement: 210/210 rows settled across 42 fixtures, with zero chronology failures.
- Canonical production prediction/settlement ledgers remain header-only; therefore production Oracle accuracy and calibration are not computable from governed evidence.
- Historical research metrics remain research-only and are not promoted to production performance.
- The controlled 50-league upstream batch remains blocked because no admissible private gateway receipt/batch is available for row-level validation.
- Acquisition queue remains exhausted; no provider credits were consumed for this milestone.

## Research metric boundary
Existing research-only BTTS/H2H metrics may be retained for diagnostic use, but must not be represented as production Oracle performance. In particular, the existing August research proxy reports classification accuracy 55.046%, Brier 0.244695, log loss 0.682436 and ROC AUC 0.565797; these figures lack the immutable production prediction-to-settlement provenance required for promotion.

The existing H2H experiment does not establish production incremental lift. The documented paired H2H comparison shows Brier +0.000391 and log loss +0.000829 versus the logistic baseline, with a bootstrap interval crossing zero; this remains exploratory evidence only.

## Release-gate classification
READY:
- Selected-50 repair baseline.
- Chronological historical-score research datasets.
- Challenger shadow settlement.

BLOCKED:
- Canonical production prediction -> exact fixture/market -> pre-kickoff timestamp -> feature provenance -> verified settlement chain.
- New 50-league private ingestion admission.
- H2H incremental production lift.

UNVERIFIED / INSUFFICIENT SAMPLE:
- Production accuracy.
- Production calibration.
- Production Brier/log loss/AUC.
- Confidence/risk-band production performance.
- League-level production performance.
- Team-level production performance.
- Current 50-league fixture readiness.

QUARANTINED:
- Provider-blocked populations for which no admissible evidence-backed recovery path exists without provider calls.

## Next admissible milestone
The next major release-readiness milestone is the first evidence-backed production-quality prediction-to-settlement cohort satisfying all immutable identity, chronology, provenance and result-trust gates. No model promotion or production performance claim should occur before that gate passes.

## Safety
Documentation/research checkpoint only. No Oracle V1.6 production logic, probabilities, thresholds, calibration, canonical production ledgers, or betting logic were changed.

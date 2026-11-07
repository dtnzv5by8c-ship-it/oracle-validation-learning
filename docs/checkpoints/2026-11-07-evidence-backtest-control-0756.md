# Project Oracle — Evidence / Backtest Control Checkpoint

Date: 2026-11-07 07:56 SAST
Branch: `research/oracle-50-league-readiness-audit`
Lane: Evidence / Backtest Control

## Baseline
- Selected-50 Market Intelligence Repair #360 remains the downstream reporting baseline.
- Acquisition is exhausted: 648 completed + 80 quarantined/provider-blocked + 0 pending = 728 governed tasks.
- Manifest compatibility for existing batch 42255401046 is CLOSED/VERIFIED; do not repeat.
- 80 HTTP-417 tasks remain quarantine-only unless existing evidence proves deterministic recovery without provider calls.
- No provider/API acquisition was performed in this checkpoint.

## Highest-value remaining gate
The canonical production prediction ledger is not currently scoreable against verified settlement evidence. Existing audit evidence records 210 challenger rows across 42 fixtures, while canonical settlement/scorecard/probability-error ledgers remain empty/header-only. Historical research and shadow metrics therefore remain research-only.

The required admissible chain is:
prediction ID -> exact fixture/market identity -> prediction timestamp < kickoff -> pre-kickoff feature snapshot/provenance -> model/version + probability -> verified settlement source/status.

## Evidence rules
- No inferred, future, unsettled, ambiguous or provenance-free outcomes are admitted.
- No research/shadow metric is promoted to production performance.
- No metric is claimed where the cohort is below the configured minimum sample.
- AUC is only reported for suitable binary outcomes with both classes present.
- Calibration is reported with sample counts and is not conflated with hit rate.
- Confidence/risk-band results remain unverified until production prediction provenance is established.

## Current gate classification
READY: acquisition/task accounting; manifest compatibility; research-only chronology controls; Selected-50 repair baseline.
PARTIAL: historical feature coverage; H2H; recent/venue form; research settlement evidence.
BLOCKED: canonical production prediction-to-settlement linkage; point-in-time xG provenance; timestamped odds provenance.
UNVERIFIED: production accuracy, calibration, Brier, log loss, AUC, league/market/risk-band production performance.
INSUFFICIENT SAMPLE: any production subgroup that cannot meet the minimum evaluation cohort after admissible joining.

## Control-plane action
Canonical continuation state updated to remove stale acquisition/manifest work from the next-work queue and to prioritize immutable prediction/settlement validation. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and governance were not modified.

# Project Oracle — Selected-50 OMI / Visual Intelligence Research Checkpoint — 2026-11-07

## Scope
- Governed universe: exactly 50 leagues.
- Branch: `research/oracle-50-league-readiness-audit`.
- Production benchmark: Oracle V1.6.
- Mode: research/reporting only.
- Acquisition queue: exhausted; this checkpoint makes no provider/API calls and does not dispatch acquisition.

## Live HEAD
- HEAD: `f084491b95be1df95d0d59b8d2d08d16ab6dbfbc`.
- HEAD change restores the backward-compatible read-only archive consent input for the Selected-50 Market Intelligence Report Repair workflow.
- The workflow remains fail-closed for direct results-provider credit usage; provider requests must remain centralized in the governed acquisition/budget path.

## Successful repair baseline
- Selected-50 Market Intelligence Report Repair was reported successful as workflow run #360, with commit `f084491` and 2m15s duration.
- The live workflow contract requires a pinned private archive, an exact successful runtime artifact, archive SHA verification, runtime branch/commit/digest reconciliation, exact 50-league schedule reconciliation, row-level history provenance QA, xG provenance QA, field coverage audit, and explicit research-only actual-results handling.
- The successful workflow baseline is therefore the downstream OMI repair baseline; no new acquisition was triggered.

## Artifact inspection boundary
- The public branch contains the workflow contract and the required downstream artifact names, including:
  - `oracle_selected50_market_intelligence.xlsx`
  - `oracle_selected50_market_intelligence.csv`
  - `oracle_selected50_market_intelligence_qa.json`
  - `oracle_selected50_50_league_coverage.csv`
  - `oracle_selected50_field_coverage_by_league.csv`
  - `oracle_selected50_field_coverage_summary.csv`
  - `oracle_selected50_field_coverage_exceptions.csv`
  - `oracle_selected50_xg_evidence_audit.csv`
  - `oracle_selected50_xg_evidence_audit_qa.json`
  - `oracle_selected50_history_provenance_sides.csv`
  - `oracle_selected50_history_provenance_matches.csv`
  - `oracle_selected50_history_provenance_qa.json`
  - `oracle_selected50_actual_results.csv`
  - `oracle_selected50_actual_results_qa.json`
- These are workflow artifacts rather than committed public files. The connected GitHub read surface does not expose the artifact ZIP for the supplied human-facing run number #360 as a workflow-run ID, so artifact payload values are not asserted here beyond the successful completion baseline. This prevents inventing coverage metrics from artifact names alone.

## Readiness rules
A feature is READY only when its row-level evidence satisfies identity, chronology, provenance and feature-specific validation. Acquisition success is not feature readiness.

Feature families:
- Fixture identity / chronology: gate on exact fixture identity and valid pre-kickoff chronology.
- Recent form / home-away splits: gate on minimum history and row-level provenance; no imputation.
- Exact H2H: exact-ID joins only; no fuzzy substitution.
- Goals / total-goal distributions / BTTS / Over 1.5 / 2.5 / 3.5 / clean sheets / failed-to-score: derived only from validated settled historical matches inside the permitted chronology window.
- xG for/against: BLOCKED unless point-in-time provenance is demonstrated; field presence alone is insufficient.
- Standings / strength: provenance and chronology required; no current-table leakage into historical snapshots.
- Timestamped odds: BLOCKED unless timestamped pre-kickoff evidence and source provenance exist.
- Sample size / recency / confidence / data-quality / risk: diagnostic fields may be reported, but confidence cannot be promoted to production readiness without its upstream evidence gates.
- Actual results / settlement: only independently verified settled fixtures qualify; future, postponed, void or unresolved fixtures remain non-settled.
- Backtesting: requires immutable pre-kickoff prediction and feature snapshots plus independently verified settlement.

## Status classification
- READY: deterministic gates pass.
- PARTIAL: some evidence exists but one or more required gates fail or are incomplete.
- BLOCKED: required evidence/provenance is absent, contradictory, future/unsettled, or otherwise inadmissible.

No PARTIAL or BLOCKED evidence is promoted to production/betting readiness.

## Current blockers carried forward
1. Artifact-level coverage values cannot be promoted from workflow filenames alone; the actual artifact payload must be available for deterministic row-level coverage.
2. Point-in-time xG provenance remains a hard gate.
3. Timestamped pre-kickoff odds remain a hard gate where provenance is absent.
4. Immutable prediction-to-settlement provenance remains required for production backtesting.
5. Any unresolved fixture/team identity, chronology, history-window or source-provenance exceptions remain quarantined.
6. The 50-league completeness gate remains exact; no other universe is permitted.

## Production protection
- Oracle V1.6 probabilities: unchanged.
- Oracle V1.6 thresholds: unchanged.
- Oracle V1.6 decision logic: unchanged.
- Oracle V1.6 calibration/governance: unchanged.
- No feature fabrication or imputation.
- No future/unsettled data admission.
- No betting report is authorized from this checkpoint.

## Next actionable step
Consume the successful repair artifact payload when a deterministic artifact reference is available, then compute and publish READY/PARTIAL/BLOCKED coverage by league, season, endpoint and feature family. Preserve the same fail-closed production/betting gates and create only research-only checkpoints until all required evidence gates pass.

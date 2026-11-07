# Project Oracle — 50-League Code Namespace Reconciliation Audit

Date: 2026-11-07

## Finding
The canonical 50-league source registry and the private prediction engine use different league-code namespaces. A direct replacement of the legacy 27-code allow-list would therefore be unsafe.

## Evidence
The private engine `scripts/oracle_four_model_predict.py` has a 27-code ACTIVE allow-list. The canonical 50-league registry has 50 source codes. Direct string intersection is only CRO, leaving 49/50 governed source identities requiring explicit mapping evidence.

## Root Cause
Provider/source identity and legacy prediction-engine identity evolved independently.

## Impact
Blind code substitution could mis-route or exclude fixtures. This is a data/universe configuration blocker, not a model-logic problem.

## Fix
Created research-only audit:
`reports/oracle-50-league-code-namespace-reconciliation-audit-2026-11-07.md`
Commit: `3bc236c84261462da5e47add2779b050d7d1e56a`

The required next control is an evidence-backed one-to-one identity bridge before any production scope expansion.

## Validation
No production code was changed. Oracle V1.6 logic, probabilities, thresholds, calibration, betting eligibility and governance remain unchanged. The downstream scope gate remains fail-closed.

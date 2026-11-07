# Checkpoint — 2026-11-07 — 50-League Prospective Coverage Gap Quantified

## Milestone
Quantified a previously unclosed prospective coverage mismatch between the governed 50-league historical universe and the live upcoming-fixture pipeline.

## Evidence
- Canonical selected-50 manifest contains exactly 50 selected leagues / 728 endpoint tasks.
- Private gateway receipt independently records Oracle-50-League and expected_leagues=50.
- Live upcoming-fixture ingestion is explicitly hardcoded to 27 leagues.
- Latest fixture manifest has 27 targets but only 14 OK_FALLBACK targets and 13 SOURCE_ERROR targets.
- Persisted upcoming fixture CSV contains only 14 unique league codes.

## Root Cause
Prospective fixture ingestion was never advanced from the legacy 27-league registry to the governed 50-league universe. The current 27-league source/fallback path also has 13 unresolved source errors.

## Impact
The prospective evidence lane cannot claim 50-league fixture coverage, so 50-league governed production readiness cannot be admitted.

## Action
Do not rerun generic ingestion or FootyStats recovery. Build the canonical 50-league prospective fixture registry from the existing governed identity set, then verify source identifiers and coverage before the next legitimate prediction cycle.

## Governance
No Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility or governance changed. No provider/API acquisition was performed. Production remains fail-closed.

Report: `reports/oracle-50-league-upcoming-coverage-audit-2026-11-07.md`

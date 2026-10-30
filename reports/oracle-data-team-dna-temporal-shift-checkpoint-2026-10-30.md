# Oracle Data & Team DNA — Temporal Shift Checkpoint

**Date:** 30 October 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Source:** Existing Private Archive QA #35 / artifact `12955356908`  
**Pinned archive SHA-256:** `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`

## New verified analysis

- Added a reproducible current-versus-historical season xG zero-rate comparison using sanitized archive QA outputs only.
- Five new unit tests pass locally.
- Eleven current-season league groups meet the existing exploratory xG outlier screen.
- Across those 11 groups, current-vs-noncurrent pooled zero rates are:
  - Team A prematch xG: 201/545 (36.88%) vs 202/4,527 (4.46%); +32.42 percentage points.
  - Team B prematch xG: 203/545 (37.25%) vs 202/4,527 (4.46%); +32.79 pp.
  - Total prematch xG: 182/545 (33.39%) vs 181/4,527 (4.00%); +29.39 pp.
- This supports a cross-league current-season data-quality/ingestion regression hypothesis. It is not proof of provider or pipeline cause: current-season samples are partial, historic seasons are pooled, and source semantics/timestamps are absent.
- Belgium's 2026/27 BTTS Yes/No and DC 1X/X2 share a 54-row zero mask and nine-row positive mask. FT 1X2 and O/U 2.5 remain mostly positive; market-specific coverage issue is confirmed at the archive-field level only.
- The archive audit date is 30 October while the event-time window ends 20 September (40-day event-window coverage gap). This is not a source freshness measurement.

## New research files

- `scripts/audit_selected50_xg_odds_temporal_shift.py`
- `tests/test_selected50_xg_odds_temporal_shift.py`
- `docs/PROJECT_ORACLE_XG_ODDS_TEMPORAL_SHIFT_AUDIT_2026-10-30.md`

## Limits and blockers

- Numeric zeros remain unchanged; no imputation or production feature changes.
- No source retrieval timestamps, bookmaker/source IDs or quote times in sanitized outputs.
- Provider `complete` is not official settlement truth.
- No immutable pre-kickoff team-attributed prediction ledger or independently verified settlement truth; team-market accuracy/calibration cannot be measured here.
- No H2H analysis or locked holdout access in this lane.

## Next action

Manual review of existing private archive ingestion metadata or archive-owner documentation for xG zero semantics, odds field availability semantics, source identifiers and quote/update timestamps. If absent, record a manual dependency. Do not call providers or incur credits. Keep all 50 leagues in the research universe; do not exclude teams or leagues based on these descriptive rates.

## Governance

Research-only. No provider/API calls or credits, no raw provider rows exported, no H2H holdout access, no production logic, frozen probability, calibration or governance changes. Production and betting eligibility remain false.

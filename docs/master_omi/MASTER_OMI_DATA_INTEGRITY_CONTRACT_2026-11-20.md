# Project Oracle — Master OMI Data Integrity & Formula Safety Contract
## Effective 20 November 2026

This is a permanent control layer around the canonical Master OMI V2.1.1 reporting architecture.

### 1. Release principle
No Master OMI workbook is released for formula/backtest use unless the Formula Input Release Gate passes. If required evidence is missing, the system fails closed.

### 2. Data classes
- VERIFIED_PREMATCH: information demonstrably knowable before kickoff and supported by valid provenance/cutoff.
- VERIFIED_ACTUALS: independently verified post-match outcomes, used only for settlement/backtesting.
- UNAVAILABLE_UNVERIFIED: missing, ambiguous, stale, identity-failed, chronology-failed or otherwise inadmissible evidence. Never replace with zero, average or estimate.

### 3. Fixture-level gates
Every fixture receives explicit:
- FORMULA_INPUT_STATUS
- BACKTEST_READY
- identity/source status
- chronology/leakage status
- data coverage status

A fixture is prediction-input ready only when mandatory pre-match inputs pass identity, chronology, provenance and range checks. A backtest row additionally requires a verified actual result.

### 4. Mandatory validation
Validate:
- exact fixture/team identity and home/away orientation
- kickoff/date reconciliation
- Last-3/Last-5 chronology
- PPG, GF/M and GA/M denominators
- venue scope
- source IDs and sample sizes
- history cutoffs
- post-match leakage
- duplicates
- numeric ranges
- missingness classification
- xG temporal provenance
- LTSS version/window/as-of/confidence
- Market Intelligence heading comments/definitions

### 5. Canonical workbook protection
Market Intelligence A:ET is structurally immutable. Never insert, delete, move, rename, reorder or overwrite the schema. New intelligence is append-only after the governed current end of the canonical intelligence contract. Oracle V1.6 production logic is unchanged by this QA layer.

### 6. Provenance
Every governed value must be traceable to its source, extraction/snapshot context, fixture/team identity, history cutoff where applicable, and transformation/calculation definition.

### 7. Schedule discrepancies
Provider date differences are never silently normalized. Where fixture identity/date cannot be independently adjudicated, actuals and pre-match intelligence remain unlinked/unverified.

### 8. Release gate
A report is PASS only when schema, comments, identity, chronology, provenance, leakage, range, duplicate, actuals and formula-eligibility checks pass. Genuine missing evidence is reported rather than fabricated.

### 9. Reproducibility
Each released report should preserve a release snapshot/hash and source manifest sufficient to reproduce the formula-input dataset used for analysis.

# Master OMI Market Intelligence — Permanent QA / Remediation Architecture

**Status:** LOCKED / PERMANENT OPERATING CONTROL
**Date:** 2026-11-22
**Canonical baseline:** Master OMI V2.1.1

## Purpose
Prevent recurring Market Intelligence data defects from reaching formulas, backtests, market intelligence decisions, or betting workflows.

## Two-stage control model
1. **Independent QA / Auditor** — inspects every governed fixture row × every Market Intelligence column, identifies defects, measures coverage, and controls release status. It must not self-certify remediation.
2. **Remediation / Fixer** — consumes the latest QA evidence, fixes only defects supported by authoritative evidence, records every change, and never declares release PASS.
3. The cycle is permanently: **AUDIT → FIX → AUDIT → FIX** until the independent QA release gate passes.

## Non-negotiable controls
- A:ET remains immutable.
- Oracle V1.6 production logic remains unchanged.
- No silent fuzzy matching.
- No timezone normalization without governed evidence.
- No historical backfill.
- No zero-filling missing evidence.
- No estimates or guessed values.
- Mandatory fields must contain verified data or an explicit UNAVAILABLE/UNVERIFIED classification; no unexplained blanks.
- Governed numeric fields must be native Excel numeric values where evidence supports a numeric value.
- Actuals remain segregated from pre-match inputs.
- CMOI remains research-only unless independently promoted through validation.
- Every remediation must record source evidence, cells/fields affected, before/after state or type, counts, hashes, and unresolved exceptions.
- The QA task is the sole release authority.

## 100% release definition
100% requires zero schema defects, zero unexplained mandatory blanks, zero invalid governed numeric types, zero duplicate fixture IDs, zero Excel errors, zero identity/chronology/leakage/provenance defects, and explicit classification for every genuinely unavailable optional value. RELEASE_DECISION remains FAIL-CLOSED until all mandatory gates pass.

## Persistence
This architecture is part of the permanent Master OMI governance pack and must be used for future Master OMI reports without requiring Nolan to restate the requirements.

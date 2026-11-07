# Project Oracle Checkpoint — H2H Fuzzy Identity & Non-Blocking Control

Date: 2026-11-07
Repository: dtnzv5by8c-ship-it/oracle-validation-learning

## Finding
H2H team identity is a reporting/evidence reconciliation layer and must not block the Oracle build merely because historical team-name variants, absent historical records, cross-division history, no prior H2H, or fewer than five H2H meetings exist.

## Evidence
- Run #56 established exact 145/145 Fixture ID joining and identified 22 diagnostic unresolved rows.
- User-approved policy: genuine no-H2H fixtures and H2H samples below five meetings are non-blocking.
- Reporting-only fuzzy resolver is league-scoped, archive-scoped and ambiguity-gated; it does not modify canonical Fixture IDs or Oracle V1.6 production inputs.
- Run #61 failed before H2H build because the reporting-layer implementation still contained a syntax defect; it did not demonstrate an H2H data-quality failure.
- Corrective commit for the current syntax-safe implementation: 4bb9924d0ee720e812b551a40254db1a072ef1a2.
- Run #62: 42387447956 is currently executing against that corrected commit. Archive extension and research stages have passed so far; no H2H quality-gate failure is currently evidenced.

## Root Cause
Historical team identity is represented inconsistently across sources. Treating missing/variant H2H history as a fixture-identity blocker over-constrains the reporting pipeline.

## Fix
1. Preserve exact governed Fixture ID as the primary fixture identity.
2. Add explicit aliases plus conservative fuzzy team-name reconciliation for H2H reporting.
3. Classify no verified same-league H2H separately from unresolved fixture identity.
4. Treat <5 H2H meetings as a quality/sample flag, not a pipeline blocker.
5. Keep ambiguous fuzzy matches fail-closed for the H2H field only.
6. Keep Oracle V1.6 production logic, probabilities, calibration, thresholds and betting governance unchanged.

## Programme impact
H2H is removed from the critical path for Oracle production readiness except where H2H is explicitly required as a market/reporting evidence field. The critical path remains immutable feature snapshot -> prediction -> engine SHA -> point-in-time xG/odds -> verified settlement -> prospective evidence -> OMI release gates.

## Actions-minute control
- Public validation repository is the default for diagnostics/research.
- Private production workflows are reserved for controlled production evidence requiring private data/credentials.
- No unnecessary private workflow execution is to be triggered.
- Latest private Autonomous League Expansion run completed successfully with substantive jobs skipped; no private run is currently active.

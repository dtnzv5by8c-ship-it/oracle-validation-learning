# Oracle Data Integrity Cycle 13 — 2026-11-15

## State inspected
- Public research repository: dtnzv5by8c-ship-it/oracle-validation-learning
- Prior durable state: 30bd0537fc343dc8c32eefbdbdd609a3266263cc
- Prospective Run 29: 43709067778 — completed with failure
- Failed governance job: 132796483540

## Highest-impact finding
Run 29 completed fixture refresh, Team State refresh, four-model prediction generation, NO_BET diagnosis, publication preparation and settlement successfully. The final governance gate failed for two distinct reasons.

1. Research-only test-contract mismatch:
   - Test expected the source literal `"research_only":"TRUE"`.
   - Production/research extension correctly assigns `row["research_only"]="TRUE"`.
   - This is a test-contract defect, not a production-data leakage finding.
   - Private Oracle test repaired at commit `013c207aad0b924cf695c000b48b22b465738930`.
   - Oracle V1.6 production logic unchanged.

2. Point-in-time leakage gate:
   - `ORACLE_POINT_IN_TIME_LEAKAGE_AUDIT_V1.0` returned FAIL.
   - Fixture `match_id=1` had source date `2026-01-02` equal to fixture date `2026-01-02` for home and aggregate state.
   - The governing rule is strict: every non-empty source date must be earlier than fixture date.
   - This must remain a hard failure. No relaxation or same-day admission is permitted.
   - The generated historical artifact is explicitly classified as `HISTORICAL_REPLAY_STATE; NOT_TRUE_HISTORICAL_PREDICTION`; therefore it cannot be promoted as point-in-time evidence.

## Coverage / evidence status
- Completed 50-league source validation baseline: 50 governed leagues, 24 ready, 26 data-gated, 0 source-error leagues, 113 fixtures in the validation window.
- No new fixture evidence admitted in this cycle.
- No PPG/GF-M/GA-M value was inferred or substituted.
- No bookmaker odds substituted for FootyStats evidence.
- No Master OMI A:ET changes.

## Governance
- Exact Fixture ID and canonical league/team identity remain mandatory.
- Five-match Team State minimum remains fail-closed.
- PPG/GF-M/GA-M denominator integrity remains hardened against duplicate historical IDs.
- Pre-match chronology remains strict.
- FootyStats evidence remains research-only until point-in-time provenance and scope are verified.
- Oracle V1.6 probabilities, thresholds, calibration, eligibility and governance remain unchanged.

## Next highest-impact item
Repair the historical evidence artifact/generation path so the state used by the point-in-time audit has source timestamps strictly earlier than the fixture date, or explicitly exclude replay-only artifacts from promotion. Do not weaken the audit rule.

After that gate passes, independently reconcile PPG/GF-M/GA-M against the qualifying five-match denominator and classify remaining field gaps by identity, chronology, five-match minimum, scope, freshness or provenance before ET+ admission.

# Oracle Signal Validation — Cycle 11 hardened denominator gate

Date: 2026-11-15
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Durable audit patch: a9d3d1af342e4c69a131759b5649229d86294288

## Change
Hardened `scripts/audit_team_state_denominators.py` so PPG/GF-M/GA-M admission requires:
- exact fixture ID, league and team identity;
- explicit historical kickoff timestamp;
- strict historical kickoff < target kickoff;
- exact team/league matching;
- five-match minimum;
- separate five-match venue denominator.

Date-only fallback is now prohibited by schema. Normalized-name matches are diagnostics only and are reported as `TEAM_MAPPING_CONFLICT`; they cannot silently substitute for exact identity.

## Current upstream evidence
The completed 50-league live fixture-source validation run 43705410134 succeeded:
- 50 governed leagues
- 24 ready
- 26 data-gated
- 0 source-error leagues
- 113 fixtures in validation window
- 24 leagues with fixture evidence
- 26 without fixture evidence
- duplicate/unexpected/missing classifications: 0

This validates fixture-source availability only. It does not certify PPG/GF-M/GA-M, FootyStats goal fields, xG or other Master OMI values.

## Current limitation
The public research repository does not contain the locked current OMI fixture CSV or authoritative historical archive required to execute the new denominator audit numerically in this run. Therefore no fixture-level coverage, Brier, log loss or AUC result is claimed here.

## Promotion status
PPG, GF/M, GA/M, venue splits and all downstream goal signals remain research/unverified until the audit is executed against the authoritative fixture artifact and historical archive.

Oracle V1.6 probabilities, thresholds, calibration, betting eligibility and A:ET remain untouched. Only ET+ evidence is eligible for future append-only research promotion.

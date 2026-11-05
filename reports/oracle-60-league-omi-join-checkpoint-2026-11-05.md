# Oracle OMI 60-League Join Checkpoint — 2026-11-05

## Change
Hardened the Master OMI provider-season join contract.

## Finding
The OMI readiness validator previously compared each row's `Provider Season ID` against the manifest's canonical `league_id`/selected ID set. That could incorrectly block valid provider-season joins or, worse, make the admission contract validate the wrong identity dimension.

## Fix
The validator now builds its OMI admission set from the manifest's `provider_season_id` or `season_id` and compares that exact identity to each OMI row's `Provider Season ID`.

A regression test covers:
- valid provider-season identity => PASS;
- canonical league ID substituted for provider-season ID => BLOCK.

## Governance
- Oracle V1.6 production logic unchanged.
- Oracle probabilities are not recalculated.
- No provider calls were made.
- No provider-sensitive data was added.
- This is an offline reporting/admission hardening change only.

## Next action
Apply the exact provider-season identity contract to the first validated upstream batch and produce per-league/per-season OMI completeness exceptions before any production admission.

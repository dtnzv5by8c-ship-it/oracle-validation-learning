# Oracle Data Integrity — Cycle 11 checkpoint

**Date:** 2026-11-15  
**Repository:** dtnzv5by8c-ship-it/oracle-validation-learning  
**Durable HEAD inspected:** 7adf047b9b1f9c2889aac9b855e51897e7d11483  
**Active run inspected:** Oracle 50-League Live Fixture Source Validation #35 / 43705410134 — IN_PROGRESS.

## Highest-impact gap addressed

The existing FootyStats Team Intelligence research calculation reconstructed PPG/GF/M/GA/M from all prior team matches and then separately calculated venue statistics. That was insufficient as an evidence control because it did not enforce the governed five-match minimum at the denominator level and did not provide a per-fixture audit trail for exact pre-match admission.

A new fail-closed denominator audit was added at:
`scripts/audit_team_state_denominators.py`

It requires:
- exact `fixture_id`, league, teams and kickoff timestamp for current fixtures;
- exact historical match IDs and league/team identity;
- strict historical timestamp < target kickoff;
- last five qualifying matches for overall Team State;
- separate last five qualifying venue matches;
- explicit `VERIFIED_5_MATCH` / `UNVERIFIED_FIVE_MATCH_MINIMUM`;
- explicit venue status;
- source, quality, substitution flag and missingness reason.

If kickoff timestamp is unavailable, the audit **does not fall back to date-only history**; it fails closed and leaves the denominator unverified.

## Why this matters

This directly controls the requested PPG/GF/M/GA/M failure modes:
- denominator error;
- wrong venue scope;
- duplicate historical rows;
- stale/post-kickoff evidence;
- league/team mapping;
- insufficient five-match sample.

No values are imputed.

## Current data limitation

The public research repository does not contain the current locked OMI fixture CSV itself; the prospective workflow references the private/internal fixture path. Therefore this cycle cannot honestly publish a fixture-by-fixture numerical coverage percentage for the live Master OMI batch.

The current live validation workflow is already running and must be allowed to complete before another overlapping validation is started.

## Production safety

- Oracle V1.6: unchanged.
- Thresholds/calibration/eligibility: unchanged.
- Master OMI A:ET: untouched.
- Repaired evidence is research/ET+ only.
- No bookmaker substitution.
- No fabricated values.
- H2H remains non-blocking when sample <5.

## Next action

Once the active live source validation run completes, execute the new denominator audit against its current fixture artifact and the authoritative historical archive. Then reconcile every fixture/team side for:
**exact ID → canonical league/team → kickoff chronology → five-match minimum → PPG/GF/M/GA/M → venue splits → provenance/freshness/quality.**

Only verified rows may feed Master OMI ET+.

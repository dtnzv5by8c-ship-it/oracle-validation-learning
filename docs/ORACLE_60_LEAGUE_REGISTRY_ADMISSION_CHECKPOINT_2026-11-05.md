# Project Oracle — 60-League Registry Admission Checkpoint — 2026-11-05

## Scope
- Governed target: **60 leagues**
- Historical window: **2024-01-01 through current**
- Production model: Oracle V1.6 unchanged
- Broad historical ingestion: **BLOCKED**

## Live evidence inspected
The current FootyStats provider-season registry on the research branch declares:
- **49 provider leagues**
- **756 provider-season records**
- unique provider season IDs
- production eligibility false
- betting eligibility false

This is not sufficient evidence for the governed 60-league universe. The missing eleven league identities are not inferred or invented.

## Engineering completed
1. Repaired the indentation defect in `scripts/validate_omi_universe_readiness.py` so the required-feature fail-closed checks execute correctly.
2. Added `scripts/validate_60_league_registry_admission.py`.
3. Added `tests/test_60_league_registry_admission.py`.
4. The new contract requires:
   - declared provider league count = 60;
   - 60 unique provider league names;
   - nonblank unique provider season IDs;
   - all 60 leagues represented by 2024+ season evidence.
5. Added the registry-admission tests to the 60-league OMI CI contract.
6. Synthetic regression coverage verifies:
   - exact 60 passes;
   - a 49-league registry cannot be promoted to 60;
   - duplicate provider season IDs block admission.

## Safety
- No provider API calls made.
- No provider credentials or raw payloads added to the public repository.
- No missing leagues were fabricated.
- No direct HTTP 417 public-provider retry was made.
- No broad historical ingestion was dispatched.
- Oracle V1.6 production logic, probabilities, thresholds and calibration remain unchanged.
- Production and betting eligibility remain false.

## Next bounded action
Obtain/validate the authoritative 60-league canonical/provider manifest, then extend the approved private gateway only from that manifest. The first gateway proof must be a bounded private smoke receipt satisfying the existing gateway receipt contract before any historical batch is admitted.

# 2026-11-07 — 50-League Team-Pair Identity Crosswalk

## Finding
The 50-league live source gate is already PASS. The remaining identity bottleneck does not require guessing a production league code from a name. A fixture carries a governed OpenFoot competition identity plus a home/away team pair, and Oracle already has historical team/league identity data.

## Evidence
- 50/50 governed league identities reconciled.
- 299 live fixtures in the governed 2026-11-07 to 2026-11-21 window.
- 26 leagues READY; 24 DATA_GATED.
- Existing internal identity bridge currently proves 158 of the 299 fixture rows against an exact unique Oracle internal namespace.
- The remaining 141 fixture rows are now represented by a canonical source + team-pair identity and remain fail-closed for production admission.
- No production model logic, probabilities, thresholds, calibration or betting governance changed.

## Root Cause
The previous bottleneck treated internal league-code mapping as a prerequisite for fixture identity. That is unnecessarily restrictive. Fixture identity can be established independently using the governed competition identity and the home/away team pair; internal production namespace admission must remain a separate evidence gate.

## Fix
Added:
- `data/prospective/oracle_50_league_team_pair_identity_crosswalk.csv`
- `scripts/build_oracle_50_league_team_pair_identity_crosswalk.py`

The resolver uses this hierarchy:
1. governed OpenFoot competition identity;
2. exact existing Oracle internal identity where proven;
3. canonical source + team-pair identity otherwise.

Unmapped/conflicted internal namespaces remain FAIL-CLOSED rather than being invented.

## Validation
Crosswalk contains all 299 currently verified live fixtures. 158 have an existing exact Oracle internal identity; 141 have canonical source/team-pair identity but are not production-admissible yet. This advances the pipeline without changing V1.6.

## Next action
Use the crosswalk to reconcile team names against Oracle historical team evidence and resolve only deterministic internal namespace matches. Then feed the resulting canonical fixture namespace into the controlled 50-league admission audit. Do not expand production ACTIVE until the downstream identity and feature-evidence gates pass.

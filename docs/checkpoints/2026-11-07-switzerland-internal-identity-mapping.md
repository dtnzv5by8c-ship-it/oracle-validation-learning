# Project Oracle — Switzerland Internal Identity Mapping Evidence

Date: 2026-11-07
Governed branch: `research/oracle-50-league-readiness-audit`

## Finding
The 50-league research identity bridge had Switzerland Super League (SUI1) fail-closed as UNMAPPED.

## Evidence
Live production `config/data_config.json` defines:
- `SWZ` = Swiss Super League in `extra_all_seasons`.

The governed 50-league registry defines:
- `SUI1` = Switzerland Super League
- FootyStats league ID `17129`
- OpenFoot competition `comp_super_league_sui`

This is a deterministic internal namespace identity; no provider ID was substituted for the Oracle internal code.

## Fix
Research-only bridge row updated:
`SUI1 -> SWZ`
with status `EVIDENCE_EXACT_UNIQUE` and `fail_closed=FALSE`.

Production model code, ACTIVE universe, probabilities, thresholds, calibration and betting governance were not changed.

## Validation
Bridge commit: `4c8e8efe962b25e3ef66bbb8e66e4291f614148f`.

Remaining identity blockers are unchanged for all other unresolved leagues. This evidence does not authorize production admission.

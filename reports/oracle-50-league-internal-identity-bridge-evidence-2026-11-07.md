# Oracle 50-League Internal Identity Bridge — Research Control

Date: 2026-11-07

## Finding
The live production codebase contains an existing league-name-to-internal-code bridge covering the legacy 27-league namespace. This provides direct evidence for the current internal identity layer and confirms that the internal codes are not the same namespace as the new 50-league canonical source codes.

## Evidence
Source: `scripts/build_oracle_team_dna_v2.py`, `LEAGUE_NAME_TO_CODE`.

Observed mappings include:
- Austria Bundesliga → AUT
- Bundesliga → D1
- Croatia HNL → CRO
- Czech First League → CZE
- Premier League → E0
- Championship → E1
- League One → E2
- League Two → E3
- Ligue 1 → F1
- Ligue 2 → F2
- Serie A → I1
- Serie B → I2
- Eredivisie → N1
- Eerste Divisie → NED2
- Primeira Liga → P1
- Ekstraklasa → POL
- Romania Liga I → ROU
- South African Premier Division → RSA
- Scottish Premiership → SC0
- La Liga → SP1
- Segunda Division → SP2
- Turkey Super Lig → T1
- Ukraine Premier League → UKR

## Root Cause
The existing Oracle database/model stack already has an internal identity namespace, while the new 50-league governance layer uses canonical source identifiers. The two namespaces must be bridged explicitly.

## Impact
This evidence reduces ambiguity for the existing 27 leagues, but it does not prove mappings for the additional 23 governed leagues. It is therefore insufficient to expand production scope.

## Fix
No production change made. The next controlled step is to build a research-only bridge table containing all 50 governed identities and populate the internal code only where exact evidence exists.

Required fields:
governed_code, governed_name, FootyStats_league_id, OpenFoot_competition_id, internal_oracle_code, evidence_source, mapping_status, fail_closed.

## Validation
Existing internal mappings are evidenced from live HEAD. No model logic, probabilities, calibration, thresholds, betting eligibility or governance were changed.

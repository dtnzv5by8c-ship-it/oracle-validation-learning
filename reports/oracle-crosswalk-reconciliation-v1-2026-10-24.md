# Project Oracle — Research Crosswalk Reconciliation v1
Date: 2026-10-24
Branch: research/oracle-crosswalk-isolation-2026-10-22
Scope: research-only reconciliation from the user-supplied FootyStats selected catalogue and 27-league endpoint audit ZIPs.
Governance: does not alter the production repository, model logic, governed registry, probabilities, weights, thresholds, calibration, or selection rules.

## Executive result
The endpoint-audit artifact covers the existing 27-code governed registry, not the proposed 44-league expansion. It reports 18 exact catalogue-name matches and 9 unmatched catalogue names. This is a provider-catalogue alias/selection diagnostic, not evidence that Oracle's established 27-league universe has shrunk. The separate catalogue ZIP contains 534 league-season rows and 34 provider league names with `chosen_leagues_only=true`.

## Exact 27-code audit reconciliation
The supplied endpoint audit reports these 18 catalogue matches:
- ENG_E0 — Premier League — England Premier League
- ENG_E1 — Championship — England Championship
- ESP_SP1 — La Liga — Spain La Liga
- DEU_D1 — Bundesliga — Germany Bundesliga
- DEU_D2 — 2. Bundesliga — Germany 2. Bundesliga
- ITA_I1 — Serie A — Italy Serie A
- ITA_I2 — Serie B — Italy Serie B
- FRA_F1 — Ligue 1 — France Ligue 1
- FRA_F2 — Ligue 2 — France Ligue 2
- NLD_N1 — Eredivisie — Netherlands Eredivisie
- NLD_N2 — Eerste Divisie — Netherlands Eerste Divisie
- PRT_P1 — Primeira Liga — Portugal Liga NOS
- PRT_P2 — Liga Portugal 2 — Portugal LigaPro
- TUR_T1 — Süper Lig — Turkey Süper Lig
- BEL_B1 — Pro League — Belgium Pro League
- SCO_SC0 — Premiership — Scotland Premiership
- ROU_R1 — Liga I — Romania Liga I
- ZAF_PSL — Premier Soccer League — South Africa Premier Soccer League

The nine unresolved catalogue matches are:
- ENG_E2 — League One
- ENG_E3 — League Two
- ESP_SP2 — Segunda División
- AUT_A1 — Austrian Bundesliga
- CHE_S1 — Swiss Super League
- POL_P1 — Ekstraklasa
- CZE_CZ1 — Czech First League
- HRV_HR1 — HNL
- UKR_UA1 — Premier League

These nine are classified `NO_CATALOGUE_NAME_MATCH` in the supplied audit only. They must not be classified as unsupported until catalogue-selection settings, alternate provider names, season availability and account entitlement have been checked. Do not silently map similarly named competitions.

## Catalogue facts
- The selected-league catalogue extract contains 534 league-season entries and 34 unique provider league names.
- The selected catalogue includes exact names for the 18 matched competitions above.
- The provider catalogue includes names such as England Premier League, England Championship, Spain La Liga, Germany Bundesliga, Italy Serie A, France Ligue 1, Netherlands Eredivisie, Portugal Liga NOS, South Africa Premier Soccer League and Turkey Süper Lig.
- The selected catalogue does not list the nine unmatched names under the exact expected aliases in the audit.
- A catalogue season row is not proof of complete fixtures, field completeness, historical coverage, pre-kickoff availability, or the account's entitlement to every endpoint.

## Endpoint probe interpretation
For each of the 18 matched competitions, the artifact reports success for the match, team, table and season-stat endpoints. However, match retrieval was intentionally limited to one row for schema probing. These endpoint responses prove connectivity/schema reachability only. They do not prove full-season completeness, historical as-of integrity, or all required feature values are populated.

The probe exposes xG/pre-match-xG and odds field names in sample match records. Field-name presence is not proof that values are non-null, timestamped, available before kickoff, or complete across fixtures and markets.

## Important governance and scope separation
- The existing governed 27-code universe and the proposed 44-league target must remain separate until owner-approved mapping governance is documented.
- The existing run's 18 leagues with predictions in the 44-target workbook are a different count from the 18 exact catalogue matches in the 27-code endpoint audit. Do not combine these counts.
- The known South Africa identity issue must be handled through the audited code `ZAF_PSL`; do not substitute `ZA` or `RSA` silently.
- Do not infer that the nine unmatched leagues have been removed from Oracle.
- Do not fabricate fixtures or probabilities to fill missing coverage.

## Next executable work, in order
1. Re-run the catalogue reconciliation with candidate-name normalization used only for discovery, while preserving original provider names and exact evidence.
2. For each unmatched competition, inspect all catalogue names/seasons and confirm whether it is absent, selected-league restricted, a naming variant, or ambiguous. If the catalogue truly omits it, record `NO_PROVIDER_MATCH` only after that check.
3. Build a distinct 44-row target crosswalk with provider season IDs and explicit statuses. Do not overwrite the protected 27-code manifest.
4. For every supported target, fetch complete season fixtures using bounded pagination and record page counts, fixture counts, duplicate IDs, season IDs and source timestamps.
5. Audit non-null coverage and point-in-time provenance for xG, odds, form and standings. Historical table results must be independently checked for as-of correctness.
6. Publish a final coverage matrix and exception ledger. Production promotion remains blocked until gates pass and the owner explicitly approves.

## Evidence and limitations
Evidence files supplied by the project owner:
- `footystats-selected-league-catalogue.zip`
- `footystats-27-league-endpoint-audit.zip`

This report does not claim a successful full-season ingestion, verified entitlement for all 44 leagues, a production accuracy rate, or completion of autonomous refresh. Those remain open until supported by full-run artifacts and source-level validation.

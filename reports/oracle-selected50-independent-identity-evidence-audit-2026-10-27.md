# Selected-50 Independent Identity Evidence Audit — 2026-10-27

**Status:** Research-only. **Parent competition IDs verified: 0/50. Provider-to-canonical bridges verified: 0/50. Human-approved mappings: 0. Production/betting eligibility: NOT_GRANTED.**

## Current branch and evidence lineage

- Research branch: `research/oracle-50-league-readiness-audit`
- Identity evidence register: [CSV](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-independent-identity-evidence-register-2026-10-27.csv)
- Register commit: [`21139591e7a7ccaedcebcebaa92411c15e201089`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/21139591e7a7ccaedcebcebaa92411c15e201089)
- One-call identity probe report: [sanitized result](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-footystats-one-call-identity-probe-result-2026-10-27.md)
- Probe workflow run: [40562430790 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790)
- Probe artifact: [12760832880](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12760832880), SHA-256 `54b25732953cae74b59963613e4c2948c643612dc86dafa11b038a58ffdb7015`
- Existing archive QA: [run 40423922693](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693), artifact 12698682583; existing runtime QA: [run 40554064150](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150), artifact 12757295232.
- This audit uses existing GitHub repository artifacts, manifests and public documentation only. **No provider API request was made.**

## Independent interpretation of the public documentation

1. The official [FootyStats League List documentation](https://footystats.org/api/documentations/league-list) says each season of a competition has a unique ID and labels `season.id` / `season.year` as the season fields. This supports treating the selected IDs as season IDs; it does not define a stable parent competition ID in the documented sample.
2. The official [League Stats / Get Season Stats and Teams documentation](https://footystats.org/api/documentations/league-season-stats-teams) documents `league-season?season_id=X` and describes `data.id` as a season ID. Its example request uses `season_id=2012`, while the displayed sample response has `data.id="161"` and season `2017/2018`. That example inconsistency prevents relying on the sample alone to establish an identity bridge.
3. The official [League Matches documentation](https://footystats.org/api/documentations/match-schedule-and-stats) defines `season_id` as the ID of the league season retrieved. The match endpoint is therefore season-scoped.
4. The approved one-call result for selected ID `16571` returned `data.id=16571`, Argentina, Primera División, 2026. This is internally consistent for that one season record, but it proves neither a parent competition ID nor mappings for the other 49 IDs.

## Full 50-row candidate audit

The linked CSV records each selected season ID, manifest country/name, provider catalogue name/year, legacy Run 56 manifest status and match count, retained private-package evidence for the 19 historical Run 56 gaps, current canonical-code candidate (if any), research-only alias code, parent-ID status, bridge status and disposition.

### Aggregate results

| Check | Result | Correct interpretation |
|---|---:|---|
| Selected manifest rows / unique selected IDs | 50 / 50 | Input manifest is internally unique |
| Current selected-season archive coverage | 50/50 selected groups; 14,051 current-season fixture rows in the existing private-archive audit | Structural archive coverage only; not canonical identity |
| Legacy Run 56 exact manifest rows | 31 | A snapshot-specific evidence layer, not the latest archive total |
| Legacy Run 56 gaps reconciled by retained package row-level QA | 19 | Not evidence that those leagues are unsupported; do not re-ingest solely to fill this old manifest gap |
| Candidate canonical matches requiring human review | 22 | Candidate only; no direct provider-ID-to-canonical proof |
| No unique match in current 27-league registry | 28 | Expansion candidates; no canonical code assigned |
| Research-only R50 grouping aliases | 50 | Derived from country/name labels; not provider IDs or production codes |
| Verified parent competition IDs | 0/50 | Remains blocked |
| Verified provider-to-canonical bridges | 0/50 | Remains blocked |
| Human-approved mappings / production-eligible mappings | 0 / 0 | Release not granted |

### The 22 candidate codes — review only

The existing country-constrained, explicit full-name/alias crosswalk proposes these candidates: `AUT_A1` Austrian Bundesliga; `BEL_B1` Belgian Pro League; `HRV_HR1` Croatian HNL; `CZE_CZ1` Czech First League; `ENG_E0` Premier League; `ENG_E1` Championship; `ENG_E2` League One; `FRA_F1` Ligue 1; `FRA_F2` Ligue 2; `DEU_D1` Bundesliga; `DEU_D2` 2. Bundesliga; `ITA_I1` Serie A; `ITA_I2` Serie B; `NLD_N1` Eredivisie; `POL_P1` Ekstraklasa; `PRT_P2` Liga Portugal 2; `SCO_SC0` Scottish Premiership; `ZAF_PSL` South African PSL; `ESP_SP1` La Liga; `ESP_SP2` Segunda División; `TUR_T1` Turkish Super Lig; `UKR_UA1` Ukrainian Premier League.

These are plausible country/name candidate correspondences, not verified ID joins. Human review must confirm competition/tier and canonical registry intent; a provider season ID, country/name equality, or sample match is not sufficient evidence of a parent ID or canonical fixture/team join.

### The 28 unmatched groups

Argentina — Primera División; Australia — A-League; Brazil — Serie A; Canada — Canadian Premier League; Chile — Primera División; China — Chinese Super League; Colombia — Categoria Primera A; Denmark — Superliga; Ecuador — Primera Categoría Serie A; Finland — Veikkausliiga; Greece — Super League; India — Indian Super League; Japan — J1 League; Mexico — Liga MX; Norway — Eliteserien; Paraguay — Division Profesional; Peru — Primera División; Republic of Ireland — Premier Division; Romania — Liga I; Russia — Russian Premier League; Saudi Arabia — Professional League; Serbia — SuperLiga; South Korea — K League 1; Sweden — Allsvenskan; Switzerland — Super League; USA — MLS; Uruguay — Primera División; Venezuela — Primera División.

No canonical code is assigned to these rows. The CSV's `R50_...` values are explicitly labelled research aliases derived from source labels only; they are not canonical codes, provider competition IDs, or permission to create production registry entries.

## Identity decision

- Keep the selected IDs in season-ID fields only.
- Keep parent competition IDs blank and bridges unverified for all 50.
- Keep all 22 candidate mappings at human review; keep all 28 unmatched rows as research-only expansion candidates.
- Do not use fuzzy matching or generic country-prefix stripping to approve any row.
- Do not modify the protected production registry or Oracle V1.6/V1.6.3 logic, probabilities, thresholds, calibration, ledgers or governance.

## Next evidence gate

Obtain a written provider answer to the exact schema/identity questions in the clarification draft. Ask for the field semantics or a documented stable cross-season identifier; do not request another API call. If the provider confirms no parent identifier is exposed, any alternative identity contract must be separately reviewed and approved while preserving each selected value as a season ID.


## Direct artifact inspection (2026-10-27)

Artifact `12760832880` was downloaded read-only and inspected. The ZIP contains only `identity-probe-summary.json` (766 bytes); no raw provider payload or API key is present. The downloaded ZIP SHA-256 was recomputed as `54b25732953cae74b59963613e4c2948c643612dc86dafa11b038a58ffdb7015`, matching the GitHub artifact metadata and the existing report. The summary confirms one attempted `league-season` request, HTTP 200, provider success, one returned record and selected ID `16571` with the same `data.id`, Argentina, Primera División and season 2026. Its own interpretation explicitly says identifier semantics remain unverified. No request was repeated.

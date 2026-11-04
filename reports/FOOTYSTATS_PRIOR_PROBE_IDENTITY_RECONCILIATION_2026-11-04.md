# FootyStats prior provider identity probe reconciled to the current 49-league catalogue

**Evidence date:** 4 November 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** offline exact-ID reconciliation of the 29 October 2026 one-season provider identity probe to the current 4 November 2026 49-league crosswalk and exact 2024-forward season plan. No API calls or raw provider payloads were used.

## Executive result

A prior sanitized identity probe contains 50 selected provider-season records. Exact joins using the current crosswalk's `legacy50_selected_provider_season_id` found **44 of the current 49 leagues** in that prior probe.

All 44 exact joins pass all of these checks:

- exact provider season ID exists in the current 2024-forward season plan under the same exact current provider league name;
- prior manifest country equals the provider-returned country;
- prior manifest competition name equals the provider-returned competition name;
- exact concatenation of provider country plus provider competition name reconstructs the current provider league name;
- prior-probe `comp_master_id` equals the observed value retained in the current candidate crosswalk.

Results:

| Check | Result |
|---|---:|
| Prior identity probe rows | 50 |
| Current crosswalk rows | 49 |
| Exact selected season ID joins | 44 |
| Exact country matches | 44/44 |
| Exact competition-name matches | 44/44 |
| Exact country + competition composite matches | 44/44 |
| Exact `comp_master_id` value matches | 44/44 |
| New current catalogue leagues without prior probe | 5 |
| Legacy selected-50 probe IDs absent from current 49 | 6 |

This materially improves provider identity evidence for the 44 overlapping competitions. The current 756-row provider-season registry still has blank `provider_country` and `provider_competition_id` columns; the 29 October probe supplies a separate exact country/name observation for the 44 matching selected season IDs. It does not provide a verified provider parent competition ID.

## Five current leagues without prior probe evidence

The following competitions were added to the current selected catalogue after the earlier selected-50 identity probe and have no matching prior probe row:

1. Bulgaria First League
2. Egypt Egyptian Premier League
3. Portugal Liga NOS
4. Qatar Stars League
5. Wales Welsh Premier League

They remain unmapped pending authoritative country/competition identity evidence and owner review. No fuzzy name matching was used.

## Six legacy selected-50 probe IDs absent from the current 49

The prior probe records the following selected season IDs, but none is referenced by the current 49-row crosswalk:

| Country | Competition | Prior selected season ID | Prior observed comp_master_id |
|---|---|---:|---:|
| Finland | Veikkausliiga | 16572 | 125 |
| India | Indian Super League | 17964 | 169 |
| Republic of Ireland | Premier Division | 16537 | 264 |
| Russia | Russian Premier League | 17178 | 268 |
| South Korea | K League 1 | 16627 | 294 |
| Venezuela | Primera División | 16617 | 339 |

This establishes that these are legacy selected-50 probe records absent from the current `chosen_leagues_only` 49-league selection. It does **not** establish that FootyStats has discontinued them or that they are unavailable in another provider catalogue query. They remain explicit owner-decision items; do not re-add them automatically.

## comp_master_id and canonical mapping limitations

The `comp_master_id` values match across the 44 exact selected-season-ID joins. This is useful consistency evidence, but it is not proof that the field is a stable parent-competition ID across multiple seasons. The joined evidence concerns one selected season ID per league; cross-season stability and provider field semantics remain unverified.

- Verified provider parent competition IDs: **0**.
- Approved Oracle canonical mappings: **0**.
- Candidate canonical IDs remain human-review-only.
- No candidate or `comp_master_id` value has been promoted.

The 44 country/name matches are exact provider identity evidence for those selected season IDs, not approval of an Oracle canonical bridge. The five new current leagues remain without prior probe evidence.

## Machine-readable outputs and reproducibility

- `scripts/reconcile_footystats_prior_probe_identity_to_current_catalogue.py`
- `tests/test_footystats_prior_probe_identity_reconciliation.py`
- `.github/workflows/footystats-prior-probe-identity-reconciliation.yml`
- `data/footystats/catalogue-season-mapping-audit-2026-11-04/current-49-prior-probe-identity.csv`
- `data/footystats/catalogue-season-mapping-audit-2026-11-04/legacy6-absent-current-catalogue.csv`
- `data/footystats/catalogue-season-mapping-audit-2026-11-04/prior-probe-identity-summary.json`

Validation workflow: [41901550508](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41901550508) — **PASS**. The exact-ID reconciler compiled, its regression suite passed, sanitized outputs were generated, and the artifact uploaded.

Artifact ID: `13359440416`  
Artifact SHA-256: `0c505b66bba2e525ef1d1bf1dc682011e87abeec99e2c51e583bfb28eb8e2232`

## Next actions

1. Keep the 44 exact provider country/name observations linked to their exact selected season IDs, but do not elevate them to canonical competition IDs.
2. Obtain authoritative parent-competition semantics and cross-season stability evidence for `comp_master_id` before considering it a provider league key.
3. Acquire authoritative provider country/name/competition-ID evidence for the five new current leagues only after the shared gateway and private archive gates are satisfied.
4. Ask the owner to decide whether the six legacy selected-50 competitions should be restored to the selected catalogue or intentionally excluded from the 49-league scope.
5. Preserve all 49 current rows and six legacy exclusions in the human decision register.

No FootyStats API requests were made; no raw payloads were read; no main-branch or private-repository writes occurred. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and eligibility remain unchanged. All outputs remain research-only and ineligible for production/betting.

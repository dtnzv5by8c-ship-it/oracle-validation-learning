# FootyStats selected-catalogue league mapping and season-boundary audit

**Evidence date:** 4 November 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** offline audit of sanitized provider-season registry, exact historical season plan, exclusions and provider-to-Oracle candidate crosswalk. No API calls, raw payload reads, private-repository access or production changes.

## Executive findings

The selected FootyStats catalogue contains 756 provider-season rows across 49 exact provider league names. The historical plan and exclusion file partition all 756 unique provider season IDs without overlap or omission:

- 182 planned provider-season partitions across all 49 leagues for the 2024-01-01 through 2026-11-04 UTC window.
- 574 season IDs explicitly excluded by the current season-label year-envelope rule.
- 49 crosswalk rows; every crosswalk league name matches the provider registry league set.
- For every league, the semicolon-delimited history provider season IDs and labels in the crosswalk exactly match the historical plan.
- All 182 planned IDs are unique and present under the exact provider league name and season label in the source registry.

This verifies exact provider-season mapping and the current crosswalk's consistency. It does **not** verify a provider-native competition/league ID or an approved Oracle canonical mapping.

## Material league-identity gap

The current sanitized provider-season registry has 756 rows, but:

- `provider_country` is blank in **756/756** rows.
- `provider_competition_id` is blank in **756/756** rows.
- The candidate crosswalk has **0 verified provider parent competition IDs**.
- A `comp_master_id` value is observed for 44 current catalogue leagues, but the existing evidence explicitly does not establish its parent-competition or canonical-ID semantics.
- Five new current-catalogue leagues have no observed `comp_master_id` in the current crosswalk evidence.

The prior reconciliation's 44 exact legacy country/competition-name matches are useful historical comparison evidence, but they do not fill the missing current provider country or competition-ID fields. They must not be treated as a verified provider-native league identifier.

Canonical status remains:

| Status | Leagues |
|---|---:|
| Candidate canonical IDs requiring human approval | 22 |
| No match in the current protected 27-league registry | 22 |
| New current catalogue leagues not assessed against that registry | 5 |
| Approved canonical mappings | **0** |

The 49-row human decision queue records the exact provider league name, catalogue season count, 2024-forward provider season IDs and labels, legacy reconciliation state, candidate canonical ID (if any), observed `comp_master_id` (if any), missing identity fields and required owner decision. All rows remain `mapping_approved=false`, `production_eligible=false`, and `betting_eligible=false`.

## Season-label and date-boundary audit

The plan applies the exact inclusive UTC fixture window:

- Start: `2024-01-01T00:00:00Z`
- End: `2026-11-04T23:59:59.999999Z`

Every one of the 182 planned rows contains these exact boundaries and requires a fixture-level kickoff filter. Season membership alone is not fixture-date coverage.

The 574 exclusions are all labelled `SEASON_OUTSIDE_HISTORY_WINDOW`; their parser-status distribution is 428 `CONSECUTIVE_YEAR_RANGE` and 146 `START_YEAR_ONLY`.

A specific edge case requires follow-up: **14 calendar-year 2023 seasons** are excluded as `START_YEAR_ONLY`. The offline metadata does not contain fixture kickoff rows for these excluded season IDs, so it cannot prove that no delayed fixture from one of those 2023 seasons was played on or after 2024-01-01. These 14 exact IDs are listed in the machine-readable summary as `CALENDAR_2023_SEASON_EXCLUDED_BY_LABEL_ONLY`. Do not add them automatically to the current 182-season plan; keep them as a date-boundary review queue until exact fixture kickoff evidence is available.

The plan includes 35 `20232024` partitions and 36 `20262027` partitions. The former are included because their season-year envelope intersects 2024; the latter are included because they intersect 2026. Both groups still require the exact fixture-level UTC filter to remove any pre-window or post-window records.

## Validation implementation

Added an offline audit script and regression suite:

- `scripts/audit_footystats_catalogue_season_mapping.py`
- `tests/test_footystats_catalogue_season_mapping.py`
- `.github/workflows/footystats-catalogue-season-mapping-audit.yml`

The validator fails closed on duplicate season IDs, incomplete plan/exclusion partitioning, crosswalk league-set differences, crosswalk season-ID/label mismatch, changed UTC boundaries, invalid season-year normalization, or any production/betting eligibility set true.

The workflow passed:

- Run: [41900985917](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41900985917)
- Conclusion: **success**
- Artifact: `13358086114`
- Artifact SHA-256: `0e53fdbc26accd70eecfa8b414b44ce68d1185c9d40be3e225ac630d0cdf747e`
- Artifact contains the 49-row sanitized human decision queue and the JSON audit summary.

Machine-readable outputs committed alongside this report:

- `data/footystats/catalogue-season-mapping-audit-2026-11-04/human-decision-queue.csv`
- `data/footystats/catalogue-season-mapping-audit-2026-11-04/summary.json`

## Interpretation and next actions

1. Obtain authoritative provider documentation or a provider-supplied field proving the meaning and scope of the 44 observed `comp_master_id` values; do not infer semantics from numeric values or league names.
2. Obtain authoritative country and provider competition identifiers for the 49 selected leagues, or retain the missing identity status and keep canonical mapping unapproved.
3. Resolve the 22 candidate mappings through explicit human review and assess the five new catalogue competitions against the owner-approved expanded Oracle registry.
4. Verify the 14 excluded calendar-year 2023 partitions against exact kickoff-date evidence before closing the 2024 lower-bound exclusion question.
5. During any future approved ingestion, filter every fixture by exact kickoff timestamp and preserve both season ID and fixture ID; do not use season membership as a substitute for date filtering.
6. Keep all 574 exclusions and 182 planned rows traceable to the original 756-row registry.

No H2H, recent form, home/away form, standings, goal history or xG coverage is certified by this offline metadata audit. xG remains quarantined pending point-in-time provenance. No provider requests were made.

## Governance

No changes were made to Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers or eligibility. No main-branch or private-repository writes were made. All outputs remain research-only with `production_eligible=false` and `betting_eligible=false`.

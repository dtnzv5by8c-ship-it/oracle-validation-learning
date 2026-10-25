# Project Oracle 50-League Readiness Audit — Run 15

**Audit timestamp:** 2026-10-25  
**Scope:** Owner-approved 50 selected FootyStats season IDs.  
**Decision:** INCOMPLETE — production readiness is NOT GRANTED.

## Research-only artifacts saved

- Crosswalk revision 16: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r16.csv`
- Concise per-league/per-market gates: `reports/oracle-selected50-per-league-market-readiness-2026-10-25-run15.csv`
- Prior crosswalk revision 14 retained as the archive-only baseline; revision 15 records the first full 50-season provider QA evidence.
- Protected production registry, model logic, weights, probabilities, thresholds, calibration, version, and canonical ledgers were not changed.

## Exact selected-ID and provider catalogue evidence

The selected manifest and the ingestion manifest are both 50 rows with exact ID-set equality. The private ingestion package for run 40176065362 matched all 50 selected IDs exactly to `season[].id`; no catalogue-unmatched IDs or ambiguous exact IDs were reported.

The sanitized schema audit (run 40180235243, artifact 12593716509) found:
- Catalogue league object keys: `country`, `image`, `name`, `season`.
- No top-level `league.id` field.
- Season object keys include `country`, `id`, and `year`.
- No parent competition ID was inferred.

Private archive QA run 40180314626 (artifact 12593552798) verified:
- 50/50 exact selected ID-set match.
- 50/50 exact composite label matches of `selected country + selected competition name` against the provider's retained `league.name` value.
- 0/50 parent competition IDs populated; separate provider country values were not retained in the ingestion ledger.
- 50/50 season folders present and structurally valid.
- 14,051 match records, 14,051 unique season/fixture ID pairs, zero duplicate pairs.
- Kickoff-like fields, score-pair fields, team-ID pairs, and team-name pairs present on all 14,051 records.

The provider ID semantics are now established as **season IDs**, not parent competition IDs. This is a provider-season-to-private-fixture join, not yet a join to Oracle's current fixture feed.

## Per-league provider season evidence

The private package was fetched on 25 October 2026. Its observed fixture dates span 16 January 2026 through 6 June 2027. Across the 50 selected seasons:

- 14,051 fixture records across 841 team records.
- 5,637 fixture rows fall within the locked primary window, 20 March 2025–20 September 2026, in this selected-season package.
- 6,912 rows have past kickoff dates; 7,004 have future kickoff dates; 135 rows are not classified into those two groups by the QA counters.
- Nonempty table payloads exist for 50/50 seasons, but standings chronology/as-of-kickoff provenance is not verified.
- Research-only recent-form-5 availability, calculated from explicitly completed earlier matches **within each selected season only**, is 11,781/14,051 home-team rows (83.84%), 11,773/14,051 away-team rows (83.79%), and 11,744/14,051 fixtures where both teams have five prior matches (83.58%). This does not include prior-season carryover and is not promoted to Oracle's current team-state feature file.
- A prior H2H meeting is available within the selected-season data for 5,294/14,051 fixtures (37.68%).
- Nonempty xG values are present on 14,051/14,051 rows. Nonempty odds values are present on 7,330/14,051 rows (52.17%). The match schema contains no verified odds timestamp and no as-of timestamp/provenance sufficient to validate xG or odds point-in-time availability.

The separate Run 56 archive remains 31/50 exact selected-season records, 9,708 archive fixture rows, and 19 IDs without a Run 56 archive manifest record. Those 19 are not zero-coverage leagues in the new provider package; the newer private package now contains all 50 selected season IDs.

## Canonical mapping state

- 50 selected IDs retained exactly.
- 22 canonical codes remain **candidates requiring human review**, never approved mappings.
- 28 rows remain **UNRESOLVED** because no exact or explicitly approved alias supports a canonical mapping.
- 0 approved mappings.
- All selected IDs have exact provider-season-level fixture evidence, but the parent competition ID remains unexposed by the catalogue schema. Canonical mappings and production eligibility remain separate gates.

## Current Oracle data state and readiness gates

Private production repository files remain stale/inconsistent:
- Protected canonical registry: 27 entries, 13 `CONTROLLED`, 14 `NOT_INGESTED`; unchanged.
- Legacy readiness matrix: 27 rows, last refreshed 1 October 2026; unchanged and not proof of selected-50 readiness.
- Current source manifest: generated 8 October 2026, requested window 1–10 October.
- Reconciliation status: generated 7 October 2026, `EVENT_TRUTH_STALE`, 108 match rows and 128 goal-event rows reported, with four completed matches missing goal-event chronology.
- Checked-in current match CSV: 241 data rows through 10 October.
- Checked-in current goal-event CSV: 137 data rows, inconsistent with the 128 reported by reconciliation status.
- Current source reconciliation CSV: 108 data rows.
- Team-state manifest: generated 7 October, claims 12,883 rows; checked-in prematch team-state CSV has zero data rows.
- Upcoming fixture CSV: 80 rows, ending 17 October.
- Feature snapshot manifest: header only, zero data rows.

Latest dry-run planner run 40180625415 (artifact 12593698287) completed successfully. Regression tests, market-gate tests, exact-catalogue resolver tests, prediction-input contract tests, and plan validation passed. The artifact evaluated 50 rows and marked all 50 production-ineligible; M-1UP is blocked and BTTS Yes, Double Chance, and Double Chance + Under 4.5 are not verified.

## Provider-call safety incident and prevention

The first selected-50 ingestion run 40176065362 completed with 201 API requests, 50/50 seasons ingested, and private package SHA-256 `9b5eecf376dac804231bfcb75d9381a4307b38f082cadd9a775d48ec3e5310dd`.

A second run, 40180281634, was triggered by a research-branch commit that edited the push-triggered ingestion workflow. It made another 201 API requests and ingested 50 seasons in the temporary runner, but failed during private-release creation because the fixed release tag already existed. It did not overwrite the existing private release; only a sanitized ledger artifact (12594446943) was uploaded. The failed run consumed requests before discovering the tag collision.

To prevent repetition, research commits 09f2aeb157168f9f837ea4174b46290952dc7c81 and 230f47cf6559b48bc6984b5a669ac58a758a2e3a changed the ingestion and schema-audit workflows to manual dispatch only, require explicit provider-credit confirmation, and preflight the existing release tag before ingestion. No subscription or billing settings were changed. No additional provider requests were made by this audit after that guard was installed.

## Outstanding blockers — do not bypass

1. Current Oracle fixtures/team IDs are not reconciled to the 50 provider season datasets.
2. Current team-state CSV is empty despite its stale manifest.
3. Event-truth row counts disagree and four completed matches lack goal-event chronology.
4. Current feed freshness and exact fixture/team joins are unverified.
5. Historical standings as-of kickoff are unavailable; the current table payload is not a historical standings snapshot.
6. xG and odds point-in-time provenance is unverified; odds timestamps are absent.
7. 19 selected IDs still lack a Run 56 archive manifest record, despite now having provider season data.
8. 22 candidate canonical mappings need human review; 28 remain unresolved.
9. M-1UP, BTTS Yes, Double Chance, and Double Chance + Under 4.5 have not passed all required gates.

**Next safe work:** reconcile the new private provider season fixtures to the current Oracle feed using exact IDs; repair the current match/event/team-state inconsistency; validate historical standings and pre-match feature timestamps; then rerun all four market gates and tests. No provider refresh should be triggered without explicit credit-use approval.

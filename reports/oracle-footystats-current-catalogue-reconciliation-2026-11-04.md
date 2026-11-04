# Project Oracle — Current FootyStats catalogue reconciliation

**Evidence date:** 4 November 2026  
**Scope:** current FootyStats selected catalogue, compared with the saved 50-league manifest from 24 October 2026.  
**Lane:** research-only; offline; no provider API calls made by this reconciliation.

## Executive result

The current FootyStats catalogue retrieved with `chosen_leagues_only=true` contains **49 leagues and 756 provider league-season records**. The exact season plan for 1 January 2024 through 4 November 2026 contains **182 provider season IDs across all 49 current leagues**.

The current 49-league catalogue is not identical to the prior 50-league manifest:

- **44** legacy country/competition pairs match the current provider name exactly, and all 44 legacy selected season IDs are present under the same exact provider name.
- **6** prior selected leagues are absent from the current selected catalogue.
- **5** leagues are newly present in the current selected catalogue.
- Net result: 49 current leagues. No missing league was silently substituted.

## Current catalogue changes

### Present in the prior 50 manifest but absent from the current selected catalogue

1. Finland — Veikkausliiga
2. India — Indian Super League
3. Republic of Ireland — Premier Division
4. Russia — Russian Premier League
5. South Korea — K League 1
6. Venezuela — Primera División

### New in the current selected catalogue

1. Bulgaria — First League
2. Egypt — Egyptian Premier League
3. Portugal — Liga NOS
4. Qatar — Stars League
5. Wales — Welsh Premier League

These are provider-catalogue membership differences, not evidence that FootyStats has permanently discontinued or lacks those competitions. The current response only establishes what was returned by the selected-catalogue query on 4 November.

## Provider-to-Oracle mapping status

The saved prior research crosswalk provides **22 canonical ID candidates** for current catalogue leagues. Every candidate remains explicitly human-review-only and is not promoted to an Oracle canonical ID.

- 22: candidate canonical IDs requiring human approval.
- 22: no match in the current protected 27-league registry.
- 5: not assessed against the current protected registry because they are new to the current selected catalogue.
- **0 approved Oracle canonical mappings.**
- **0 verified provider parent competition IDs.**

The current protected registry contains 27 leagues and is not the full expanded research universe. A no-match in that registry does not mean that no canonical mapping can ever exist.

The prior evidence also contains 24 historical-ledger league-code candidates. These are based on ordered team-pair plus calendar-date joins, not kickoff-precise fixture identity. They remain candidates only and cannot be used as canonical IDs or approved joins.

The provider-supplied `comp_master_id` values were observed in an earlier diagnostic, but their semantics and cross-season stability are not established. They are retained as evidence only; the parent-competition ID field remains blank.

## 2024-forward season map

- History start: **2024-01-01 UTC**.
- Inclusive end: **2026-11-04 UTC**.
- Current selected leagues: **49**.
- Current catalogue season records: **756**.
- Planned season partitions intersecting the window: **182**.
- Every planned row retains the exact provider season ID and season label.
- Every fixture returned by a future endpoint run must still be filtered by its explicit kickoff timestamp. A 2023/24 season partition can contain pre-2024 fixtures; a 2026/27 partition can contain post-4-November fixtures.

The plan is not evidence that the 182 seasons have been ingested. It is an exact-ID acquisition worklist only.

## Endpoint and field investigation status

The offline endpoint contract audit documents:

| Oracle requirement | FootyStats source / method | Current status |
|---|---|---|
| Fixtures and completed results | `league-matches`, paginated by season | Contract documented; authenticated historical retrieval not completed |
| Team identities and season membership | `league-teams`, paginated by season | Contract documented; exact current 2024-forward coverage not verified |
| H2H | Exact prior match history derived from team IDs, with optional `match` detail endpoint | Coverage not verified; one-match detail requests may be costly |
| Recent form and home/away form | Derived from exact prior completed fixtures and ordered venue roles | Not rebuilt for the full current 49-league / 182-season scope |
| Standings | `league-tables` or validated reconstruction from results | Fixture-time and competition-format validity not established |
| Goals and goal environments | Exact result fields from completed fixtures | Historical field coverage not verified for the current catalogue scope |
| xG | Match/detail fields with pre-match-labelled values | **Quarantined**; no verified point-in-time capture/revision provenance |

Pagination validators require explicit provider page metadata and exact page row counts. A successful HTTP response alone is not treated as complete retrieval.

## Request and storage governance

- User-approved absolute ceiling: **1,800 FootyStats requests per rolling 60 minutes**.
- The budget helper uses an operational reservation ceiling of 1,500, preserving 300 requests of headroom.
- The shared request-budget helper is now integrated into a single manual-dispatch FootyStats endpoint preflight gateway on the governed research branch. It uses the repository-wide concurrency group `footystats-global-api-gateway`, a durable reservation commit before provider access, a timestamp-only rolling ledger, 1.1-second pacing, and no retries.
- The gateway enforces the 1,800 absolute rolling-hour limit and 1,500 operational reservation ceiling with 300 headroom; any lower provider `request_limit` is binding.
- The new sanitized endpoint preflight checks up to five endpoints per season (matches page 1, teams page 1, tables, season, and one exact-match details/H2H sample). It persists only field-presence/pagination metadata and payload hashes, never raw payloads.
- The preflight workflow has not yet been manually dispatched. No additional provider API requests were made by the gateway implementation.
- Raw provider payloads have not been written to the public research repository. The protected private archive write path remains gated and must not be bypassed; full historical ingestion is not yet started.
- No API key or secret was read by the offline reconciliation.

## Validation and outputs

- Governed branch: `research/oracle-50-league-readiness-audit`.
- Crosswalk builder: `scripts/reconcile_footystats_current_catalogue_to_legacy50.py`.
- Regression tests: `tests/test_footystats_current_catalogue_reconciliation.py`.
- Contract workflow: `.github/workflows/oracle-selected50-contract-tests.yml`.
- Earlier validation run: [Oracle Selected-50 Safety Contract Tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41861736989).
- New targeted preflight contract run: [FootyStats Budgeted Preflight Contract Tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41864509844), job `126695135837`. Its log records py_compile success and 35 passing unit/contract tests; the GitHub run metadata reader still reports queued/no final conclusion, so formal workflow completion remains unverified.
- Gateway implementation checkpoint: [ORACLE_FOOTYSTATS_BUDGETED_PREFLIGHT_GATEWAY_2026-11-04.md](ORACLE_FOOTYSTATS_BUDGETED_PREFLIGHT_GATEWAY_2026-11-04.md).
- Machine-readable crosswalk: [current-catalogue-provider-to-oracle-candidate-crosswalk.csv](../../data/footystats/current-catalogue-reconciliation-2026-11-04/current-catalogue-provider-to-oracle-candidate-crosswalk.csv).
- Machine-readable summary: [current-catalogue-reconciliation-summary.json](../../data/footystats/current-catalogue-reconciliation-2026-11-04/current-catalogue-reconciliation-summary.json).

## Next gates

1. Reconcile the five newly selected competitions against the protected canonical registry and owner-approved expanded Oracle universe.
2. Resolve the six legacy manifest exclusions with the owner/provider configuration; do not re-add them automatically.
3. Manually dispatch the sanitized endpoint preflight workflow and inspect its per-season endpoint/field coverage report; the available GitHub connection cannot dispatch workflows itself.
4. Resolve owner-approved canonical Oracle mappings for the 44 exact-name matches, 22 human-review candidates, six legacy exclusions and five newly selected competitions. The current reconciliation has zero approved canonical mappings and zero verified parent competition IDs.
5. Confirm the approved private raw-data destination and write permission without touching production files.
6. Build the resumable full-pagination ingestion executor behind the same global request gateway; checkpoint every page and verify exact fixture/team identity.
7. Derive H2H, recent form, venue splits and goal features from the exact completed match spine; separately validate fixture-time standings.
8. Keep xG quarantined until provider point-in-time capture and revision semantics are verified.
9. Rebuild the Master OMI and Visual Intelligence only after the source data and field-level coverage pass their gates.

## Governance

Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility were not changed. All mapping candidates and season-plan outputs remain research-only, `production_eligible=false` and `betting_eligible=false`. No provider API calls were made by this reconciliation.

## 2026-11-04 offline ingestion-manifest implementation update

- Added `scripts/build_footystats_full_ingestion_manifest.py` and six regression tests. The planner consumes only sanitized endpoint-preflight reports plus the exact provider season plan.
- It requires exact provider season ID, league name and season label agreement. Any missing, incomplete or mismatched preflight row remains explicitly blocked in the coverage output; no fuzzy joins or silent omissions.
- For each preflight-verified season it plans every `league-matches` page, every `league-teams` page, and one `league-tables` plus one `league-season` snapshot request. Planned batches are capped at 1,500 requests and must still be reserved against the live ledger before execution.
- H2H, recent form and home/away form are planned to be derived from the complete exact chronological match spine. Fixture-time standings remain unresolved; xG remains quarantined.
- The central manual-dispatch preflight workflow now runs the planner after the preflight attempt and commits/uploads the sanitized manifest and coverage summary. This is still an offline plan, not raw-data ingestion.
- Targeted contract log run 41865887561 / job 126699886190 reports 42 tests OK, including the six manifest tests and workflow integration test. GitHub run metadata remains queued/no conclusion despite the completed test and cleanup log.
- No provider API request or private archive write was made by this update. Full historical ingestion remains blocked until the protected private raw-data destination is authorized and validated.

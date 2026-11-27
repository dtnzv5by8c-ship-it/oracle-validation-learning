# Master OMI MI Root-Cause Cycle — 2026-11-27 02:10 SAST

## Status
- FAIL-CLOSED / NOT RELEASED.
- Latest current reconciliation is CURRENT with 372/372 exact governed FootyStats fixture identities and 100% coverage at generation 2026-11-26T23:49:37Z.
- A fresh rolling 50-league spine refresh has been triggered after this cycle; no stale spine is admissible for release.

## Root-cause matrix
| Field / fixture scope | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|
| Governed weekly fixture input | Prospective workflow was independently rebuilding `oracle_upcoming_fixtures.csv` instead of consuming the governed rolling spine | Public `data/fixtures/governed_50league_current.csv` + manifest | Prospective workflow changed to consume and freshness-check the public rolling 50-league spine as its sole current fixture input | FIXED IN CODE; awaiting fresh execution |
| Exact fixture reconciliation | Reconciliation logic previously depended on obsolete/local spine path | Public rolling spine + exact FootyStats `fixture_id` | Reconciliation now reads the public rolling spine and intersects exact provider IDs only | VERIFIED 372/372 |
| Rolling-spine freshness | Last persisted spine generation was 21:43Z and is stale for the <=90-minute release gate | Public rolling spine manifest | Triggered a fresh 50-league producer execution | IN PROGRESS |
| Current Team State | Durable manifest reports 14,028 rows; binary publication must be independently verified before admission | Current Team State + manifest | Current-data workflow already contains non-empty, hash/row-count persistence gates | BLOCKED pending independent binary verification |
| Current prediction ledger | `omi_prediction_ledger_current.csv` absent from public governed repository | Private prospective production output, when generated | Prospective workflow now consumes the governed rolling spine and produces the authoritative current ledger | BLOCKED |
| Master OMI schema | Public MI artifact currently 372 rows x 139 columns; canonical release requires 264 columns | Canonical V2.1.1 / Master OMI contract | Downstream assembly remains blocked until authoritative prediction ledger and required enrichment layers exist | BLOCKED |
| xG PIT provenance | xG values cannot be promoted without valid capture timestamp | Authoritative xG source with capture timestamp | Keep `UNVERIFIED_NO_CAPTURE_TIMESTAMP`; never infer or backfill | UNVERIFIED |
| H2H / Recent Form / venue | Populate only from pre-kickoff authoritative history; insufficient samples remain explicitly unavailable | FootyStats / current match history | Existing current MI builder uses strict kickoff cutoffs and explicit unavailable statuses | CONTROLLED |
| A:ET / Oracle V1.6 | No release build may mutate protected production logic | Canonical V2.1.1 + protected A:ET hash | No changes authorized | PRESERVED |

## Evidence
- Current reconciliation: `372 matched / 372 governed`, coverage `1.0`, status `CURRENT`.
- Current match rows: 2,672; goal events: 6,694.
- Current source manifest generated 2026-11-26T23:49:30Z with no recorded source errors.
- Current MI artifact: 372 rows x 139 columns; mandatory sample fields inspected had no blanks, but canonical 264-column release contract is not yet satisfied.
- Current prediction ledger is not present in the public repository.

## Release decision
FAIL-CLOSED. No release workbook generated or promoted. No stale spine, frozen dated spine, fuzzy match, timezone normalization, zero-fill, estimation, post-kickoff evidence, or Oracle V1.6/A:ET mutation is permitted.
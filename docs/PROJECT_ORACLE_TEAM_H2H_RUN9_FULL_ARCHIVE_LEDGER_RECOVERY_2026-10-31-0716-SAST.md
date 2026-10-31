# Project Oracle — Full Private Archive Ledger Recovery (Run 9)

**Run timestamp:** 31 October 2026, 07:16 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Status:** research-only; production and betting eligibility not granted

## Executive result

This pass located the exact existing private 50-league archive release and retrieved its sanitized ingestion-ledger Actions artifact. The raw private ZIP itself was not downloaded because the available GitHub connector exposes Actions-artifact download but not private release-asset binary download.

The archive is no longer an unknown asset. GitHub release metadata identifies the exact raw asset, and its SHA-256 digest matches the `sha256` value recorded inside the sanitized ledger:

- **Private release:** `423439954`
- **Tag:** `research-selected50-footystats-history-20261025`
- **Raw ZIP asset:** `675196963` — `oracle-selected50-footystats-private-ingestion.zip`
- **Size:** 66,416,916 bytes
- **SHA-256:** `bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261`
- **Checksum asset:** `675196962` — `private-package.sha256` (117 bytes)

The sanitized ledger came from the already-completed **Oracle Selected-50 FootyStats Exact-ID Ingestion #3**, run ID `40197946253`, workflow ID `395766553`, commit `1cae3f9c5b94332488a41419f44cc955c4e45a0b`. The run completed successfully on 25 October 2026; its job and all substantive steps succeeded. Its sanitized Actions artifact is ID `12601278426`, name `oracle-selected50-sanitized-ingestion-ledger`, 3,571 bytes, digest `761e650baa0e66d398ce2d169231d3e26357e9a67896826581b959309beda28e`, expiring 1 November 2026 at 14:03:14 UTC.

The ingestion run's historical ledger records 801 FootyStats requests. **This Run 9 used zero FootyStats API credits**; it only read existing GitHub metadata and downloaded the existing sanitized artifact.

## Verified archive coverage

The sanitized ledger reports:

- 50 selected league groups;
- 50/50 exact selected-season ID matches;
- 200 historical provider seasons selected and 200 ingested;
- zero failed seasons, zero unmatched selected IDs and zero ambiguous exact IDs;
- 59,049 raw `matches.json` rows;
- 3,366 team-season observations (the sum of each season's `team_count`, not a unique-team count).

Every selected ID occurs exactly once as the current selected season ID in its group's four-season ledger. The 200 `(selected_id, season_id)` keys reconcile **200/200** against the prior `Archive Season Inventory`, with zero mismatches in provider season year, match count, team count or ingestion status.

## Exact reconciliation against Run64 and the 19 unprofiled groups

| Scope | Groups | Seasons | Raw match rows | Team-season observations |
|---|---:|---:|---:|---:|
| Existing Run64 profile extract | 31 | 93 | 30,257 | Not exposed in that summary |
| Full private archive for those same 31 groups | 31 | 124 | 40,797 | 2,265 |
| Additional private archive coverage for those 31 groups | — | 31 | 10,540 | — |
| The 19 Run64-unprofiled groups | 19 | 76 | 18,252 | 1,101 |
| **Full private 50-group archive** | **50** | **200** | **59,049** | **3,366** |

The row counts reconcile exactly: `30,257 + 10,540 + 18,252 = 59,049`. The season folders reconcile exactly: `93 + 31 + 76 = 200`.

For the 19 groups previously unavailable in Run64, the new sanitized ledger matches the existing full-archive inventory **19/19** on four exact season IDs, provider-year set, raw match-row count, maximum team count and team counts by season. Those groups are not empty and are not missing from the private archive.

## What this does — and does not — unlock

The new evidence proves the private raw package contains all 50 selected groups and 200 ingested seasons. It also shows the existing Run64 extract is incomplete relative to that private package: it has 93 season folders and 30,257 rows for 31 groups, while the private archive has 124 season folders and 40,797 rows for those same groups.

However, the sanitized ledger exposes counts only. It does **not** expose team IDs, fixture IDs, kickoff timestamps, scores, status per match, `no_home_away`, or raw `teams.json`. Therefore this run does not calculate new Team DNA or H2H metrics, and it does not fill the 19 missing profiles. Existing 732 Team DNA profiles and 7,188 exact H2H pair profiles remain the Run64 results for 31 groups.

Raw match-row counts are not equivalent to completed scored matches or primary-window matches. The primary validation window remains 20 March 2025–20 September 2026; it cannot be reconstructed from this counts-only artifact.

## Recovery route and current blocker

The current branch's legacy 50-league ingestion workflow is a disabled fail-closed stub; it must not be dispatched. The existing `oracle-selected50-private-archive-qa.yml` workflow is pinned to the older tag `research-selected50-footystats-history-40375285207` and SHA `7c60a239…`; it cannot validate the new 20261025 package as-is because the new release digest is `bc64fbad…`. Do not bypass or weaken checksum validation.

The available GitHub connector can download Actions artifacts by artifact ID but has no release-asset binary-download action. The raw private ZIP asset is identified and digest-pinned, but its bytes were not retrievable in this run. The next required step is a separately reviewed, read-only release-asset retrieval/profile job that:

1. reads only the existing release tag `research-selected50-footystats-history-20261025`;
2. verifies SHA-256 `bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261` before extraction;
3. performs offline, exact-ID Team DNA and H2H profiling across all 50 groups;
4. exports sanitized profile CSVs/workbook only, never raw provider payloads;
5. preserves exact fixture/team IDs, UTC chronology, status/score quarantine and `no_home_away` venue exclusions.

## Governance

- FootyStats API credits used in this run: **0**.
- Completed ingestion, snapshot, runtime, backtest or bridge workflows rerun: **none**.
- Oracle V1.6 production logic changed: **no**.
- Oracle V1.6 probabilities changed: **no**.
- `production_eligible=false`; `betting_eligible=false`.
- Historical ingestion run #3 did use 801 provider requests on 25 October; that is historical provenance, not usage by this run.

## Workbook deliverable

- Workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v18_Full_Archive_Ledger_Reconciliation_0716SAST.xlsx`
- SHA-256: `fa9978b0a44cc0364729bf686a7c091ded6f11aa657e2e51e7b8c8cf33d23136`
- Size: 38,965,984 bytes
- Worksheets: 157
- New Run 9 tabs: 9
- All 148 original v17 worksheet XML parts were preserved byte-for-byte.

The workbook adds full 50-league coverage, the 200-season ledger, 76-season detail for the 19 unprofiled groups, 200-row exact season reconcilation, 19-row missing-group reconcilation, release provenance, Run64 reconciliation and recovery gates.

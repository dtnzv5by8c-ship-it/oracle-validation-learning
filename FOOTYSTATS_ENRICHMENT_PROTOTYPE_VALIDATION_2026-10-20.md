# FootyStats Enrichment Prototype Validation — 20 October 2026

## Status

**Report-only prototype tested; not production validated.** No Oracle production logic, probabilities, weights, thresholds, calibration, or promotion gates were changed. PR #9 remains unmerged. No paid subscription was purchased.

## Source data recheck

The consolidated FootyStats inventory records 47 source exports. Three normalized masters were recovered and re-read:

| Normalized master | Rows |
|---|---:|
| Spain Segunda División, 2024/25–2026/27 | 1,398 |
| Belgium Pro League + France Ligue 2, 2024/25–2026/27 | 1,851 |
| Greece Super League + Romania Liga I + South Africa PSL, 2024/25–2026/27 | 2,246 |
| **Total** | **5,495** |

Across these three normalized masters, the recheck found zero unparsed kickoff dates and zero duplicate league/season/date/home/away keys. Existing inventory coverage remains six governed leagues out of 27, covering 18 of 81 governed league-season combinations. Greece remains outside the governed 27.

## Oracle fixture enrichment sample

The local prototype was run against the Oracle curated report workbook and its Visual Intelligence tab:

- 227 rows produced for 227 nonblank, unique canonical Oracle Fixture IDs.
- Zero duplicate Oracle fixture IDs in the output.
- 12 fixtures had an exact source identity match using fixture date + normalized home team + normalized away team.
- 195 fixtures belong to leagues not represented in the currently available local FootyStats masters.
- 20 fixtures in represented leagues had no exact source fixture in the masters.
- 164 Oracle prediction rows joined to the Visual Intelligence fixture rows using exact date/home/away identity.
- 984 raw probability cells across six markets were copied unchanged. No probability was recalculated.

The FootyStats masters do not carry Oracle Fixture IDs, so the identity crosswalk is explicit and no fuzzy matching is performed. Ambiguous source identities are flagged rather than accepted.

## Chronology and feature checks

Four local synthetic tests passed:

1. Recent form uses completed matches strictly before the cutoff; future matches do not leak into the form sequence.
2. H2H excludes target/future meetings.
3. Historical standings are reconstructed from prior completed results rather than current/final snapshots.
4. Team-name normalization handles accents but does not fuzzy-match distinct names.

The prototype uses a conservative midnight-UTC cutoff for a fixture date when the source workbook does not establish a reliable kickoff timezone. This avoids same-day leakage but may omit earlier matches from the same date. Competition-phase/split rules are not yet audited; reconstructed positions are therefore marked with a phase-validation warning.

## FootyStats API assessment

Official published plan details reviewed on 20 October 2026:

- Hobby: £29.99/month, up to 50 selected leagues, 1,800 requests/hour.
- Serious: £69.99/month, up to 150 selected leagues, 3,600 requests/hour.
- Everything: £389.99/month, 1,500+ leagues, 4,500 requests/hour.

Official documentation describes a league-list endpoint with unique season IDs, league-match pagination and `max_time`, and league-table `max_time` as-of queries. Those descriptions do **not** verify the exact 27 competition mappings or historical season/field coverage. No account-key catalogue response was obtained and no subscription was purchased.

Official references:
- https://footystats.org/api
- https://footystats.org/api/documentations/league-list
- https://footystats.org/api/documentations/match-schedule-and-stats
- https://footystats.org/api/documentations/league-table
- https://footystats.org/api/documentations/terms-of-use-and-legal

The provider's API legal page prohibits resale/redistribution. Keep licensed CSV/API payloads and credentials private; do not commit them to this public repository.

## Acceptance status

| Requirement | Status |
|---|---|
| Reproducible processing of recovered normalized CSV masters | Partial — normalized masters re-read; raw CSV import pilot still needs end-to-end private validation |
| Six governed league CSV coverage documented | Pass for inventory; field/season data quality gaps remain |
| Greece kept separate | Pass |
| Chronological form/H2H/standings tested | Pass on synthetic test cases; real-league phase rules remain unverified |
| Exact Oracle fixture uniqueness | Pass for 227-row sample |
| Exact source Fixture ID join | Partial — external masters lack Oracle IDs; explicit identity crosswalk used |
| Oracle probability preservation | Pass for sample — values copied unchanged |
| Sample CSV/QA output | Pass — generated privately |
| API 27-league/season/field coverage | Blocked — requires account-selected league catalogue and controlled API tests |
| Autonomous private import | Outstanding |
| Production logic changes / paid purchase / merge | None |

**Next:** keep PR #9 open and unmerged; implement and test the complete private import/CI path; verify account-specific API coverage before any purchase recommendation; audit competition-phase rules; do not close Issue #10 until all acceptance criteria are genuinely satisfied.

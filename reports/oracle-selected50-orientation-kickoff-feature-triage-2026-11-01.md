# Project Oracle — Selected-50 Orientation, Kickoff and Feature-Block Triage

**Evidence date:** 1 November 2026 (SAST)  
**Repository lane:** `research/oracle-50-league-readiness-audit`  
**Purpose:** Report-only data-quality analysis and v1.4 candidate QA hardening. No production model or probability changes.

## Executive result

The latest pinned runtime artifact was reconciled against its exact current-snapshot trace. This establishes a fixture-level orientation review list for the 434-fixture reporting horizon, provides a mutually exclusive triage of the 19 schedule discrepancies, and decomposes the 24 feature-blocked fixtures into 25 team-side history shortfalls plus common pair/environment feature gaps.

The v1.4 report-only candidate was hardened with fail-closed orientation QA, side-history audit reconciliation and a separate kickoff-triage CSV. The push-triggered CI checks passed. The manual-dispatch-only archive/runtime rebuild was not run in that CI event, so no new v1.4 workbook is claimed.

The v1.3 template remains the locked canonical weekly contract. The v1.4 work is an isolated candidate and does not change the workbook's 19-sheet structure, 38-column Oracle V1.6 Output or 83-column Market Intelligence view.

## 1. Evidence provenance

| Evidence | Value |
|---|---|
| Source runtime run | `41175230838` (run number 177) |
| Source runtime commit | `ea3f46dab4e54b71a818ab8d8723f36426e36bef` |
| Runtime artifact ID | `13032880970` |
| Downloaded runtime ZIP SHA-256 | `e4bca38c8ab8e6afd5c23d241e4b55fe3ce6277e656172e8cda910718c897ae0` |
| Runtime report SHA-256 | `eac94582e048398df2c17a2e302897dd73648f410b86d655563802192c6a4910` |
| Snapshot workflow run | `41174900415` |
| Snapshot artifact ID | `13031728960` |
| Snapshot trace SHA-256 | `052d4c854426a195e0c7db2a419102f28e671486314fe1cbe08f35f1899714d0` |
| Snapshot trace rows | 2,262 |
| Pinned archive SHA-256 | `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f` |

The runtime artifact contains 434 future-fixture rows. All 434 were joined to the snapshot trace by the exact ordered identity tuple: selected season ID, fixture ID, home team provider ID and away team provider ID. The join produced 434/434 matches, zero duplicate snapshot identities and zero unmatched runtime fixtures.

## 2. Fixture orientation review — 66 flags

The 434 runtime fixtures reconcile as follows:

| Snapshot value | Fixtures | Interpretation |
|---|---:|---|
| `no_home_away=1` | 66 | No home/away distinction; review required for home/away-oriented markets |
| `no_home_away=0` | 368 | Home/away distinction present |
| Unknown or unmatched | 0 | Exact snapshot join passed |

The 66 flagged fixtures are 15.21% of the 434-fixture horizon. They are concentrated in seven competitions:

| Competition | Flagged fixtures |
|---|---:|
| Primera División | 29 |
| Categoria Primera A | 10 |
| Liga MX | 9 |
| Primera Categoría Serie A | 8 |
| Division Profesional | 4 |
| Premiership | 3 |
| Veikkausliiga | 3 |
| **Total** | **66** |

The complete fixture-level list is reproducible from `current_snapshot_candidate_trace.csv` and the runtime report using the exact composite identity above. The v1.4 candidate emits this as `oracle_selected50_fixture_orientation_audit.csv` and exposes the orientation status in the existing Data Quality & Risk worksheet.

FootyStats' public Match Details documentation defines `no_home_away=1` as meaning there is no home/away distinction for the match. It does not define the flag as a neutral-venue indicator. Therefore:
- do not relabel these fixtures as neutral venues;
- do not swap or infer home/away team roles;
- retain the original raw probabilities unchanged;
- mark home/away-oriented markets review-required;
- keep every affected row production-ineligible and betting-ineligible.

The full 2,262-row snapshot trace has 503 rows with flag 1 and 1,759 with flag 0. The 66 count above is only the exact 434-fixture runtime-horizon subset; these two populations must not be conflated.

## 3. Kickoff discrepancy triage — 19 rows

The existing Schedule Reconciliation queue contains 19 exact-identity kickoff mismatches across nine competitions. Signed deltas were independently recomputed as archive kickoff minus runtime kickoff. The mutually exclusive triage buckets are:

| Triage bucket | Rows |
|---|---:|
| Archive kickoff exactly at 00:00 UTC — review indicator | 9 |
| Non-midnight absolute delta greater than 24 hours | 3 |
| Non-midnight absolute delta up to 150 minutes | 5 |
| Non-midnight absolute delta greater than 150 minutes and below 24 hours | 2 |
| **Total** | **19** |

The separately reported indicators overlap: 9 archive-midnight rows; 7 rows with absolute delta greater than 24 hours; and 5 rows with absolute delta up to 150 minutes. Four of the seven >24-hour rows are also in the archive-midnight group.

| Competition | Discrepancies |
|---|---:|
| Professional League | 6 |
| Primera División | 2 |
| Ligue 1 | 2 |
| LigaPro | 2 |
| Ligue 2 | 2 |
| Liga I | 2 |
| Ukrainian Premier League | 1 |
| MLS | 1 |
| Super League | 1 |
| **Total** | **19** |

No one of the 19 kickoff-mismatched fixtures overlaps the 66 no-home/away flags in this runtime horizon (0/19), using the same exact ordered identity. The two data-quality populations are distinct in this artifact.

The triage buckets are indicators, not root-cause diagnoses. A UTC-midnight archive value may be a date-level placeholder, but that cannot be asserted from the timestamp alone. A large delta may indicate a stale or conflicting date/time, but it is not proof of which source is correct. All 19 rows remain `REVIEW_REQUIRED` with `MANUAL_AUTHORITATIVE_EVENT_TIME_REVIEW_ONLY_NO_AUTO_CORRECTION`. No kickoff is changed.

The v1.4 candidate emits a separate `oracle_selected50_kickoff_discrepancy_triage.csv` and QA JSON from the workflow-generated queue. It recomputes each signed delta from timezone-aware timestamps, rejects inconsistent deltas and duplicate exact fixture identities, and preserves manual-only resolution. This is a sidecar artifact, not a workbook worksheet.

## 4. Feature-blocked fixtures and team-side histories

The source runtime has 24 feature-blocked fixtures (5.53% of the 434-fixture horizon) across 15 competitions. The report-only side-history audit identifies 25 team-side histories below the five-match feature-complete gate:

| Side | Histories below 5 |
|---|---:|
| Home | 15 |
| Away | 10 |
| **Total** | **25** |

Of those 25 histories:
- 21 have four feature-complete prior matches (one short of the five-match gate);
- 4 have three (two short).

The 24 blocked fixtures are distributed across:
- Premier League 3; Premier Soccer League 3;
- Pro League 2; Bundesliga 2; 2. Bundesliga 2; LigaPro 2; Serie B 2;
- Ligue 1 1; Ekstraklasa 1; Ukrainian Premier League 1; Süper Lig 1; Segunda División 1; Professional League 1; Super League 1; Indian Super League 1.

There is a second, independent feature gap: six pair/environment features are absent on all 24 blocked fixtures:
`pair_btts_mean`, `pair_fts_mean`, `pair_cs_mean`, `score_environment`, `shot_environment` and `score_gap5`.

Additionally, seven home-side fields are missing on the 15 fixtures with a short home history, and seven away-side fields are missing on the 10 fixtures with a short away history. Thus, adding another historical match may resolve the side-count shortfall for 21 histories, but it does not by itself prove the six pair/environment features can be computed. No feature threshold is relaxed and no missing value is imputed.

The v1.4 candidate writes a fixture-side audit with exact fixture/team IDs, observed feature-complete sample count, missing-feature list and explicit NO eligibility flags. A reconciliation gate verifies that the side-row count, home/away totals, sample counts and eligibility flags agree with the runtime QA summary.

## 5. FootyStats historical pre-match xG provenance

The latest evidence does not change the xG decision:

- 434 current-horizon fixtures contain numeric home, away and total pre-match-labelled xG values.
- 0/434 have a verified historical capture/publication timestamp.
- 0/434 are prediction-eligible or betting-eligible.
- All candidates remain quarantined.

A fresh review of the official public documentation confirms:
1. The Match Details endpoint documents `key` and `match_id` as request parameters. Its public completed-match example returns `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`, but the endpoint's published variable table does not define their point-in-time lifecycle and the example provides no field-level capture timestamp, revision ID or updated-at timestamp.
2. The League Matches endpoint documents `max_time` for league/team statistics as of a timestamp. The public documentation does not establish that it freezes those three match-level xG fields.
3. The FAQ says match statistics are usually available around 20 minutes after full-time. That is not a publication-time guarantee for the pre-match-labelled xG fields.

Official references:
- https://footystats.org/api/documentations/match-details
- https://api.football-data-api.com/match?key=example&match_id=579101
- https://footystats.org/api/documentations/match-schedule-and-stats
- https://footystats.org/api/documentations/faq

The user has confirmed that the active Hobby subscription supports all 50 selected leagues; no package upgrade is required for this universe. The actual cost/credit treatment for a prospective capture pilot and provider-side xG publication/revision semantics still require confirmation. No authenticated API request or account credit was used in this investigation.

Historical xG remains excluded from Oracle features, historical backtests, calibration, forecasts and betting until an immutable pre-kickoff snapshot or equivalent provider revision history proves the value effective before kickoff. Prospective captures, if separately authorised and budgeted, must retain raw response bytes, exact fixture identity, request-start and response-received UTC timestamps, hashes and all revisions. A response received after kickoff cannot be used as a pre-match input.

## 6. Research-only code and workflow changes

The v1.4 candidate now includes:
- fail-closed orientation QA requiring an exact snapshot match for every runtime fixture, valid binary flag coverage, zero unknowns, zero duplicate keys and no eligibility promotion;
- early persistence of orientation and feature-block diagnostics so a failed full report run still has evidence to upload;
- reconciliation of the runtime's blocked team-side rows against its QA counts, including duplicate exact side-key checks;
- a separate kickoff discrepancy triage script and CSV/QA output;
- push-triggered unit tests for the triage script;
- workflow artifact paths for orientation, feature-block and kickoff-triage evidence, including failure diagnostics.

Relevant commits on the research branch:
- `2f8056d` — kickoff triage script;
- `11476dd` — triage tests;
- `1003414` / `dbbe692` — orientation and feature-block fail-closed QA;
- `fdf1ca3` — QA regression tests;
- `ddf6876` / `0124cf6` — workflow QA, artifact and test integration;
- `e10dfec`, `5cebc99`, `2fd1580` — v1.4 candidate contract, dictionary and continuity documentation.

The latest push-triggered checks on commit `0124cf69766bce4a10728a225d0991fff3a2cede` all passed:
- Market Intelligence repair: 24 tests passed;
- goal-market research: 6 tests passed;
- field-coverage audit: 3 tests passed;
- kickoff discrepancy triage: 4 tests passed;
- contract-tests and plan checks: success.

Workflow run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41275489895

Important limitation: this was a push-triggered CI run. The private-archive download, runtime-artifact download, full workbook rebuild, orientation/feature artifact gates, kickoff-triage build and field-coverage rebuild are manual-dispatch-only and were skipped. Passing CI proves the tests pass; it does not prove that a new v1.4 workbook or triage artifact was generated.

## 7. Governance and next execution gate

- v1.3 remains the locked canonical weekly Market Intelligence workbook contract.
- v1.4 remains a report-only candidate pending full manual-dispatch workflow QA.
- Preserve the exact 19 worksheet names/order, 38-column Oracle V1.6 Output, 83-column Market Intelligence view, supporting evidence tabs and QA.
- No manual workbook reconstruction is permitted.
- No Oracle V1.6 production logic, probabilities, thresholds, market definitions or governance were changed.
- All orientation, kickoff and feature-block outputs remain research-only, production-ineligible and betting-ineligible.
- All unverified xG remains quarantined.

**Next execution gate:** manually dispatch the existing Selected-50 Market Intelligence repair workflow on `research/oracle-50-league-readiness-audit`, with the already specified read-only archive confirmation, pinned archive release and verified runtime run ID `41175230838`. Inspect the resulting workbook and sidecar artifacts against the locked v1.3 contract before considering any v1.4 candidate acceptance.

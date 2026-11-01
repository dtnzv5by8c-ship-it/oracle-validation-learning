# Project Oracle — Selected-50 Run 41276694062 Verification
**Date:** 2026-11-01  
**Classification:** Research/reporting-only. Production and betting eligibility remain NOT_GRANTED.

## Executive result

The governed Selected-50 report-repair workflow has now completed a full rebuild successfully. This is a verified GitHub-generated workbook produced by the existing generator and workflow; it was not rebuilt manually or from a blank workbook.

The v1.3 template remains the locked canonical weekly contract. The generated v1.4 reporting enhancement is a technically validated candidate only; it is not promoted or substituted for v1.3 without explicit owner approval.

## 1. Exact execution evidence

| Item | Verified value |
|---|---|
| Repository | `dtnzv5by8c-ship-it/oracle-validation-learning` |
| Branch | `research/oracle-50-league-readiness-audit` |
| Workflow run | `41276694062` (run number 154) |
| Job | `124760189970` |
| Run conclusion | `success` |
| Workflow head commit | `bdc053f138f8df559abd25670cbbfd18a2fd4838` |
| Artifact ID | `13071003389` |
| Artifact name | `oracle-selected50-market-intelligence-repair` |
| Artifact SHA-256 | `443e3f0be7d4640d4f166dddd4ae6611e68ecc74a86be3f8823f82fdafb41965` |
| Generated workbook SHA-256 | `ba0171c7db07d63b5d0dc91c2ccf7a1e5db6b6e02d0a21f6a18e94f52e66a36f` |
| Source runtime run | `41175230838` |
| Pinned archive SHA-256 | `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f` |
| Provider API calls during rebuild | `0` |

The downloaded ZIP digest was independently checked against the GitHub artifact digest. The workbook was opened and inspected directly.

## 2. v1.3 contract preservation

Canonical template:
- Path: `reports/templates/ORACLE_MARKET_INTELLIGENCE_TEMPLATE_V1_3.md`
- Blob SHA: `32b9e4d46db10d6a5cf6ccf0cb0748c61f33149f`
- Status: LOCKED WEEKLY REPORTING TEMPLATE.

Candidate template:
- Path: `reports/templates/ORACLE_MARKET_INTELLIGENCE_TEMPLATE_V1_4.md`
- Blob SHA at this run: `856e7d50eae5834ce5a510c8e13ea1b066fffbb6`
- Status: candidate only; no canonical promotion.

Verified workbook contract:
- Exactly 19 worksheets, with the exact v1.3 names and order.
- `Oracle V1.6 Output`: exactly 38 columns.
- `Market Intelligence`: exactly 83 columns.
- The 38-column Oracle V1.6 Output and 83-column Market Intelligence view are cell-for-cell identical to the v1.3 reference workbook from run `41268816105`.
- The original 25 Data Quality & Risk columns and their values are unchanged; 15 report-only candidate fields are appended to that existing sheet (40 columns total).
- No twentieth worksheet was added.
- Existing supporting tabs and row grains are retained. The two additional Definitions & Governance rows document the new report-only controls; coverage appendices are regenerated for the 340-field candidate matrix.

The v1.3 template file was not changed. The v1.4 candidate remains unpromoted in accordance with the owner's instruction that v1.3 remains canonical.

## 3. Selected-50 field coverage

| Measure | Verified result |
|---|---:|
| Selected league-season groups | 50 |
| Groups with fixtures in the seven-day horizon | 46 |
| Groups without fixtures in the horizon | 4 |
| Runtime fixtures | 434 |
| Exact archive joins | 434 |
| Unmatched/quarantined exact joins | 0 |
| Field occurrences in v1.4 candidate | 340 |
| League/field matrix rows | 17,000 |
| Field exception rows | 965 |

The v1.4 candidate adds 15 fields to Data Quality & Risk only. This expands the field audit from 325 to 340 occurrences and from 16,250 to 17,000 league/field records. It does not change the v1.3 worksheet count or the frozen 38/83-column contracts.

## 4. Orientation enhancement — 66 fixtures

Exact composite identity was verified using selected season ID, fixture ID and ordered home/away team IDs.

| Orientation result | Fixtures |
|---|---:|
| `no_home_away=1` | 66 |
| `no_home_away=0` | 368 |
| Unknown orientation among matched runtime fixtures | 0 |

All 66 flagged fixtures carry:
- `fixture_orientation_status=NO_HOME_AWAY_DISTINCTION`
- `home_away_market_review_status=REVIEW_REQUIRED_NO_HOME_AWAY_DISTINCTION`

The flag is not interpreted as a neutral venue. It does not change or recalculate Oracle probabilities. The 66 flags are report-only review controls.

## 5. Runtime feature support — 24 fixtures / 25 team sides

The generated workbook and separate feature-block audit show:

| Measure | Result |
|---|---:|
| Feature-blocked fixtures | 24 |
| Blocked team-side histories | 25 |
| Home-side histories | 15 |
| Away-side histories | 10 |
| Sides with four feature-complete prior matches | 21 |
| Sides with three feature-complete prior matches | 4 |

The source runtime's strict 20-feature gate is distinct from descriptive score-based Team Form Evidence. Six pair/environment features are absent on all 24 blocked fixtures; seven home-side features are absent across 15 fixtures and seven away-side features across 10 fixtures.

The five-match eligibility gate is unchanged. No imputation or threshold relaxation was applied.

Remaining gap: the current runtime artifact exposes the blocked feature names and side counts, but not the exact prior historical source fixture IDs/rows excluded for each side. A separate research-only feature-provenance export from the private archive/runtime is required before the 25 histories can be closed individually.

## 6. Kickoff discrepancies — external evidence overlay

The workflow-generated queue still contains 19 `REVIEW_REQUIRED` rows. I checked the exact fixture identities against official league/club sources and published local kickoff times, then converted local times using the applicable 2026 time-zone rules.

Result:
- 11/19 external sources corroborate the runtime kickoff.
- 8/19 remain unresolved or have conflicting official/secondary evidence.
- No runtime or archive kickoff was changed.
- No automatic correction was applied.
- The canonical workbook queue remains `REVIEW_REQUIRED` until a human review is recorded.

The 11 runtime times with official corroboration are:
1. O'Higgins–Ñublense — official club and Chilean league schedules.
2. Veres–Chornomorets — official Chornomorets match-day notice.
3. Vancouver Whitecaps–Seattle Sounders — official Whitecaps preview plus B.C. Government confirmation that PCT is UTC-7.
4. Olympique Lyonnais–Angers — official LFP rescheduling notice.
5. Lusitânia Lourosa–Farense — official SC Farense fixture notice.
6. Panathinaikos–AEK — official Panathinaikos fixture page.
7. Reims–Sochaux — official LFP page body confirms 2 Nov 20:45 local; the page title/slug is mismatched, so that caveat is retained.
8. Universidad de Concepción–O'Higgins — official Campeonato Chileno match page.
9. Montpellier–Metz — official Montpellier club notice.
10. UTA Arad–Petrolul — official LPF club calendars.
11. FC Argeș–Dinamo — official LPF club calendars.

The eight not closed:
- Tondela–Felgueiras: conflicting secondary kickoff times; no authoritative club/league confirmation located.
- Lorient–Brest: official LFP material contains a date/time wording conflict and a separate title/body mismatch.
- Six Saudi Pro League fixtures: official schedule evidence is incomplete; Al Hazem–Al Nassr and Al Ittihad–NEOM have official team-page date/TBD conflicts against the runtime date.

A separate 19-row source-evidence register is keyed by exact fixture ID and records runtime/archive UTC, source URL, local time/timezone, converted UTC where corroborated, evidence status and review decision:
`reports/oracle-selected50-kickoff-source-evidence-2026-11-01.csv`.

This is an external research evidence overlay, not a manual edit to the canonical workbook. The original schedule queue and its no-auto-correction controls remain unchanged.

## 7. FootyStats historical pre-match xG — quarantine retained

Latest archive summary:
- 59,049 historical match records across 200 match files/season folders.
- 51,983 records have settled status and complete scores.
- 0 parse errors.
- 0 `ingestion_manifest.csv` rows.
- 59,049 non-empty field-presence counts for each of `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`. These are field-presence counts, not proof of numeric validity or historical availability.
- 434 upcoming fixture candidates have numeric pre-match-labelled values.
- 0 verified historical capture timestamps.
- 0 prediction-eligible and 0 betting-eligible xG rows.

A further code-path gap is confirmed in `scripts/build_footystats_archive_features.py`:
- It looks for and reads `ingestion_manifest.csv`.
- It hard-codes `xg_capture_time_utc` to blank.
- It hard-codes `xg_temporal_provenance_status` to `UNVERIFIED_NO_CAPTURE_TIMESTAMP`.
- It writes the manifest separately to `manifest_reconciliation.csv` and counts its rows; it does not join manifest rows to exact fixture IDs/field values to establish xG capture time.

Therefore, adding a manifest file alone would not close provenance. A future research-only change must define and validate an exact fixture/field/raw-response-hash/capture-time join, with the raw response retained immutably. Until provider evidence or genuine historical snapshots exist, all 434 xG candidates remain quarantined.

No authenticated FootyStats API calls or private credits were used. The current public Match Details sample response returns numeric `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch` values for a completed 2019/20 fixture, but the response has no capture timestamp, immutable snapshot ID or revision number. The published Match Details variable table does not define a point-in-time capture or revision mechanism for these fields. The League Matches documentation describes `max_time` as returning league/team statistics up to a specified time; it does not document an immutable per-fixture xG snapshot. FootyStats' FAQ says match statistics are usually available within 20 minutes after full-time. None of these statements proves that the historical pre-match-labelled xG value was captured or available before that fixture's kickoff.

Provider references:
- Match Details endpoint and sample response: https://footystats.org/api/documentations/match-details
- League Matches `max_time` definition: https://footystats.org/api/documentations/match-schedule-and-stats
- FootyStats FAQ update timing: https://footystats.org/api/documentations/faq

## 8. Governance and next actions

Unchanged:
- Oracle V1.6 production logic, probabilities, thresholds and calibration.
- Production eligibility: NOT_GRANTED.
- Betting eligibility: NOT_GRANTED.
- xG prediction/betting eligibility: 0.
- v1.3 canonical weekly workbook contract.

Next actions:
1. Keep v1.3 as canonical. The v1.4 candidate has a successful full build and passed QA, but requires explicit owner approval before any canonical promotion.
2. Manually review the 11 externally corroborated schedule rows and preserve the 8 unresolved rows as `REVIEW_REQUIRED`; do not alter the canonical queue automatically.
3. Obtain the private-archive/runtime feature-source trace for the 25 blocked team-side histories, including exact historical fixture IDs, kickoff cutoffs, missing-feature flags and source hashes.
4. Obtain FootyStats written confirmation on xG field definitions, first availability, post-publication revisions and historical as-of snapshot availability. If no historical proof exists, propose a separately approved prospective capture pilot.
5. Do not modify Oracle V1.6 production logic or probabilities.

All outputs from this run and the source-evidence overlay are research/reporting-only, production-ineligible and betting-ineligible.

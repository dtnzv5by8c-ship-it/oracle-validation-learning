# Project Oracle — Selected-50 report workflow CI reconciliation

**Evidence cutoff:** 1 November 2026, 04:03 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research/reporting workflow only. No production model changes or provider API calls.

## 1. CI failure diagnosis

The report workflow push check on commit `a353886c5ebf26493d13910fa5e2c4af67681cf0` failed in the offline test step, before any private archive or runtime-artifact operation.

Failing test:
- `test_50_league_coverage_sheet_includes_no_fixture_groups_and_quarantine`

Cause:
- The test expected the summary metric label `Groups without fixtures in seven-day horizon`.
- The report builder's current summary contract emits `Groups with no 7-day fixtures`.
- The test assertion was stale; the implementation's summary metric and no-fixture count logic were not changed.

## 2. Report-only correction

Updated only the test assertion to match the current report-builder metric label.

Commit:
- `7263afc0656fb635b0206ebd6c8f0edfd31094eb`
- Message: `test: align coverage summary assertion with current metric label`

No production or report-generation logic was modified in this correction.

## 3. Verified checks after correction

The new commit completed all three GitHub check runs successfully:

| Check | Run ID | Result |
|---|---:|---|
| Market Intelligence repair tests | 41263509084 | SUCCESS |
| Contract tests | 41263509087 | SUCCESS |
| Plan / research gates | 41263509100 | SUCCESS |

The Market Intelligence repair job log confirms:
- Market Intelligence report tests: 21 passed.
- Experimental goal-market research tests: 6 passed.
- Selected-50 field-coverage audit tests: 3 passed.
- Total in that job: 30 tests passed.

The contract-tests job also completed successfully, including the offline xG/odds temporal-shift, season event-time and per-league coverage checks.

## 4. Critical limitation: this was CI validation, not a report rebuild

The successful Market Intelligence repair check was triggered by a branch push. In that event mode, the following manual-dispatch-only steps were skipped:
- private archive consent/token validation;
- pinned private archive download and SHA-256 verification;
- source runtime artifact download and provenance verification;
- archive-wide feature/provenance build;
- report workbook rebuild;
- 50-league field-coverage rebuild;
- final artifact upload.

Therefore, this CI success proves the tests pass; it does **not** prove that a new workflow-generated Market Intelligence workbook has been produced.

## 5. Selected-50 and xG evidence remains unchanged

The latest reconciled field-level audit remains:
- 50 selected league-season groups;
- 325 field occurrences across nine source sheets;
- 16,250 league/field scope rows;
- 965 final exception rows after report-only status normalisation;
- zero unmapped source rows.

The pinned historical FootyStats archive remains identified by SHA-256:
`7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.

Its prior archive audit reports 59,049 match records across 200 season folders, 51,983 settled-status/score-complete records, zero parse errors and zero ingestion-manifest rows. The feature builder records no verified xG capture timestamp.

For the current Run #124 reporting horizon:
- 434 upcoming fixture rows have numeric pre-match-labelled home, away and total xG candidates;
- 0/434 have verified capture timestamps;
- all 434 remain quarantined;
- prediction eligibility = 0;
- betting eligibility = 0.

Public FootyStats documentation does not establish Match Details `max_time` support or an immutable per-fixture historical xG snapshot/revision mechanism. No authenticated provider request was made.

## 6. Next execution gate

Run the existing workflow manually from the governed research branch with:
- `confirm_private_archive_read=true`;
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`;
- `runtime_run_id=41175230838`.

The workflow also requires the already-configured `ORACLE_PRIVATE_REPO_TOKEN` repository secret and read access to the pinned private archive. If those controls pass, inspect the generated artifact and verify its workbook, 50-league field matrix, exception register, xG audit and QA outputs.

If manual dispatch or the required secret/archive access is unavailable, do not substitute a local partial rebuild or claim the artifact was generated.

## Governance

- Research/reporting only.
- No authenticated FootyStats API calls or provider credits used.
- Unverified pre-match-labelled xG remains quarantined from historical backtests, forecasts, calibration and betting.
- Oracle V1.6 production logic, probabilities, thresholds and calibration remain unchanged.
- No production merge or betting approval is implied by passing CI.

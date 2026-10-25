# Oracle 50-League Compatibility Audit — 2026-10-25

## Purpose and guardrails

This is a **research-only, static compatibility audit** for the governed 50-league target. It does not change Oracle production code, production model logic, probabilities, calibration, thresholds, or production configuration. It does not authorize live predictions or paid provider ingestion.

## Current verification

- Latest research-only Selected-50 Dry-Run Planner run: [40187374647](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40187374647), completed **success** on 2026-10-25. Job steps confirm dry-run generation, conservative market gates, planner regression, market gate regression, exact catalogue resolver, prediction input contract, output validation, and artifact upload all passed.
- Production V4 router run [40183610511](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40183610511) failed. The job API exposed one failed job but no step summaries; the available log route did not provide usable logs. Root cause remains **unconfirmed**. Do not infer billing, runner, secret, or policy cause without logs.
- Production V4 router preflight expects `active_leagues == 27` and `fixtures == 12836`. It cannot be treated as proof of readiness for the governed 50-league universe.
- Production repository inventory exposed 73 workflow files, with operational 27-league naming/assumptions in workflows including `openfoot-27-league-coverage.yml`, `oracle_27_league_dna_lab.yml`, `oracle_27_league_market_vetting.yml`, `oracle_27_league_prediction_readiness.yml`, `oracle_final_assessment.yml`, and `oracle_v4_router.yml`.
- Explicit operational 27-league assumptions were found in `scripts/build_oracle_historical_intelligence.py`, `scripts/build_four_model_report.py`, `scripts/validate_four_model_production.py`, `scripts/build_oracle_team_dna_v2.py`, `scripts/ingest_upcoming_fixtures.py`, `scripts/oracle_final_assessment.py`, and `config/oracle_major_league_registry_v1.json`. Several frozen historical manifests also say 27 / 12,836; those may correctly describe the historical sample and must not be rewritten as if 50-league evidence already exists.

## Priority findings

### P0 — Production gate compatibility: BLOCKED

Operational workflows/scripts and current preflight expect the old 27-league universe. Do not change production blindly. First define a separately versioned 50-league manifest contract, identify which runtime paths should consume it, and rebuild the dependent evidence while preserving historical baselines.

### P0 — Production workflow failure diagnostics: UNRESOLVED

Run 40183610511 is failed, but job-step logs were unavailable via the connected read path. No root cause can responsibly be assigned. The next action is to retrieve usable logs/job initialization diagnostics through GitHub Actions; only then fix the demonstrated infrastructure or script cause. Do not repeatedly rerun production or paid/data-ingest jobs on speculation.

### P1 — Canonical 50-league identity and archive coverage: OPEN

The selected-50 dry-run has 50 selected season IDs; 31 had records in the audited Run 56 manifest and 19 did not. The exact missing IDs and selected labels are listed in [the compatibility report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-50-league-compatibility-audit-2026-10-25.md) and recorded in the machine-readable [Run 56 manifest-gap triage ledger](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/data/run56_selected50_manifest_gap_triage.csv). Each row explicitly records provider request status as `UNKNOWN_NOT_INFERRED` and production eligibility `NO`. A missing manifest row does not prove the provider request failed or the season ID is invalid.

Next: reconcile these 19 IDs against already-retained catalogue/request logs/archive evidence by exact season ID. Classify each as exact match, no catalogue match, duplicate, attempted with failure evidence, or request state unknown. No guessed parent IDs and no paid requests merely to fill the evidence gap.

### P1 — Verified settlement truth: OPEN

The selected archive contains incomplete and suspended records. A date plus numeric score is not settlement proof, especially when future-dated records have scores. Admit a result only with explicit final status and valid score, or an independently verified outcome.

### P1 — Point-in-time feature integrity: OPEN

Non-empty xG/odds-named fields do not prove valid scale, correct fixture mapping, bookmaker/market identity, timestamp or availability before kickoff. Keep them unavailable for production gating until provenance is verified.

### P2 — Backtest, calibration and production accuracy: BLOCKED

The audited prediction ledger has 210 rows across 42 fixture IDs, all labelled `CHALLENGER`. Settlement, model scorecard, postmortem and probability-error ledgers have zero data rows. There are no production/live-labelled predictions from which canonical production accuracy can be calculated.

## Required gates, in priority order

1. **P0:** Obtain usable diagnostics for production workflow initialization; fix only the demonstrated cause.
2. **P0:** Define and version the canonical 50-league manifest/compatibility contract separately from frozen 27-league historical baselines.
3. **P1:** Reconcile exact season IDs and all 50 coverage rows, including the 19 Run 56 evidence gaps.
4. **P1:** Validate exact stable fixture/team IDs; quantify missing, duplicate, unmatched and ambiguous joins. No fuzzy joins for approval.
5. **P1:** Validate result settlement, recent form, standings chronology, H2H, xG and odds as-of kickoff.
6. **P2:** Join immutable pre-kickoff predictions to verified outcomes by exact fixture, market, model/version and timestamp; only then calculate accuracy/calibration.
7. Re-run research-only contract/regression tests and preserve immutable production baselines.
8. Grant production readiness only after every market gate passes and governance explicitly approves promotion.

## Market and release decision

- Production readiness: **NOT GRANTED**
- BTTS Yes: **NOT_VERIFIED**
- Double Chance: **NOT_VERIFIED**
- Double Chance + Under 4.5: **NOT_VERIFIED**
- M-1UP: **BLOCKED**

The latest research planner is green, but it is a dry-run planning result—not proof that all 50 leagues are prediction-ready. No production files, model logic, probabilities, calibration or thresholds were changed. No paid provider calls were made by the dry-run.


## Expedited continuation update — 2026-10-25 11:32 UTC

- Added the research-only machine-readable contract `config/oracle_selected50_compatibility_contract_v1.json`, defining the 50 exact selected season IDs, country/competition labels, fail-closed evidence gates and production guardrails. It does not infer parent competition IDs.
- Added `tests/test_selected50_compatibility_contract.py` and wired it into the research dry-run workflow.
- The gated workflow [run 40189247302](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40189247302) completed **success**. The new contract test passed along with the existing planner, market gate, catalogue resolver, prediction-input and output validation steps. This verifies the contract and research planner only.
- Further production job diagnostics for [run 40183610511](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40183610511) show the failed job had `runner_id: 0`, an empty runner name, no job steps, and start/end times about two seconds apart. This is evidence the failure occurred before a runner/step sequence was recorded; it is consistent with a job initialization/runner-allocation failure, but does not establish the exact root cause. The logs endpoint still returns BlobNotFound. Do not patch model code based on this evidence.
- Production remains untouched and not approved. The 19 Run 56 manifest gaps, outcome/feature provenance, and historical production accuracy gates remain open.


## Runner failure interpretation — documentation cross-check

GitHub's current hosted-runner documentation lists `ubuntu-slim` as supported for private repositories, so the label alone is not evidence of an unsupported runner choice. The production failure's `runner_id: 0`, blank runner name and zero steps point to a failure before recorded runner execution. The previously reported Actions budget/spending-limit restriction is a plausible explanation, but the present run payload and unavailable logs do not prove it. Verify the repository/organization Actions billing and spending-limit status in GitHub before any production rerun; do not raise the spending limit without Nolan's approval. Sources: [GitHub-hosted runners reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).


## Run 56 gap interpretation refinement — 2026-10-25 11:40 UTC

The 19 IDs in `data/run56_selected50_manifest_gap_triage.csv` have **no Run 56 manifest record**, but that is not equivalent to missing data across all retained archives. The separate private Selected-50 ingestion package QA run [40185145631](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185145631) previously reported all 50 selected season IDs as `INGESTED`. Therefore these 19 are currently a **Run 56 provenance/manifest discrepancy**, not confirmed failed provider requests or confirmed absent archive data.

The triage ledger was updated to record that distinction on all 19 rows. Provider request status remains `UNKNOWN_NOT_INFERRED` because the exact private-package per-season rows and original request logs have not yet been reconciled in this audit. Do not repeat ingestion or spend provider calls to fix a manifest discrepancy. Next: retrieve/reconcile the exact private package row-level evidence and request logs against these IDs. The package-level QA is not enough to assert every row is complete, valid, or production-eligible.

No market gate changes: production readiness remains `NOT_GRANTED`; BTTS Yes, Double Chance, and DC + Under 4.5 remain `NOT_VERIFIED`; M-1UP remains `BLOCKED`. No production code, model logic, probabilities, calibration, thresholds, or production files changed.


## Artifact-level recheck — 2026-10-25 11:45 UTC

- Research planner run [40189946356 / Run #88](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40189946356) completed successfully; all 12 substantive workflow steps passed.
- Downloaded and inspected the run's actual artifact `oracle-selected50-dry-run-plan.zip` (artifact ID `12597875008`), not just the job status. It contains the 50-row coverage matrix, 50-row market gate table, and JSON summaries.
- Artifact summary confirms `DRY_RUN_ONLY`, 50 selected season IDs, 31 Run 56 manifest records, 19 without Run 56 records, 31 exact archive coverage rows, 9,708 records across those exact-matched seasons, 9,708 parseable kickoffs/team-ID-complete/score-complete rows, and 3,488 rows meeting the preliminary allowed-status filter. These are archive-level counts, not approved settled labels.
- The market summary explicitly reports all 50 as not production eligible; fixture-join gates blocked, freshness blocked/stale, recent form/standings/H2H unverified, xG/odds point-in-time provenance blocked; BTTS Yes, Double Chance, and DC + Under 4.5 are `NOT_VERIFIED`; M-1UP is `BLOCKED`. Live API calls made: 0.
- Root cause of the 19 gaps is narrowed to a scope mismatch in the current planner's evidence source: the plan reconciles Run 56's manifest/archive only, while separate package QA reported all 50 ingested. The artifact itself cannot reconcile that separate package. This is a confirmed limitation of current audit evidence, not proof the private package records are invalid or missing.
- No production files or model logic were changed. No provider calls were made. The next data-side action remains exact reconciliation of the retained private package rows/request logs by season ID; production remains not approved.


## Private Selected-50 row-level reconciliation — 2026-10-25

- Retrieved and inspected the sanitized private archive QA artifact from research workflow [40185145631](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185145631), artifact ID **12596036240**. The artifact reports an exact 50/50 selected season-ID set match, 50/50 manifest metadata matches, 50/50 country-plus-competition composite label matches, 50/50 season folders with valid JSON files, and no missing/invalid season files.
- This resolves the specific question of whether the 19 Run 56 manifest-gap seasons are absent from the retained private package: **they are present in the package QA evidence**. The 19 rows in the triage ledger now include per-season row counts and feature-availability counts. They remain **not production eligible**.
- Integrity: the QA artifact's private archive SHA-256 is `9b5eecf376dac804231bfcb75d9381a4307b38f082cadd9a775d48ec3e5310dd`, matching the release asset digest reported by GitHub for [the private ingestion package](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/releases/tag/research-selected50-footystats-ingestion-20261025). The raw package remains private; the public research artifact contains only sanitized QA output.
- Package totals: 14,051 match records and 14,051 unique season/fixture-ID pairs; no duplicate pairs; all 14,051 rows have kickoff-like fields, explicit score pairs, team-ID pairs and team-name pairs. These are structural checks, **not** independent fixture-join or settlement validation.
- The package includes 5,637 rows in the primary 2025-03-20 to 2026-09-20 window; 48/50 seasons have at least one fixture with recent-form-5 values for both teams. The QA report identifies Australia A-League (season 17326) and India ISL (season 17964) as having zero rows with recent form for both teams in the audited package summary. Those seasons require targeted data/chronology diagnosis and affected fixtures must be quarantined until resolved.
- H2H coverage is present for 5,282 fixture rows overall, but this is not proof of as-of-kickoff chronology or valid feature joins. The package contains 6,916 `complete`, 7,083 `incomplete`, and 52 `suspended` statuses; the 6,898 completion candidates in QA are not settlement-approved outcomes. Non-empty xG/odds fields remain unverified for semantics, scale, market/bookmaker identity and pre-kickoff timestamp.
- **Remaining gaps:** request-level logs are still not independently reconciled; provider parent competition IDs are not populated in the QA package; exact joins against the canonical fixture slate, final settlement truth, feature point-in-time provenance, the production runner initialization failure, the 27-to-50 runtime migration, and production-labelled prediction history remain open. No model or production changes were made; production readiness remains **NOT_GRANTED**.


## Recent-form gap root-cause diagnostics — 2026-10-25

- Enhanced the research-only private archive QA to report per-season provider-status counts and past-date rows with explicit finished status and numeric scores. Workflow [40191138446](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191138446) completed **success**; the raw package was downloaded from the existing private release, with no provider API calls, and only sanitized QA was uploaded as artifact **12598490513**.
- **Australia A-League (season 17326 / 2026–27):** 156 records; 9 past-date rows, all 9 with explicit `complete` status and numeric scores; 145 future rows, all status `incomplete`; 0 fixture rows have five prior completed matches for both teams; 16 have prior H2H. This is insufficient current-season team history for the recent-form-5 gate, not proof that the season package is missing.
- **India ISL (season 17964 / 2026–27):** 78 records; 14 past-date rows, all 14 with explicit `complete` status and numeric scores; 62 future rows, all status `incomplete`; 0 fixture rows have five prior completed matches for both teams and 0 have a prior H2H in this selected-season archive. The package is structurally present, but current-season-only history is insufficient.
- The QA script explicitly restricts prior-form and H2H histories to the selected season and does not include prior-season carryover. Therefore the defensible fix is **not** to fabricate form values: either supply a separately verified prior-season history layer in research and test exact team-ID continuity, or mark affected fixtures `INSUFFICIENT_PRIOR_MATCH_HISTORY` and exclude them from markets requiring those features. Production feature logic has not been changed.
- This does not close the broader feature provenance gate. Fixture-slate exact joins, final settlement truth, point-in-time xG/odds validation, the private production runner failure, 27-to-50 runtime compatibility and production-labelled backtest history remain unresolved. Production readiness remains **NOT_GRANTED**.


## Latest continuation verification — 2026-10-25 12:00 UTC

- The updated evidence register and triage ledger triggered research dry-run planner [run 40191221412](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191221412), which completed **success**. All 12 substantive steps passed: dry-run plan generation, conservative market gates, planner and market-gate regression tests, exact catalogue resolver tests, prediction-input contract tests, governed Selected-50 compatibility contract, output validation and artifact upload. The planner made **zero network/provider calls**.
- Additional planner runs [40191217526](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191217526) and [40191213281](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191213281) also completed successfully against adjacent audit commits.
- The latest triage ledger records all 19 Run 56 gaps as present in the private package QA evidence, with exact per-season match counts, primary-window counts, recent-form-5 coverage, H2H counts, QA artifact ID and archive digest. It also records the verified insufficient-history cases for Australia and India.
- The successful research workflows establish only that the audit contracts and dry-run planner are passing. They do **not** clear the production runner, migrate production to 50 leagues, certify settlement/features, or establish production prediction accuracy. Release status remains **NOT_GRANTED**.


## Structural fixture-integrity audit — 2026-10-25

Research-only private archive QA [run 40191502265](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191502265), artifact **12598431755**, passed after replacing the per-season hardcoded duplicate count with actual counters and adding structural integrity metrics. The sanitized artifact reports:

- 14,051 records across 50 seasons; 14,051 unique season/fixture-ID pairs; **0 duplicate fixture-ID pairs**.
- **0** missing fixture IDs, missing home/away team-ID pairs, same home/away team IDs, missing/unparseable kickoff values, missing score pairs or invalid numeric score pairs.
- 50/50 selected season IDs, 50/50 valid season folders, 50/50 exact selected metadata matches; raw payload remains private.

These are structural completeness results only. They do not establish that provider fixture IDs map exactly to the canonical Oracle fixture slate or that team IDs are canonical across competitions/seasons. Parent competition IDs are not retained in the package. Cross-source joins, settlement truth and point-in-time feature provenance remain unverified; production readiness remains **NOT_GRANTED**. The dry-run planner [run 40191502235](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191502235) also passed all substantive steps.

## Production runner failure pattern

The latest private-repository workflow failure, [run 40190338066](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40190338066), has the same pre-step pattern as [run 40183610511](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40183610511): the first job has `runner_id=0`, blank runner name, zero steps, and no retrievable job log; dependent jobs are skipped. This confirms a repeated pre-runner/job-initialization failure pattern, but does not independently prove the billing/spending-limit cause. The user has reported that private Actions minutes are exhausted. Continue with public research workflows; do not consume private Actions retries, raise spend limits, or change production workflow/model files without a verified cause and explicit approval.


## Runtime assumption inventory — pinned production source scan

Read-only public research workflow [run 40191635164](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191635164) completed **success** against private production source SHA `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381`. All 13 specified runtime-consumer files were found. The sanitized artifact [12597788395](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40191635164/artifacts/12597788395) records **82 pattern matches**: 79 fixed-27 references, one fixed 12,836 historical-fixture count, one `ACTIVE = 27` assignment, and one `league_count: 27` registry value. Matches are concentrated in:

- `scripts/ingest_upcoming_fixtures.py` (16)
- `.github/workflows/oracle_27_league_market_vetting.yml` (12)
- `.github/workflows/oracle_27_league_prediction_readiness.yml` (12)
- `.github/workflows/oracle_27_league_dna_lab.yml` (10)
- `.github/workflows/oracle_final_assessment.yml` (7)
- `scripts/validate_four_model_production.py` (6)
- `.github/workflows/openfoot-27-league-coverage.yml` (5)
- `scripts/oracle_final_assessment.py` (5)
- `config/oracle_major_league_registry_v1.json` (3)
- `scripts/build_four_model_report.py` (2)
- `.github/workflows/oracle_v4_router.yml` (2)
- `scripts/build_oracle_historical_intelligence.py` and `scripts/build_oracle_team_dna_v2.py` (1 each)

This is a static pattern scan, not a code migration. Some 27/12,836 values correctly describe frozen historical samples. The operational 50-league migration remains blocked until each match is semantically classified as a frozen baseline versus a runtime universe assumption and the governed 50-ID manifest is wired through a reviewed, tested production change. No private source files were modified.

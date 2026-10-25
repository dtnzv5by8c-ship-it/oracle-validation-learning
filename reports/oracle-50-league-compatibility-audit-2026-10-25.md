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

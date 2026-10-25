# Oracle 50-League Compatibility Audit — 2026-10-25

## Purpose and guardrails

This is a **research-only, static compatibility audit** for the governed 50-league target. It does not change Oracle production code, production model logic, probabilities, calibration, thresholds, or production configuration. It does not authorize live predictions or paid provider ingestion.

## Current verification

- The latest research-only Selected-50 Dry-Run Planner run completed successfully: [run 40186945881](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40186945881).
- Production workflow review confirms the current V4 router preflight expects `active_leagues == 27` and `fixtures == 12836`. This is incompatible with treating the existing historical-intelligence artifact as a verified 50-league universe without a separately governed migration and rebuilt evidence.
- Production repository inventory exposes **73 workflow files** under `.github/workflows`; several retain 27-league naming or assumptions. Examples include:
  - `openfoot-27-league-coverage.yml`
  - `oracle_27_league_dna_lab.yml`
  - `oracle_27_league_market_vetting.yml`
  - `oracle_27_league_prediction_readiness.yml`
  - `oracle_final_assessment.yml` (named “Oracle Final 27-League Assessment”)
  - `oracle_v4_router.yml` (27-league / 12,836-fixture historical preflight)
- Code-search evidence also identifies fixed 27-league / 12,836-fixture expectations in:
  - `scripts/build_oracle_team_fixture_intelligence.py`
  - `research/ORACLE_FINAL_BUILD_COMPLETION_V1.json`
  - `research/oracle_intelligence/oracle_v4_manifest.json`
  - `data/historical_spine_execution_manifest.json`
  - `research/oracle_intelligence/oracle_historical_intelligence_manifest.json`
  - `research/four_model/baselines/BACKTEST_BASELINE_V1.0.json`
  - `research/historical_spine/canonical_historical_spine_baseline.json`
  - `data/historical_match_spine_manifest.json`
  - `research/team_dna_v2/ORACLE_TEAM_DNA_V2_MANIFEST.json`
  - `research/team_fixture_intelligence/oracle_team_fixture_intelligence_manifest.json`

Further static inspection confirms `scripts/ingest_upcoming_fixtures.py` explicitly describes and configures the active 27-league universe, while `oracle_final_assessment.yml` builds a fixture file named `oracle_weekend_fixtures_27.csv` using a 27-league fallback. These are operational paths that cannot be assumed to cover the governed 50-league target.

These are not all necessarily defects: immutable historical baselines may correctly describe the original 27-league sample. The defect is using those 27-league artifacts as proof of 50-league readiness, or making a 50-league run depend on the old count without a separately versioned and validated manifest.

## Priority findings

### P0 — Production gate compatibility

**Status: BLOCKED.** The V4 router’s historical-intelligence preflight is hard-coded to 27 leagues and 12,836 fixtures. Do not change it blindly: first define the correct 50-league manifest contract and establish whether this router is expected to consume it. Production remains untouched.

### P1 — Canonical 50-league identity and coverage

**Status: OPEN.** The selected-50 dry-run found 50 selected season IDs, but only 31 had manifest records in the audited run and 19 lacked manifest records. A missing manifest row does not prove that a provider request failed; exact season/competition identity and coverage must be reconciled without guessing IDs.

### P1 — Verified match outcomes

**Status: OPEN.** The selected archive includes records marked incomplete or suspended, and numeric scores/date alone are insufficient settlement proof. Only explicit final status plus valid score, or an independently verified outcome, can be admitted.

### P1 — Point-in-time feature integrity

**Status: OPEN.** Non-empty xG/odds-named fields do not prove genuine values, correct fixture mapping, market/bookmaker identity, or availability before kickoff. Keep these features unavailable for approval until provenance and timestamps are verified.

### P2 — Backtest, calibration and production accuracy

**Status: BLOCKED.** The production prediction ledger previously audited has 210 rows across 42 fixture IDs, all labelled CHALLENGER; the settlement, model scorecard, postmortem and probability-error ledgers have no data rows. No production accuracy rate can currently be calculated from those ledgers.

### P0 diagnostic — Production workflow initialization

**Status: UNRESOLVED.** Production workflow failures have not yielded usable job-step logs through the available read path. This is not enough evidence to attribute the cause to billing, runners, secrets, or policy. Do not repeatedly rerun production jobs or change settings without a diagnostic signal.


### Additional operational hard-coded universe checks

Further production code search found these explicit 27-league operational assumptions:

- `scripts/build_oracle_historical_intelligence.py`: aborts unless the admitted historical match set contains exactly 27 unique leagues.
- `scripts/build_four_model_report.py`: sets `ACTIVE = 27` and tracks a fixed partial-coverage list.
- `scripts/validate_four_model_production.py`: expects the readiness manifest's active universe count to equal 27.
- `scripts/build_oracle_team_dna_v2.py`: records a passing league-count check only when the current set has 27 leagues.
- `scripts/ingest_upcoming_fixtures.py`: documents and configures the active 27-league fixture universe.
- `scripts/oracle_final_assessment.py` and `.github/workflows/oracle_final_assessment.yml`: consume/write a 27-league fixture file and a 27-league fallback path.
- `config/oracle_major_league_registry_v1.json`: active-universe registry states `league_count: 27`.

These findings make the migration scope broader than the V4 preflight alone. Historical baselines and frozen research artifacts should remain historically accurate; operational 50-league readiness must be established by a new governed contract and rebuilt/validated evidence. No such production migration was applied.

## Required next gates

1. Publish the authoritative 50-league canonical competition-season manifest with source-backed IDs and explicit versioning.
2. Reconcile all 50 selected seasons to manifests and provider coverage; label unknowns as unknown.
3. Validate fixture and team identity with stable IDs; quantify unmatched, ambiguous, duplicate and missing joins.
4. Admit results only with explicit final-status/outcome evidence.
5. Validate xG and odds provenance as-of kickoff.
6. Join immutable pre-kickoff predictions to verified results by exact fixture, market, model/version and timestamp; only then calculate accuracy and calibration.
7. Run research-only contract/regression tests and preserve immutable production baselines.
8. Grant production readiness only after the governed acceptance gates pass.

## Decision

**Production readiness: NOT GRANTED.** The latest research planner passes, but that is a dry-run planning result, not evidence that all 50 leagues are prediction-ready. Market states remain BTTS Yes = NOT_VERIFIED, Double Chance = NOT_VERIFIED, DC + Under 4.5 = NOT_VERIFIED, and M-1UP = BLOCKED.

No production files or model logic were modified for this audit.

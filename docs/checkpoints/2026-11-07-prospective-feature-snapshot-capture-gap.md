# 2026-11-07 — Prospective evidence snapshot audit: capture gap confirmed

## Scope
Audited the live private `oracle-football-data/main` after prospective cycle #431. No production workflow was rerun and no provider acquisition was performed.

## Findings
Current private state:
- main HEAD: `85c630e677c1ac408672973e4f0c643d31a9fc19`
- prediction archive: 900 CHALLENGER rows / 180 fixtures
- canonical settlement ledger: 25 rows / 5 fixtures
- all 25 canonical settlement rows retain blank historical provenance by append-only design.

### Immutable feature snapshot control
`archive/FEATURE_SNAPSHOT_MANIFEST.csv` is header-only (0 snapshot rows).

The publication adapter `scripts/prepare_prospective_four_market_publication.py` currently creates `feature_snapshot_id` from a SHA-256 payload containing:
- fixture identity
- market/model version
- raw probability
- prediction timestamp
- data cutoff
- source manifest hash
- state manifest hash

It does **not** include the actual pre-match feature values used by the prediction engine. Therefore the current feature_snapshot_id is a metadata/probability identity, not an independently materialized immutable feature snapshot.

The live prediction rows do contain a valid dataset-level `pre_match_state_hash` pointing to the locked historical prematch state artifact. Independent reconstruction against that artifact shows:
- 175/180 fixtures have both home and away pre-match state available before fixture date;
- 4/180 have only one side;
- 1/180 has neither;
- no post-kickoff state was introduced by this audit.

This is useful dataset-level provenance, but it does not retroactively prove the exact feature vector captured at prediction time.

### Model-code attribution
Current prospective rows use `model_code_sha` values inherited from the GitHub Actions `GITHUB_SHA` at publication time. For the latest 2026-11-07 batch this value is `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7`, which is the settlement-provenance code commit, not the four-model prediction-engine commit. The actual prediction-engine file at that commit is unchanged and has blob SHA `fe28863f24609dad7536e9a6a964a864b9f4bb5b`.

Therefore current prospective model-code attribution is not admissible as an exact model-engine commit reference.

## Decision
This is a genuine evidence-control blocker, not a production-model defect. Do not modify Oracle V1.6 logic, probabilities, thresholds, calibration, betting eligibility or governance.

Next repair must be reporting/evidence-only:
1. materialize the actual pre-match feature inputs used for each newly generated challenger prediction;
2. create immutable feature snapshot records with source hashes and leakage status;
3. bind prediction rows to those snapshots;
4. capture the actual prediction-engine code revision separately from the workflow/settlement commit;
5. preserve existing 900 prediction rows as immutable historical evidence; do not rewrite them retroactively;
6. exercise the repaired capture on a fresh challenger cycle before considering this gate closed.

No FootyStats calls are required for this blocker.

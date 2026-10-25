# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 14)

Audit timestamp: 2026-10-25 (SAST)
Research branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**
Scope: exact 50 IDs from `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`. No substitution of the protected 27-league registry.

## Direct live-repository reinspection

### Owner-selected manifest and crosswalk
- Selected manifest blob SHA: `f6f9069b692b79a7595d1513a3413e8660763632`.
- Crosswalk revision 14 blob SHA: `36cb42ade4034febdc86287bfb5eddd30397cfe5`.
- Crosswalk shape: 50 rows, 50 unique IDs, exact set equality with the selected manifest.
- Status counts: 22 `CANDIDATE_REQUIRES_HUMAN_REVIEW_NOT_APPROVED`; 28 `UNRESOLVED_NO_EXACT_OR_EXPLICIT_ALIAS`; 0 approved mappings.
- Archive evidence: 31 selected IDs exactly equal an archived season ID and have fixture rows in that season folder; 19 selected IDs have no exact archive season-ID join. This is historical season-level evidence, not a verified current provider-ID-to-fixture join or proof of parent-competition ID semantics.

### Protected registry and existing readiness matrix
- Protected registry: `config/oracle_major_league_registry_v1.json`, blob SHA `81d6db487e498fc84a87a7457b0de7215537f15c`, version `ORACLE_MAJOR_LEAGUE_REGISTRY_V1.0`; 27 entries, 13 `CONTROLLED`, 14 `NOT_INGESTED`.
- Existing matrix: `data/league_readiness_matrix.csv`, blob SHA `602061ebe0bbecdd3c11876307cebe45b0ed2ffd`; 27 rows, 22 `PRODUCTION-READY`, 5 `PARTIAL`, last refresh `2026-10-01T17:25:35.759116Z`.
- These artifacts remain the legacy 27-league scope and are not evidence that the owner-selected 50 leagues are ready. Neither file was changed.

### Locked historical window and archive coverage
Primary window: 2025-03-20 through 2026-09-20. The crosswalk's 31 exact season-level joins yield:
- 15,016 archive fixture rows.
- 15,003 settled-status rows with complete scores (99.91%).
- Team IDs complete: 15,016/15,016 (100%).
- Parseable kickoff timestamps: 15,016/15,016 (100%).
- Home recent-form-5 coverage: 14,612/15,016 (97.31%).
- Away recent-form-5 coverage: 14,591/15,016 (97.17%).
- Provisional standings for both sides: 14,467/15,016 (96.34%).
- Numeric xG fields and at least one odds field are present on 15,016 rows, but odds timestamps are 0/15,016 and verified point-in-time xG/odds provenance is 0/15,016.
- The archive's `provider_league_id` field is blank across all 126 archive-manifest rows. Do not interpret field presence as pre-kickoff provenance.

### Current data freshness and consistency
- `data/current_source_manifest.json`: generated `2026-10-08T04:32:49.356196Z`; requested window 1–10 October.
- `data/current_reconciliation_status.json`: generated `2026-10-07T04:33:52.511010Z`; `EVENT_TRUTH_STALE`, reports 108 match rows and 128 goal-event rows, with four completed matches lacking chronology.
- `data/current_team_state_manifest.json`: generated `2026-10-07T04:33:53.351088Z`, claims 12,883 rows; actual `database/current_prematch_team_state.csv` has 0 data rows.
- Actual current files: matches 241 rows; goal events 137 rows; source reconciliation 108 rows; upcoming schedule 80 rows ending 2026-10-17; immutable `archive/FEATURE_SNAPSHOT_MANIFEST.csv` has 0 data rows.
- The counts in the current reconciliation status do not match the currently checked-out goal-event CSV (128 reported versus 137 actual), so current event truth must be rebuilt and reconciled before predictions.

### Latest inspectable workflow evidence
- Research Run 56: [workflow run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155799320). Its single job completed successfully; test, archive freshness, exact-scope guard, archive identity, standings, feature coverage, crosswalk, aliases, team-identity, kickoff-candidate, and report-upload steps all completed. Artifact `oracle-footystats-archive-feature-audit`, ID `12583524862`, size 51,604,642 bytes, digest `sha256:a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`. The run's head SHA was `cb461151e407f1be1e747109792a745d0f17cf93`; its success is diagnostic evidence and does not clear current readiness gates or certify later report-only commits.
- Private Expansion run `40149882862`: `prepare` failed; downstream jobs skipped; no artifacts.
- Private Current Staging run `40135966324`: `current` failed; no artifacts.
- Private prediction run `40145302396`, settlement run `40146540242`, run-to-completion run `40135975383`, and major audit run `40135966514`: each failed in its primary job and had no artifacts.
- Previously inspected failed-job log retrieval returned `BlobNotFound`/HTTP 404, so root causes are not established.

## Diagnostic workflow and execution blocker

The research-only workflow `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml` exists and is configured for manual dispatch. It checks the manifest's 50 unique IDs, makes one read-only FootyStats league-list request if the existing `FOOTYSTATS_API_KEY` secret is present, suppresses response bodies and request-error details, and uploads only a sanitized schema summary. It does not ingest fixtures or write production files.

The connected GitHub tool surface has no workflow-dispatch action. Therefore this run did not execute the diagnostic and made no provider API call. The account-specific provider schema is still unverified. The raw provider response was not retained in existing catalogue artifacts.

## Market gates

- M-1UP: **BLOCKED** — event truth is stale, current selected-50 fixture/team joins are unverified, and only historical season-level joins exist.
- BTTS Yes: **NOT PRODUCTION READY** — current selected-50 joins and point-in-time feature provenance are unverified.
- Double Chance: **NOT PRODUCTION READY** — current selected-50 joins and point-in-time feature provenance are unverified.
- Double Chance + Under 4.5: **NOT PRODUCTION READY** — current selected-50 joins and point-in-time feature provenance are unverified.

## Next safe actions
1. Manually dispatch the read-only schema diagnostic from the GitHub Actions page in the research repository; no paid provider change is requested.
2. Use its sanitized artifact to determine whether the 50 selected IDs appear in league-level or season-level ID fields; do not infer or relabel IDs without this evidence.
3. Resolve the 19 archive-unmatched IDs only from exact provider evidence and retain unresolved status otherwise.
4. Repair current event counts, rebuild the empty prematch team-state CSV, refresh current fixtures for the exact selected-50 scope, and establish exact fixture/team ID bridges.
5. Require timestamped, point-in-time xG and odds evidence and rerun market-specific gates and tests before any readiness declaration.

## Governance
No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry, or canonical ledgers were changed. No draft PR was merged, no gate was bypassed, and no paid provider change was made.

# Project Oracle — 50-League Scope-Safety and Current Evidence Audit (Run 7)

- Audit timestamp: 2026-10-25 04:24 SAST / 2026-10-25 02:24 UTC
- Branch: `research/oracle-50-league-readiness-audit`
- Status: **INCOMPLETE — production eligibility NOT GRANTED**
- Mode: research/reporting only. No production model, registry, or ledger changes.

## 1. Selected-50 integrity checks

Live-read checks were performed against:
- `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`
- the previous 50-row crosswalk revision 4
- private `config/oracle_major_league_registry_v1.json`
- private `data/league_readiness_matrix.csv`
- private current-source, reconciliation, team-state and feature-snapshot manifests
- current visible workflow run listings and the latest quality-matrix artifact.

The checks passed:
- Selected manifest rows: 50; unique provider IDs: 50.
- Crosswalk rows: 50; unique provider IDs: 50.
- Selected-manifest and crosswalk ID sets: exactly equal.
- Canonical candidate rows: 22, all labelled review-only/not-approved.
- Unresolved rows: 28.
- Production eligibility values in all rows: `NOT_GRANTED`.
- Market status distribution: M-1UP blocked for all 50 by stale event truth and missing selected-ID join; BTTS Yes, Double Chance and DC Under 4.5 unverified for all 50.

The research-only updated register is [revision 5](oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r5.csv), commit `d155b8c0b927686d2c25b389f27c46ef0fd42fb6`. It has 50 rows, 50 unique provider IDs and 115 columns. Added fields record the exact-scope workflow review, latest visible run evidence, source staleness, checksum verification, and the feature-snapshot manifest gap. Candidate codes remain candidates, never approvals.

## 2. Protected registry and readiness matrix

- The protected canonical registry has 27 entries; this is not substituted for the owner-approved 50-league scope.
- The legacy readiness matrix has 27 rows and was last successfully refreshed at `2026-10-01T17:25:35.759116Z`.
- The matrix's labels are stale and are not selected-provider-ID readiness proof.
- The selected-50 scope remains preserved even when there is no exact canonical mapping.

## 3. Current data and immutable feature snapshots

Verified from private repository files:
- Current source manifest generated `2026-10-08T04:32:49.356196Z`.
- Current reconciliation generated `2026-10-07T04:33:52.511010Z`, status `EVENT_TRUTH_STALE`, 108 current match rows, 128 goal-event rows, and four completed matches without retrieved goal-event chronology.
- Current team-state manifest generated `2026-10-07T04:33:53.351088Z`, 12,883 rows.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv` contains only its header and zero data rows. Therefore no immutable feature snapshots are indexed in that manifest. This is a material blocker for a fully reproducible prediction-to-settlement validation trail; it does not prove that no feature files exist anywhere else, only that this controlled manifest is empty.

These snapshots are not joined to the selected 50 provider IDs. Current fixtures, canonical team bridges, recent form, standings, xG/odds as-of-kickoff provenance and market readiness remain unverified for the selected-50 scope.

## 4. Quality-matrix artifact re-verification

Re-downloaded artifact `oracle-per-league-quality-matrix-40135938108` (artifact ID `12576693830`, GitHub digest `sha256:1684c954d875d109dc0af639f67291cd5ba0b2858e5e148d243446cd1717e552`). The artifact contains an outer ZIP with `oracle-per-league-quality-matrix.zip`; the inner ZIP contains the coverage CSV, H2H pairs CSV, summary JSON, Markdown report and `SHA256SUMS`.

All four entries listed in the internal `SHA256SUMS` matched their computed SHA-256 hashes. The summary confirms:
- 126 season manifest rows/files, 42 provider folder names, 35,819 match records, 35,819 distinct fixture IDs and zero duplicate fixture-ID keys.
- 36 provider folders have at least one H2H pair with five or more meetings.
- The artifact explicitly marks production readiness `NOT_ASSESSED`.
- Stored-payload non-null rates of 100% for many xG/odds fields are presence checks only. The report states that H2H chronology, neutral venue, team-ID continuity and strict pre-kickoff cutoff were not validated. These data cannot establish selected-50 readiness.

## 5. Newly verified workflow scope risk

Reviewed public workflow `.github/workflows/footystats-full-selected-league-historical-ingestion.yml` on the research branch.

Its actual behavior is:
- requires secrets `FOOTYSTATS_API_KEY` and `ORACLE_PRIVATE_REPO_TOKEN`;
- calls FootyStats `league-list` with `chosen_leagues_only=true`;
- ingests every league returned by that provider-selected catalogue for season-start years 2024, 2025 and 2026;
- packages and transfers a release to the private repository;
- its summary explicitly states that the provider-selected catalogue is **not** the governed Oracle league registry.

The reviewed workflow does not compare the returned provider-ID set against the exact 50 IDs in the recovered owner-approved manifest before ingesting/transferring. Therefore it is **not safe to use as proof of exact selected-50 coverage** without a preflight set-equality guard and explicit selected-ID filtering. It was not dispatched in this run. The connected GitHub tools expose no workflow-dispatch action, and no provider API execution action is available here; no API call or private release was fabricated.

## 6. Latest workflow evidence

Latest visible private run listing:
- Expansion #208, run ID `40149882862`: failure in `prepare`; `controlled`, `controlled_gate`, `expansion` and `finalize` were skipped; zero artifacts.
- Four-Model Live Prediction #78, run ID `40145302396`: failed in `predict`; no step details exposed by the connected job endpoint.
- Four-Model Live Settlement #38, run ID `40146540242`: failed in `settle`; no step details exposed.
- Run To Completion #26, run ID `40135975383`: failed; no step details exposed.
- No newer private run appeared in the current first-page run listing at audit time. This is not a claim about runs outside the returned page.

The private expansion manifest currently says `COMPLETE_RESEARCH_ONLY`. The inspected workflow's prepare gate is designed to set `proceed=false` and exit successfully when that status is read. Nevertheless run #208's prepare job failed. The job endpoint returned no step summaries/log URL, and prior log retrieval returned `BlobNotFound`; the discrepancy is verified, but its root cause remains unknown. Do not infer that the gate ran successfully or change the workflow blindly.

The latest visible public quality-matrix run remains [run #4](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40135938108), success. Its artifact is valid and checksummed; it does not establish production readiness.

## 7. Required safe remediation

1. Add a research-workflow preflight that reads the recovered 50-row manifest and compares its exact provider-ID set with the provider catalogue before any historical API requests or private release. Fail closed on missing/extra IDs; never silently substitute catalogue selection.
2. Ensure the ingestion package retains non-null `provider_league_id` separately from `season_id` in every manifest row and validates that invariant before transfer.
3. Diagnose the #208 prepare failure from actual step logs once available; preserve the current production workflow and do not infer a cause from the job-level conclusion alone.
4. Refresh current fixture/event truth and controlled team-state data, then join it to exact selected provider IDs, fixture IDs and canonical home/away team IDs.
5. Populate/validate immutable feature snapshots and point-in-time provenance before evaluating accuracy or promoting any market.
6. Continue row-by-row canonical review and market gates for M-1UP, BTTS Yes, Double Chance and DC Under 4.5.

## Decision

The selected-50 manifest/crosswalk integrity checks pass, and the latest research artifact's internal checksums pass. However, all 50 market rows remain unverified, 28 competitions are unresolved, no selected-provider-ID-to-fixture-to-canonical-team join is verified, current event truth is stale, and the controlled feature-snapshot manifest is empty. The selected-catalogue ingestion workflow also lacks an exact 50-ID guard.

**Do not declare completion or production readiness.** No production model logic, weights, probabilities, thresholds, calibration, version, protected registry or canonical ledgers were changed. No draft PR was merged, no quality gate was bypassed, and no paid provider change was made.

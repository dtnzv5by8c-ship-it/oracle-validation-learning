# Oracle Run #53 — Fixture Identity Review Queue
Date: 2026-10-22
Status: research-only triage; no fixture identity approved.

## Scope
The Run #53 artifact (workflow run 39662641163, artifact 12375010712) contains 210 staged market rows across 42 distinct source fixtures. A review queue was generated from the actual artifact, collapsing five market rows per fixture into one review row.

## Candidate classification (distinct fixtures)
- 21 fixtures: one provisional archive candidate in a competition-aligned folder.
- 4 fixtures: competition mismatch or crosswalk gap.
- 17 fixtures: no exact kickoff-and-team candidate.
- 0 verified identities; 0 eligible for scoring.

These counts are distinct fixtures. The workflow's fixture-candidate summary counts market-prediction rows (105 aligned, 20 mismatch/gap, 85 no candidate); do not confuse those row counts with fixture counts.

## Review queue columns
The CSV includes source fixture ID, competition code, UTC kickoff, source home/away names, number of market rows, candidate status, candidate archive fixture ID/competition/season, candidate home/away team IDs and matching status, same-pair archive row count, verification status, human review status, evidence notes, and production eligibility.

All 42 rows are initialized to:
- fixture_identity_verified=NO
- human_review_decision=PENDING
- production_eligibility=NOT_GRANTED

Candidate IDs are leads only. The queue does not approve or write any candidate ID into a canonical ledger.

## Immediate root cause
The private production repository's scripts/prepare_prospective_four_market_publication.py builds fixture IDs from league code, date, and slugified team names. The canonical publication/ledger schema retains fixture ID, competition, date/time, and team names but has no separate provider fixture ID or separate canonical home/away team IDs. The research adapter therefore fails closed.

## Safe resolution path
1. Trace each row to an authoritative provider fixture catalogue/season manifest, where available.
2. Approve only exact source-ID + competition + season + kickoff + home/away identity matches, with recorded evidence.
3. Keep normalized name matches as candidates until source identity is independently supported.
4. If upstream provider IDs were never retained, recommend a separately reviewed schema change at fixture ingestion/publication; do not infer IDs from names or silently modify production.
5. Keep unresolved rows excluded from metrics. No historical accuracy or calibration claim is supported until valid prediction/result pairs pass all evaluation gates.

## Governance
Research-only. No production model logic, probabilities, thresholds, calibration, model version, canonical registry, secrets, or provider plans changed. No paid API calls made. Production eligibility remains NOT_GRANTED.


## Upstream source-manifest trace (completed 2026-10-22)
The private repository's `data/fixtures/oracle_upcoming_fixtures.csv` contains only `league_code,date,home_team,away_team,kickoff_time`; it has no provider fixture ID or provider home/away team IDs. Its companion `data/fixtures/oracle_upcoming_fixtures_manifest.json` is a league-level acquisition summary (source priority, season, status and source row counts), not a per-fixture ID crosswalk. The ingestion script retrieves provider fixtures but normalizes the output to the five-column CSV. Thus the currently retained source CSV plus manifest cannot independently restore provider IDs for the 42 rows.

### Root-cause conclusion
The provider identifiers appear to be dropped at fixture ingestion/normalization, then a synthetic slug ID is generated at publication. The exact authoritative ID may still exist in provider raw responses or earlier workflow artifacts, but it is not present in the reviewed retained CSV/manifest schema. No claim is made that it is unrecoverable everywhere.

### Remediation decision
- Immediate: retain the 42-row candidate-only review queue; do not approve candidate IDs or score rows.
- Required future upstream change (separate approval): extend fixture ingestion output and its manifest to preserve source/provider fixture ID, provider competition ID, provider home-team ID, provider away-team ID, source name, retrieval timestamp and raw-response/snapshot hash. Keep Oracle's synthetic fixture key as a separate internal ID rather than substituting it for provider identity.
- Backfill: only map historical rows from retained raw provider evidence or an independently verified source snapshot; otherwise leave `UNRESOLVED`.
- Production governance: no private production code has been changed in this research pass.


## Additional source-code trace and current scheduled run (2026-10-22)
A further read-only inspection of `scripts/ingest_upcoming_fixtures.py` confirmed the extraction code can capture a provider-like identifier from raw Football Charts records (keys include `id`, `match_id`, `fixture_id`, or `slug`) as `source_match_id`, and can capture a slug. However, the final dataframe is explicitly written with only `league_code,date,home_team,away_team,kickoff_time`. This pinpoints the loss at the final normalization/export boundary for that source path. It does not prove every provider returns a stable canonical fixture ID, and the extracted generic `id` is not sufficient by itself to identify the provider namespace.

The private repository's latest scheduled workflow run observed during this check was Oracle Autonomous League Expansion run #192, ID `39706504130`, created 2026-10-22 01:34:51 UTC; its `prepare` job failed and later jobs were skipped. The run has no uploaded artifacts. The job-log endpoint returned a 404/BlobNotFound response, so the precise failure message could not be independently recovered through the available GitHub connector. This run is separate from the successful research-only archive audit. It should be investigated before claiming autonomous league expansion is healthy; no rerun or production modification was made.

## Completion boundary
The research-only identity investigation is complete to the extent of retained evidence: root cause is located in the ingestion/export schema; a 42-fixture manual review queue exists; scoring remains correctly blocked. Historical accuracy/backtesting and a permanent production fix are not complete because canonical identities and valid production prediction/result rows are unavailable in retained records. The permanent ingestion schema fix requires explicit approval before implementation under the project's production-governance rules.


## Follow-up investigation (2026-10-22, read-only)
- The latest private-repository run list shows repeated failures on the autonomous league-expansion workflow: #189 (21 Oct), #190 (21 Oct), #191 (21 Oct), and #192 (22 Oct). In addition, the four-model live prediction run #72 and live settlement run #34 failed on 22 Oct.
- For expansion run #192, the `prepare` job failed and all downstream jobs were skipped. The available connector cannot retrieve the job log (GitHub log URL returns 404/BlobNotFound), and there are no run artifacts. Run #191 has the same prepare-failed/downstream-skipped shape and its log endpoint also returns 404. Therefore the exact runtime error is **unconfirmed**; the observed failure pattern is confirmed.
- The current expansion workflow's prepare gate attempts to find prior completed controlled-league artifacts through the GitHub Actions API, using `GITHUB_TOKEN`. The evidence currently available does not distinguish a token/API access issue, missing eligible prior artifacts, or another prepare-step exception. No speculative fix was committed.
- A repository tree audit found retained historical SportMonks canonical fixture and xG payload paths, but those are date-partitioned historical datasets and are not proven raw responses for the 42 prospective source fixtures. They cannot be used to approve those fixtures without an exact, independently verified match.
- Current safe completion: the diagnosis and review queue are documented; the research audit passes mechanically but has zero eligible scoring rows. The live prediction/settlement and expansion workflows are not healthy based on their latest observed runs. Do not interpret a workflow's successful conclusion as model accuracy.
- To finish historical validation honestly, the remaining blockers are: (1) authoritative identity evidence for source fixtures, (2) valid production prediction and settlement rows, and (3) a retrievable root-cause log for the scheduled workflow failures. The permanent ingestion/export change is still a separate production-governed change and was not applied.


## Visibility and regression milestone update (2026-10-22 04:10 UTC)

- Public research PR #15 adds a repeatable fixture-identity regression workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/15
- The public workflow retrieves only the proposed ingestion script and regression tests from private PR #20 using the existing repository secret. It does not call any football-data provider APIs, change production code, or spend private-repository Actions minutes.
- Verified successful public runs:
  - Run #4, PR-triggered: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39715822257
  - Run #5, push-triggered with test evidence artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39720726994
  - Run #6, PR-triggered with test evidence artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39720732512
- Run #4 logs explicitly show `3 passed in 0.60s`. Runs #5 and #6 completed successfully after the workflow was updated to write a GitHub job summary and upload a 30-day test-evidence artifact.
- The public workflow is now scheduled every six hours and also supports manual dispatch. This provides ongoing visible regression status in GitHub Actions while the chat is inactive. It is a test heartbeat only, not a claim that the entire Oracle build runs autonomously or that the production prediction/settlement workflows are healthy.
- Current code review boundary: the tests cover three targeted extractor cases (provider IDs separate from slug; missing IDs remain missing; deterministic fingerprint). Further coverage is still required for alternate provider payload shapes and downstream CSV/manifest output. PR #20 remains a draft and is not merged.
- Historical fixture review remains blocked at zero verified identities / zero eligible scoring rows in the last verified audit. The regression tests do not resolve old fixture identities or create valid historical production prediction rows.

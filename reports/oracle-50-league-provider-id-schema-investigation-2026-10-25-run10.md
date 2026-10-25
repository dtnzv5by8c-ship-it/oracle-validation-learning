# Project Oracle — Selected-50 Provider ID Schema Investigation (Run 10)

Audit time: 2026-10-25 05:07 UTC / 07:07 SAST
Branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**
Scope: exactly the 50 owner-selected FootyStats IDs in the recovered manifest. Research/reporting only.

## New finding: documented league-list schema does not establish a parent competition ID

Official FootyStats documentation for `league-list`:
https://footystats.org/api/documentations/league-list

The published sample response contains each catalogue item as `name` plus a `season` array. The sample places `id` inside each season object and explains that each season of a competition has a unique ID; it does not show a top-level parent competition `id` on the league object.

The public catalogue-transfer workflow at `.github/workflows/footystats-full-universe-catalogue-transfer.yml` currently writes:
- `provider_league_id = league.get('id')`
- `season_id = season.get('id')`

The acquired catalogue artifact has 43 rows and all 43 `provider_league_id` values blank. The downstream archive manifest has 126 rows and all 126 `provider_league_id` values blank. This is consistent with the workflow requesting a parent ID that is not present in the documented sample schema.

**Causality is narrowed, but not fully proven:** the raw account-specific API response was not retained in the catalogue package. We therefore cannot assert that every live response omits the top-level field. The evidence does prove that the workflow's current `league.get('id')` output is blank in the saved artifact and that the published example does not establish that field. Do not invent a replacement field.

## Identifier policy

- Preserve all 50 owner-selected IDs exactly as supplied.
- Do not reinterpret them as season IDs merely because 31 IDs numerically match an archive season ID.
- Keep parent competition ID and season ID as separate fields.
- The saved selection manifest records the IDs and display names but the current repository evidence does not resolve the underlying checkbox/API identifier semantics.
- Continue to mark candidate canonical codes as review-only and unresolved rows as `UNRESOLVED`.

## Current scope and crosswalk validation

- Owner-selected manifest: 50 rows, 50 unique IDs.
- Crosswalk revision 11: 50 rows, 50 unique IDs; exact set equality with the manifest.
- Canonical candidates requiring review: 22.
- Unresolved: 28.
- Approved mappings: 0.
- Exact selected ID → provider competition ID → fixture ID → canonical home/away team joins: 0/50 verified.
- Crosswalk production eligibility: `NOT_GRANTED`.

Revision 11 corrects the stale status recorded for scope-guard Run #56: live jobs and the artifact show that the workflow completed successfully, while its scope decision remained `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`.

## Protected registry and legacy readiness matrix

Read live from the private default branch:
- Protected registry `config/oracle_major_league_registry_v1.json`: 27 entries; 13 marked `CONTROLLED`, 14 `NOT_INGESTED`. This is the protected legacy universe, not the selected-50 scope.
- `data/league_readiness_matrix.csv`: 27 rows; 22 status labels `PRODUCTION-READY`, 5 `PARTIAL`; every row has last-successful-refresh timestamp 2026-10-01T17:25:35.759116Z. These labels are stale and do not establish selected-provider-ID readiness.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv`: header only, zero indexed feature snapshots.

## Historical and current evidence

The latest inspected public archive feature audit is workflow Run #56:
https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155799320

- Conclusion: success; 98 tests passed.
- Artifact ID: 12583524862.
- Artifact digest: `sha256:a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`.
- Archive summary: 35,819 match rows, 35,819 chronological feature rows, 126 season folders, 28,491 rows with accepted settled status and complete scores, zero parse errors, zero duplicate nonempty fixture IDs. The archive freshness gate passed at execution time.
- Scope guard decision: `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`; this is a successful diagnostic run, not a scope pass.

Name-based archive evidence remains limited to 31/50 exact country + competition-name matches after diacritic normalization; 19/50 have no exact name match in the audited snapshot. Those 31 matches have 30,257 season-folder records across 2024–2026, but they are not exact parent-provider-ID joins.

Current private data is stale:
- `data/current_source_manifest.json`: generated 2026-10-08; requested dates 2026-10-01 through 2026-10-10.
- `data/current_reconciliation_status.json`: generated 2026-10-07; `EVENT_TRUTH_STALE`; 108 current-match rows, 128 goal-event rows; four completed matches lack retrieved goal-event chronology.
- `data/source_reconciliation_manifest.json`: 108 rows, zero matched, 108 unverified, eight HTTP 403 source errors.
- `data/current_team_state_manifest.json`: generated 2026-10-07; 12,883 rows, history window 5.
- `data/fixtures/oracle_upcoming_fixtures.csv`: latest dates only through 2026-10-17 and legacy league codes, not a fresh selected-50 fixture feed.

## Latest inspected workflow outcomes

Public research Run #56 succeeded as an audit job and uploaded the artifact above. Its steps included unit tests, archive freshness, exact-scope guard, archive identity audit, standings reconstruction, feature coverage, crosswalk/alias review and prediction identity/fixture-candidate audits.

Private runs remain failed with no artifacts:
- Expansion #208 / run ID 40149882862: `prepare` failed; remaining jobs skipped.
- Current staging #366 / run ID 40135966324: `current` failed.
- Live prediction #78 / run ID 40145302396: `predict` failed.
- Settlement #38 / run ID 40146540242: `settle` failed.
- Run-to-completion #26 / run ID 40135975383: `run-to-completion` failed.
- Major audit #16 / run ID 40135966514: `audit` failed.

The jobs API returns empty step summaries for the inspected failed jobs; log retrieval returns `BlobNotFound`; the inspected runs have no artifacts. Failure conclusions are verified; underlying root causes are not. The connected GitHub tools expose no workflow-dispatch action in this execution, and no provider API call was made.

## Market readiness

- **M-1UP:** blocked by stale event truth and missing selected-ID joins.
- **BTTS Yes:** not verified for the selected 50; exact joins and point-in-time feature provenance are absent.
- **Double Chance:** not verified for the selected 50; exact joins and point-in-time feature provenance are absent.
- **Double Chance + Under 4.5:** not verified for the selected 50; exact joins and point-in-time feature provenance are absent.
- xG numeric fields and fields labelled pre-match are present in the name-matched archive snapshot, but verified as-of-kickoff xG provenance is 0 rows.
- Odds fields are present in the archive snapshot, but odds timestamp fields and verified pre-match odds provenance are 0 rows.
- H2H is not cleared for selected-50 use; chronology and identity have not been established for this scope.

## Next safe actions

1. Preserve the exact selected IDs and names; do not change the owner-approved scope.
2. Trace the saved checkbox field semantics and obtain a raw, sanitized provider catalogue response or equivalent schema evidence without exposing credentials.
3. Update the catalogue generator only after the real source identifier field is evidenced; preserve parent competition ID separately from season ID.
4. Regenerate catalogue/archive manifests and rerun exact-50 set equality; fail closed on blank, duplicate, missing or extra IDs.
5. Only then establish fixture and canonical team joins, refresh current data, index immutable feature snapshots, verify standings/recent form and prove xG/odds point-in-time provenance.
6. Reassess each market independently; do not treat a successful diagnostic workflow as a readiness pass.

## Governance

No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry or canonical ledgers were changed. No draft PR was merged, no gate was bypassed, and no paid provider change was made.

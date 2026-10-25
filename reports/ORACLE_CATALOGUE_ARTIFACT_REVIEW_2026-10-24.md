# Oracle Catalogue Artifact Review — 2026-10-24

## Evidence reviewed

Uploaded artifact: `oracle-44-league-broader-catalogue-discovery 5.zip`

Provider summary generated at `2026-10-23T22:37:54.332564+00:00`:
- Provider catalogue entries: 1,737
- Target universe: 44
- Exact alias candidate targets: 41
- Fuzzy candidates requiring review: 3
- Targets with no candidate found: 0
- Candidate crosswalk rows: 56
- Unique target codes: 44
- Targets with season IDs: 44
- Targets with season labels: 44
- Targets with season dates: 0
- Structural validation errors: 0
- Warnings: 19
- Mapping approval: NOT_GRANTED

## Interpretation

The artifact demonstrates successful broad catalogue retrieval and candidate generation. It does not demonstrate 44 verified mappings or fixture readiness. Multiple candidates remain for CRO, CO and EC. Provider season dates are absent for every target; do not infer season dates from labels. The 19 warnings include unresolved candidate rows and duplicate candidate rows requiring manual review.

The exported `provider_league_id` field is blank. The provider's season IDs are populated and are the relevant IDs to carry into match-data requests; do not treat a blank parent ID as proof that the season IDs are invalid.

## Required gates before prediction

1. Run the research validator/unit-test workflow against the current branch.
2. Resolve competition identity and season IDs from provider metadata, keeping each decision auditable and unapproved until evidence is sufficient.
3. Run the fixture-data audit by verified season ID, checking pagination termination, expected fixture counts, duplicate fixture keys, kickoff timestamps/time zones, match status, and data freshness.
4. Verify odds/market observations have source and observation timestamps suitable for the intended use. No historical backtest without point-in-time pre-kickoff data and verified settlements.
5. Report each target as READY, PARTIAL, BLOCKED, or UNVERIFIED based on evidence; never convert missing evidence to zero or silently map aliases.
6. Keep the 44-league research universe separate from the governed 27-league production universe.

## Governance

This is a research-only artifact review. No production model logic, probabilities, calibration, thresholds, market definitions, or production registry were changed. No mapping is approved by this report.

# Oracle 44-League Audit — Code Review and Next Fixes
Date: 2026-10-23
Branch: research/oracle-crosswalk-isolation-2026-10-22

## Scope
Reviewed the current research workflow `.github/workflows/oracle-44-league-footystats-full-season-audit.yml`. This is a research-only code review. No production code or registry was changed.

## Defects to fix before relying on the output

1. **Catalogue scope is restricted.** The workflow calls `league-list` with `chosen_leagues_only=true`. The 20 `NO_EXACT_ALIAS_MATCH` rows therefore mean only that aliases were not found in this selected catalogue. They do not establish that the provider lacks those competitions. The next iteration should retrieve the provider's full accessible catalogue where the API contract/subscription permits, preserve exact names and IDs, and produce candidate suggestions without auto-approving fuzzy matches.
2. **Season selection is not validated.** For a single exact alias, the workflow chooses the season with the largest first year parsed from `year`. It does not validate season start/end dates or whether the season is current/relevant. Store all available season IDs/date labels in discovery output and require explicit evidence before choosing a season.
3. **Pagination assumption is unverified.** The workflow assumes `max_per_page=100` and short-page termination. A short page is only a retrieval stopping condition, not evidence that the full season was returned. Confirm provider pagination semantics and compare returned fixture IDs/counts with an independent schedule or official totals where possible.
4. **Upcoming fixture counter is incorrect.** `upcoming_rows` currently counts fixtures with missing home or away goal counts. That can count abandoned, postponed, in-play, or incomplete records as upcoming. Derive fixture status from documented provider status and kickoff time, and separately report missing goals.
5. **Final status classification is too narrow and potentially unsafe.** Only a small set of text statuses are treated as final. The provider may use numeric/status variants. Inspect actual returned status values, document the mapping, and retain unknown values as unresolved instead of silently treating them as non-final.
6. **xG field-name reporting is misleading.** The workflow derives `xg_fields` from keys in its own normalized fixture dictionary, so the list can show expected fields even when the provider payload does not contain them. Capture actual source field presence separately from normalized output fields.
7. **Odds coverage is too narrow.** The current counter considers only 1X2 odds. Label it specifically as 1X2 odds coverage; do not imply all bookmaker markets are available.
8. **No source completeness or as-of proof.** Response hashes and page counts prove which responses were seen, not whether data was complete or historically available before kickoff. Add explicit provenance fields and do not call historical feature values pre-match unless the provider documents/records a reliable timestamp.
9. **No independent regression tests are visible in this workflow.** Add tests for 44 target rows, no duplicate target-season-match keys, missing IDs/timestamps, ambiguous aliases, failed API pages, pagination ceiling, unknown statuses, and no false-success status when data is incomplete.
10. **Scheduled operation is not configured in this workflow.** Current triggers are manual dispatch and a push affecting this workflow file. Add a bounded weekly schedule only after confirming rate limits and secret availability; use concurrency protection and clear failure summaries. Do not create self-triggering loops.

## Verified baseline from the uploaded audit archive
- Target leagues: 44.
- Candidate season IDs: 24.
- Pagination reached a short page for 24 targets; 20 targets were not retrieved.
- Fixture rows: 7,216.
- Unique target-season-match keys: 7,216.
- The audit itself states full-season completeness and historical as-of provenance are not established.
- Production model logic, production registry and production predictions were unchanged.

## Recommended implementation order
1. Expand catalogue discovery and generate a reviewable alias candidate report.
2. Correct fixture status semantics and source-versus-normalized field reporting.
3. Validate season selection and provider pagination.
4. Add automated unit/regression tests and fail-closed acceptance checks.
5. Add scheduled execution and clear run summaries after tests pass.
6. Run again and compare exact per-league counts against this baseline.
7. Only then proceed to team context and historical prediction/settlement validation.

## Completion state
NOT COMPLETE. This code review identifies concrete failure modes. It does not claim fixes have already been implemented or that all 44 leagues are supported.

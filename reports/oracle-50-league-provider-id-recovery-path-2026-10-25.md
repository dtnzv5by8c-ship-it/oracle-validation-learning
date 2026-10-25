# Project Oracle — Provider ID Recovery Path (Research Only)
Date: 2026-10-25
Branch: `research/oracle-50-league-readiness-audit`
Status: DOCUMENTATION-VERIFIED CANDIDATE; SELECTED-50 LIVE RESPONSES NOT YET VERIFIED
Production eligibility: NOT_GRANTED

## Evidence reviewed
- The official [FootyStats league-list documentation](https://footystats.org/api/documentations/league-list) describes each season's nested `season[].id` as a unique season ID. The published sample does not establish a top-level parent competition ID.
- The official [FootyStats league-teams documentation](https://footystats.org/api/documentations/league-teams) lists `id` as the team ID and `competition_id` as the competition ID in team records. It uses `season_id` to select the season and documents `max_time` for as-of statistics.
- The existing selected-50 manifest values were reconciled to nested season IDs for 50/50 selected entries. They must not be re-labelled as parent competition IDs.

## Safe recovery procedure
1. Do not call the provider until explicit `confirm_provider_credit_usage=true` confirmation is provided for the existing guarded workflow.
2. After confirmation, make a bounded diagnostic request for a small sample of selected season IDs using the existing Hobby package and conservative rate limits.
3. Retain raw provider responses only in the private workflow workspace. Public output must contain sanitized field-presence counts, status codes, and non-sensitive consistency outcomes only.
4. For each season, inspect team records for `competition_id`. Require a non-empty value and agreement across all returned teams. Compare the result to the exact catalogue country/name and selected season record.
5. Do not infer the parent ID from a season ID, team ID, display label, or research alias. If any response is blank or inconsistent, keep the parent ID unresolved.
6. Only after the sample passes, assess the minimum additional calls needed to verify all 50 selected seasons within the existing credit/rate allowance. Do not automatically scale to 50 calls without a bounded plan and explicit credit authorization.
7. Keep production registry/crosswalk unchanged until the evidence is independently reviewed and approved.

## Automated guard added
A static test in `tests/test_footystats_ingestion_workflow_contract.py` verifies that the existing ingestion contract keeps `season_id` distinct from `provider_league_id`. The public dry-run planner runs this test; it makes no network/API calls.

## Remaining blockers
- No account-specific `league-teams` response has yet been inspected for these 50 selected seasons.
- Canonical Oracle competition/team/fixture mappings are not approved.
- Combo predictor target and settlement-ledger definition disagree; Combo probabilities remain blocked in governed reports.
- Historical standings-as-of-kickoff and xG/odds provenance remain unverified.
- Production remains `NOT_GRANTED`; M-1UP remains blocked.

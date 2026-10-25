# Oracle Fixture Lifecycle and Timing Audit — 2026-10-23
Branch: research/oracle-crosswalk-isolation-2026-10-22
Input: uploaded `oracle-44-league-footystats-full-season-audit.zip`, sanitized fixture audit CSV.
Method: read-only status and field-presence audit; no predictions generated.

## Observed provider statuses
- `complete`: 2,930 rows
- `incomplete`: 4,270 rows
- `suspended`: 16 rows
- Total: 7,216 rows

The existing pipeline's `upcoming_rows` metric counts rows with null goal values. That is not a reliable upcoming-fixture classifier. In this artifact, all rows have both goal fields populated, yet 4,270 are marked `incomplete` and 16 `suspended`. These cannot be treated as settled merely because goal fields are populated. Status must be interpreted according to provider documentation and independently confirmed settlement data.

## Observed nonempty field counts
All 7,216 rows have nonempty values in each of these columns: `homeGoals`, `awayGoals`, `team_a_xg`, `team_b_xg`, `team_a_xg_prematch`, `team_b_xg_prematch`, `odds_ft_1`, `odds_ft_x`, and `odds_ft_2`.

This is only a field-presence result. It does not prove that the values are numerically valid, that the odds were available before kickoff, that xG fields have the expected provider semantics, or that an incomplete/suspended match is settled. The audit schema has no per-observation timestamp or capture-time provenance for these values; therefore, feature timing cannot be verified from this artifact.

## Backtesting gate
**Historical backtesting remains blocked.** Before a match can be considered settled, its status must map to an explicitly supported settled state and be cross-checked against a trusted settlement source. Before a feature or odds value can be used historically, its availability timestamp must be at or before kickoff and its source must be recorded. Unknown, incomplete, suspended, postponed, abandoned, in-play, or ambiguous statuses must not be silently counted as settled.

## Research-only code added
`scripts/audit_fixture_lifecycle.py` writes a conservative lifecycle classification and explicitly sets `feature_timing_verified=false` for every row because the input schema has no point-in-time timestamps. It does not change production logic or create predictions. The script is committed but has not yet been wired into or observed running in GitHub Actions.

## Remaining blockers
1. Run the broader catalogue discovery workflow and inspect its artifact.
2. Reconcile all candidate season IDs and official fixture counts; do not infer completeness from short-page pagination.
3. Obtain documented status semantics and independently verified results/settlements.
4. Capture and enforce feature/odds as-of timestamps.
5. Integrate both validators and the lifecycle audit into a research workflow, fail-closed on structural issues.
6. Run the historical league-market and team-context analysis only after the above gates pass.
7. Confirm successful recurring runs and artifact availability after schedule activation on the default branch.

No production model logic, weights, thresholds, probabilities, selection rules, market definitions, or governed 27-league registry were changed. No production predictions were created and no PR was merged.

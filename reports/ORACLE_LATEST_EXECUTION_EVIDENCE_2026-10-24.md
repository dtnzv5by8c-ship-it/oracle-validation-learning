# Oracle 44-League Pipeline — Latest Execution Evidence and Blockers
Date: 2026-10-24
Branch: research/oracle-crosswalk-isolation-2026-10-22
Status: research-only; production untouched.

## Re-analysis of the uploaded fixture artifact
The sanitized fixture CSV was re-read locally on 2026-10-24:
- Rows: 7,216
- Target codes represented in fixture rows: 24
- Provider status counts: `complete` 2,930; `incomplete` 4,270; `suspended` 16.
- Rows with all three 1X2 odds fields parseable as finite numeric values greater than 1.0: 3,200.
- Rows with zero, invalid, or incomplete 1X2 odds: 4,016.
- Per-observation timestamp fields for odds/features: absent.
- Kickoff years represented: 2026 and 2027.

A positive numeric odds test is only a minimum sanity check, not proof of a valid bookmaker quote, source, capture time, or pre-kickoff availability. The 4,016 rows must not be treated as having usable full 1X2 odds. The 7,216 rows include unresolved/suspended states and 2027 kickoff dates, so this artifact is not a verified historical settlement dataset.

## Code committed in this checkpoint
- `scripts/oracle_fail_closed_quality_gate.py`: rejects the artifact for historical backtesting when odds are zero/invalid/incomplete or observation-time columns are absent.
- `.github/workflows/oracle-44-league-artifact-quality-gate.yml`: a post-workflow artifact validation workflow that downloads the source audit artifact, runs structural/lifecycle/quality checks, and uploads evidence even when the quality gate fails.
- Existing broader catalogue discovery, lifecycle audit, and unit-test workflow remain in the research branch.

## What has not been confirmed
The new GitHub Actions workflows have not been observed running successfully. GitHub's `workflow_run` trigger requires the workflow definition to exist on the default branch; this branch-only commit does not activate that trigger by itself. The catalogue discovery job has not yet yielded a verified artifact. API secret availability and provider access are not verified by code inspection alone.

## Immediate technical gates
1. Get the research workflows reviewed/available on the repository default branch through the normal pull-request path; do not merge automatically.
2. Trigger and inspect the broader catalogue artifact; resolve exact/ambiguous/missing provider league IDs and inspect season IDs, labels, start/end dates.
3. Add a documented season-window check and independent fixture-count reconciliation. Do not use short-page termination as proof of completeness.
4. Run the quality gate on the source artifact; expected outcome is failure until valid odds and timing provenance are present.
5. Obtain provider-documented status semantics and independent settlement confirmation.
6. For any future collection, record provider response/capture timestamps for each odds and feature value, then enforce timestamp <= kickoff. Historical timestamps cannot be retroactively inferred from the current snapshot.
7. Retrieve actual historical Oracle prediction records and verified settlements; only then run market/league/team metrics. Do not infer accuracy from match coverage.

## Governance
No production model logic, probabilities, weights, thresholds, selection rules, market definitions, or governed 27-league registry were changed. No production predictions were created. No pull request was merged.

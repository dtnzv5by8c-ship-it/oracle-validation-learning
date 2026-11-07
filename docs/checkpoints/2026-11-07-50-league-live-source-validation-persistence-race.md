## 50-league live source validation execution — persistence race — 2026-11-07

### Finding
The first genuine manual 50-league live fixture-source validation execution completed the source validation and exact board reconciliation successfully, but the final evidence-persistence step failed because the governed research branch advanced concurrently.

### Evidence
Workflow run: `42361333640`.
Validator result:
- governed_leagues: 50
- READY: 26
- DATA_GATED: 24
- SOURCE_ERROR: 0
- fixtures_in_window: 299
- leagues_with_fixture_evidence: 26
- leagues_without_fixture_evidence: 24
- scope_reconciliation_passed: true

Reconciliation result:
- status: PASS
- classification_counts: DATA_GATED 24, READY 26
- fixtures_in_window: 299
- missing: []
- unexpected: []
- duplicates: []

The runner successfully created both evidence files locally, then its push was rejected with `fetch first` because the remote `research/oracle-50-league-readiness-audit` branch contained concurrent work.

### Root Cause
The workflow checked out a moving governed research branch and attempted a direct push without first integrating concurrent control-plane commits. Oracle continuation automation can legitimately advance that same branch while the workflow is running.

### Impact
The live source-validation computation and reconciliation are proven by the run logs, but the canonical persisted artifacts are absent. Therefore the production source-validation gate remains fail-closed until the artifacts are successfully persisted and re-read from live GitHub.

### Fix
Hardened the default-branch workflow persistence step in commit `b5987ca1194469e65e61296157cf1f2b75acaf89`:
- fetch the latest governed branch
- rebase the evidence commit
- retry the push up to three times
- never force-push
- fail explicitly if the bounded retries cannot persist evidence

### Validation
The workflow YAML change is committed to `main`. The failed run must not be rerun as-is because that run references the old workflow definition. A new manual or scheduled execution using the hardened workflow is required. Oracle V1.6 production logic and probabilities remain unchanged.

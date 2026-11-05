# Project Oracle — FootyStats Selected-50 Delta Gateway Checkpoint — 2026-11-05

## Governed state
- Selected-50 governed leagues: 50/50
- Provider seasons: 182
- Planned historical ingestion tasks: 728
- Prior 910-request preflight: preserved; do not rerun
- Oracle V1.6 production logic/governance: unchanged
- Private `oracle-football-data` repository: protected; no private historical ingestion started

## Delta run reviewed
- Workflow run: 42066402790
- Main commit: 802aa9b0459167ef1bf5c68f6f2af4b60c4261da
- Result: FAIL-CLOSED
- Delta plan: 20 seasons × 5 endpoint checks = 100 reserved requests
- Provider requests: 1 attempted before the gateway parser failed; 0 successful provider responses were validated
- Failure: the curl status capture returned an empty status string, so the workflow correctly refused to treat the response as valid data.
- This is a gateway transport/status-capture defect, not evidence of provider data unavailability.
- The reservation was finalized ABORTED with observed actual requests recorded from the timestamp ledger.

## Repair
Main commit:
- `2ea024ffe37bfc5ad392d38c2c21b6af15528188`

Repair:
- deterministic HTTP status capture using curl `-o <temporary body> -w %{http_code}`
- temporary provider response body is deleted after parsing and is not committed
- every attempted request timestamp is persisted immediately, including fail-closed transport failures
- no retry loop was added
- explicit HTTP non-200 responses remain fail-closed

## Governance
The repair does not alter Oracle V1.6 production logic, probabilities, thresholds or calibration. No private historical ingestion is authorized by this checkpoint.

## Next gate
1. Public contract tests must pass against the repaired gateway contract.
2. Manual dispatch of the repaired Delta Gateway with `confirm_provider_api_usage=true`.
3. Inspect all 100 provider requests across all 20 delta seasons and all five endpoint checks per season.
4. Only after all gates pass, prepare the private archive receipt and historical-ingestion authorization checkpoint.

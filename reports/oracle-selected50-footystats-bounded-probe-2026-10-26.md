# FootyStats Selected-50 Bounded Endpoint Probe — 2026-10-26

**Status:** Completed endpoint/schema smoke probe; research-only. Production eligibility remains NOT_GRANTED.

## Run and artifact

- Workflow run: [40267591627 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40267591627)
- Branch: `research/oracle-50-league-readiness-audit`
- Code commit: `f56f15b0673f8ec91b9d2299f66cf5365c30291f`
- Artifact: [footystats-selected50-bounded-endpoint-probe](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40267591627/artifacts/12626971847)
- Artifact SHA-256: `aca547becd07b7312a98f503f1975fb61332836d6770531dbbca50064781987f`
- Artifact size: 6,045 bytes

## Actual request ledger

| Endpoint | Requests | HTTP 200 + provider success |
|---|---:|---:|
| `league-list` | 1 | 1 |
| `league-matches` | 50 | 50 |
| `league-teams` | 50 | 50 |
| `league-tables` | 50 | 50 |
| `league-season` | 50 | 50 |
| **Total** | **201** | **201** |

The workflow had a hard cap of 201 requests, used no retries, and made exactly 201 requests. Provider metadata reported 1,594 requests remaining in the observed request window after the probe. This is a request-window indicator; it does **not independently establish a separate monthly billing/credit balance**.

## Selected-50 result

- Crosswalk rows checked: 50.
- Exact selected season IDs found in the live chosen-league catalogue: 50/50.
- Unique live catalogue league labels represented by those IDs: 50.
- Leagues with all four endpoint responses successful: 50/50.
- Endpoint failures: 0.
- `league-matches` intentionally requested only one row per selected season for schema inspection; this is not full match-history ingestion.
- `league-teams` returned between 8 and 30 teams per season.
- Provider season-year values: 33 rows use `20262027`; 17 use `2026`. Preserve the original values and normalize only with an explicit, tested rule; do not guess.
- The live catalogue name and exact season-ID match are provider-catalogue evidence only. They do not approve canonical competition codes, establish parent competition IDs, or verify fixture/team joins.

## Data safety and governance

- API key was not logged or saved.
- Raw provider payloads were not saved in the artifact.
- No private repository transfer was attempted.
- No production model logic, probabilities, calibration, thresholds, or frozen 27-league baseline were changed.
- Combo and M-1UP remain blocked; all Selected-50 outputs remain research-only.

## Artifact-status caveat

The workflow run and endpoint step completed successfully, and the downloaded CSV records show 201/201 successful responses and 50/50 four-endpoint successes. However, the artifact's summary JSON retained the intermediate status `IN_PROGRESS_OR_STOPPED_FAIL_CLOSED` because the checkpoint writer overwrites the final status on save. Therefore this report's completion status is based on the verified workflow conclusion and the independently inspected endpoint-result and league-matrix CSVs, not that stale summary status field. Do not rerun the live probe merely to correct this metadata defect; correct the status-writer logic in a future code-only change that cannot trigger live requests.

## Next actions

1. Keep the provider season-year strings as received and add a tested normalization rule with regression cases for both `20262027` and `2026`.
2. Reconcile the 50 exact provider season IDs to authoritative parent competition IDs and canonical fixture/team identities. This probe does not do that.
3. Refresh the current fixture schedule and immutable point-in-time feature snapshot.
4. Reconcile official result/settlement truth, especially Combo, before model evaluation.
5. Only after identity, point-in-time and settlement gates pass, ingest the required historical rows into a safe private destination and validate completeness. Do not publish raw licensed provider data in the public repository.


## Follow-up hardening after the probe

- The live workflow is now **manual-dispatch-only**; commits no longer trigger provider calls automatically.
- The summary checkpoint writer was corrected to preserve a final status instead of overwriting it with an intermediate status. The original artifact above remains immutable and retains its old status field; its independently verified endpoint CSVs remain the evidence for the completed run.
- Added and CI-tested conservative season-year parsing: `20262027` becomes start 2026/end 2027; `2026` becomes start 2026/end unknown; malformed or unsupported tokens are quarantined. The helper preserves the raw token and does not alter production data/model logic.
- Added a no-network governance contract test for the live probe. Both new tests passed in [dry-run planner run 40268199040](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40268199040). No additional provider calls were made.
- Remaining gates are unchanged: authoritative parent competition IDs, canonical fixture/team joins, current schedule refresh, immutable point-in-time feature snapshots, official settlement truth, and Combo/M-1UP readiness.

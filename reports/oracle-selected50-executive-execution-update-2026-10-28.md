# Oracle Selected-50 Executive Execution Update — 2026-10-28 08:55 UTC

## Decision

**Research execution is progressing; production/betting release remains NO-GO.** The bounded provider work and current research validation completed successfully, but identity approval, current-feed freshness, exact fixture/team joins, official settlement truth, and market calibration are still open. No release gate is being bypassed.

## New execution evidence

| Workstream | Latest result | Evidence |
|---|---|---|
| FootyStats season identity | 50/50 HTTP 200; 50/50 returned season ID/country/name checks; 50 distinct provider `comp_master_id` values | [Workflow run 40562430790](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790); [identity reconciliation report](oracle-selected50-footystats-master-id-reconciliation-2026-10-28.md) |
| FootyStats current schedule retrieval | 50/50 `league-matches` requests passed; one page per selected season; 871 fixtures in next 14 days and 871 recent completed matches in the prior 14-day lookback | [Final 50-league readiness matrix](oracle-selected50-final-readiness-matrix-2026-10-28.md) |
| Cross-provider fixture join audit | 71 FotMob current rows; 10 exact joins across 2 selected seasons; 0 exact joins to the historical Oracle ledger; 577 date-only ledger candidates excluded from approval | [Workflow run 40646418126](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126); [sanitized artifact 12797871592](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126/artifacts/12797871592) |
| Candidate FotMob bridges | 2 strong candidates, both human-review only: Canadian Premier League → FotMob ID 1000001192 (4 exact joins; 1 pre-kickoff snapshot row) and EFL League One → ID 938219 (6 exact joins). 0 canonical code candidates. | Same cross-provider audit artifact |
| Research runtime | PASS | [Workflow run 40646418147](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418147) |
| Safety contract tests | PASS | [Workflow run 40646418166](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418166) |
| Dry-run planner | PASS | [Workflow run 40646418143](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418143) |

## Provider allocation

The user authorized bounded FootyStats usage and stated a limit of 1,800 requests/hour. Today's bounded identity and schedule checks used 100 requests total (50 `league-season` + 50 `league-matches`) with no retries. That is about 5.6% of the stated hourly ceiling. The hourly ceiling is not a view of remaining monthly credits; the credit dashboard was not accessed. No further broad API fan-out is needed until these results are reviewed.

## Current-feed snapshot finding

The accessible production `data/current_source_manifest.json` is dated **2026-10-08 04:32:49 UTC**, with requested dates 1–10 October. It is stale for a 28 October live run. The CSV is an existing staging snapshot, not a current validated feed. The current ingestion code admits rows by display league name before recording `league_id`; this is the confirmed cross-competition identity defect. I did not refresh through that unsafe name-only path and did not change production code.

## Gate-by-gate status

| Gate | Status | Next action |
|---|---|---|
| Selected-50 archive inventory | OBSERVED; not completeness proof | Preserve historical/feature counts with provenance limits |
| FootyStats selected season identities | PASS as provider evidence | Obtain formal semantics for `comp_master_id`; no automatic canonical promotion |
| FootyStats current schedule source | PASS as retrieval | Validate full pagination and schedule/season semantics before treating as complete |
| FotMob current-feed freshness | FAIL / STALE | Obtain a fresh staging snapshot only after an approved ID/country allowlist prevents name-only admission |
| FootyStats → FotMob bridge | 0 approved; 2 candidates | Human-review candidate evidence, including pre-kickoff timing |
| Exact fixture/team joins | PARTIAL evidence only | Resolve canonical competition/team IDs and kickoff provenance; do not use date-only joins as settled truth |
| Official settlement truth | NOT VERIFIED | Verify final status/score from authoritative match-level sources and exclude non-complete 0–0 placeholders |
| Combo market | BLOCKED | Keep probabilities masked until predictor/settlement contract and canonical joins reconcile |
| Calibration / betting evidence | NOT APPROVED | Temporal calibration and verified odds/ROI methodology still required |
| Production model/governance | UNCHANGED | No model logic, probabilities, thresholds, calibration, registry or ledgers changed |

## Immediate execution plan

1. Keep the 50 observed `comp_master_id` values as provider-side evidence only; do not write them to the protected canonical registry.
2. Review the two FotMob bridge candidates against source IDs, country/category and match timestamps. They remain unapproved.
3. Do not re-run the unsafe current-ingestion workflow. Build and test the reviewed allowlist gate in research/staging first; unknown or ambiguous IDs must be quarantined.
4. Use the current-feed source manifest only as historical provenance for the stale snapshot, not as proof of live freshness.
5. Re-run exact fixture/team/settlement checks after approved IDs and a fresh staging manifest are available.
6. Publish the final matrix with separate columns for historical archive, current source freshness, provider identity, exact join, market readiness and production eligibility.

## Governance confirmation

Research-only artifacts and workflows were used. No raw provider payload or API key was retained in the report. The production model, protected 27-league registry, probabilities, calibration, thresholds, ledgers and governance were not modified. Production and betting eligibility remain **NOT GRANTED**.

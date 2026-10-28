# Oracle Selected-50 Post-Deadline Execution Checkpoint — 2026-10-28 12:15 SAST

## Executive summary

The noon target has passed. The team has made material progress on identity evidence, but mandatory release gates remain open. **Decision: NO-GO for production predictions and betting release.** Continue research-only remediation without changing production scoring logic or guessing identifiers.

## New completed work since the 07:50 checkpoint

### 1. FootyStats identity probe completed successfully

Actions run [40562430790, attempt 6](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790) completed successfully after the approved bounded probe. The probe made exactly 50 sequential requests to the `league-season` endpoint (one per selected season ID), no retries.

- HTTP 200 + provider success: 50/50
- Requested season ID matches returned `id`: 50/50
- Country/name checks align to the selected manifest: 50/50
- Non-null `comp_master_id`: 50/50
- Distinct observed `comp_master_id`: 50
- Country mismatches: 0

This establishes **provider-side identity evidence**, not approved Oracle canonical mappings. FootyStats API overview exposes `comp_master_id` as a field but does not define it precisely enough in the public documentation available here to equate it to an Oracle canonical ID. Values remain research-only and are not written into the protected registry.

### 2. Exact cross-provider fixture audit completed

Research run [40646418126](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126) passed and produced artifact [12797871592](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126/artifacts/12797871592).

Audit findings:
- 50 selected seasons inspected against the existing private FootyStats archive and current FotMob snapshot.
- 14,051 FootyStats archive rows inspected.
- Current FotMob snapshot has 71 rows.
- 10 exact normalized ordered-team-pair + UTC-kickoff join rows total, across only 2 selected leagues.
- 2 FotMob bridge candidates require human review:
  - Canada — Canadian Premier League, FootyStats `comp_master_id=524`, FotMob league ID candidate `1000001192`; four exact fixture joins, three score agreements, one pre-kickoff snapshot row; **quarantine until source-status/score provenance is resolved**.
  - England — EFL League One, FootyStats `comp_master_id=6`, FotMob league ID candidate `938219`; six exact fixture joins, three score agreements, no pre-kickoff row in these candidates; **human review still required**.
- Approved canonical bridges: 0.
- Exact historical Oracle ledger fixture joins: 0.
- 24 selected seasons have date-only overlap, which is not enough for a valid join.
- Production eligibility remains false.

### 3. 50-row matrix updated

The selected-50 matrix now adds observed FootyStats `comp_master_id`, any FotMob bridge evidence, and current-feed freshness status for each selected league. The two candidate IDs are explicitly marked review-required, not approved. The other 48 have no verified FotMob bridge in this audit.

[Open the updated 50-league readiness matrix](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-league-readiness-matrix-2026-10-27.md)

## Gate status

| Gate | Status | Decision evidence |
|---|---|---|
| Research tests and runtime | PASS | Latest safety, runtime, dry-run and exact cross-provider audit runs succeeded |
| FootyStats season identity | PASS for provider response validation | 50/50 recognized; parent/master field semantics still not approved as Oracle canonical ID |
| FotMob/current-feed freshness | FAIL | Accessible manifest generated 2026-10-06 07:49:26 UTC; last requested date 2026-10-08; no newer authoritative manifest verified |
| Canonical league bridges | FAIL | 0 approved; 2 candidates require human review; 48 no verified FotMob bridge |
| Exact fixture/team/settlement | FAIL | 10 exact cross-provider candidate joins across 2 leagues only; 0 exact joins to the Oracle historical ledger; settlement truth not comprehensively verified |
| Combo market | FAIL / MASKED | Settlement contract disagreement unresolved |
| Production and betting release | **NO-GO** | Required identity, freshness, fixture and settlement gates are not all satisfied |

## Current-feed refresh investigation

The production workflow `.github/workflows/oracle_current_data.yml` is configured to run at 04:20 UTC and can be manually dispatched. However, it calls `scripts/ingest_current_fotmob.py`, which filters incoming FotMob competitions by display name (`league_name in TARGET_LEAGUES`) rather than a reviewed exact league-ID + country/category allowlist. It then commits staging files to production `main`. It is therefore **not safe to use as an emergency refresh path** before an identity guard is reviewed and approved.

Latest visible production runs for current data, live prediction, live settlement and autonomous expansion are failures; the accessible manifest remains stale. A fresh staging refresh must be isolated from production and must enforce an approved identity allowlist before accepted rows are emitted.

## Immediate next actions

1. Obtain authoritative semantics for FootyStats `comp_master_id` and document whether it is a competition master key, not an Oracle canonical key.
2. Review the two FotMob bridge candidates against an authoritative league catalogue, country/category and full match evidence. Resolve Canada's pre-kickoff snapshot row before any approval.
3. Build a reviewed 50-row FotMob league-ID + country/category allowlist from authoritative evidence. Do not infer IDs from display names or from FootyStats IDs.
4. Implement a research-only current-feed refresh that writes to a research artifact, records requested dates and per-request hashes, rejects unknown IDs, and never pushes to production `main`.
5. Reconcile fixture IDs, team IDs, UTC kickoff, status, score, and settlement truth; keep ambiguous rows quarantined.
6. Once gates pass, request a separate production change review; do not automatically promote research outputs.

## Governance and budget

- The bounded FootyStats probe used 50 requests, within the user-stated 1,800 requests/hour ceiling. That ceiling does not independently verify remaining monthly credits.
- No further FootyStats requests are required for the immediate next step; existing archive and probe evidence should be used first.
- Research branch only. No production repository files, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers or governance changed by this checkpoint.

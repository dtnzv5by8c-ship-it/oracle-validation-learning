# Project Oracle — Verified Progress Checkpoint

Checkpoint date: 2026-10-31
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Governed branch: research/oracle-50-league-readiness-audit
Checkpoint commit before this record: ba483e7db1b6c25255b1b6dc21d866e41438cb60

## Latest verified Market Intelligence rebuild

- Workflow: Oracle Selected-50 Market Intelligence Report Repair
- Run number: 124
- Run ID: 41229773531
- Event: workflow_dispatch
- Status/conclusion: completed / success
- Runtime checkout commit: ba483e7db1b6c25255b1b6dc21d866e41438cb60
- Artifact: oracle-selected50-market-intelligence-repair
- Artifact ID: 13053167426
- Artifact SHA-256: 429019182bc4f522ff7035f5dd574814325d1431ef67388a8588d817f455c396
- Artifact size: 1,106,692 bytes
- Retention expiry: 2026-11-14T18:31:29Z
- Run URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41229773531
- Artifact URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41229773531/artifacts/13053167426

## Verified job execution

All report job steps completed successfully, including:
1. Checkout of the governed research branch at the exact checkpoint commit.
2. Explicit read-only archive confirmation and existing private token check.
3. Download and SHA-256 verification of pinned private archive release `research-selected50-footystats-history-40375285207`.
4. Runtime run/artifact/branch/commit/digest provenance checks.
5. Exact-join, chronology, duplicate guard and market masking tests.
6. Archive-wide feature audit and pinned archive coverage verification.
7. Research-only goal-market estimates and chronological backtest.
8. Rebuild of the locked 38-column report and QA gates.
9. Upload of workbook, CSV, QA, evidence trace, join quarantine, schedule queue, xG audit, archive summary and goal-market research outputs.

Test results:
- Selected-50 Market Intelligence test suite: 20 passed.
- Goal Market Research Engine test suite: 6 passed.
- Pinned archive digest matched; 59,049 match records, 200 season folders, zero parse errors, zero provider API calls.

## Report QA

- Runtime fixture rows: 434.
- Report fixture rows: 434.
- Selected league groups: 50.
- Exact archive joins: 434.
- Unmatched or quarantined report joins: 0.
- Duplicate archive composite keys: 0.
- Locked schema: PASS_38_COLUMNS.
- League group gate: PASS.
- Required join gate: PASS.
- `production_eligible=false`.
- `betting_eligible=false`.

This is a successful report build and evidence-integrity check, not a declaration of 50-league production readiness.

## Research-only goal-market findings

434 forecast rows: 422 forecastable and 12 explicitly blocked by `BLOCKED_LEAGUE_BASELINE_LT20`.

Backtest (n=46,687):
- Over 1.5: Brier 0.19001 vs league baseline 0.18982 (worse).
- Over 2.5: 0.24821 vs 0.24741 (worse).
- Under 4.5: 0.11768 vs 0.11784 (slightly better Brier; log loss 0.39740 vs 0.39729, worse).
- Home Over 1.5: 0.24119 vs 0.24542 (better).
- Away Over 1.5: 0.21778 vs 0.22032 (better).
- All statuses: UNCALIBRATED_RESEARCH_ONLY.

Do not promote or merge these experimental estimates into Oracle V1.6.

## Carried-forward blockers and controls

- xG: numeric values exist but capture timestamps/revision provenance are not verified; keep quarantined and ineligible.
- Schedule discrepancies: preserve REVIEW_REQUIRED; no automatic kickoff correction.
- League positions: provisional conventional-table calculation; competition-specific rules and tie-breaks remain unverified.
- Cross-season H2H verification remains incomplete.
- Historical model accuracy/calibration/profitability remains unvalidated without immutable pre-match predictions, official settlements and contemporaneous odds.
- FootyStats snapshot approval was limited to one 50-request snapshot and has been consumed. No additional API calls without fresh explicit approval.
- OpenFoot must not be removed until all dependent workflows have been replaced and tested with OpenFoot disabled.
- Main and governed research branches previously showed substantial divergence. Do not merge/rebase/synchronize wholesale without path-level review.

## Continuity / next steps

1. Start future weekly reporting from the locked template v1.2 and existing generator; never rebuild manually.
2. Preserve the 12-tab workbook contract, 38-column Oracle V1.6 output and 83-column Market Intelligence view.
3. Continue field-level evidence/readiness audit for the Selected-50 universe; this run validates 50 league groups in the report, not every field/market for every league.
4. Keep all research outputs separate from production and betting eligibility.
5. Resolve schedule, xG provenance, league-table rules, canonical league/team identity mappings and OpenFoot dependencies in isolated, testable changes.
6. Keep Oracle V1.6 production logic, thresholds and probabilities unchanged.
7. User manually dispatches governed report workflow per execution protocol; do not claim autonomous or background runs.

## Canonical references

- Template: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/templates/ORACLE_MARKET_INTELLIGENCE_TEMPLATE_V1.md
- Field dictionary: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/docs/ORACLE_MASTER_INTELLIGENCE_DATA_DICTIONARY_V1.md
- Continuity lock: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/docs/ORACLE_MASTER_INTELLIGENCE_CONTINUITY_LOCK.md
- Execution protocol: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/docs/PROJECT_ORACLE_EXECUTION_PROTOCOL.md

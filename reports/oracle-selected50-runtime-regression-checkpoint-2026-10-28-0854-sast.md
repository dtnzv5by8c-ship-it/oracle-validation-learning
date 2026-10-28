# Selected-50 Runtime & Regression Checkpoint — 2026-10-28 08:54 SAST

## Decision

**Research runtime and regression QA: PASS. Production release: NOT APPROVED. Betting release: NOT APPROVED.**

This checkpoint records a reporting-only cross-provider audit correction, successful regression validation, and independent inspection of the latest generated artifacts. No provider API calls were made. The private archive tag remains `research-selected50-footystats-history-40447419806`; the archive checksum guard passed.

## Branch and commits

- Branch: `research/oracle-50-league-readiness-audit`
- Branch head before this checkpoint: `964d962024c9e02f3cdf5a2703a8b4d44b96674b`
- Fix commit: [`964d962024c9e02f3cdf5a2703a8b4d44b96674b`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/964d962024c9e02f3cdf5a2703a8b4d44b96674b)
- Fix scope: `scripts/audit_selected50_cross_provider_fixture_joins.py` and `tests/test_selected50_cross_provider_fixture_joins.py` only.

## Evidence: latest workflow runs

| Workflow | Run ID / number | Tested commit | Result | Artifact |
|---|---:|---|---|---|
| Selected-50 Research Runtime | [40646418147 / #147](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418147) | `964d962024c9e02f3cdf5a2703a8b4d44b96674b` | PASS | [12797526943](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418147/artifacts/12797526943) |
| Selected-50 Dry-Run Planner | [40646418143 / #512](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418143) | same | PASS | [12797517430](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418143/artifacts/12797517430) |
| Safety Contract Tests | [40646418166 / #214](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418166) | same | PASS | no artifact |
| Exact Cross-Provider Fixture Join Audit | [40646418126 / #15](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126) | same | PASS | [12797871592](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126/artifacts/12797871592) |

All workflow job steps completed successfully. Runtime Run #147 passed archive access/checksum, Combo target tests, feature/training support tests, isolated runtime build, output validation, and artifact upload.

### Artifact SHA-256

- Runtime #147, artifact #12797526943: `cd281b5dd35656815879ba546ffb860bd1db75cc8daeca6db3373bb777ba16db`
- Dry-run #512, artifact #12797517430: `d1e3890965ddb633997142e3582ebca70f97f9f573df1361ea27c7cfacab4342`
- Cross-provider #15, artifact #12797871592: `f9efee081b0a01e5f5cb98b5ff0632e733906373fd933a5d901a62c0ff3047e8`

Each ZIP was downloaded, independently SHA-256 hashed, and inspected; each digest matches GitHub artifact metadata.

## Evidence-backed defect corrected

Safety Contract Tests Run #213 (ID `40645975218`) failed in `test_pre_kickoff_snapshot_is_not_counted_as_settlement_conflict`: the test expected Python `None` after reading a CSV, but CSV serializes `None` as an empty field. This obscured the intended meaning of a pre-kickoff snapshot's status comparison.

The research audit now emits explicit `NOT_COMPARABLE_PRE_KICKOFF` in `status_agree`. The regression test asserts this sentinel, verifies the candidate is not marked `_SOURCE_CONFLICT`, and retains the zero-conflict assertion. Safety Run #214 passes; the cross-provider audit output also shows the explicit sentinel. No canonical bridge is approved by this change.

The cross-provider artifact comparison shows the only data-column change from Run #14 to Run #15 is this one `status_agree` field on the pre-kickoff row. All other CSV outputs are unchanged; summary changes are limited to generated timestamp.

## Required Combo and feature-support regressions

- Combo predictor-target contract: **5/5 passed** in Runtime #147.
- Feature/training support diagnostics: **5/5 passed** in Runtime #147.
- Combo settlement-governance tests: **3/3 passed** in Dry-Run #512.
- Cross-provider join tests: **7/7 passed** in Safety Run #214.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Dry-run network calls: 0; paid-provider calls: 0.

### Combo semantics remain unresolved

- Research predictor: Double Chance AND total goals **2–4 inclusive**.
- Existing settlement helper: Double Chance AND total goals **<5**, including 0–1 goals.
- Home Combo disagreement: 0–0 and 1–0.
- Away Combo disagreement: 0–0 and 0–1.

The 121-scoreline diagnostic is `DIAGNOSTIC_ONLY_NOT_A_MARKET_DEFINITION_APPROVAL`. Both Combo probability columns remain blank in every prediction and governed fixture row. Do not unmask them without an authoritative market definition, canonical fixture/team joins, and official settlement truth.

## Runtime artifact inspection

Runtime #147 artifact #12797526943 contains 14 files; SHA-256 matches the digest above. The prediction and governed reports each contain 463 rows and 463 unique fixture IDs. Their fixture ID sets match.

- Selected league groups: 50.
- Historical seasons loaded: 200.
- Deduplicated historical records: 59,049.
- Explicitly completed historical records: 51,983.
- Upcoming fixture rows: 463.
- Fixtures with at least one raw research-market prediction: 438.
- Fixtures blocked by required features: 25.
- Fixtures blocked by unavailable training: 0.
- League-market readiness rows: 250.
- League-market walk-forward rows: 750.
- Combo probability values remaining in exports: 0.
- Production-eligible fixture rows: 0.

An exact fixture-ID comparison between Runtime #146 and #147 found the same 463 IDs and exact equality of BTTS, DC_HOME, DC_AWAY, COMBO_HOME and COMBO_AWAY probability fields. The code change did not alter runtime probabilities.

## Historical 26-row blocker reconciliation

Run #112 artifact #12757295232 contained 461 fixtures and 26 rows with the generic feature/training block. Runtime #147 contains 463 fixtures and 25 rows classified `BLOCKED_MISSING_REQUIRED_FEATURES`, with zero training-gate failures.

The current 25 blocked IDs equal the Run #112 blocked IDs after removing fixture `8614496`, Vicenza–Modena, scheduled for 2026-10-27 19:00 UTC. It has left the future-fixture horizon; this is not a model improvement.

Current blocked IDs:
`8614468, 8614546, 8572270, 8572687, 8548576, 8550587, 8557813, 8558098, 8562297, 8568598, 8572538, 8572559, 8572597, 8572852, 8573896, 8583531, 8584398, 8614227, 8620732, 8623411, 8623413, 8562283, 8573871, 8614510, 8604050`.

- Insufficient prior home matches: 16 fixtures.
- Insufficient prior away matches: 10 fixtures.
- Both sides below five-match minimum: 1 fixture (overlap).
- Home-only blocks: 15; away-only blocks: 9; both-sides block: 1.
- Feature coverage: 35% for 24 fixtures; 0% for one fixture.
- Every blocked fixture has `PASS_ALL_MARKET_MODELS`; each market reports 44,568 eligible training rows.

The five-completed-match home/away history requirement remains unchanged. No features were imputed or fabricated.

## Cross-provider evidence and remaining gates

The latest cross-provider audit reports 10 exact FootyStats–FotMob joins across two candidate groups (four Canadian Premier League, six England EFL League One), one pre-kickoff snapshot row, zero source-conflict rows, 577 date-only historical-ledger overlaps, zero exact historical-ledger joins, and zero approved canonical bridges. The Canada candidate still uses the observed FotMob label “Premier League” and remains human-review-only.

The existing source manifest was generated `2026-10-06T07:49:26Z`; it is stale. Current-feed evidence remains insufficient for a governed slate.

- Parent competition IDs verified: **0/50**.
- Approved provider-season-to-current-feed bridges: **0/50**.
- Canonical fixture joins verified: **0**.
- Canonical team joins verified: **0**.
- Official settlement truth verified: **0**.
- Current governed fixture rows emitted: **0**.
- Production and betting eligibility: `NOT_GRANTED`.

The Selected-50 runtime is a research/challenger pipeline. Its output contract does not certify canonical identity, official settlement truth, or point-in-time provenance. Raw walk-forward metrics remain uncalibrated; no odds/ROI benchmark is approved.

## Change boundary

No provider API calls were made. The research-only cross-provider audit and regression test were the only code changes. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, protected registry, ledgers, and governance remain unchanged.

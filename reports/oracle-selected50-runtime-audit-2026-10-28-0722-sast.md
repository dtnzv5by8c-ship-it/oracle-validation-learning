# Selected-50 Runtime Audit — 2026-10-28 07:22 SAST

## Decision

**Research runtime/output QA: PASS. Production release: NOT APPROVED. Betting release: NOT APPROVED.**

This is a documentation-only checkpoint. No runtime code defect requiring a change was found in this audit. No provider API calls were made. Production Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers, and governance remain unchanged.

## Live branch and latest workflows

Branch: `research/oracle-50-league-readiness-audit`

- Branch head before this checkpoint: `48dec28ac493a206c8ef5f1394508c15bd4d9472`
- Latest runtime-tested code commit: `f149d0656f7c72ebd0dc7080603516ddee106832`
- Latest planner/safety/archive-audit code commit: `b2a4f7998ba95950929a0610d3a4b3e264d1c0f7`
- Compare from runtime-tested commit to pre-checkpoint branch head: four commits ahead; only two workflow files and two Markdown reports changed. No runtime script, probability logic, thresholds, calibration, canonical registry, or ledger changed.

| Workflow | Run ID / number | Tested commit | Result |
|---|---:|---|---|
| Selected-50 Research Runtime | [40633725121 / #125](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633725121) | `f149d0656f7c72ebd0dc7080603516ddee106832` | PASS |
| Selected-50 Dry-Run Planner | [40633801419 / #479](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801419) | `b2a4f7998ba95950929a0610d3a4b3e264d1c0f7` | PASS |
| Safety Contract Tests | [40633801353 / #173](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801353) | `b2a4f7998ba95950929a0610d3a4b3e264d1c0f7` | PASS |
| FootyStats Archive Feature Audit | [40633801455 / #62](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801455) | `b2a4f7998ba95950929a0610d3a4b3e264d1c0f7` | PASS; 207 tests |

The runtime's private archive guard passed and retained tag `research-selected50-footystats-history-40447419806`; the downloaded archive checksum check passed. No provider API calls were made.

## Artifact integrity and inspection

The ZIPs were downloaded, independently SHA-256 hashed, and inspected. Each local digest matches the GitHub artifact metadata.

| Evidence | Artifact | Files | SHA-256 |
|---|---|---:|---|
| Runtime #112 historical comparison | [12757295232](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232) | 14 | `983a4f3cc09dcb94ab03e7693bc65ad46ed23cf4cdd2d92d05f543a75cfdbf50` |
| Runtime #120 comparison | [12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212) | 14 | `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84` |
| Latest runtime #125 | [12792931105](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633725121/artifacts/12792931105) | 14 | `e07d12177fdb96ffd217c5a955d95cecfb74ca443ab86bd423943a6ee234d9d9` |
| Latest dry-run #479 | [12792208906](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801419/artifacts/12792208906) | 25 | `bc9929206d4a61dddb13b1d74493c30891053d8fb112eb7f0ab91568c04c6950` |
| Latest archive audit #62 | [12792058856](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801455/artifacts/12792058856) | 547 | `276aac82af03db7d3b2b4e43a13699526e547ca6f705262d1a008ff9d8e37f75` |

## Required regression tests and output contract

- Runtime Combo predictor-target contract: **5/5 passed**.
- Runtime feature/training support diagnostics: **5/5 passed**.
- Dry-run Combo settlement-governance regression tests: **3/3 passed**.
- Safety workflow logs: 22 bounded-probe tests, 17 score/settlement tests, 7 current-feed identity-contract tests, and 2 offline staging-adapter tests passed.
- Archive feature audit: **207 tests passed**.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Dry-run planner: zero network calls and zero paid-provider calls.

The three Combo settlement tests confirm (1) the 121-scoreline grid is complete and diagnostic-only, (2) the disagreements are exactly the low-goal scorelines, and (3) the market crosswalk keeps both Combo markets blocked.

## Historical 26-row blocker reconciliation

Run #112 artifact #12757295232 contains 461 fixture rows and 26 rows marked `NO_PREDICTION_FEATURE_OR_TRAINING_GATE`. Run #125 artifact #12792931105 contains 463 rows and 25 rows marked `BLOCKED_MISSING_REQUIRED_FEATURES`, with **zero training-gate failures**.

The exact reconciliation was independently checked:

- The 25 currently blocked fixture IDs in Run #125 match the 25 blocked IDs from Run #112 after removing fixture `8614496`.
- Fixture `8614496`, Vicenza–Modena, was scheduled for 2026-10-27 19:00 UTC and has left the future-fixture horizon. This is a rolling-horizon change, not a model improvement.
- Run #125 has 463 unique fixture IDs in each fixture export, with identical ID sets.
- The 25 remaining blocks are all `BLOCKED_MISSING_REQUIRED_FEATURES`; all 463 rows pass the five-market model-training support check.
- Per blocked fixture, eligible training support is 44,568 rows for each market: BTTS, DC_HOME, DC_AWAY, COMBO_HOME, and COMBO_AWAY.
- Insufficient prior home matches: 16 fixtures; insufficient prior away matches: 10; both sides below the five-match minimum: 1 (overlap).
- Therefore: 15 home-only blocks, 9 away-only blocks, 1 both-sides block. Coverage is 35% for 24 rows and 0% for the both-sides block.

The runtime requires at least five completed matches in the relevant home/away orientation strictly before kickoff. It correctly leaves unsupported features missing; do not impute or relax this requirement.

## Runtime output comparison

Runtime #120 and #125 were joined by exact fixture ID:

- 460 overlapping fixture IDs; three new fixture IDs in #125 (Internacional–Coritiba, Millonarios–América de Cali, Alianza Lima–Cienciano).
- BTTS, DC_HOME and DC_AWAY probability fields were exactly equal across all 460 overlapping fixtures, including nulls.
- Both Combo probability fields remained null in every overlapping row and throughout the full #125 export.
- Latest runtime #125: 463 fixture rows, 438 with at least one raw research-market prediction, 25 feature-blocked, zero training-blocked; all rows production-ineligible.
- Readiness matrix: 250 unique league-market rows. Walk-forward metrics: 750 unique league-market-fold rows.

## Combo target vs documented settlement semantics

The target does **not** match the current settlement helper.

- Research predictor and crosswalk target: Double Chance AND total goals between 2 and 4 inclusive.
- Settlement helper `scripts/settle_market_from_final_score.py`, for selections `HOME_1X_U45` and `AWAY_X2_U45`: Double Chance AND total goals ≤ 4, equivalent to Under 4.5 with no lower bound.

The mismatch is at Home Combo scores 0-0 and 1-0, and Away Combo scores 0-0 and 0-1. The three settlement-governance tests and five predictor-target tests pass by keeping this mismatch explicit. They do not establish official bookmaker settlement truth. The crosswalk itself says `OFFICIAL_SETTLEMENT_RULES_NOT_VERIFIED` and requires the authoritative target to be confirmed.

Both Combo probability columns are blank in both runtime exports; Combo remains blocked until the market owner confirms the definition and canonical fixture/team joins plus official settlement truth are verified. Do not silently change the predictor or helper and do not unmask Combo probabilities.

## Remaining release gates

- Provider parent competition IDs verified: **0/50**.
- Approved provider-season-to-current-feed bridges: **0/50**.
- Canonical fixture joins verified: **0**.
- Canonical team joins verified: **0**.
- Official settlement truth verified: **0**.
- Current-feed governed fixture slate: **0 rows**; the dry-run snapshot reports last fixture date 2026-10-17 and schedule-window end 2026-10-22.
- Provider catalogue ID field: 43 rows, all blank; archive manifest provider ID field: 126 rows, all blank.
- xG/odds point-in-time provenance: unverified; no odds/ROI benchmark approved.
- Raw BTTS holdout accuracy: 53.588% vs majority-class baseline 54.143%; raw and uncalibrated.

**Next useful action:** resolve authoritative league identity and settlement policy from existing evidence; do not refresh through the legacy display-name-only ingestion path. The offline staging adapter is tested but has not been executed against a real current-feed source snapshot. No source snapshot was fabricated.

## Change boundary

No runtime code changes were made in this checkpoint; no provider API calls were made. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.

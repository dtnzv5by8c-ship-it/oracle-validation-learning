# Selected-50 Snapshot Contract Hardening & Runtime Evidence — 2026-10-28 17:24 SAST

## Decision

**Research-only snapshot validation hardened and validated in public CI. Runtime baseline remains PASS. Production and betting release remain NOT_GRANTED.** No provider API calls were made by this task, no private-repository Actions were run, and no production repository was written.

## Evidence read before editing

- Canonical handover: `PROJECT_ORACLE_CANONICAL_HANDOVER.md`, current through Section 61.
- Latest detailed runtime audit: `reports/oracle-selected50-runtime-audit-2026-10-28-1118-sast.md`.
- Snapshot/runtime reconciliation: `reports/oracle-selected50-snapshot-runtime-coverage-2026-10-28.md`.
- Latest invalid-score quarantine report: `reports/oracle-selected50-invalid-score-quarantine-2026-10-28-1622-sast.md`.
- Live branch before this documentation checkpoint: `59e41259c4bf014d2dc94fa9ada7e8e792b089f8`.

## Concrete defect and fix

The current-fixture snapshot workflow uploads its sanitized JSON after running `scripts/validate_selected50_current_fixture_snapshot.py`. That validator previously checked top-level counts, IDs, required non-empty fields, and release guards, but did not verify the chronology and numeric integrity of the actual fixture rows. An invalid or timezone-naive kickoff, a `date_unix`/ISO kickoff mismatch, a wrong window class, or a completed-status row with invalid/missing scores could therefore pass the snapshot publication contract.

The research-only validator now fails closed on:
- Missing, malformed, timezone-naive or out-of-window retrieval/window timestamps.
- A window that is not the declared 30-days-back plus 14-days-forward interval.
- Missing, malformed or timezone-naive kickoff timestamps.
- Kickoffs outside the declared snapshot window, or `window_class` inconsistent with the kickoff and declared boundary.
- `date_unix` values that are not finite non-negative integer timestamps or differ from the UTC kickoff by more than one second.
- Nonblank scores that are fractional, negative, non-finite or Boolean.
- Completed-status rows without two valid integer scores, or whose kickoff is later than snapshot retrieval.

Valid integer-valued decimal score strings and genuine 0–0 scores remain valid. This is a source-integrity contract only; it does not turn provider status/score into official settlement truth.

Updated `tests/test_selected50_current_fixture_snapshot.py` with 17 tests covering the existing snapshot contract plus timestamp provenance, epoch consistency, declared-window chronology, score validation and completed-status chronology. Updated `.github/workflows/oracle_identity_resolver_tests.yml` to compile the validator, trigger on these files, and run the current-snapshot validator suite offline.

## CI validation on the changed code

The code/test/workflow commit is `59e41259c4bf014d2dc94fa9ada7e8e792b089f8`. All three relevant public workflows completed successfully on that exact commit:

| Workflow | Run | Result | Evidence |
|---|---:|---|---|
| Identity & Settlement Evidence Tests | #15 / `40716236591` | PASS — 82 tests across six suites | [Run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40716236591) |
| Selected-50 Dry-Run Planner | #538 / `40716236615` | PASS — 64 tests across its offline suites | [Run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40716236615) |
| Selected-50 Safety Contract Tests | #240 / `40716236614` | PASS — 69 tests across its offline suites | [Run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40716236614) |

The new current-fixture snapshot validator suite passed **17/17**. The identity workflow also passed evidence-register (10), resolver (7), adapter (15), feature-blocker (15), and snapshot/runtime coverage (18) suites. The dry-run and safety workflows are offline; their logs include no provider-call execution. The manual-only snapshot workflow was not rerun.

### Artifact integrity

Downloaded/extracted artifacts were independently hashed; all calculated SHA-256 values match GitHub artifact metadata.

| Artifact | ID | SHA-256 |
|---|---:|---|
| Identity/settlement #15 | 12829290375 | `821774c27cadc5d28467aa187b55cb2411884b23f94ff8f68c84f075c3bbfe23` |
| Dry-run #538 | 12826679966 | `ed863e3075a3dbd8f54d3f8a5967ee8bc86104e34df6d908617e5cab63afada2` |
| Runtime #155 | 12825172425 | `381adbf7840708b0f69b3b1310c3ed79c4606949d05091b074d93560ddfd5a4a` |
| Current snapshot #1 | 12825256201 | `3d94f60e12bd3a606af74f1bac87b4aa81a81f7a2d7bab515ee0a5e449f68fa5` |

Artifact links:
- [Identity/settlement artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40716236591/artifacts/12829290375)
- [Dry-run artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40716236615/artifacts/12826679966)
- [Runtime artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40708378185/artifacts/12825172425)
- [Current snapshot artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40708750173/artifacts/12825256201)

## Latest runtime output inspected

The latest runtime remains Run #155, started at `2026-10-28T14:41:07Z` on source commit `38cd37ad868337160869d50cd92ad12f9c1cfd7c`. Runtime code was not changed by the snapshot-validator commit, so the unchanged runtime was not rerun.

- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- 50 selected groups; 462 unique fixture rows in both exports.
- 437 rows have at least one raw research-market output.
- 25 rows are blocked by missing required features; zero are blocked by unavailable model training.
- 250 league-market readiness rows and 750 league-market walk-forward rows.
- Zero production-eligible rows.
- Combo probability columns remain blank; the artifact reports zero visible Home/Away Combo probabilities.

The earlier 26-row blocked set has reconciled to 25 as the rolling fixture horizon changes. Current diagnosis remains 26 side-history gaps: 16 home-side and 10 away-side, with one fixture in both groups. All affected sides have three or four qualifying venue-specific matches; all five market models have training support. The five-match rule remains unchanged. No feature was imputed and no prediction was fabricated.

## Existing current snapshot reviewed (not requested by this task)

The already-completed public workflow [Current Fixture Snapshot #1](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40708750173) and its artifact were inspected; this task did not dispatch the workflow or make provider calls. The workflow log confirms 50 planned/attempted requests, 50 HTTP-200 provider successes, zero request failures, and the sanitized artifact reports 2,250 rows: 869 future-14-day rows and 1,372 recent completed-30-day rows. The artifact also records 486 `no_home_away` rows, 19 suspended rows, no persisted raw provider payload/API key, no production ledger write, and `NOT_GRANTED` production/betting eligibility.

The snapshot retrieval timestamp is `2026-10-28T14:44:00.366308Z`; Runtime #155 started at `14:41:07Z`, so this snapshot was captured **173.37 seconds after runtime start**. It must not be used as evidence that the snapshot was available to Run #155. The existing snapshot/runtime audit correctly fails closed for this chronology. An independent inspection found no violation of the new timestamp, window-class, epoch-consistency or completed-score checks in the downloaded snapshot, but this snapshot remains FootyStats-native evidence—not a canonical FotMob/Oracle feed and not official settlement truth.

## Unresolved gates

- Canonical competition bridges approved: 0/50.
- Canonical fixture/team joins verified: 0.
- Official settlement truth verified: 0.
- Point-in-time xG/odds provenance verified: 0.
- Combo predictor target remains Double Chance AND 2–4 total goals inclusive; settlement helper remains Double Chance AND total goals <5, including 0–1 goals. The 121-scoreline diagnostic identifies Home Combo disagreements at 0–0 and 1–0, and Away Combo at 0–0 and 0–1. Preserve masking.
- The 25 feature-blocked fixtures remain blocked until valid prior home/away history is available.

The cross-provider audit is unchanged at Run #15 (`40646418126`); its implementation and tests were not modified, so it was not rerun. The new snapshot is not substituted for the stale FotMob current feed.

## Safety

No provider API calls were made by this task. No private-repository Actions, private archive reads, production repository writes, or production model changes were performed. The existing snapshot run described above predates this task. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, protected registry, ledgers and governance remain unchanged.

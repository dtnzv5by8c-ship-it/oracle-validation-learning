# Selected-50 Feature-Blocker Diagnostics — 2026-10-28 15:23 SAST

## Decision

**Research-only diagnostics implemented and locally validated. The 25 feature blocks remain valid under the existing five-match home/away rule. A workflow safety mismatch was also corrected in this change. Production and betting release remain NOT_GRANTED.**

## Reproducible input

- Runtime run: [#154 / 40687715830](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715830)
- Runtime artifact: [#12816016919](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715830/artifacts/12816016919)
- Runtime-tested commit: 48ee494b8fc6802d2b086793420f90681179fc61
- Artifact ZIP SHA-256: b7fb063b5d5f6b1e41b10930114468497fdd04cd2881bd56dd2e8ddb8e5bdb66
- Input file: oracle_selected50_governed_fixture_report.csv

## Diagnostic results

| Measure | Result |
|---|---:|
| Runtime fixture rows | 463 |
| Unique fixture IDs | 463 |
| Fixtures blocked by missing required features | 25 |
| Missing side-history rows | 26 |
| Home-side gaps | 16 |
| Away-side gaps | 10 |
| Fixtures with both sides below minimum | 1 |
| Blocked side rows with 3 or 4 qualifying oriented matches | 26 |
| Rows with count >=5 but side features still missing | 0 |
| Rows with unknown oriented-history count | 0 |
| Fixtures failing all-market training support | 0 |
| Visible Combo probabilities | 0 |

The 25 blocked fixtures resolve to 25 season-scoped provider-team keys across 26 side gaps. Arezzo (provider team ID 2335 in selected season 17404) appears in two different fixtures: one home-side gap and one away-side gap, each with four qualifying oriented matches. This key is source-scoped diagnostic evidence only, not a canonical team mapping.

## Interpretation and limits

All 26 affected team-side histories have runtime-reported counts of three or four. No blocked side has a count of five or more while its side-form features remain missing. This is evidence against a feature-builder contradiction in these 25 rows; the current gate is consistent with the reported counts.

The script does not reconstruct the underlying historical match lists or prove why each history count is low. It copies the counts and missing-feature names from the runtime report. It does not map teams by normalized display name, borrow prior-season identities, impute features, create predictions, or grant production eligibility.

The script refuses to run if either Combo probability column is nonblank. The predictor/settlement mismatch remains unresolved: predictor = Double Chance plus 2–4 goals inclusive; settlement helper = Double Chance plus fewer than five goals. Official market semantics and official settlement truth remain unverified.

## Workflow safety correction

The canonical handover stated that the research runtime was manual-dispatch-only, but the live workflow still contained a push trigger that could read the existing private archive on qualifying code pushes. This change removes that push trigger and adds a regression test. The runtime workflow now requires an explicit manual dispatch with private-archive confirmation and the governed archive tag.

## Code and validation

- New script: scripts/diagnose_selected50_feature_blockers.py
- New tests: tests/test_selected50_feature_blocker_diagnostics.py
- Local unit tests: 15/15 passed, including the manual-only workflow guard.
- Diagnostic status: PASS_RESEARCH_ONLY_FEATURE_BLOCKER_DIAGNOSTICS.
- Generated side CSV SHA-256: f13b5c768b967f2f4e95255b233b5fc38322f8d44b3119d49dcd56d7013a449f
- Generated team CSV SHA-256: a8b517ec1825969d45a7b719a8babee098719ff3b7adda7a354840f704221cb9
- Generated summary JSON SHA-256: 9d1a5b9bab5242d7f7b3c4840b207e373fb99aff31254313d3af2afbaa370f0a

GitHub Actions validation is now complete: identity/settlement Run #13 (40699110792) passed the 15 feature-blocker tests and the 13 snapshot/runtime coverage tests; Safety Run #235 (40699110635) and Dry-Run #533 (40699110621) also passed. The runtime workflow's manual-only trigger guard is covered by regression tests. The runtime was not rebuilt because runtime/model code did not change. No provider API calls were made.

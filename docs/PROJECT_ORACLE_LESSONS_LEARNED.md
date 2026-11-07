# Project Oracle Lessons Learned

Last updated: 2026-11-07

## Current control lessons
- GitHub live state is authoritative; never assume a file or workflow exists because it was mentioned in prior conversation context.
- Inspect live HEAD and active workflow runs before changing or rerunning anything.
- A failed downstream quality step caused by a skipped upstream artifact must be classified separately from the upstream root cause.
- H2H team aliases are reporting-only identity controls; they must never rewrite canonical Fixture IDs or competition identity.
- Genuine no-history H2H, unresolved team identity, and league-code conflict must remain separate fail-closed classifications.
- Never weaken the 20% H2H unresolved identity gate to obtain a green workflow.
- Challenger prediction/settlement evidence cannot be promoted to Oracle V1.6 production evidence.
- Missing settlement provenance must remain incomplete; never infer source fields from outcome data.
- Exhausted HTTP-417 provider experiments remain quarantined unless new evidence changes the entitlement/root-cause assessment.
- A running equivalent workflow is not duplicated.

## Current specialist handoffs
- Continuous Build Control: H2H reporting is closed as an accepted non-blocking layer after Run #64; do not repeat H2H work unless new evidence identifies a regression. Focus integration control on the immutable prospective evidence handoff and manifest-hash compatibility gate.
- Validation: resolve remaining 50-league identity and source-admission gates.
- Evidence/OMI: establish immutable prospective feature/provenance and verified settlement evidence using admissible sources.

## Production readiness
Production remains fail-closed until canonical 50-league source/identity, snapshot, xG, odds, freshness, market observation, prediction linkage and verified settlement gates pass.


## Continuous Build Control — H2H closure and evidence handoff — 2026-11-07
- Run #64 (42391142276) is confirmed SUCCESS with all 17 substantive steps passed and artifact `oracle-h2h-report-64`.
- H2H is operational and non-blocking: 206/206 exact Fixture IDs, 10.68% unresolved identity diagnostic, no quality-gate failures.
- Do not rerun H2H merely to reduce genuine no-history or low-sample cases.
- Highest-value integration handoff is now the existing prospective evidence cohort: resolve the manifest-hash compatibility discrepancy for batch `42255401046`, then establish/verify immutable prediction → fixture → pre-kickoff feature snapshot → verified settlement provenance.
- This handoff remains research-only until production governance gates pass; no Oracle V1.6 production logic or governance changes are permitted.


## Continuous Build Control — prospective evidence persistence — 2026-11-07
- Run #447 proved the protected historical-state correction: publication governance and historical integrity both passed.
- The remaining failure was isolated to Step 18 evidence persistence. The evidence commit was created locally but the subsequent rebase failed because unstaged generated files remained; the fallback incorrectly assumed an active rebase.
- Persistence was corrected in private workflow commit `b812815782b694bf7929d2dc330cb6051f1f6f97` by stashing generated working-tree changes before rebase and restoring them before staging/pushing.
- This is integration/evidence plumbing only. Do not alter Oracle V1.6 model logic or production governance.
- The next valid prospective execution should be used to prove persistence and then inspect the pushed immutable snapshot manifest/values and exact prediction-to-snapshot-to-engine linkage.

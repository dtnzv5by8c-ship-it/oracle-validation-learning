# Oracle Selected-50 Remediation Sprint Result — 2026-10-29

## Execution evidence
- Research branch: research/oracle-50-league-readiness-audit
- Remediation code commit: 4e611ea37c0e63c9125a018ca1010c1aba4ef266
- Workflow commit: caf9b83d236c3bf30b48d5d6639af18ad387ce2b
- Successful run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40857731232
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40857731232/artifacts/12890146738
- Workflow compiled and executed the research-only closure script successfully; five output files uploaded.

## Results
- 50/50 league rows now have an explicit terminal identity status.
- 26 rows matched an exact country/competition entry to a source-specific Oracle code visible in the inspected Oracle configuration. These are not asserted to be global canonical IDs and are not production-approved.
- 24 rows are explicitly marked PROVIDER_ONLY_UNMAPPED; no fuzzy mapping was invented.
- Combo research definition fixed at the documented DC + Under 4.5 rule: DC outcome true and total goals 0–4 inclusive. Frozen predictions remain untouched.
- Settlement eligibility policy now requires explicit finished/complete status, valid score and source provenance; numeric scores on non-finished rows are not settled.
- Point-in-time policy now states that historical features require immutable evidence of observed_at < kickoff_at. Actual/post-match xG, standings without as-of timestamps, odds without capture timestamps and other unproven fields are excluded by policy.
- The 435-fixture gate inventory preserves 24 rows with missing required features as blocked.
- API calls in this remediation workflow: 0.
- Production writes/model changes: 0.

## Honest closure status
| Objective | Status |
|---|---|
| Stop repeating provider identity calls | CLOSED — existing 50-call probe reused |
| Every league has explicit identity status | CLOSED — 50/50 terminal statuses, 26 source-code matches and 24 unmapped |
| Combo definition conflict | CLOSED FOR RESEARCH SPEC — DC + Under 4.5, 0–4 goals; no frozen prediction changes |
| Point-in-time inclusion rule | CLOSED AS A GOVERNED RULE; actual feature snapshots still need evidence to qualify |
| Exact fixture/team joins across all current fixtures | OPEN — no all-fixture canonical join evidence in this workflow |
| Official settlement truth | OPEN — provider/source truth reconciliation not established by this workflow |
| Historical validation on only verified PIT features | OPEN — must run after eligible timestamped source snapshots are available |
| Production release | NOT_GRANTED |

## Next actions to actually close remaining evidence gates
1. Use authoritative finished fixture sources to recompute research-only Combo labels and compare with the prior ledger; retain provenance per fixture.
2. Join selected-50 current fixtures by provider fixture/team IDs against Oracle's exact canonical IDs. Keep unresolved joins quarantined.
3. Build an eligible-feature dataset by requiring source timestamp and kickoff timestamp, then rerun walk-forward diagnostics only on that subset.
4. Publish per-league/per-market coverage; only then consider a release review.

No claim is made that the remaining evidence gates have been completed. The point of this sprint was to replace ambiguous statuses with explicit machine-readable outputs and stop duplicate calls/audits.

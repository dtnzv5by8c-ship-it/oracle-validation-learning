# Project Oracle — Handover Checkpoint
Date: 2026-10-26
Branch: `research/oracle-50-league-readiness-audit`
Status: Research-only. Production eligibility: NOT GRANTED.

## Executive decision
CONTINUE — do not roll back or restart. Preserve the existing Oracle V1.6 production benchmark and continue the existing Gates 1–7 plan. The 50-request provider audit and research runtime have completed successfully, but evidence does not support production release or betting use. No production model logic, probabilities, calibration, thresholds, production registry, or production ledgers were changed by this checkpoint.

## Live repositories
- Production/private repo: `dtnzv5by8c-ship-it/oracle-football-data`
- Research repo: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Active research branch: `research/oracle-50-league-readiness-audit`
- Selected-50 manifest: `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`
- Historical validation window: 2025-03-20 through 2026-09-20.
- Production benchmark: Oracle V1.6. Master Development Model: V1.6.3. Do not alter either.

## Latest run evidence
- Selected-50 parent competition ID reconciliation: run [40363975646](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975646), SUCCESS. Exactly 50 requests; 50/50 API rows succeeded; each response contained a competition_id matching the selected ID sent; 50 distinct values. No raw provider payloads or API keys saved. This proves provider endpoint field behavior only; it does not prove canonical Oracle crosswalk.
- Selected-50 research runtime/backtest: run [40363975427](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975427), SUCCESS. Artifact [12669347817](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975427/artifacts/12669347817), `oracle-selected50-research-runtime-report`.
- Dry-run planner: run [40363975536](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975536), SUCCESS.
- Safety contract tests: run [40363975454](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975454), SUCCESS.
- Prior ingestion: run [40355232706](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40355232706), SUCCESS; 50 selected leagues / 200 season IDs ingested, zero ingestion failures. Season-level counts are not unique fixture coverage proof.
- Prior runtime report: run [40359783454](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40359783454), SUCCESS; showed unresolved identity, settlement, point-in-time provenance and Combo definition gaps.
- Prior schema diagnostic: run [40362039075](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40362039075), SUCCESS; catalogue exposes season IDs but did not provide verified parent competition IDs.

## Latest runtime verification — 2026-10-26
- Latest research runtime run [40372357659](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40372357659) completed SUCCESS on the research branch. Artifact [12672479177](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40372357659/artifacts/12672479177), `oracle-selected50-research-runtime-report`, 150,811 bytes, SHA-256 `023ec4a0a09385b9447ef6d6f77d535122003deabc6ffd6a3d5a4484db54c7e3`.
- Runtime contract status: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`; 50 selected groups, 250 league-market rows, 750 league-market-fold rows, 15 market-fold rows, and 456 governed fixture rows. Production and betting eligibility remain false.
- The latest governed output carries explicit reason codes for all 456 rows: confidence `NOT_CALCULATED_UNCALIBRATED_MODEL`; risk `NOT_QUANTIFIED_NO_VALIDATED_RISK_MAPPING`. Confidence/risk percentages remain blank intentionally; Combo probabilities are fully blocked/masked.
- Latest primary holdout backtest: BTTS accuracy 53.588% vs majority baseline 54.143% (below baseline); DC Home 70.126% vs 69.786% baseline; DC Away 60.422% vs 56.275%; Combo Home 57.40% vs 56.945%; Combo Away 64.934% vs 64.896%. These are raw, uncalibrated diagnostics; Combo remains blocked by target/settlement definition mismatch, and no odds-based ROI is approved.
- Code/workflow hardening at commit `97e546de90691d39ccfeab7046ec66dfc4b31515`: confidence/risk reason codes now propagate to the governed report, and the workflow no longer contains a private release-write step. This preserves research-only output boundaries.
- This runtime success verifies report contract and artifact generation only. It does not resolve canonical identities, official settlement truth, point-in-time feature/odds provenance, live-feed freshness, calibration, or production autonomy.

## Archive and identity findings
- Latest private archive QA evidence, documented in `reports/oracle-50-league-latest-private-archive-coverage-2026-10-26.md`: 50/50 selected season IDs/folders, 14,051 fixture records, 14,051 unique season-fixture pairs, zero duplicate pairs, 5,637 rows in the primary validation window in that snapshot.
- This does NOT prove complete coverage of the full 18-month window for all leagues.
- Prior identity snapshot: parent competition IDs verified 0/50; approved canonical mappings 0; canonical fixture joins 0/50; canonical team joins 0/50; official settlement truth 0/50.
- A research candidate-code crosswalk has 21 unique candidate matches to the existing 27-league production registry, but all require human review; 29 selected competitions have no candidate match in that registry. Candidate name/alias matches are not authoritative provider-ID-to-canonical mappings. Do not promote these automatically. The 50 selected leagues are a distinct universe from the existing 27-league registry.
- Current-feed identity quarantine: 12/50 selected groups had display-label rows, 5 of those had ambiguous feed league IDs; zero verified provider-season-to-feed bridges. Do not use display-name-only joins.
- Parent-ID audit response `competition_id` equalled selected ID, likely reflecting endpoint's parameter semantics; treat as provider-field evidence only, not proof of parent-vs-season ID identity or Oracle crosswalk.

## Coverage/data exceptions
- Australia A-League (selected ID 17326) and India Indian Super League (17964) have zero primary-window rows and zero recent-five prior-form rows in the latest selected-season snapshot.
- Provider status counts differ from completed-status candidates by four records.
- 135 rows have neither past nor future kickoff-date classification in the snapshot.
- 33 raw season-year tokens are `20262027`; 17 are `2026`. Preserve raw values; do not silently normalize.
- Nonempty table payloads exist for all 50, but historical standings as-of-kickoff are not verified.
- xG-like fields exist, but source semantics/as-of timestamps are unverified.
- Odds values exist on some rows, but point-in-time odds provenance (bookmaker, market, price, exact fixture join and timestamp before kickoff) is unverified.
- Exact canonical fixture/team IDs and UTC kickoff identity are not independently reconciled.
- Do not infer missing data, fill blanks, or allocate aggregate archive counts to individual leagues without evidence.

## Research performance (raw, uncalibrated; not betting approval)
Latest runtime walk-forward diagnostics:
- BTTS: mean fold accuracy 53.973%; primary holdout 53.588% versus majority-class baseline 54.143% (below baseline).
- Double Chance Home: 70.163% mean fold accuracy.
- Double Chance Away: 60.631%.
- Combo Home: 57.550%.
- Combo Away: 64.907%.
- Walk-forward metric arithmetic audit passed for stored aggregate metrics, but does not independently verify fixture identities or settlement truth.
- No verified odds-based ROI or profitability claim is supported. No 90% accuracy promise.
- Combo remains blocked because predictor target/settlement definitions mismatch. M-1UP remains event-truth-gated.
- All research output remains `production_eligible=false` and `betting_eligible=false`.

## Gates 1–7 current decision
1. Provider identity/canonical crosswalk: PARTIALLY ADVANCED, BLOCKED. Provider endpoint test passed; approved crosswalk and exact canonical fixture/team joins still missing.
2. Historical coverage/features: PARTIALLY ADVANCED, BLOCKED. Archive QA passes structural checks; complete historical coverage, kickoff/date/status anomalies, season tokens and point-in-time feature provenance unresolved.
3. Outcome/settlement truth: BLOCKED. Need authoritative final status, valid scores, exact fixture identity and independently evidenced settlement labels.
4. Market semantics: BLOCKED for affected markets. Combo mismatch unresolved; M-1UP independent event-truth gate remains.
5. Validation/calibration: RESEARCH DIAGNOSTICS ONLY. BTTS below majority baseline on primary holdout; identity/settlement evidence and sufficient league-market samples/calibration curves still needed. Do not tune production.
6. Autonomy/reliability: NOT DEMONSTRATED. Push-triggered research runs are not proof of scheduled execution, freshness handling, retries, recovery and alerting. Do not run private production workflows or increase GitHub spending without explicit approval.
7. Governance/evidence: BLOCKED. Must compile evidence pack, exception register, checksums, gate proofs and explicit human release review.

## Non-negotiable constraints
- Do not create a new model or redesign Oracle.
- Do not change production model logic, probabilities, calibration, thresholds, production registry or production governance.
- Do not modify production repo or run private production workflows without explicit permission.
- No GitHub spending-limit increase.
- Raw FootyStats payloads and API keys must never be exposed or committed.
- Keep research-only data/outputs in the research repo and mark every unresolved/ambiguous row gated.
- No fabricated fixtures, outcomes, IDs, odds, xG, standings or accuracy.
- Do not claim all 50 leagues are ready because all 50 seasons ingested.
- Do not call a gate complete without evidence.
- User has approved one bounded read-only FootyStats audit of up to 50 extra requests; that audit has already been used. Do not spend additional provider requests without a new explicit approval.
- The user wants forward progress without loops/repeated questions. Continue the existing work and make the best evidence-backed executive decisions. Ask only when a material authorization is genuinely required.
- Do not claim the assistant works autonomously after the active turn; only runs actually evidenced in GitHub count.

## Next execution order
1. Inspect current research branch head and the existing registry/readiness evidence before making any changes.
2. Build a sanitized 50-row reconciliation report that clearly separates (a) exact provider-selected season ID, (b) any provider parent competition ID, (c) candidate canonical code, (d) authoritative mapping evidence, (e) review status. Use only existing approved data; no fuzzy auto-approval and no more API calls.
3. Reconcile existing source files and registry where exact authoritative evidence exists; retain 29 unmatched or otherwise unresolved entries as BLOCKED rather than inventing 50 mappings.
4. Produce per-league year-by-year coverage and per-market readiness using actual row-level evidence; explicitly identify unavailable fields and exceptions.
5. Reconcile settlement truth and Combo semantics in research-only tests. Do not change production definitions.
6. Re-run research-only tests/runtime only when a meaningful change is made; capture exact run IDs and artifact checksums.
7. Document scheduled-operation/recovery gap and safe evidence required, without invoking private production workflows or paid calls.
8. Produce updated Gate 1–7 ledger and final executive decision. Unless all evidence gates pass, decision remains NOT GRANTED for production; state exactly what is fixed, what is evidence-only, what remains blocked and why.


## Update — bounded FootyStats ingestion batch 5 (2026-10-26)

- User explicitly authorized additional bounded FootyStats API calls on 2026-10-26 to expedite completion.
- Authorization commit: `774db3ff0952b93bdbd8e6dd8e4351ce7abb0d52`.
- Ingestion workflow run: [40375285207](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40375285207) — `success`.
- Sanitized artifact ID: `12674706565`; artifact SHA-256: `1de868a6319a558d103b9c11d07ee903ce1d06944b17db06eb0a584e8a45595f`; expires 2026-11-02.
- Provider calls: 57; hard cap: 250; last observed provider request-window remaining: 1,743. This is not monthly credit evidence.
- Exact selected season ID matches: 50/50; selected seasons: 200; historical seasons ingested: 200; failed seasons: 0; unmatched selected IDs: 0; ambiguous exact IDs: 0.
- Ingestion status: `COMPLETED`. Raw provider payloads were transferred to the private Oracle repository release only; no raw provider payloads were uploaded to the public research artifact. Production model logic and probabilities unchanged.
- Important limit: provider catalogue returns no provider parent league ID for some selected season rows (`provider_league_id=NOT_EXPOSED_BY_CATALOGUE`). Therefore 50/50 selected season ID matches do **not** prove canonical parent competition IDs, Oracle team/fixture crosswalks, official settlement truth, or production readiness.
- This batch supersedes the earlier checkpoint statement that no further API calls were authorized; the user's explicit new authorization permitted this bounded batch. Do not start another paid/provider batch without further explicit authorization.
- Research runtime, dry-run planner, and safety contract tests also succeeded on commit `774db3ff0952b93bdbd8e6dd8e4351ce7abb0d52`: runs [40375285255](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40375285255), [40375285092](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40375285092), and [40375285014](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40375285014).

## Updated next execution order

1. Reuse the new private archive from batch 5 as the current historical source; verify its release tag/checksum before any downstream ingestion.
2. Compare the new sanitized ledger against the existing selected-50 readiness and identity ledgers. Resolve only fields explicitly present and semantically authoritative; keep parent competition IDs and canonical Oracle mappings blocked when absent.
3. Rebuild the research runtime from the new private archive and validate all output-contract checks; publish only derived/sanitized research artifacts.
4. Use the updated season archive to reassess historical status/score/date exceptions and point-in-time features. A score on a non-final status is not settlement truth.
5. Re-run market backtests only after verified outcome labels and target semantics are available; do not calibrate or alter production probabilities.
6. Update the 50-league readiness workbook, gate ledger, and executive decision with the new artifact/run evidence. Production eligibility remains `NOT_GRANTED` until all evidence gates pass and explicit human release approval exists.

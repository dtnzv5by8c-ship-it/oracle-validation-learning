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


## Update — verified runtime after archive switch (2026-10-26)

- Updated workflow default private archive tag to `research-selected50-footystats-history-40375285207` in commit `b98e162f874672e62b827d0135fbb17245de0b97`.
- The first contract run after this change correctly caught a stale test assertion expecting the prior archive tag. Fixed that assertion in commit `b86699f803ec8a2638a59e1ceab2e69d8f85e44e`.
- Final verification on `b86699f803ec8a2638a59e1ceab2e69d8f85e44e`:
  - Safety contract tests [40376972102](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40376972102): SUCCESS.
  - Dry-run planner [40376972098](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40376972098): SUCCESS.
  - Research runtime/backtest [40376972017](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40376972017): SUCCESS.
- Latest runtime artifact ID `12674589642`, name `oracle-selected50-research-runtime-report`, SHA-256 `1686c03dcb84f678f288d2848dffd17ff8c6830d3e34c8700e3251c3191aed4a`; run created 2026-10-26T18:22:53Z.
- Latest governed report QA: 460 fixture rows, 460 unique source fixture IDs; all rows production-ineligible; 433 raw Combo home and 433 raw Combo away probabilities masked; zero Combo probabilities remain. Other market probabilities remain research-only and NOT_FOR_BETTING until canonical joins, settlement truth and calibration are verified.
- Primary holdout still shows BTTS accuracy 53.588% vs majority baseline 54.143%, below baseline. DC Home and DC Away diagnostics are stronger but remain uncalibrated and not production/betting eligible.
- The runtime workflow's archive tag change is now verified through successful runtime execution, not just code inspection.
- Production status remains `NOT_GRANTED`. Provider selected-season ID matches do not establish parent competition IDs, canonical Oracle mappings, verified settlement truth or current live-fixture freshness.


## Update — latest runtime reverified after checkpoint commit (2026-10-26)

- Latest runtime [40377435717](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40377435717) completed successfully on commit `b1ea894288f4189acfb68ca351131919f63869e1`.
- Safety contracts [40377435742](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40377435742) and dry-run planner [40377435780](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40377435780) also succeeded on the same commit.
- Latest artifact ID `12674229022`; SHA-256 `889095cd570bc0b4f333f193ed104734dd22e51bba26d3d8d89117873e9e2ad8`.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`; 50 selected groups; 460 governed fixture rows; 460 unique source fixture IDs; 2,300 prediction rows; 40 of 50 selected groups currently have prediction-bearing upcoming fixtures; 27 fixture candidates lack a supported prediction (source feature QA states 27 unsupported candidates). All outputs remain research-only and production/betting ineligible.
- The archive swap and stale test fix are verified. Combo Home/Away probabilities remain fully masked; raw predictor/settlement disagreement persists (9,335 Home, 8,017 Away), so Combo is blocked.
- Provider parent competition IDs remain unavailable for all 50 groups; the season ID is still used only as a grouping surrogate in research outputs. No authoritative canonical crosswalk has been established.
- Schedule file contains upcoming fixture candidates across all 50 selected groups, but its rows are marked `FIXTURES_FOUND` not freshness/identity approved. Do not treat schedule presence as verified live-feed freshness.
- Settlement QA shows status/score structural consistency checks, but official settlement truth remains unverified. Non-finished records with scores are quarantined from training truth.
- Backtest/market diagnostics remain raw and uncalibrated. BTTS primary holdout is below majority baseline; no betting edge or ROI claim approved.
- Production status remains `NOT_GRANTED`. No production repository changes, production logic changes, calibration changes, or probability changes made.
- Next action: prioritize authoritative identity bridge recovery from existing repository evidence and source records; where absent, document external identity dependency rather than infer IDs. Then validate exact historical fixture settlement, and only after those gates pass evaluate market-specific research eligibility.


## Update — completed runtime artifact review (2026-10-26, follow-on)

- Reviewed completed runtime [40377879159](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40377879159), artifact `12676936403`, SHA-256 `9b000f480d4affda9a8a23c6164cee608e638a20baf190d6c362ba47969ff802`.
- Runtime output contract passed. Feature QA confirms 50 selected groups, 200 historical season folders loaded, 59,049 deduplicated raw records, 51,983 explicitly completed records, 460 upcoming fixture candidates and 2,300 raw research prediction rows.
- 40/50 selected groups have prediction-bearing upcoming fixtures. This is report-generation coverage, not canonical identity/freshness certification.
- League-market walk-forward status counts across 250 league-market rows: 100 insufficient fold sample/metric; 75 mixed Brier skill across folds; 71 positive Brier skill in all folds (diagnostic only); 4 no positive Brier skill in all folds. All edge claims remain NOT_APPROVED and production_eligible=NO.
- 150 of 250 league-market pairs met the minimum 100-train/100-test sample criterion in all three folds; this sample criterion alone does not confer eligibility.
- 460 governed fixtures have unique source fixture IDs; Combo home/away probabilities are masked on all 433 rows where raw Combo probabilities were present. Combo remains blocked because the predictor definition (Double Chance plus 2–4 total goals inclusive) differs from the documented settlement comparator (Double Chance plus fewer than five goals). Do not choose a market definition silently; requires governed definition alignment.
- Feature QA says xG/odds are excluded from features because semantics and point-in-time provenance are unverified; current team-table positions are display-only snapshots rather than historical standings.
- Parent competition IDs unavailable: 50/50. Canonical team/fixture joins and official settlement truth remain unverified. No production logic/probabilities changed; production/betting eligibility remains false.
- Next step: use exact provider/source identity evidence where present; produce a league-level identity gap matrix that distinguishes existing canonical candidates from unresolved leagues. Do not use label similarity to auto-approve. For market evaluation, keep DC/BTTS research-only until exact settlement and point-in-time evidence gates pass; Combo remains blocked pending governed market-rule reconciliation.


## Update — crosswalk source-of-truth reconciliation (2026-10-26)

- Re-read the live artifact `reports/oracle-selected50-protected-registry-candidate-crosswalk-2026-10-26.csv` at blob `70273bb08f931fa61e0db55f29caae71c8e9a436`.
- Exact current CSV counts: 50 selected rows; 21 candidate exact-country/competition matches requiring human approval; 29 with no unique match in the protected 27-league registry; zero verified provider-ID-to-canonical-ID bridges; zero verified fixture identities; zero verified team identities; zero production-eligible rows.
- This current CSV is the source of truth for the current split and supersedes stale 22/28 counts in older checkpoint snapshots. Do not overwrite it with older counts.
- Current runtime on the checkpoint commit: [40379059499](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379059499) was still in progress at last check. Safety contracts [40379059412](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379059412) and dry-run planner [40379059390](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379059390) passed.
- Next safe action: inspect final runtime result, then use existing exact evidence to classify the 21 candidates and 29 unmatched groups. Do not auto-approve candidate names or add mappings to the protected registry. Any new mapping must be backed by an authoritative provider parent ID and exact source evidence; otherwise keep research-only alias/quarantine.


## Update — exact 50-league identity and market gate matrix (2026-10-26)

- Added `reports/oracle-selected50-identity-and-market-gate-matrix-2026-10-26.csv` in commit `e6e33d787721d784fe156e9d832f9c6ec6c92168`.
- Matrix contains exactly 50 rows, keyed by selected FootyStats season ID and provider country/competition label, with separate fields for candidate canonical code/name, protected registry status, identity gap, provider-parent-ID status, provider-to-canonical bridge, fixture/team identity, official settlement truth, BTTS/DC/Combo readiness, production eligibility, and next action.
- Matrix is explicitly evidence-gated: no candidate mapping is approved; provider parent competition IDs are marked unavailable in archive manifest; fixture/team identity and official settlement truth remain unverified; BTTS/DC are research-only pending exact fixture/final-score verification; Combo Home/Away blocked for target-vs-ledger mismatch; all 50 production_eligible=NO.
- Current crosswalk source counts: 21 candidate mappings needing human approval; 29 no unique match in protected 27-league registry; 0 verified provider-to-canonical bridges; 0 verified fixture identities; 0 verified team identities; 0 production-eligible.
- Current market settlement crosswalk: BTTS and DC formulas align with production target formulas but official settlement rules are not verified; Combo predictor target (DC plus 2–4 total goals inclusive) conflicts with settlement ledger comparator (DC plus fewer than five total goals). This is preserved as a blocking discrepancy; no market definition was silently changed.
- Runtime [40379246263](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379246263) was still in progress at last check. Safety contracts [40379246217](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379246217) and dry-run planner [40379246193](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379246193) passed on the previous checkpoint commit.
- Next: inspect matrix via exact 50-row contract test, verify latest runtime result, then reconcile each candidate only when authoritative provider parent IDs or exact source identity evidence exists. Do not modify protected production registry or production model logic.


## Update — identity/market matrix contract and latest verification (2026-10-26)

- Matrix: `reports/oracle-selected50-identity-and-market-gate-matrix-2026-10-26.csv`, current blob SHA `69ec56b838333be0a01e026644e0bb92a19a67c3`; 50 unique selected season IDs, one row per governed selected league.
- Added a no-network contract test to `tests/test_footystats_selected50_bounded_probe_contract.py` in commit `da19c7ac4358647158e780b295c0b386fabd85d3`. It checks row count and uniqueness, required gate columns, no approved registry mappings, unavailable parent IDs, unverified provider/fixture/team/settlement identity, Combo blocks, and `production_eligible=NO` for all rows.
- Safety contract run [40379704321](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379704321) succeeded on commit `da19c7ac4358647158e780b295c0b386fabd85d3); dry-run planner [40379704324](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379704324) was in progress at the checkpoint update.
- Matrix/runtime build on the prior matrix commit `e6e33d787721d784fe156e9d832f9c6ec6c92168` completed successfully: [40379475087](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379475087). Its report artifact is [12677008201](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379475087#artifacts), 151,690 bytes, created 2026-10-26T18:39:40Z. This verifies research runtime execution on the matrix commit, not production eligibility.
- Latest runtime on the test commit `da19c7ac4358647158e780b295c0b386fabd85d3` was still in progress when this note was written: [40379704245](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40379704245). Do not treat as complete until its final status/artifact is inspected.
- Identity resolution outcome is unchanged: 21 candidate mappings require human/authoritative approval; 29 have no unique match in the protected 27-league registry; zero verified provider-to-canonical bridges, fixture identities or team identities. No mappings have been silently promoted.
- Settlement/market decision is unchanged: official settlement truth remains unverified; BTTS and DC remain research-only pending exact fixture/final-score verification; Combo Home/Away remain blocked by the predictor/ledger target mismatch. No production logic or probabilities changed.
- Executive decision: production readiness remains `NOT_GRANTED`. Remaining blockers require authoritative identity bridges, exact fixture/team joins, trusted official settlement labels and governed Combo market-definition reconciliation. These cannot be truthfully completed from current repository evidence alone; no additional paid provider calls were made.


## Update — provider parent-ID reconciliation and runtime cost guard (2026-10-26)

### Verified provider evidence

- Read-only FootyStats parent-ID probe completed successfully in [run 40382835076](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40382835076), workflow commit `19248b3fefffe7fd82bf99eaaeb3dcf15dafc802`.
- The probe made exactly 50 read-only requests, one match row per selected ID, with a 50-request hard cap, no retries, and a 2.1-second delay between requests to remain below 30 requests/minute. All 50 returned HTTP 200 and `success=true`.
- Direct match-record evidence returned `competition_id` equal to the selected ID for 50/50 leagues; all 50 competition IDs were unique. The one-row probe also exposed 50 unique source match IDs and home/away team IDs for all 50 leagues.
- Sample record statuses: 24 `complete`, 26 `incomplete`. These are schema/identity samples only; they are not a full-history reconciliation. Scores on incomplete records (commonly 0-0) are not outcome truth, and even complete samples still require canonical fixture/team joins and authoritative settlement verification.
- Last observed provider request-window remaining: 1,750. This is only a request-window signal; monthly credit balance was not exposed or verified. No raw provider payload or API key was saved or published.
- Workflow artifact ID `12679900833`; ZIP SHA-256 `68eebc2ae98a701284aa128a6b969e7637f86f737a12602cd2de2d53d656249b`; original sanitized CSV SHA-256 `2fc3bb76b9051d32c3645de58ba5a1385a01e5601cc383e0da7390a3b8aa835b`; summary SHA-256 `859780c779ba6b357d66474eaed9809ecbc1221959407dc4b542c815230637e4`.
- Persisted the sanitized 50-row evidence in `reports/oracle-selected50-parent-id-probe-2026-10-26.csv` (blob SHA `6bfc5e77f2046191b79a54053ea3a7b4ddf75dc7`) so it does not depend on the 14-day workflow-artifact retention period.

### Updated identity crosswalk and matrix

- Updated `reports/oracle-selected50-identity-and-market-gate-matrix-2026-10-26.csv` (blob SHA `8c2ff966aad565f4471b6fbd2fa56255a6b07c33`) with the observed provider parent competition ID, evidence run, and one-sample source fixture/team/status/kickoff/score fields for every league.
- Updated `reports/oracle-selected50-protected-registry-candidate-crosswalk-2026-10-26.csv` (blob SHA `b8bfb42766a13feaa9f99408bcea99f1f40f8e13`) to reflect that the provider match endpoint confirms the selected ID as `competition_id`. Provider-to-canonical verification remains `NO`; exact source IDs do not automatically establish Oracle canonical IDs.
- Re-inspected the private canonical registry read-only: `config/oracle_major_league_registry_v1.json` blob SHA `81d6db487e498fc84a87a7457b0de7215537f15c` contains 27 canonical league entries with code/country/competition/readiness fields, but no FootyStats provider-ID field in the registry entries. No private file was changed and no production workflow was run.
- Current mapping counts remain 21 candidate canonical rows requiring authoritative/human approval and 29 leagues with no unique row in the protected 27-league registry. Verified provider-ID-to-canonical bridges: 0; canonical fixture identities: 0; canonical team identities: 0. The 21 candidates are not auto-approved based on names.
- Matrix now explicitly distinguishes source provider IDs observed from canonical joins still unverified. BTTS and Double Chance remain research-only; official settlement truth remains unverified; Combo Home/Away remain blocked for the predictor-versus-ledger target mismatch; every row remains `production_eligible=NO`.

### Workflow efficiency and verification

- The parent-ID workflow was made rate-limited and expanded to emit only allowlisted fixture/team/status/score fields; raw payloads remain suppressed. Contract coverage asserts the hard cap, 2.1-second delay, request-window guard, sanitized output, and absence of credential/raw-payload logging.
- Added validation of the persisted 50-row probe and the updated matrix. Safety contracts passed on commit `e1ddbaa1018738a41bfdd21415eef1c17c411063` in [run 40383685732](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40383685732). The earlier stale assertion failure on intermediate commit `87246da8d7702a8cd7b305f22b11303b6d07209a` was corrected; the subsequent safety run passed.
- Root-cause efficiency fix: the research runtime workflow now ignores report-, test-, and Markdown-only pushes, preventing costly full backtests from being started for checkpoint and report commits. Workflow change commit `c5e9a0bb865fd9352a418e8d7a64b7574684a60c`; guard test commit `f41323e0031887f991fd695dc65895c5878155aa`. Safety/dry-run runs were still in progress for the newest trigger-filter commit at the time of this checkpoint; verify their final statuses before claiming completion.
- Latest known runtime [40383685862](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40383685862) was still in progress when this checkpoint was updated. Older redundant runtime jobs were triggered by earlier report/test commits before the new path filter took effect; do not start more runtime runs merely to refresh documents.

### Executive decision

The provider match-record probe observed `competition_id` equal to the selected ID for all 50 selected groups, but the response rows exposed no non-empty `season_id` values. This is **not proof of parent-competition semantics** and does not establish a provider-to-Oracle canonical crosswalk, exact canonical fixture/team identity, historical outcome truth, point-in-time feature provenance, or market settlement semantics. No production registry/model/probability/calibration/threshold/ledger was changed. Production release remains `NOT_GRANTED`.


## Update — runtime QA now consumes parent-ID probe evidence (2026-10-26)

- Updated research-only `scripts/build_selected50_research_runtime.py` in commit `659263b36301ccac5701787bb0d7c70c03ab70e1` to validate and read the persisted 50-row match-record probe. It adds separate QA fields for parent IDs verified from match records, sample fixture/team ID presence, the 24/26 complete/incomplete sample-status split, and an explicit `provider_sample_scores_are_settlement_truth=false`.
- Updated `scripts/validate_selected50_runtime_outputs.py` in commit `9f974dd531c87bf7b16763b7f55b2ed33e31092f` to require 50/50 probe IDs, 50 source fixture IDs, 50 home/away team-ID pairs, zero provider-to-canonical bridges, and no use of sample scores as settlement truth.
- Safety contracts passed on the validator commit: [40384191412](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40384191412). The newest safety run after adding the corresponding integration assertions also passed: [40384212766](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40384212766). Dry-run planner passed on the newest test commit: [40384213168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40384213168).
- Runtime integration verification is still pending: [40384191364](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40384191364) was in progress on commit `9f974dd531c87bf7b16763b7f55b2ed33e31092f` when this note was written. Do not claim the new QA fields are runtime-verified until this run finishes successfully.
- A prior runtime after the identity matrix update passed output-contract validation in [40383594810](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40383594810), artifact ID `12678584584`, ZIP SHA-256 `6eeff0cbcfa6de7a3ff523360a1fd2bdc7b6d15cd6eb177c4da17a53c0e2d4e1`. That artifact predates the new probe-QA fields, so it is not evidence that the latest script integration has passed.
- The runtime workflow now ignores report/test/Markdown-only pushes; subsequent checkpoint/report edits should not start another expensive backtest. The current in-progress runtime jobs were started by earlier code commits before the trigger guard had fully taken effect.
- Production model logic, production probabilities, calibration, thresholds, registries and ledgers remain unchanged. Production readiness remains `NOT_GRANTED`.


## Update — bounded 50-league match coverage audit and corrected identity semantics (2026-10-26)

### Verified provider audit

- Workflow run [40391540391](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40391540391) completed **SUCCESS** on workflow commit `af143fcd42f3f320027e67dbd0f7d5184b85f938`.
- Sanitized artifact ID `12684045977`; artifact ZIP SHA-256 `47392a7986e43d35bc9ada442e157d52fa945b51175d7f1e632bd03c34e67f6`; artifact link: [match-coverage audit artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40391540391#artifacts).
- The workflow used 50 read-only requests, hard cap 50, no retries. All 50 returned HTTP 200 and provider `success=true`. Last observed provider request-window remaining was 1,750; **monthly credit/billing balance remains unverified** and must not be inferred from that value.
- First-page results: 14,051 match rows; 14,051 unique fixture IDs within their respective selected groups; zero duplicate fixture-ID rows; `pager.max_page=1` for all 50 groups. All 14,051 rows had a status field, both provider team IDs, both score fields and a Unix kickoff field.
- Provider status counts: `complete=7,040`, `incomplete=6,958`, `suspended=53`. Kickoff range observed: 2026-01-16 23:20:00 UTC through 2027-06-06 00:00:00 UTC.
- No non-empty `season_id` field values were returned. The rows expose `competition_id` and `season`; `competition_id` equals the selected ID in all 50 groups. This is an observed provider-field relationship only, **not** proof of parent-competition semantics or canonical Oracle identity. Score-field presence does not establish final-score/settlement truth, especially for incomplete or suspended rows.
- No raw provider payloads or API keys were saved. No production logic or probabilities were changed.

### Saved research artifacts and code

- Expanded the identity/market matrix to 43 columns, adding per-league first-page row counts, status counts, fixture-ID uniqueness, team/score/kickoff field presence, pagination and evidence-run identifiers. Current matrix blob SHA: `ae08700e2d16c2a83ed7157b7c021a65714bbd52`.
- Permanent summary and league-by-league table: [Selected-50 match-coverage audit report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-match-coverage-audit-2026-10-26.md), created in commit `346111724ac61aad37d939842d5b181eea871590`.
- Identity reconciliation ledger updated to distinguish provider `competition_id` observation from canonical mapping. Current ledger blob SHA: `d73c8505d6d08b15a4d0428bfc1083a9d76353c2`.
- Audit workflow code was corrected to use the provider `season` field instead of a misleading `season_id` comparison and changed to manual-dispatch-only to prevent accidental API calls from workflow-file edits. This corrected workflow version has **not** been rerun; the evidence above belongs to run `40391540391`. No further provider requests were made.
- Research runtime and validator now load and enforce the persisted 50-row coverage matrix, retain parent-ID semantics as unverified, and report the exact coverage totals. Commit: `5e80a67fe5c8530f417b38cb8aa61d2a90638835`.

### Runtime verification after coverage integration

- Safety contract tests [40392688038](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40392688038): **SUCCESS**.
- Dry-run planner [40392687717](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40392687717): **SUCCESS**.
- Research runtime/backtest [40392687925](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40392687925): **SUCCESS**; output contract passed.
- Runtime artifact ID `12686010824`, SHA-256 `7ac103f46c737a4ec81e70d88d2b6ec31a5818dd84689db1a4da87603898362d`, expires 2026-11-09 20:08:03 UTC.
- Runtime QA: coverage contract `PASS_PROVIDER_MATCH_COVERAGE_CONTRACT_50_OF_50`; 14,051 first-page rows; 14,051 unique fixture IDs; zero duplicates; zero pagination-truncated groups; 50/50 groups with `competition_id` matching the selected ID; zero non-empty `season_id` values; zero verified provider-to-canonical bridges; parent-competition semantics explicitly `false`.
- Governed runtime report: 462 fixture rows; 435 Combo Home and 435 Combo Away probabilities masked; all rows remain production-ineligible.
- Primary-window BTTS holdout remains 53.588% accuracy versus 54.143% majority baseline. Double Chance Home and Away diagnostics remain raw/uncalibrated and are not approved for betting.

### Executive decision and remaining blockers

- The match-coverage and output-contract evidence layer is materially stronger, but canonical identity and settlement gates are **not closed**.
- Still blocked: authoritative provider-to-Oracle league bridge; exact canonical fixture/team joins; independently verified final-score/settlement labels; historical point-in-time feature/odds/xG provenance; governed Combo predictor-versus-ledger definition reconciliation.
- No monthly provider credit balance is evidenced. The 50-request batch is complete; do not make further provider calls until an approved safe budget preflight can establish that the planned request count fits the existing limits.
- Production eligibility remains `NOT_GRANTED`; Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain untouched. All changes are research-only.


## Update — protected canonical-registry source review (2026-10-26)

- Read-only inspection of the private canonical registry `config/oracle_major_league_registry_v1.json` (blob `81d6db487e498fc84a87a7457b0de7215537f15c`) confirmed 27 canonical league entries with fields `id`, `country`, `competition`, `tier`, `wave`, and `readiness`; there is no FootyStats/provider ID field in the registry schema.
- The private readiness matrix (blob `602061ebe0bbecdd3c11876307cebe45b0ed2ffd`) records league readiness/source provenance but not the 50-league FootyStats ID bridge.
- The private source-reconciliation manifest (blob `154d940a3a0e8235578710dd7c4cc9bca2404fa2`) reports 108 FotMob rows, zero matched/agreed/conflicting rows and 108 unverified against the alternate source. This cannot independently promote FootyStats candidate mappings.
- The private historical match-spine manifest (blob `5d8ffe45cc1ad62c9c17972499eefa8236e44e77`) is FotMob-derived for 27 leagues and the primary historical window; it is a different provider namespace/universe, not a FootyStats crosswalk.
- Saved the evidence review: [canonical registry evidence review](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-canonical-registry-evidence-review-2026-10-26.md), commit `61fe0e3b0e437a062b9e341c9d00ae2a7d978c59`.
- Conclusion is unchanged and now backed by explicit source inspection: **0/50 provider-to-canonical bridges verified; 21 candidates still require authoritative evidence/human approval; 29 have no unique match in the protected registry; 0/50 canonical fixture joins and 0/50 canonical team joins verified.** No mapping was approved from name similarity.
- No provider calls were made during this source review. The 50-request match audit remains the latest provider batch; monthly credits remain unverified. The parent-ID/match-coverage workflow is now manual-dispatch-only to avoid accidental calls on code edits.
- Latest confirmed research runtime [40392687925](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40392687925), safety contracts [40393109251](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40393109251), and dry-run planner [40393109357](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40393109357) all succeeded. Production readiness remains `NOT_GRANTED`.


## Update — official FootyStats ID semantics and one-call diagnostic hardening (2026-10-26)

### New authoritative provider documentation evidence

- Reviewed official FootyStats [League List documentation](https://footystats.org/api/documentations/league-list), which states each competition season has a unique ID and identifies `season > id` as the season ID.
- Reviewed official FootyStats [League Matches documentation](https://footystats.org/api/documentations/match-schedule-and-stats): the request parameter `season_id` is defined as the ID of the league season (lines 93–97), and the response field `competition_id` is explicitly defined as “Season ID of the league” (lines 365–367).
- This resolves a field-semantics ambiguity: the 50/50 match-record equality is a **season-ID relationship**, not evidence of a parent competition ID. The existing finding of zero parent competition IDs in the provider archive/catalogue remains valid.
- Updated all 50 rows in `reports/oracle-selected50-identity-and-market-gate-matrix-2026-10-26.csv` to `PROVIDER_DOCS_DEFINE_COMPETITION_ID_AS_SEASON_ID_NOT_PARENT_ID`; updated the evidence scope and next actions. Current matrix blob SHA: `a0a7f70c2a4688aa38df251f03086bbab5505e03`. No canonical mappings were approved.
- Updated runtime builder and output validator to enforce the documented field semantics, emit the official documentation source URLs in sanitized QA, and keep parent ID verification false. Commits: `a061ef4f8b8ce06472fe52ae47b10575202ac3de` (runtime builder) and `2a02f3b2fbdd263663d833810d95ce5df5d0269e` (validator).
- Updated the offline contract test and canonical-registry evidence review: test commit `a349c574aef72ccb350f4fb0c710c405786052f2`; evidence review commit `73ffc6fbf67e025e14c15eef4b3554a8df01d02b`.

### Provider budget and dispatch constraints

- Inspected the existing research workflows. `FOOTYSTATS_API_KEY` is referenced by the approved research workflows; prior successful provider runs demonstrate that the secret was available when those runs executed. Secret values were not read or exposed. The private archive token is referenced only by the existing private-archive ingestion workflow.
- The current tool connection exposes GitHub read/contents operations and workflow-run inspection, but **does not expose a workflow-dispatch action**. The selected-50 parent/match audit is intentionally `workflow_dispatch`-only; I did not weaken its trigger or create a push-triggered paid request.
- The latest provider request-window observation remains 1,750 from the prior audit. This is request-window metadata, **not** a verified monthly credit balance. No FootyStats API calls were made in this run.
- Hardened `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml` to require `confirm_provider_credit_usage=true`, cap the diagnostic at one `league-list` request, report provider request-window metadata when returned, and explicitly mark `monthly_credit_budget_verified=false`. Workflow commit: `4160df9df672aa77dbef8bec58342cae5967e1ed`; matching offline contract test commit: `0f612c2b509105a8e1118478132f4051c80010ac`.
- Safe next action if another provider call is approved: in GitHub Actions, manually run **Oracle Selected-50 Provider ID Schema Diagnostic** with `confirm_provider_credit_usage=true`, after confirming the current FootyStats account credit/billing budget. It consumes exactly one read-only catalogue request and publishes sanitized schema/ID-field evidence only. Do not paste the key into chat.

### Verification status

- Safety contract tests [40400391891](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400391891) passed on workflow-hardening commit `4160df9df672aa77dbef8bec58342cae5967e1ed`.
- Safety contract tests [40400246466](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400246466) and dry-run planner [40400246429](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400246429) passed on commit `a349c574aef72ccb350f4fb0c710c405786052f2`.
- The new safety-test run for commit `0f612c2b509105a8e1118478132f4051c80010ac` was queued as [40400416482](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400416482) at the last status check; the dry-run planner [40400416383](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400416383) was also queued. Earlier intermediate commits had failures while matrix, runtime validator and tests were being synchronized; later safety/dry-run runs passed on corrected commits.
- Runtime [40400232375](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400232375) was still in progress on commit `2a02f3b2fbdd263663d833810d95ce5df5d0269e`; do not treat the updated runtime QA as verified until this run or a later runtime completes successfully.
- Canonical league/fixture/team joins, official settlement truth, historical point-in-time feature provenance and Combo definition reconciliation remain blocked. Production readiness remains `NOT_GRANTED`; no production repository or production model files were changed.


### Automation verification update — 2026-10-27 00:03 SAST

- Re-read the live research branch commit list. Latest branch head at inspection: `2fb873f27f66c10ee87d46dcb68ef99997768c5a` (`docs: checkpoint provider ID semantics and safe dispatch gate`, committed 2026-10-26T20:59:12Z). No later research-branch commits were present in the live branch history.
- The previously pending runtime has now completed successfully: [run 40400232375](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400232375), head `2a02f3b2fbdd263663d833810d95ce5df5d0269e`, conclusion `success`, completed 2026-10-26T21:00:15Z.
- Runtime artifact: [artifact 12689595658](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400232375/artifacts/12689595658), `oracle-selected50-research-runtime-report`, 151,946 bytes, expires 2026-11-09T21:00:10Z. SHA-256 of uploaded ZIP from Actions log: `2df3f941252edceec8b990a8c88a1769309a440bcd8e4ebebb9319e038d77298`.
- Runtime validator result: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`; 50 selected groups; 460 governed fixture rows; 750 league-market-fold rows; zero Combo Home/Away probabilities remaining; `production_eligible=false`; `betting_eligible=false`.
- Runtime QA reconfirmed 14,051 first-page match rows across 50 groups, 14,051 unique fixture IDs, zero duplicate fixture-ID rows, zero groups flagged as pagination-truncated, all 14,051 rows with status, both team IDs, both score fields and Unix kickoff; status counts complete=7,040, incomplete=6,958, suspended=53. These are structural provider-coverage checks, not official settlement truth.
- Runtime QA also confirms provider match-record `competition_id` is documented as the season ID, not a parent competition ID; explicit nonempty `season_id` values in the audited match payload were zero. Parent competition IDs verified=0/50; provider-to-canonical bridges verified=0; official settlement truth remains unverified.
- Safety contract tests [40400461788](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400461788) and dry-run planner [40400461640](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40400461640) both succeeded on the latest checkpoint commit `2fb873f27f66c10ee87d46dcb68ef99997768c5a`.
- Provider budget/dispatch recheck: the approved schema diagnostic remains manual-dispatch-only and requires `confirm_provider_credit_usage=true`; it is hard-capped at one catalogue request and suppresses raw response bodies. The available GitHub connector has no workflow-dispatch operation, and current monthly FootyStats credit balance is not observable through the available read-only tools. No API call was made in this automation run; the last observed request-window remaining value 1,750 is historical and is not proof of current monthly credits.
- Exact safe next action for any further provider request: confirm current account credits/billing in FootyStats, then manually dispatch `Oracle Selected-50 Provider ID Schema Diagnostic` in GitHub Actions with `confirm_provider_credit_usage=true`. Do not weaken its manual trigger, introduce a push-triggered paid call, or expose credentials.
- No production repository/workflow was touched. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain unchanged. Production readiness remains `NOT_GRANTED`.


## Automation update — stale archive snapshot and dynamic freshness fix (2026-10-27)

### Corrected evidence freshness labelling

- Rechecked the exact source runs: private-archive QA run [40183451811](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183451811) was created at `2026-10-25T10:07:11Z`; the later 200-season FootyStats ingestion [40375285207](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40375285207) was created at `2026-10-26T18:09:53Z` and completed successfully.
- The previously titled “Latest Private-Archive Coverage” report was based on the pre-batch-5 QA artifact, not QA generated against the later batch-5 archive. Its 14,051-row selected-season snapshot is retained as historical evidence but must not be represented as current 200-season historical-archive coverage.
- Updated `scripts/build_selected50_latest_private_archive_coverage.py` and its regression test to stamp every generated row and summary with `PRE_BATCH5_QA_SNAPSHOT_SUPERSEDED_FOR_CURRENT_ARCHIVE_COVERAGE`, source QA run/time, and superseding ingestion run/time. Updated the report title and executive instructions accordingly.
- The superseding ingestion does not, by itself, resolve canonical identity or settlement truth. A fresh private-archive QA artifact against the exact batch-5 archive tag is still needed for a like-for-like row-level status/date exception reconciliation.

### Fixed the schedule-age clock and reduced report-only workflow churn

- `scripts/build_selected50_governed_readiness_matrix.py` previously froze `AUDIT_DATE` at 2026-10-26, so scheduled runs could report stale-schedule ages that stopped advancing. It now computes the audit date from current UTC and writes that date into the matrix/summary/gate.
- Updated `tests/test_selected50_governed_readiness_matrix.py` to use a fixed explicit test date for deterministic assertions.
- Updated the dry-run workflow to calculate the expected date deltas from the recorded audit date rather than hard-code “9 days” and “4 days”. The underlying schedule snapshot remains stale (last fixture date 2026-10-17; manifest window end 2026-10-22); this fix corrects its age reporting and does not approve or fabricate a new slate.
- Added `paths-ignore` for report/Markdown-only pushes in the dry-run planner workflow so checkpoint/report edits do not repeatedly launch the full planner. Test/code/workflow changes still trigger the appropriate validation.
- Exact commits: `d154f92c548b156122a49447d2a9e396d897cf12` (snapshot freshness metadata); `f5f58debb24d3a1651e56553120c1f436281550a` (freshness regression assertions); `8e1668316def72da08333cf0f51b8bcd86315faa` (report relabel); `2032127948b1d3fe302db882d2ff04915988b9bf` (UTC audit date); `0d01f773a749f0c04721046cbccd8385711f7b16` (deterministic test date); `2df02bfec2f21f7a0167a11cf21d6b25bf41f650` (dynamic workflow validation); `167d844fc9af5f3bef39207d4fc1c557772543e6` (summary-reference correction); `7dfbd378b3f20d05e44313a33cfaa3919b8c4d98` (report-only planner path filter).
- An intermediate dry-run failed on the premature reference to the summary variable before it was initialized (runs [40417457025](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40417457025) and [40417495832](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40417495832)). The reference was corrected in commit `167d844fc9af5f3bef39207d4fc1c557772543e6`; dry-run [40417533761](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40417533761) then passed, followed by latest-head dry-run [40417572839](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40417572839) — SUCCESS.
- Latest-head safety contracts [40417572834](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40417572834) — SUCCESS.
- Research runtime [40417533574](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40417533574) was still in progress at last check on commit `167d844fc9af5f3bef39207d4fc1c557772543e6`; no new artifact or completion claim is made here. Earlier redundant runtime jobs may still be running from successive code commits; no cancellation action is available through the connected GitHub tools.

### Provider budget/dispatch and release gates

- No FootyStats calls were made in this automation run. The provider diagnostic references the existing `FOOTYSTATS_API_KEY` GitHub secret inside the workflow, but the connected read-only GitHub tools cannot verify current secret presence or expose monthly provider credits. The historical request-window remaining value of 1,750 is not current monthly-credit evidence.
- The one-call schema diagnostic remains manual-dispatch-only and requires `confirm_provider_credit_usage=true`; the available GitHub connection has no workflow-dispatch operation. Do not weaken the manual trigger or introduce a push-triggered paid call. Exact safe action for a further provider call: confirm current FootyStats account credits, then manually dispatch the existing one-call diagnostic in GitHub Actions.
- No production repository/workflow was changed. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain untouched. Provider-to-canonical bridges, canonical fixture/team joins, official settlement truth, point-in-time xG/odds provenance and Combo target reconciliation remain blocked. Production readiness remains `NOT_GRANTED`.


## Update — current private archive status/score/date QA and commit-pinned workflow verification (2026-10-27)

### Corrected archive source and reproducible evidence binding

- The private archive QA workflow had been pointing at stale release tag `research-selected50-footystats-history-20261025`. Corrected it to the exact batch-5 archive tag used by the runtime: `research-selected50-footystats-history-40375285207` (commit `8f4de15ca522906ed5ab9880de365df3ed6be90b`).
- Added a regression test for the QA/runtime archive-tag match (commit `ab1a945ae4eb14e954572ef0c3db092929d01186`).
- Private archive QA and safety contract workflows now check out the exact triggering commit via `github.sha`, rather than a moving branch head, so run SHA and tested code are bound consistently (commits `cba6f423b56a79ab188acaec39385e3efce5a0aa` and `428eb46e63c54fca1d5740b52f9de9fcb52b18ea`). Contract tests enforce this.
- Added archive QA for provider status, score-pair patterns, kickoff-date exceptions and invalid score pairs (script commits `ceeb3b5400ffa0bf605a2b42d36f1f28316e8443`, `0604dd6a080d08fd8d4982626af9b7d1b05af243`, `44f4a9741c2554277c708334edaefc080d980672`). Regression-test fixes are included in `fbae8a90878df4565523de093afb1adb1a54e1e4` and `d06a2c0a491cad687c92656638767aab66d7b345`.
- Published the sanitized audit at `reports/oracle-selected50-private-archive-status-score-date-audit-2026-10-27.md`; its evidence cross-check was committed in `3d825e34345185130f243aace174c7997cde4c4c`.

### Fresh private archive QA — exact batch-5 archive

- Commit-pinned QA run [40423922693](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693) — SUCCESS.
- Sanitized artifact [12698682583](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693#artifacts), ZIP SHA-256 `2fd2242e46d58267f7dbbffc35fb43675c7d74dd5168446e802b45a5a7667e2b`.
- Archive SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- QA date UTC: `2026-10-27`. Selected IDs in archive manifest: 50/50; historical seasons: 200; ingested: 200/200; not ingested: 0; match rows: 59,049; team rows: 3,366; duplicate match IDs within a season: 0; repeated match IDs across season rows: 0. All 59,049 rows have IDs, parseable kickoff dates and two parseable non-negative integer score fields. Observed date range: 2023-01-20 through 2027-06-06.
- The 50 selected-current-season folders contain 14,051 rows, matching the previously audited selected-season snapshot. This reconciles structural coverage for those folders; it does not prove full primary-window coverage or canonical identity.
- Provider status counts across all 200 seasons: 51,983 `complete`, 6,962 `incomplete`, 57 `suspended`, 47 `canceled`. No missing status/date or invalid score pairs were observed. There are 27 `incomplete` rows with kickoff dates before the audit date (23 in the 50 selected-current-season folders).
- **Critical score/status finding:** all 7,066 non-complete rows with parseable score pairs are 0-0: 6,962 incomplete, 57 suspended and 47 canceled. Zero non-complete rows have a non-zero score pair. The pattern is consistent with default/placeholder 0-0 values; do not treat them as settled scores or training labels.
- Selected 50 current-season rows: 7,040 complete, 6,958 incomplete, 53 suspended; all 7,011 incomplete/suspended rows with score pairs are 0-0.
- The runtime independently corroborates this in its 50-row `oracle_selected50_settlement_truth_qa.csv`: 59,049 source rows, 51,983 complete-status numeric-score rows, 7,066 non-finished numeric-score rows, zero non-integer scores, all rows marked `INTERNAL_STATUS_SCORE_QA_ONLY_OFFICIAL_SETTLEMENT_UNVERIFIED` and `production_eligible=NO`.

### Latest runtime and checks

- Research runtime [40423792877](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423792877) — SUCCESS on commit `44f4a9741c2554277c708334edaefc080d980672`.
- Runtime artifact [12698452196](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423792877#artifacts), ZIP SHA-256 `ef5359a46102f87c222b80b5e1a38793d25d64f3c9f50de55e56817c24ea0f2e`. Output contract: PASS; 50 selected groups, 463 governed fixture rows, 2,315 prediction rows, 250 league-market rows and 750 league-market-fold rows. 437 raw Combo Home and 437 raw Combo Away probabilities masked; zero Combo probabilities remain. All rows remain production- and betting-ineligible.
- Safety contract tests [40423976833](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423976833) — SUCCESS on commit `5ae82c2b13138956b3bbdaa907229cc8dfdfbf56`.
- Dry-run planner [40423939739](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423939739) — SUCCESS on commit `d06a2c0a491cad687c92656638767aab66d7b345`; latest commit-pinned QA workflow validation and dry-run [40423922632](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922632) also succeeded.
- Several intermediate contract/dry-run runs failed while the new test assertions were being introduced (missing-status sentinel and absent zero-count Counter keys). The assertions and counter handling were corrected; the later pinned runs above passed. Do not cite intermediate failures as the final state.

### Current release gates and provider budget

- The QA confirms structural completeness, not official settlement truth. Do not use non-complete 0-0 pairs for training/evaluation. Exact canonical fixture/team joins, parent competition IDs, historical standings as-of-kickoff, point-in-time xG/odds provenance and Combo target/settlement reconciliation remain blocked.
- Provider parent competition IDs verified: 0/50. Provider match-record `competition_id` is documented as a league season ID; it is not a parent competition ID. Provider-to-Oracle canonical bridges remain 0/50.
- No FootyStats API calls were made in this run. Current monthly credits cannot be verified via the available tools, and there is no workflow-dispatch operation. The one-call schema diagnostic remains manual-only; confirm the current FootyStats account credit balance before manually dispatching it with `confirm_provider_credit_usage=true`. No credentials were exposed, no raw payloads were published, and no paid plan was changed.
- Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain untouched. Production readiness remains `NOT_GRANTED`.


## Automation continuation — runtime score quarantine regression and live provider gate (2026-10-27 01:00 UTC)

### Live state inspected
- Research branch head before this change: `b6766482a1d26d970f4de30892396f78d27ffeb7`; latest prior safety contract run [40424163022](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40424163022) succeeded on that exact commit.
- The current private archive QA is pinned to batch-5 release `research-selected50-footystats-history-40375285207` and reads the archive from the private production repository only; no production workflow or file was changed.
- Provider schema diagnostic exists at `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml`. It references the configured `FOOTYSTATS_API_KEY` secret inside the runner, requires explicit `confirm_provider_credit_usage=true`, makes at most one read-only catalogue request, suppresses the raw response, and declares monthly credits unverified. Secret values cannot be read through the available GitHub connector.
- The available GitHub tool connection has no workflow-dispatch operation and cannot inspect FootyStats account monthly credits. No provider API call was made in this automation run. The last historical request-window remaining figure is not current monthly-credit evidence.

### New regression protection
- Commit `6174e54835f0c2f5e68c54ac52571196edeb9590` adds a test to `tests/test_footystats_selected50_bounded_probe_contract.py` that AST-loads the actual runtime score/status functions without importing the full modelling dependency stack.
- The test asserts that numeric 0-0 scores with `incomplete`, `suspended`, `canceled`, or `abandoned` statuses cannot be considered completed; a provider-`complete` 0-0 remains structurally complete (0-0 can be a legitimate final score); missing/negative scores fail closed. It also locks the runtime target assignment and training-row gates to the `finished` flag and confirms future candidate selection excludes finished and canceled/postponed/suspended/void/abandoned rows.
- This is research-only test coverage. No model code, probabilities, calibration, thresholds, production registry or ledger was changed.
- The safety contract workflow checks out the triggering SHA and runs this test file on every push to the research branch. The new run has not yet been observed in the Actions run list at checkpoint time; do not claim this new test has passed until its run is complete.

### Release decision and next action
- Fresh batch-5 archive QA remains the latest successful source QA: [run 40423922693](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693), artifact [12698682583](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693#artifacts), archive SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- All 7,066 non-complete archive rows have 0-0 score pairs; these remain excluded from training/evaluation by the runtime's status-based `finished` gate. Official settlement truth is still unverified.
- The only safe next provider action remains manual dispatch of the one-call schema diagnostic after confirming the current FootyStats account credit balance. The connector cannot dispatch it, so no API calls are claimed.
- Canonical parent competition IDs, provider-to-Oracle bridges, canonical fixture/team joins, official settlement labels, historical standings as-of-kickoff, point-in-time xG/odds provenance, and Combo target/settlement reconciliation remain hard blockers. Production readiness remains `NOT_GRANTED`.


### Follow-up verification — status quarantine test and workflow efficiency (2026-10-27 01:00 UTC)

- Safety contract test run [40429801588](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40429801588) — SUCCESS on commit `6174e54835f0c2f5e68c54ac52571196edeb9590`, including the new AST-based test of runtime status/score quarantine.
- Dry-run planner [40429801626](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40429801626) — SUCCESS on the same test commit; no network/provider calls.
- Added markdown-only path filtering to the safety contract workflow in commit `a25bd78ffd3a891fe90f76744e0bc99ad94c5c85`, then added a regression assertion in commit `86678934620888999c99ec9723413c600e7ab3e4`. This avoids running the safety suite for checkpoint/report Markdown-only changes while still running it for test/code/workflow changes. Both checks succeeded on the final code/test commit: safety [40429893100](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40429893100) — SUCCESS; dry-run planner [40429893103](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40429893103) — SUCCESS.
- The new status/score regression test confirms non-complete 0-0 or non-zero score rows do not pass the runtime's completed-match gate, while a provider-`complete` 0-0 remains structurally completed because a real 0-0 final score is possible. Training targets and candidate selection remain gated on the runtime's `finished` flag.
- This checkpoint update is Markdown-only and is intentionally excluded from the contract-test push trigger; no additional run is expected from this documentation-only commit.
- No provider requests were made. The one-call schema diagnostic is manual-dispatch-only, the available GitHub connector cannot dispatch workflows or read secret values, and current monthly FootyStats credits remain unverified. No credentials or raw provider payloads were exposed.
- Production readiness remains `NOT_GRANTED`; no production repository, model logic, probabilities, calibration, thresholds, registries or ledgers were modified.


## Automation continuation — primary-window per-league archive coverage (2026-10-27 02:00 UTC)

### What changed
- QA script commit [03c0aa66c398648f13e46f283a51e9fdd7857c45](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/03c0aa66c398648f13e46f283a51e9fdd7857c45) adds exact inclusive primary-window coverage calculations for 2025-03-20 through 2026-09-20, calendar-year split metrics, per-season counts, and a 50-row selected-group coverage CSV. The selected-group labels are inherited from the exact selected-season catalogue relationship for research grouping only; they are not canonical Oracle IDs or approved mappings.
- The archive QA now rejects missing or duplicate season IDs in the ingestion manifest rather than silently collapsing them in a dictionary.
- QA workflow commit [ca7b6e8b8098a1930ab22534c374b0be9fefb87e](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/ca7b6e8b8098a1930ab22534c374b0be9fefb87e) validates the new coverage totals, 50 unique selected groups, one selected-current-season ID per group, and all identity/settlement/production flags remaining NO; it publishes the new CSV in the sanitized artifact.
- Contract-test commit [f482ce8e8c73cf6aa81f103f5c55e50cbf29054b](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/f482ce8e8c73cf6aa81f103f5c55e50cbf29054b) adds inclusive-boundary tests, manifest duplicate/missing-ID fail-closed tests, and contract assertions for the per-league artifact.
- Runtime workflow filter commit [94bf3e84aa7a80ec144ba1b9814b11fdd8e030a1](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/94bf3e84aa7a80ec144ba1b9814b11fdd8e030a1) excludes changes to the archive-QA-only script from the expensive model runtime trigger. This prevents future QA-only fixes from automatically starting a full backtest.

### Verified latest QA evidence
- QA run [40435674199](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435674199) — SUCCESS on commit `ca7b6e8b8098a1930ab22534c374b0be9fefb87e`; the primary-window reconciliation validation step passed.
- Sanitized QA artifact [12704500660](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435674199#artifacts), SHA-256 `214820e02ab38568e720d728ee08a44e913ba4a47a0fe365d89084fbb6c42e3d`. The artifact includes `selected50_primary_window_coverage.csv` and `selected50_season_qa.csv`; no raw provider match payloads were exported.
- Safety contract tests [40435682643](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435682643) — SUCCESS on commit `f482ce8e8c73cf6aa81f103f5c55e50cbf29054b`.
- Dry-run planner [40435682706](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435682706) — SUCCESS on the same test commit; no network/provider calls.
- Latest verified branch head before this checkpoint append: `f482ce8e8c73cf6aa81f103f5c55e50cbf29054b`.

### Primary-window coverage findings
- Locked window: 2025-03-20 through 2026-09-20 inclusive.
- Across all 200 archived season folders: 22,291 match records, 22,291 unique provider match IDs, zero duplicate provider IDs across the window; this is provider-record coverage, not a canonical-fixture count.
- Statuses in that window: 22,256 `complete`, 24 `canceled`, 6 `incomplete`, 5 `suspended`.
- All 35 non-complete rows with parseable score pairs are 0-0; none is settlement truth. Keep them quarantined.
- Calendar split: 2025-03-20 to 2025-12-31 = 11,648 records (11,618 complete, 24 canceled, 3 incomplete, 3 suspended); 2026-01-01 to 2026-09-20 = 10,643 records (10,638 complete, 3 incomplete, 2 suspended).
- The selected-current-season folders alone contribute 5,637 records in the locked window (5,633 provider-complete); that is a narrower slice than the 22,291 records across the 200-season archive.
- The group matrix contains exactly 50 unique selected-group labels, exactly one selected-current-season ID per group, and coverage records for all 50 groups. Lowest observed per-group record counts are India Indian Super League 98, Canada Canadian Premier League 206, and Australia A-League 207. These counts do not certify completeness, representativeness, canonical identity, or sufficient backtest sample size. Per-league row counts and status counts are in the artifact CSV.
- Summary marks `primary_window_coverage_is_canonical_fixture_count=false`, `official_settlement_truth_verified=false`, and `production_eligible=false`.

### Provider and release gates
- No FootyStats requests were made in this run. The current monthly credit balance cannot be verified through available tools, and this GitHub connection has no workflow-dispatch action. Existing one-call schema diagnostic remains manual-only with `confirm_provider_credit_usage=true`; do not use the historical request-window remaining value as monthly credit evidence.
- Parent competition IDs verified: 0/50; provider-to-Oracle canonical bridges: 0/50; canonical fixture/team joins and official settlement truth remain unverified. Historical standings-as-of-kickoff and point-in-time xG/odds provenance remain unverified; Combo remains blocked by target/settlement mismatch.
- The runtime run [40435508754](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435508754), started on an earlier QA-script-only commit before the runtime path filter was added, was still in progress at last inspection. It is not needed to verify this QA-only change and must not be represented as complete unless its final status is checked.
- No production repository or workflow was modified. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain unchanged. Production readiness remains `NOT_GRANTED`.


## Follow-up — verified per-league coverage artifact and null-ID guard (2026-10-27 02:00 UTC)

- Fixed a manifest edge case in `scripts/qa_selected50_private_archive.py`: null season IDs are now treated as missing, not stringified as `"None"`. Commit [a63dbdcfdffebd456f4e496998895fdd034f6a29](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/a63dbdcfdffebd456f4e496998895fdd034f6a29). Test for null IDs added in commit [9beaa92289f13519f6c73331501317c991c0d2de](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9beaa92289f13519f6c73331501317c991c0d2de).
- Latest private archive QA run [40435810643](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435810643) — SUCCESS on the QA-script commit; its new primary-window reconciliation step passed. Artifact [12704281575](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435810643#artifacts), 33,063 bytes, SHA-256 `ae68282b86705d9a4275c5d764798e1bfd9c2d3b2e2d3d713db0b182eae9bfc0`. It contains the per-league `selected50_primary_window_coverage.csv` and season-level QA CSV; raw provider match payloads were not exported.
- Safety contract tests [40435818378](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435818378) — SUCCESS on commit `9beaa92289f13519f6c73331501317c991c0d2de`, including null-ID, duplicate-ID, inclusive-window and per-group coverage contract tests.
- Dry-run planner [40435818156](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435818156) — SUCCESS on the same commit; all network-free planning and market-gate checks passed.
- The QA-only runtime trigger exclusion is in commit [94bf3e84aa7a80ec144ba1b9814b11fdd8e030a1](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/94bf3e84aa7a80ec144ba1b9814b11fdd8e030a1). A runtime that had already started before that filter, [run 40435508754](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435508754), subsequently completed SUCCESS on older QA-only commit `63f3f110703e967c115795b4fdca53ade8d3f95e`; artifact [12703552484](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40435508754#artifacts). No model-runtime source was changed by this coverage work.
- Latest verified branch head before this checkpoint append: `9beaa92289f13519f6c73331501317c991c0d2de`.

### Coverage summary confirmed from the latest QA artifact
- 50 selected-group rows; 50 unique country/competition labels; exactly one selected-current-season ID per group; no group has zero primary-window records.
- Primary window (2025-03-20 through 2026-09-20 inclusive): 22,291 archive match records, 22,291 unique provider match IDs, zero duplicate IDs across season folders.
- Status counts: 22,256 `complete`, 24 `canceled`, 6 `incomplete`, 5 `suspended`. All 35 non-complete rows with parseable score pairs are 0-0; they remain quarantined from settled-outcome evaluation.
- Calendar 2025 (2025-03-20 through 2025-12-31): 11,648 records (11,618 complete, 24 canceled, 3 incomplete, 3 suspended). Calendar 2026 (2026-01-01 through 2026-09-20): 10,643 records (10,638 complete, 3 incomplete, 2 suspended).
- The 50 selected-current-season folders contribute 5,637 rows within the window, of which 5,633 are provider-complete. This is a narrower slice than the 22,291 rows across the full 200-season archive.
- Lowest per-group archive counts are India Indian Super League 98, Canada Canadian Premier League 206, and Australia A-League 207. The CSV records every group’s season-folder count, provider-season IDs, year-split rows, status counts and fail-closed flags.
- Group labels are inherited from the exact selected-season catalogue relationship for research grouping only. They are not canonical Oracle IDs. All 50 rows explicitly mark parent competition ID, canonical mapping, canonical fixture/team joins and official settlement truth as unverified, and `production_eligible=NO`.
- QA summary confirms `primary_window_coverage_is_canonical_fixture_count=false`, `official_settlement_truth_verified=false`, and `production_eligible=false`.

### Provider gate
- No FootyStats API calls were made. The current monthly credit balance cannot be read through the available tools, and the GitHub connection has no workflow-dispatch action. The one-call schema diagnostic remains manual-only and capped at one request; only manually dispatch it with `confirm_provider_credit_usage=true` after confirming the current provider credit balance. Do not infer monthly credits from the historical request-window value.
- Provider parent competition IDs and provider-to-Oracle canonical bridges remain 0/50 verified; exact canonical fixture/team joins, official settlement truth, historical standings as-of-kickoff, point-in-time xG/odds provenance and Combo target/settlement reconciliation remain blocked. Production readiness remains `NOT_GRANTED`.
- Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain untouched.


## Follow-up — strict final-score validation in research settlement utility (2026-10-27 03:03 UTC)

- Live branch was inspected before edits; prior head was `ad2efd627ea408ba393e0300be04520a86edbc52`. Current code change commit `7120f61d1508ecf54449a699fa79d59fe08b3006` updates only the research settlement utility to reject final-score values that are non-finite, negative, boolean, malformed, or fractional instead of silently truncating with Python `int()`. The accepted format remains integer-valued score input (including numeric strings such as `"2.0"`).
- Regression tests added in commit `925d6aeceed53b43253656ba6e62df1ff79eb165` for fractional, NaN, infinity, negative, boolean and malformed scores. These are settlement-data integrity guards; no Oracle prediction model or production settlement code was changed.
- Safety workflow now runs both the existing bounded-probe governance contracts and `tests/test_score_market_settlement.py` (commit `f3a634ab8d9514daa43d4f4e840e117f2a1ce418`). The current-head safety run [40441908324](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441908324) completed successfully, including the new score-settlement tests.
- Runtime workflow now ignores pushes that only change `scripts/settle_market_from_final_score.py`, because the runtime builder does not import this utility; this avoids launching a full archive/backtest for utility-only changes. Filter change commit `e61719644cde2352f1f910e62af085c1c145cf1b`.
- Dry-run planner [40441908348](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441908348) had completed all planning and regression-test steps successfully but was still finishing artifact upload when checked. The older runtime and archive-feature-audit jobs triggered by the initial utility commit were still in progress at last inspection; do not represent those as complete until their final statuses are checked.
- No FootyStats API requests were made. The provider schema diagnostic workflow is manual-only, references the existing `FOOTYSTATS_API_KEY` secret without exposing it, and requires `confirm_provider_credit_usage=true`; this GitHub tool connection exposes no workflow-dispatch action and cannot inspect secret values or the current monthly credit balance. Do not infer monthly credits from historical request-window metadata.
- Existing primary-window archive findings remain unchanged: 22,291 records across the 50-group research catalogue for 2025-03-20 through 2026-09-20, but these are not canonical Oracle fixture counts. Parent competition IDs verified 0/50, provider-to-canonical bridges 0/50, canonical fixture/team joins and official settlement truth unverified; Combo remains blocked. All outputs remain research-only and `production_eligible=false`.
- No production repository/workflow was touched; Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain unchanged.

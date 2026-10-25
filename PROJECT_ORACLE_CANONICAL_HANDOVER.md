# Project Oracle — Canonical Handover & Completion Pack
Last reviewed: 2026-10-25
Purpose: single source of truth for continuing the existing Project Oracle without making Nolan repeat decisions or context.

## 1. Non-negotiable objective
Deliver a usable, evidence-backed Oracle prediction report for the governed 50-league universe, with per-fixture market probabilities and the supporting Visual Intelligence needed to judge the fixture:
- recent form (including home/away splits where source data supports it);
- H2H, with the count/window and source freshness visible;
- league position/table context;
- xG/xGA and other feature inputs with their definitions, scale, timestamps and provenance;
- market probability outputs for the governed markets (BTTS, Double Chance, Combo; M-1UP only when its own evidence gate passes);
- confidence/risk profile, data coverage/freshness, and explicit missing/unverified indicators;
- report export that can be used by the user without further reconstruction.

Do not substitute more audits or planning for the next executable step. Every work session must state: (a) artifact changed or run executed, (b) evidence/results, (c) blocker requiring user action, if any, and (d) next concrete action.

## 2. Approved operating constraints
- FootyStats API: user explicitly authorizes using the existing Hobby package within its request/credit/rate/coverage limits. Do not upgrade the package or incur extra charges. Inspect the package's actual limits and API behavior before bulk ingestion; batch/throttle/cache and avoid repeat calls. Never log, commit, or print the API key.
- GitHub: private repository Actions allowance is exhausted until the user's stated reset on 2026-11-01. Do not dispatch/rerun private Actions workflows or ask the user to increase spend. Use the public research repository and its free public-repo Actions runners for safe research/ingestion preparation. Confirm actual workflow permissions/secrets and destination behavior before a live run.
- Public repo: dtnzv5by8c-ship-it/oracle-validation-learning, branch research/oracle-50-league-readiness-audit.
- Private production repo: dtnzv5by8c-ship-it/oracle-football-data, branch main.
- Production safety: do not create a new model, redesign Oracle, change production model logic, probabilities, calibration, thresholds or the frozen historical baseline. The 50-league runtime must be isolated from the legacy 27-league runtime until validation and approval.
- No fabricated fixtures, probabilities, odds, xG, joins, settlement results, backtest metrics or source provenance. Never mark a field verified merely because a value is present.
- Production release status remains NOT_GRANTED until all required gates pass. Research/challenger outputs must be labelled as such and must not be represented as production-approved.
- The user's primary historical modelling window previously locked was 2025-03-20 through 2026-09-20. The user now requests extracting data from 2024 as well; resolve the exact start/end coverage against the Hobby package and data availability before ingesting. Preserve the locked primary window for comparable validation; treat earlier 2024 data as an additional historical extension unless the user explicitly changes that baseline.

## 3. Required workflow — execute, do not endlessly re-plan
1. Inspect current public research branch, current workflow definitions, and the latest run/artifacts before modifying anything.
2. Validate the Hobby API's supported endpoints, pagination, historical coverage, per-season availability, rate/credit limits, and the canonical IDs for the exact selected 50 leagues. Use only confirmed API capabilities.
3. Check the public repo has the required GitHub Actions secrets configured without exposing values: FOOTYSTATS_API_KEY and ORACLE_PRIVATE_REPO_TOKEN. The latter is only needed if the workflow must write a package to the private repository. Never attempt to read secret values.
4. Run a small, low-cost API smoke test on a limited set of exact league/season IDs; record request counts, response schema, timestamps and credit impact. Only then perform bounded/cached ingestion within the Hobby allowance.
5. Build a normalized historical data lake, including fixtures/results and available team/league data from 2024 onward where the API supports it. Store raw/normalized data in a safe private destination; do not publish raw licensed provider data in the public repo unless the provider terms explicitly allow it. Public repo may contain code, schema contracts, sanitized QA and summaries.
6. Validate canonical fixture/team/competition IDs, kickoff time zones, home/away identity, result/settlement truth, season coverage, duplicate rates, missingness, historical as-of timestamps, xG definitions/scales, odds bookmaker/market/timestamp provenance, and current-season recent-form availability. Produce a league-by-league coverage matrix.
7. Build recent form, home/away recent form, H2H, table position, xG features and market inputs from source rows with timestamps. Prevent leakage: only use data available before the fixture kickoff.
8. Execute existing Oracle logic in an isolated 50-league research/challenger path. Do not change production logic or alter probabilities in the frozen 27-league runtime. If the model runtime cannot execute outside private Actions, use a verified public-safe path only if it can run the same code and access data securely; otherwise identify the exact technical access blocker rather than pretending it ran.
9. Backtest chronologically on historical seasons and the locked primary window; report sample sizes, market-level accuracy, calibration/Brier score and log loss where supported, baseline comparison, coverage and failure cases. Do not claim >90% accuracy unless measured on a leakage-safe held-out sample and calibrated appropriately.
10. Generate a fixture-level report for the next available schedule in the 50-league universe. Include probabilities, recent form, H2H, Visual Intelligence, confidence/risk, source freshness and clear unavailable-data flags. No unsupported predictions for fixtures without required inputs.
11. Keep 50-league production eligibility blocked until the canonical joins, settlement truth, point-in-time feature provenance, market-specific validation, exact probability parity against frozen production where applicable, and human release approval all pass.

## 4. Current evidence / known state as of 2026-10-25
- Public research repo: dtnzv5by8c-ship-it/oracle-validation-learning, branch research/oracle-50-league-readiness-audit.
- Private production repo: dtnzv5by8c-ship-it/oracle-football-data, main.
- Latest known public research candidate SHA: e23f0d2da15b7789c86b74dcd355c93df8b4d0c6.
- Latest known passing public CI:
  - Data Gate Contract run 40195483506: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40195483506
  - Dry-Run Planner run 40195483497: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40195483497
  These are contract/dry-run tests; they do NOT prove live API ingestion or production prediction completion.
- Selected-50 data-gate matrix: data/oracle_selected50_data_gate_matrix_2026-10-25.csv. 50 rows/15 columns; all 50 production_eligible=NO; exact canonical joins, settlement truth and point-in-time provenance remain NOT_VERIFIED. The 19 Run56 manifest gaps are reconciliation gaps, not proof the fixtures are absent from the archive.
- Sanitized archive QA previously reported 50/50 selected season IDs, 14,051 records and 14,051 unique season/fixture-ID pairs; 5,637 rows in 2025-03-20–2026-09-20; 11,742 records with recent-form-5 values for both teams; 5,282 H2H prior-meeting rows; 7,330 records with odds-named values; xG-named fields present in 14,051. These are field-presence/archive QA only, not proof of correct semantics, point-in-time availability, settlement approval, market validity or production readiness.
- Two selected seasons (Australia A-League season ID 17326 and India ISL season ID 17964) were flagged as having insufficient current-season history with prior-season history unverified.
- Private fixture file was last observed with fixtures through 2026-10-17; its manifest was generated 2026-10-08 and declared 27 active leagues. It is stale for a current 50-league prediction report.
- Private production status last observed declared 27 active leagues, 70 fixtures, development/challenger gates; M-1UP had insufficient out-of-sample evidence. A 50-league production runtime is not yet verified.
- The public live-ingestion workflow .github/workflows/oracle-selected50-footystats-live-ingestion.yml is manual-dispatch only and requires confirm_provider_credit_usage=true, FOOTYSTATS_API_KEY and ORACLE_PRIVATE_REPO_TOKEN. It now resolves the governed 50 selected season IDs to their exact parent competitions and targets provider seasons whose year starts at 2023, so calendar-2024 season overlaps are included. It throttles successful calls to 2.1 seconds (conservative against Hobby's published 1,800 requests/hour) and counts attempted requests. It packages raw data only for the private release; the public artifact is sanitized. It has not been dispatched. The connected GitHub tools expose run inspection but not workflow dispatch, so Nolan must click Run workflow once the secrets are confirmed.
- Known workflow: .github/workflows/oracle-selected50-footystats-live-ingestion.yml (verify exact current path/name from the live branch before action).

## 5. Current decisions — do not ask Nolan to repeat
- Use the existing FootyStats Hobby package within its limits; user has explicitly authorized its use for the project.
- Use the public repository while private Actions is capped. Do not rerun private workflows before 2026-11-01.
- Continue the existing Project Oracle; no redesign/new model and no production logic changes.
- Target 50 leagues, not 27, for the new isolated data/runtime/report path.
- User wants actual completion and usable predictions, not another cycle of apologies, status-only audits, or repeated handover prompts.
- User wants a persistent handover/memory pack to be consulted whenever continuing in a new chat.

## 6. User input still required only if technically necessary
Do not ask for confirmation of authorization already given. Ask only if the next step truly cannot proceed without an answer—for example, if the Hobby dashboard/package terms show an ambiguous credit cap or a workflow requires Nolan to click Run workflow because the connected GitHub integration cannot dispatch it. If a manual action is needed, give one precise instruction and state exactly what will happen, expected credit use if knowable, and how to verify success.

## 7. Definition of done
Done means a real, traceable run has ingested supported historical/current data within the Hobby limit; validated and reported 50-league coverage; built leak-safe recent form/H2H/table/xG/odds features with provenance; run the existing model in an isolated 50-league research path; backtested market probabilities honestly; and generated a usable next-fixture report with Visual Intelligence and explicit risk/data gaps. Production remains blocked until its own governance gates pass.

## 8. Implementation update — 2026-10-25
- User has explicitly authorized use of the existing FootyStats Hobby API package within its plan limits. Do not ask for this authorization again.
- Official FootyStats API pages state Hobby includes up to 50 chosen leagues and 1,800 requests/hour; league-list returns season IDs, historical availability varies by league, and league-matches supports pagination up to 1,000 matches per page. Do not confuse request rate limits with a separate monthly credit pool.
- Updated the selected-50 ingestion workflow on the research branch to collect all provider seasons with season year >= 2023 for the 50 selected competitions (captures 2023/24 seasons overlapping calendar 2024), fetch match, team stats, table and season stats, and keep raw data out of public artifacts. Calls are throttled at 2.1 seconds after successful responses.
- Added tests/test_footystats_ingestion_workflow_contract.py to verify the explicit provider-credit gate, secrets guards, 50-league manifest, historical season expansion, Hobby throttling, raw-data privacy and embedded Python syntax.
- CI run 40196322870 failed because one test assertion's capitalization did not match the workflow comment. That assertion was corrected in commit 7fb0b66a131407726248ff55dedc30a5fc323a99. Verify the subsequent candidate run before treating the safety-test suite as green.
- Latest ingestion workflow code commit before the test fix: f5ea4d5637eea628f020cda8d805aad43a06adb7. Refresh this handover whenever material workflow/run status changes.
- Next action is not another audit: verify the new public CI result, then have Nolan trigger the manual ingestion workflow with confirm_provider_credit_usage=true. If the workflow reports a missing secret or insufficient private release permission, stop and report the exact missing item without exposing secrets or retrying API calls.

# Project Oracle — 50-League Readiness Audit Checkpoint
- Run date: 2026-10-24 (SAST)
- Branch: `research/oracle-50-league-readiness-audit`
- Scope: owner-selected 50 FootyStats competitions; research/reporting only
- Decision: **NOT COMPLETE — production eligibility NOT GRANTED**

## Live source verification
The owner-selected manifest was fetched from the research branch and contains exactly 50 numbered rows. Blob SHA: `f6f9069b692b79a7595d1513a3413e8660763632`.
- Manifest: [50-league selected manifest](oracle-footystats-selected-50-league-manifest-2026-10-24.md)
- Current protected registry fetched from the private canonical repository: `config/oracle_major_league_registry_v1.json`, blob SHA `81d6db487e498fc84a87a7457b0de7215537f15c`. It declares a 27-league active universe. This audit does not change it.
- Existing canonical readiness matrix fetched: `data/league_readiness_matrix.csv`, blob SHA `602061ebe0ecbe45b0ed6e5c6dcbf2c9d9c0f8b7` (see source SHA verification below; use repository blob SHA as returned by GitHub). Matrix refresh timestamp is 2026-10-01T17:25:35.759116Z, so it is stale for a current-readiness decision.
- Existing four-model readiness snapshot: `data/oracle_four_model_readiness_v1.2.json`, effective date 2026-10-01; 11,364 controlled rows across the old 27-league universe, max result date 2026-09-20; BTTS/DC/Combo coverage reported full for 22 and partial for 5. These aggregate results cannot be assigned to the 50 selected provider IDs without a verified crosswalk.

## Evidence currently supported
- Existing archive audit (research report and prior workflow artifact): 35,819 match records across 126 season groups; 28,491 records with settled status and complete scores; 34,083 rows with provisional standings for both sides (95.2%); no parser errors and no duplicate fixture IDs in that audit.
- Existing archive evidence reports 42 distinct provider competition names in the ingested manifest versus 43 in a prior selected-catalogue audit. Difference remains unresolved.
- Historical xG field presence is not proof that the values were available before kickoff. Point-in-time xG/odds provenance remains unverified.
- Current archive-level totals are not per-selected-league coverage. No historical/current fixture counts, team-ID coverage, recent-form availability, or standings coverage are allocated to the selected 50 without exact provider-ID-to-competition evidence.
- Existing production/research prediction audit remains blocked: 210 staged challenger rows, no verified fixture identities, and no eligible rows for a defensible scoring calculation; canonical settlement and scorecard ledgers were previously reported empty. No accuracy or profitability claim is supported.

## Crosswalk status
The row-level [50-league crosswalk/readiness register](oracle-50-league-crosswalk-readiness-register-2026-10-25.md) remains the scope-of-record. All 50 rows are retained; canonical mapping is `UNRESOLVED` unless exact provider ID + country + competition evidence ties the provider competition to a canonical code. A same/similar display name alone is insufficient. The private registry's 27 entries are reference evidence only, not a replacement scope. Any future candidate code must be labelled candidate/review-required, never approved.

## Latest workflow inspection
The latest 10 validation-repository workflow runs fetched from GitHub API were all H2H reporting or exact-ID join tests on branch `fix/h2h-run31-diagnostic-remediation`, not the 50-league audit:
- [H2H Reporting run #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720): completed successfully, event `pull_request`; artifact `oracle-h2h-report-47`, ID `12573751940`, SHA-256 `549d8352e939d076bfc764ab8730ced15ec7b5d5bc51026831dd5ddf59231c3f`.
- [H2H exact-ID join tests run #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716): completed successfully.
- Several adjacent H2H reporting runs were cancelled while their exact-ID tests succeeded. These are not evidence that a 50-league refresh or readiness gate ran.
- No 50-league-specific workflow dispatch was performed in this checkpoint. The available evidence does not establish a safe supported workflow for refreshing provider data or calculating per-league/per-market readiness, so no provider refresh was attempted.

## Required blockers before completion
1. Produce a machine-readable, row-level link from each of the 50 exact FootyStats IDs to exact archive competition/season records and (where justified) a candidate canonical code; resolve the 42-vs-43 archive catalogue discrepancy.
2. Calculate per-league historical/current fixture counts, source freshness, exact home/away team-ID coverage, recent-form and standings availability, and field missingness from actual artifacts.
3. Verify xG and bookmaker odds point-in-time provenance; absent timestamp/snapshot proof must remain gated.
4. Assess each supported market separately using registry requirements: BTTS Yes, Double Chance, DC Under 4.5/Combo, and M1UP. M1UP requires chronological goal events and pre-match team state; it must remain event-truth-gated where event coverage is not verified.
5. Run the relevant research-only tests and inspect their generated artifacts. Verify chronological out-of-sample evaluation, calibration, stability, and governance gates before any production eligibility decision.

## Safety and governance
No production code, model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry, or canonical ledger was modified. No PR was merged, no gate bypassed, and no provider purchase/change was made.

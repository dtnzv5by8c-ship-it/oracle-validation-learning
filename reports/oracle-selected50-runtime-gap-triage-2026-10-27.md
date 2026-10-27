# Oracle Selected-50 Runtime Gap Triage and Regression Evidence — 2026-10-27

## Scope and evidence boundary

This is a research-only follow-up to Research Runtime run #112. It reads the existing sanitized artifact and repository code; it makes no FootyStats API calls and does not alter production data or model logic.

- Runtime run: [40554064150](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150), run #112, completed successfully at 2026-10-27 17:50 UTC.
- Artifact: [12757295232](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232), `oracle-selected50-research-runtime-report.zip`.
- Artifact SHA-256 reported by GitHub: `983a4f3cc09dcb94ab03e7693bc65ad46ed23cf4cdd2d92d05f543a75cfdbf50`.
- Runtime source commit: `adae74577d9f5c73f4981ec69c8d3068fd718fac`.
- Follow-up contract/planner fix commit: `3f09de48d356dd31c077d8a28ddacdc5d6d8005d`.
- Safety contract workflow: [run #148 / 40556270993](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40556270993), success.
- Dry-run planner: [run #455 / 40556271022](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40556271022), success.

The runtime artifact is a valid research snapshot, not a production release certificate. The runtime code itself was not changed by the follow-up test repair.

## 1. Regression defect repaired

The earlier contract-test and planner runs failed because two assertions looked for runtime JSON metadata in the workflow YAML. The metadata is emitted by `scripts/oracle_selected50_provider_schema_diagnostic.py`; the workflow YAML owns the manual-dispatch and pre-request confirmation guards.

The test now reads both files and verifies:
- provider-credit and monthly-credit confirmation are manual-dispatch inputs, defaulting to false;
- the workflow stops before invoking the diagnostic unless both confirmations are true;
- the diagnostic script reports `planned_api_requests=1`, `hard_request_cap=1`, `monthly_credit_budget_verified=false`, and secret/payload-suppression flags;
- the script's provider endpoint is checked in the script, not incorrectly searched for in YAML.

Evidence after the fix:
- Safety contract workflow #148 passed: 22 bounded-probe contract tests and 17 score/settlement contract tests; no failures.
- Dry-run planner #455 passed, including the bounded-probe governance tests and the other planner, identity, settlement, market-gate, and walk-forward checks.
- Both workflows ran on commit `3f09de48d356dd31c077d8a28ddacdc5d6d8005d`. No paid-provider calls were made by these checks.

## 2. Runtime and 250-row market-readiness result

Artifact contract result: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.

| Measure | Verified result |
|---|---:|
| Selected season-ID groups | 50 |
| Source season rows loaded | 200 |
| Deduplicated historical match rows | 59,049 |
| Explicitly completed historical rows | 51,983 |
| Future-fixture candidates in seven-day horizon | 461 |
| Fixture groups with at least one scheduled candidate | 47 |
| Fixtures with raw research probabilities | 435 |
| Fixtures blocked by feature support | 26 |
| League-market readiness rows | 250 (50 groups × 5 markets) |
| League-fold rows | 750 |
| Production-eligible market rows | 0/250 |
| Combo probabilities left visible in governed report | 0 |
| Production model logic changed | false |
| Production probabilities changed | false |

The five markets are BTTS, DC_HOME, DC_AWAY, COMBO_HOME, and COMBO_AWAY. Every one of the 250 rows has `production_eligible=NO`; every provider parent-competition ID is unavailable in the archive manifest. Per-league sample gates are not sufficient for release: even where the sample gate is met, stability, canonical identity, official settlement truth, point-in-time provenance, calibration, and verified odds/ROI evidence remain open.

### Per-market fold-stability distribution

These are diagnostics against league prevalence, not betting-edge claims.

| Market | Positive Brier skill in all available folds (diagnostic only) | Mixed across folds | No positive skill across folds | Insufficient fold sample/metric | Production eligible |
|---|---:|---:|---:|---:|---|
| BTTS | 3 | 23 | 4 | 20 | NO (all 50 rows) |
| DC_HOME | 17 | 13 | 0 | 20 | NO (all 50 rows) |
| DC_AWAY | 19 | 11 | 0 | 20 | NO (all 50 rows) |
| COMBO_HOME | 12 | 16 | 2 | 20 | NO (all 50 rows) |
| COMBO_AWAY | 18 | 12 | 0 | 20 | NO (all 50 rows) |

For each market, 49/50 groups pass the minimum train/test sample gate but still require stability and odds validation; one group remains below the minimum sample gate. Raw walk-forward metrics are uncalibrated and do not establish profitability. The separate BTTS primary holdout's 53.588% threshold accuracy remains below its 54.143% majority-class baseline.

## 3. Root cause of the 26 feature-blocked fixtures

Code inspection confirms the research runtime uses a strict 20-feature vector. Each side's seven recent-form features are emitted only when at least five completed matches in the relevant home/away orientation are available. Pairwise features are then derived from the side features. The prediction function returns no probability if any required feature is null. No imputation is performed.

Artifact evidence:
- 26/26 blocked rows have fewer than five prior home matches for the home side, fewer than five prior away matches for the away side, or both.
- Home-side history is below five in 17 rows; away-side history is below five in 10 rows; one row has both sides below five.
- 25 rows show 35% feature coverage (7/20); one row shows 0% (0/20).
- These counts explain the feature-side block. The report artifact does not expose per-fixture model-fit internals, so no additional model-training failure is asserted.
- The current report's generic block reason is safe but underspecified. These fixtures remain blocked; there is no evidence-supported feature value to invent or impute.

| Fixture ID | Kickoff UTC | Country / competition | Fixture | Home prior home matches | Away prior away matches | Input coverage |
|---:|---|---|---|---:|---:|
| 8614496 | 2026-10-27 19:00 | Italy / Serie B | Vicenza – Modena | 3 | 5 | 35% |
| 8614468 | 2026-10-28 19:00 | Italy / Serie B | Juve Stabia – Hellas Verona | 5 | 3 | 35% |
| 8614546 | 2026-10-28 19:00 | Italy / Serie B | Carrarese – Arezzo | 5 | 4 | 35% |
| 8572687 | 2026-10-30 17:30 | Germany / 2. Bundesliga | Energie Cottbus – Bochum | 4 | 5 | 35% |
| 8572270 | 2026-10-30 19:30 | Germany / Bundesliga | Elversberg – Mainz 05 | 3 | 5 | 35% |
| 8583531 | 2026-10-31 10:30 | Turkey / Süper Lig | BB Erzurumspor – Çorum Belediyespor | 4 | 5 | 35% |
| 8573896 | 2026-10-31 11:00 | Portugal / LigaPro | Amarante – Porto II | 4 | 5 | 35% |
| 8568598 | 2026-10-31 11:00 | Ukraine / Ukrainian Premier League | Livyi Bereh – Bukovyna | 5 | 4 | 35% |
| 8572597 | 2026-10-31 12:00 | Germany / 2. Bundesliga | Wolfsburg – Osnabrück | 4 | 5 | 35% |
| 8584398 | 2026-10-31 13:00 | Spain / Segunda División | Real Sociedad II – Girona FC | 5 | 4 | 35% |
| 8623411 | 2026-10-31 13:30 | South Africa / Premier Soccer League | Milford – Sekhukhune United | 4 | 5 | 35% |
| 8550587 | 2026-10-31 13:45 | Poland / Ekstraklasa | Wieczysta Kraków – Jagiellonia Białystok | 4 | 5 | 35% |
| 8614227 | 2026-10-31 14:00 | Italy / Serie B | Cremonese – Benevento | 5 | 3 | 35% |
| 8572538 | 2026-10-31 14:30 | Germany / Bundesliga | Schalke 04 – RB Leipzig | 3 | 5 | 35% |
| 8572559 | 2026-10-31 14:30 | Germany / Bundesliga | Borussia M'gladbach – Paderborn | 5 | 3 | 35% |
| 8620732 | 2026-10-31 14:55 | Saudi Arabia / Professional League | Al Feiha – Al Faisaly | 5 | 4 | 35% |
| 8557813 | 2026-10-31 15:00 | England / Premier League | Coventry City – Sunderland | 4 | 5 | 35% |
| 8558098 | 2026-10-31 15:00 | England / Premier League | Hull City – Ipswich Town | 4 | 5 | 35% |
| 8623413 | 2026-10-31 18:15 | South Africa / Premier Soccer League | Kruger United – Richards Bay | 4 | 5 | 35% |
| 8572852 | 2026-10-31 19:30 | Germany / 2. Bundesliga | Karlsruher SC – Heidenheim | 5 | 4 | 35% |
| 8562297 | 2026-10-31 19:45 | Belgium / Pro League | Waasland-Beveren – Union Saint-Gilloise | 4 | 5 | 35% |
| 8548576 | 2026-10-31 19:45 | France / Ligue 1 | Troyes – Le Mans | 4 | 4 | 0% |
| 8573871 | 2026-11-01 11:00 | Portugal / LigaPro | FC Vizela – Académica Coimbra | 5 | 4 | 35% |
| 8614510 | 2026-11-01 14:00 | Italy / Serie B | Arezzo – Ascoli | 4 | 5 | 35% |
| 8562283 | 2026-11-01 17:30 | Belgium / Pro League | Lommel United – KAA Gent | 4 | 5 | 35% |
| 8604050 | 2026-11-02 17:30 | Greece / Super League | Kalamata – Iraklis Thessaloniki | 4 | 5 | 35% |

**Disposition:** keep all 26 rows blocked. Do not relax the five-match gate, fill missing values with zero, substitute unverified cross-season identity, or alter production logic. Any future research-only feature change would need a separately versioned experiment and fresh out-of-sample evaluation.

## 4. Schedule-freshness check — only the three flagged groups

The existing runtime schedule snapshot contains no fixture in the seven-day horizon for these three groups. The calendar-year coverage artifact has observed 2026 archive rows for each, but zero observed 2027 rows. These facts establish a gap in the current snapshot, not whether the feed is stale or the competition is simply between seasons. No provider API call or official external schedule check was performed in this audit.

| Selected season ID | Country / competition | Archive rows | Explicitly completed rows | 2026 calendar-year rows (completed) | 2027 rows observed | Upcoming fixtures in seven days | Finding |
|---:|---|---:|---:|---:|---:|---:|---|
| 16741 | Canada / Canadian Premier League | 463 | 463 | 112 (112) | 0 | 0 | Freshness unresolved; season timing vs schedule gap not distinguishable from this artifact |
| 16789 | China / Chinese Super League | 960 | 952 | 240 (232) | 0 | 0 | Freshness unresolved; season timing vs schedule gap not distinguishable from this artifact |
| 16627 | South Korea / K League 1 | 882 | 882 | 198 (198) | 0 | 0 | Freshness unresolved; season timing vs schedule gap not distinguishable from this artifact |

No missing fixture was synthesized. All three groups remain production-ineligible. Resolution requires an approved source check or later verified schedule evidence, not a guessed fixture.

## 5. Settlement, identity and production-integrity gates

- Archive settlement/status QA: 59,049 deduplicated rows; 51,983 explicitly completed; 7,066 non-complete rows have numeric 0–0 placeholders (6,962 incomplete, 57 suspended, 47 canceled). Non-complete placeholders remain excluded from settled truth.
- Selected season IDs matched to provider season-ID fields: 50/50. Direct parent competition IDs verified: 0/50. Provider-to-Oracle canonical bridges verified: 0.
- Existing 27-league registry candidates: 22 require human review; 28 have no candidate match; approved mappings: 0.
- All 461 current fixture rows have unverified canonical fixture joins, unverified canonical team joins, and settlement truth marked `NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC`.
- Combo home/away probabilities remain masked. No betting edge or ROI claim is made.
- Oracle V1.6 production benchmark and V1.6.3 Master Development Model are preserved. No production model logic, probabilities, thresholds, calibration, protected registry, ledgers, governance, or production workflow was changed.
- Production eligibility and betting eligibility remain `NOT_GRANTED` for all 50 groups and all 250 market rows.

## 6. Release decision

**RESEARCH QA: PASS for the verified artifact and regression checks. PRODUCTION/BETTING RELEASE: NOT APPROVED.**

The research-only contract-test defect is repaired and the relevant safety and dry-run workflows pass. The substantive identity, official settlement truth, canonical joins, point-in-time provenance, calibration and verified-odds gates remain open. All 50 groups stay ineligible unless every evidence gate passes and explicit release approval is recorded.

### Remaining permission-dependent action

The identity endpoint follow-up remains a draft. Before any FootyStats call, the account holder must verify the current monthly credit balance and explicitly approve a strictly bounded one-request diagnostic. This audit did not request a key, call the provider, or purchase/upgrade anything.


## Runtime/regression addendum — 2026-10-27, run #116

**Current verified runtime:** [Run #116 / 40564605057](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564605057), source commit `61ffc6dbfe83b43c4cf4a2da153550dd2f84203f`, success.  
**Current artifact:** [Artifact 12761018892](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564605057/artifacts/12761018892), SHA-256 `0ee27fffd3f03289dde95eddf811910e2aba35f8dfb9872f9c498e9d75043131`, 14 files, expires 2026-11-10 18:59:07 UTC.

### Verified runtime and regression results

- Combo target regression: **4/4 tests passed**. The tests preserve the documented predictor target, expose the low-goal settlement disagreement, retain the five-goal loss case, and test export masking.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Current output: 50 selected groups, 250 league-market readiness rows, 750 league-market-fold rows, 15 aggregate market/fold rows, and 456 fixture rows.
- Both exported CSVs contain **zero visible Combo probabilities**: 456/456 prediction-report rows carry `combo_probability_status=BLOCKED_SETTLEMENT_SPEC_MISMATCH`; both Combo columns are blank in the prediction report and the governed report.
- All rows remain production-ineligible; production and betting eligibility remain false. Parent competition IDs verified: 0/50; provider-to-canonical bridges verified: 0.
- The run reads the existing private archive and makes no provider API calls.

### Combo decision — preserve the disagreement, do not redefine it

PR [#26](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/26) restored the existing research/predictor target to **Double Chance AND 2–4 total goals inclusive**. The settlement helper still accepts **Double Chance AND total goals <5**, including 0–1 total-goal outcomes. The disagreement is real: Home Combo differs at 0–0 and 1–0; Away Combo differs at 0–0 and 0–1. PR [#28](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/28) corrected the validation output to describe this as unresolved and added fail-closed assertions. Combo probabilities remain blocked pending an authoritative market definition, canonical fixture/team joins, and official settlement truth.

### Feature/training support block — current rolling horizon

The current run has **25 fixture rows blocked by unsupported features**. The prior run had 26; this one-row decrease is a rolling horizon/minimum-lead-time effect, not a feature repair.

- 16 of 25 have fewer than five prior home matches in the required home orientation.
- 10 of 25 have fewer than five prior away matches in the required away orientation.
- One fixture has both sides below five; the union is 25 rows.
- 24 rows have 35% feature coverage (7/20); one has 0% (both histories below five).
- The code requires all 20 features and returns no probability when any required feature is null; it does not impute. The artifacts support a feature-support explanation. They do not expose per-fixture model-fit internals, so no separate model-training failure is asserted.

### Artifact supersession and safety note

- Run #114 artifact [12762340995](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40563743594/artifacts/12762340995) is **superseded and must not be used**: its prediction CSV exposed raw Combo values even though the governed CSV masked them.
- Run #115 artifact [12761018459](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564105545/artifacts/12761018459) masks Combo values, but its runtime-validation JSON still carried stale wording about the target being resolved; it is superseded by run #116.
- These older GitHub artifacts remain available until their retention expiry. Use run #116 as the current runtime artifact.
- The earlier note above that the identity endpoint request remained a draft has since been superseded: the separately approved one-call probe completed successfully in [run 40562430790](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790). It confirmed only the selected Argentina season record; it did not verify any parent competition ID. No further provider requests are authorized by that result.

**Final runtime decision:** research runtime and output-contract QA pass. Combo, production, and betting release gates remain blocked. Oracle V1.6/V1.6.3 production logic and probabilities remain unchanged.


## Runtime support-gate diagnostics improvement — 2026-10-27

The latest verified runtime artifact is Run #116 ([workflow run 40564605057](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564605057)), based on code commit `61ffc6dbfe83b43c4cf4a2da153550dd2f84203f`; artifact `12761018892` (SHA-256 `0ee27fffd3f03289dde95eddf811910e2aba35f8dfb9872f9c498e9d75043131`). It contains 456 fixture rows: 431 with at least one raw research-market probability and 25 with none. The earlier Run #112 had 26 blocked rows; the difference is the rolling seven-day horizon/minimum-lead-time selection, not a feature repair.

Code review found that the report used the generic `NO_PREDICTION_FEATURE_OR_TRAINING_GATE` status without recording which gate failed per fixture. This research-only patch adds:
- exact missing required feature names and a 20-feature support status;
- per-market model-training availability and eligible training row counts;
- an explicit block reason distinguishing missing features, model-training failure, combined failure, and supported research prediction;
- fail-closed output-contract checks and unit tests for these classifications.

This is reporting/diagnostic metadata only. It does not impute features, alter model fit criteria, change probabilities, or loosen release gates. Combo remains masked in every exported prediction report; production and betting eligibility remain `NOT_GRANTED`.


## Support-gate diagnostic validation — Run #118 (2026-10-27)

- Runtime run [#118 / 40568181225](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181225): **SUCCESS**.
- Runtime code commit: `3c2fa91b681b92941ab1d058992564abc52263b5`.
- Artifact: [`oracle-selected50-research-runtime-report` / 12763094895](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181225/artifacts/12763094895).
- Artifact ZIP SHA-256: `b303635b788b2dc538d98aee237bab4ba9ebecaf589acbdeaba36f008276c5d7` (matches the GitHub artifact digest).
- The new per-fixture support-diagnostics unit test passed; the runtime output contract passed.
- Combo target/settlement tests passed in Run #118, and the three Combo settlement-governance regression tests plus diagnostic-output validation passed in [dry-run planner Run #462 / 40568181013](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181013). The safety contract workflow also passed in [Run #156 / 40568181168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181168).

### Evidence-backed diagnosis of blocked fixture rows

The refreshed artifact contains 456 fixture rows: **431** have at least one raw research-market probability and **25** have none. The previous Run #112 had 26 blocked rows; the one-row difference is the rolling horizon/minimum-lead-time effect. Vicenza–Modena (fixture `8614496`, kickoff 2026-10-27 19:00 UTC) had left the upcoming-fixture horizon, not been repaired.

The new output-contract summary records:
- `feature_support_blocked_rows = 25`
- `rows_with_any_unavailable_market_model = 0`
- `rows_without_any_supported_prediction = 25`
- `prediction_block_reason_counts = {BLOCKED_MISSING_REQUIRED_FEATURES: 25, RESEARCH_PREDICTION_AVAILABLE: 431}`

All 25 blocked fixtures have `training_support_status=PASS_ALL_MARKET_MODELS`; all five market models have 44,568 eligible training rows at the relevant target cutoff. Therefore, the artifact supports a **feature-support failure, not a model-training failure**, for these rows:
- 24 rows have 35% feature coverage (7/20 features), because one side has fewer than five completed prior matches in its required home/away orientation; the seven side-specific fields and six dependent pair/environment fields are missing.
- One row, Troyes–Le Mans (`8548576`), has 0% coverage because both required histories are below five; all 20 features are missing.
- Across the 25 rows, 16 have fewer than five prior home matches and 10 have fewer than five prior away matches; one fixture is counted in both groups.

No imputation or model-logic change was introduced. The output now names missing features and records training support per market, making this distinction machine-checkable. Combo probabilities remain masked in both exported CSVs, and production/betting eligibility remains `NOT_GRANTED`.


## Run #119 update — computed Combo disagreement audit (2026-10-27)

The runtime was rerun after research-only PR #29 merged as commit `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`. See the full [Run #119 runtime/regression checkpoint](oracle-selected50-runtime-regression-checkpoint-2026-10-27-run119.md).

- Workflow Run #119: [40577750724](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724), success.
- Artifact: [12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010), 14 files, SHA-256 `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca` (local digest matches GitHub).
- The runtime target-contract tests passed 5/5, including the original home/away/five-goal cases, export masking, and the new disagreement-counter test. Feature/training diagnostics passed 4/4. Output validator returned `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- The per-league Combo disagreement counters were previously hard-coded to zero by omission (initialized but never incremented). PR #29 now calculates disagreements on deduplicated, explicitly finished records with valid integer scores only; nonfinal numeric placeholders are excluded.
- Computed internal QA counts: **9,335 home-side** and **8,017 away-side** predictor-versus-settlement disagreement rows. All 50 groups have nonzero counts for both sides. Aggregate counters reconcile to the 50 per-league QA rows.
- These are internal status/score diagnostics, not official settlement truth. Combo probabilities remain blank in both exports.
- Current rolling-horizon output: 459 fixture rows, 459 unique IDs, 2,295 prediction rows, 25 feature-blocked fixtures, 434 with at least one research-market prediction, zero unavailable market models. The change from the previous run's 456 rows reflects the rolling horizon, not model improvement.
- Parent competition IDs remain 0/50 verified; canonical bridges remain 0. Production/betting eligibility remains `NOT_GRANTED`. Production model logic and probabilities remain unchanged.

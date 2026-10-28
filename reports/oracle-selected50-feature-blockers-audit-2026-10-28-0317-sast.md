# Selected-50 Runtime — Feature/Training Blocker Audit

**Audit timestamp:** 2026-10-28 03:17 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Runtime source commit tested:** `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2`  
**Branch head at audit start:** `fbee3d414376b72aae342dc3038fa1cc105fe4e7` (documentation-only changes after runtime commit)  
**Runtime run:** [#120 / 40608511893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893)  
**Artifact:** [#12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212)  
**Artifact SHA-256:** `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`

## Verification result

- Runtime job completed successfully; all 12 job steps, including archive guard/checksum, Combo target tests, feature/training diagnostics, runtime generation, output validation and upload, succeeded.
- Combo predictor-target regression tests: 5/5 passed.
- Per-fixture feature/training support tests: 5/5 passed.
- Combo settlement-governance tests: 3/3 passed in Dry-Run Planner [#465 / 40608512212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608512212).
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Dry-run planner logged zero network calls and zero paid-provider calls.
- Artifact was downloaded and inspected locally; independently computed SHA-256 matches GitHub.
- Both prediction and governed reports contain 460 unique fixture IDs. Both Combo probability columns are empty in both exports.
- Production and betting eligibility remain false.

## Exact current blocked-fixture diagnosis

The report has 460 upcoming fixture rows: 435 have supported raw research-market outputs, and 25 are blocked by required features. No fixture is blocked by model-training availability.

Every blocked row has:
- `prediction_status=BLOCKED_MISSING_REQUIRED_FEATURES`
- `feature_support_status=BLOCKED_MISSING_REQUIRED_FEATURES`
- `training_support_status=PASS_ALL_MARKET_MODELS`
- 44,568 eligible training rows for each of BTTS, DC_HOME, DC_AWAY, COMBO_HOME and COMBO_AWAY.

The feature builder requires at least five completed matches in the relevant orientation, strictly before kickoff. The 25 blocked rows partition into 15 missing home-side history only, 9 missing away-side history only, and 1 missing both sides. That is 16 fixtures with home count below five, 10 with away count below five, with one fixture overlapping. Twenty-four rows retain the seven features from the adequately supported side (35% of 20 features); one row has no supported side features (0%).

| Fixture ID | Kickoff UTC | League | Home | Away | Home prior-home n | Away prior-away n | Missing side |
|---:|---|---|---|---|---:|---:|---|
| 8614468 | 2026-10-28 19:00 | Italy — Serie B | Juve Stabia | Hellas Verona | 5 | 3 | Away |
| 8614546 | 2026-10-28 19:00 | Italy — Serie B | Carrarese | Arezzo | 5 | 4 | Away |
| 8572270 | 2026-10-30 19:30 | Germany — Bundesliga | Elversberg | Mainz 05 | 3 | 5 | Home |
| 8572687 | 2026-10-30 17:30 | Germany — 2. Bundesliga | Energie Cottbus | Bochum | 4 | 5 | Home |
| 8548576 | 2026-10-31 19:45 | France — Ligue 1 | Troyes | Le Mans | 4 | 4 | Both |
| 8550587 | 2026-10-31 13:45 | Poland — Ekstraklasa | Wieczysta Kraków | Jagiellonia Białystok | 4 | 5 | Home |
| 8557813 | 2026-10-31 15:00 | England — Premier League | Coventry City | Sunderland | 4 | 5 | Home |
| 8558098 | 2026-10-31 15:00 | England — Premier League | Hull City | Ipswich Town | 4 | 5 | Home |
| 8562297 | 2026-10-31 19:45 | Belgium — Pro League | Waasland-Beveren | Union Saint-Gilloise | 4 | 5 | Home |
| 8568598 | 2026-10-31 11:00 | Ukraine — Premier League | Livyi Bereh | Bukovyna | 5 | 4 | Away |
| 8572538 | 2026-10-31 14:30 | Germany — Bundesliga | Schalke 04 | RB Leipzig | 3 | 5 | Home |
| 8572559 | 2026-10-31 14:30 | Germany — Bundesliga | Borussia M'gladbach | Paderborn | 5 | 3 | Away |
| 8572597 | 2026-10-31 12:00 | Germany — 2. Bundesliga | Wolfsburg | Osnabrück | 4 | 5 | Home |
| 8572852 | 2026-10-31 19:30 | Germany — 2. Bundesliga | Karlsruher SC | Heidenheim | 5 | 4 | Away |
| 8573896 | 2026-10-31 11:00 | Portugal — LigaPro | Amarante | Porto II | 4 | 5 | Home |
| 8583531 | 2026-10-31 10:30 | Turkey — Süper Lig | BB Erzurumspor | Çorum Belediyespor | 4 | 5 | Home |
| 8584398 | 2026-10-31 13:00 | Spain — Segunda División | Real Sociedad II | Girona FC | 5 | 4 | Away |
| 8614227 | 2026-10-31 14:00 | Italy — Serie B | Cremonese | Benevento | 5 | 3 | Away |
| 8620732 | 2026-10-31 14:55 | Saudi Arabia — Professional League | Al Feiha | Al Faisaly | 5 | 4 | Away |
| 8623411 | 2026-10-31 13:30 | South Africa — Premier Soccer League | Milford | Sekhukhune United | 4 | 5 | Home |
| 8623413 | 2026-10-31 18:15 | South Africa — Premier Soccer League | Kruger United | Richards Bay | 4 | 5 | Home |
| 8562283 | 2026-11-01 17:30 | Belgium — Pro League | Lommel United | KAA Gent | 4 | 5 | Home |
| 8573871 | 2026-11-01 11:00 | Portugal — LigaPro | FC Vizela | Associação Académica de Coimbra OAF | 5 | 4 | Away |
| 8614510 | 2026-11-01 14:00 | Italy — Serie B | Arezzo | Ascoli | 4 | 5 | Home |
| 8604050 | 2026-11-02 17:30 | Greece — Super League | Kalamata | Iraklis Thessaloniki | 4 | 5 | Home |

## Combo target and settlement contract

The research predictor is Double Chance AND total goals between 2 and 4 inclusive. The existing settlement helper is Double Chance AND total goals <5, including 0–1 goals. The rules disagree on 0–0/1–0 for Home Combo and 0–0/0–1 for Away Combo. The authoritative market definition is not approved, so Combo remains blocked and masked in both CSV exports. The score-grid diagnostic is logic-only and is not proof of official bookmaker settlement.

## Other limitations and release gate

- Provider parent competition IDs verified: 0/50.
- Provider-to-canonical bridges verified: 0.
- Canonical fixture/team joins: not verified.
- Official settlement truth and point-in-time provenance: not verified.
- Walk-forward metrics are raw and uncalibrated; odds provenance is not verified.
- The current-feed governed fixture slate remains unavailable; the runtime artifact is research-only and must not be presented as a current production-ready fixture report.
- Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, protected registry, ledgers and governance were not changed.

## Next action

No runtime code defect was established by this verification, so no new runtime dispatch was necessary for the documentation-only branch changes. Keep the 25 feature blocks and Combo mask. Prioritize authoritative canonical identity and settlement evidence; do not add fabricated history or make provider calls in this workstream.

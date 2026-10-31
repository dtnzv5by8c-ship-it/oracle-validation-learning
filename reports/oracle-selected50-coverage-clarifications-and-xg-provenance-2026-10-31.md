# Project Oracle — Selected-50 Coverage Clarifications and xG Provenance Addendum

**Evidence cutoff:** 31 October 2026 (SAST)  
**Source runtime:** Run `41175230838`, artifact `13032880970`  
**Runtime commit:** `ea3f46dab4e54b71a818ab8d8723f36426e36bef`  
**Pinned archive SHA-256:** `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`  
**Lane:** Reporting-only; no production writes, no provider API call using the user's account.

## 1. Corrected interpretation of 50-league report coverage

The Selected-50 QA scope contains all **50** governed league-season groups. The current seven-day fixture report contains **434 fixtures across 46 groups**; four groups have no fixture in the reporting horizon. This is 50/50 group representation in QA, not complete fixture-level intelligence or 50/50 prediction readiness.

- Three supported raw research markets — BTTS Yes, Home 1X and Away X2 — each have 410/434 values (94.47%); 24 fixtures are blocked by the runtime feature-support gate.
- Fourteen forecast/market fields are unavailable from the Run #124 Oracle output and remain explicitly unavailable. They must not be synthesized from empirical rates.
- Historical Accuracy is validated on 0/434 fixtures; A+ Setup is graded on 0/434.
- League positions are present for 434/434 but are provisional conventional-table reconstructions; 0 are independently verified official historical standings.
- Evidence Risk is a data-evidence coverage score, not outcome risk, probability of losing or calibrated predictive confidence.

## 2. Audit workbook correction

The first local coverage-audit workbook contained a reporting-label defect in its `Market Field Coverage` tab: it applied `NOT AVAILABLE FROM ORACLE V1.6 OUTPUT` to identity/context and descriptive fields that were actually present in the Market Intelligence report. The source workbook's `Market Data Coverage` tab and raw 38-column report show those fields are present; the corrected audit now separates:

- identity/context fields;
- supported raw market outputs;
- unsupported market outputs;
- descriptive form and provisional table values;
- explicit no-evidence/status rows;
- partial samples;
- unvalidated/ungraded fields.

H2H needs a further distinction: **144/434** fixtures have at least one prior meeting in the exact report scope; **290/434** have `NO_VERIFIED_PRIOR_H2H`. H2H average total goals is numeric for 144 fixtures and blank for the other 290. A non-empty status string is not a usable H2H statistic.

The corrected local workbook includes a 50-row xG coverage tab and a 25-row side-by-side reconciliation of descriptive score form against runtime model history support. It is a reporting artifact only.

## 3. Descriptive form is not the same as model feature support

A material scope difference was found between the two existing research paths:

- `scripts/build_selected50_market_intelligence_report.py` builds descriptive team form from score-complete records using a `SETTLED` status set that includes `after extra time`, `aet` and `penalties`.
- `scripts/build_selected50_research_runtime.py` builds model history using a narrower `FINISHED` status set, strict fixture identity/kickoff/team-ID eligibility, duplicate-signature quarantine and the 20-feature contract. The feature set includes goals, BTTS, failed-to-score, clean sheets, shots, shots on target and derived pair/environment features. Its five-match gate fails closed when the eligible history is shorter than five.

Run #124 has **24 blocked fixtures and 25 blocked team-side histories**: 21 sides have runtime oriented-history N=4 and four have N=3. The descriptive Team Form Evidence tab has 844/868 side rows with five score-based matches and 851/868 with at least three. Among the 25 runtime-blocked sides, 24 still show five descriptive score-based matches and one shows three.

This is not evidence that the runtime should relax its five-match gate. It demonstrates that the report's score-only descriptive history is not the same eligibility contract as the runtime's feature-complete history. Exact per-match exclusion reasons for each affected side have not yet been replayed against the raw source rows. Keep the runtime gate unchanged; the recurring report should label these two measures separately.

## 4. FootyStats xG documentation review

The public FootyStats Match Details sample response for EPL fixture `579101` includes `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch` alongside actual-match xG fields. This confirms that the pre-match-labelled fields can appear in an API response for a historical match. It does **not** establish when those values were first available or whether they were frozen before kickoff.

The reviewed documentation does not define a per-fixture xG capture timestamp, immutable snapshot identifier or revision history:

- Match Details documents `key` and `match_id` as query parameters; the public sample response contains no `captured_at`, `updated_at`, snapshot ID or revision-history field.
- League Matches documents `max_time` as returning league/team statistics up to a UNIX timestamp. It is not documented as an immutable per-fixture xG snapshot or xG revision-history mechanism.
- The FootyStats FAQ says match statistics are usually available around 20 minutes after full-time.

Selected-50 archive evidence remains: **434/434** upcoming fixture rows have numeric pre-match-labelled home/away/total xG across 46 fixture groups; **0/434** have capture timestamps; all **434/434** remain quarantined. Four selected groups have no fixture in the seven-day horizon.

The documentation review used the public example endpoint only. No private FootyStats key, authenticated user-account request or private API credit was used. A public sample response is not a substitute for a controlled account test or point-in-time archive.

Official references:
- Match Details: https://footystats.org/api/documentations/match-details
- League Matches: https://footystats.org/api/documentations/match-schedule-and-stats
- FAQ: https://footystats.org/api/documentations/faq
- Public documented sample: https://api.football-data-api.com/match?key=example&match_id=579101

## 5. Decisions and next actions

1. Keep all 434 xG rows quarantined until pre-kickoff capture time and revision provenance are demonstrated.
2. Preserve the runtime five-match feature gate; do not impute or relax it.
3. Replay the 25 blocked team-side histories against raw archive records to identify exact differences between the descriptive `SETTLED` contract and runtime `FINISHED`/identity/duplicate eligibility.
4. Update the recurring Market Intelligence workbook to distinguish descriptive score-form sample size from runtime model feature-support status.
5. Keep the 14 unsupported market fields unavailable; keep accuracy and A+ ungraded until their exact validation gates pass.
6. Retain the four no-fixture groups in the 50-row coverage summary so absence from the seven-day fixture sheet is not misread as missing league data.

**Governance:** No Oracle V1.6 production logic, thresholds, calibration, raw probabilities or market definitions were changed. All research outputs remain non-production and non-betting eligible.


## 6. Corrected local audit artifacts

The corrected reporting workbook and companion extracts were generated from the verified Run #124 artifacts. SHA-256 values:

- `Oracle_Selected50_Market_Intelligence_Coverage_Audit_CORRECTED_2026-10-31.xlsx`: `a237f35012135271827e1d58f212612b2808aba57b1e91c036633d00695eeacd`
- `oracle_selected50_50_league_xg_coverage_2026-10-31.csv`: `2d1b534c717873ddf3be05552f7d4d2c8885b7b638abecb3e40d20900e7cf2d8`
- `oracle_selected50_form_scope_reconciliation_2026-10-31.csv`: `0ad83c1f43b85b3ceafd63ee3f02e02e8b4ffbcd33fbc80369176a3fe8b3a3db`

The workbook contains 50 league rows in the xG detail tab (46 with fixture rows, four without), 434/434 numeric home, away and total xG values, zero capture timestamps and 434 quarantined rows. The form reconciliation tab contains all 25 runtime-blocked team-side histories. These are local report artifacts; the repository change is documentation-only.

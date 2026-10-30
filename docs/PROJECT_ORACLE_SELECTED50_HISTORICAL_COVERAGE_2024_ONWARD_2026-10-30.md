# Project Oracle — Selected-50 Historical Archive Coverage (2024 onward)
**Audit date:** 30 October 2026 UTC  
**Scope:** The governed 50-league FootyStats selection; exact country + competition grouping; four archived season folders per league (200 season folders).  
**Classification:** Research-only archive coverage and feature-quality audit. No production model changes.

## Coverage reconciliation
- Exact selected groups: 50/50.
- Archive season folders: 200/200; exactly four folders per selected group.
- Calendar-year league rows: 200 (50 leagues × 2024, 2025, 2026, 2027).
- Season-year rows: 800 (200 season folders × four calendar years).
- Unmatched or missing season folders: 0.
- Undated match rows: 0.
- Provider archive rows by calendar year: 2024 = 14,761; 2025 = 15,029; 2026 = 14,605; 2027 = 4,452.
- As of 30 October 2026, rows with kickoff on/before audit date: 2024 = 14,761; 2025 = 15,029; 2026 = 12,222. Total historical-date rows across 2024–30 October 2026 = 42,012. Of these, 41,781 have provider status `complete`; 231 are non-complete and must be excluded from completed-match outcome validation.
- Future-dated rows: 2,383 in the remainder of 2026 and 4,452 in 2027 (6,835 total). These must not enter historical training, calibration or backtesting.

## Feature quality interpretation
The provider archive stores numeric fields for all rows, but numeric presence is not the same as a valid or point-in-time value. Zeros are preserved as observed and not imputed or recoded. The raw calendar-year quality rollup shows:
- 2024 prematch xG zero rates: home 5.47%, away 5.50%, total 4.87%; BTTS odds zero 0.45%; DC odds zero about 1.4%.
- 2025 prematch xG zero rates: home 5.14%, away 5.21%, total 4.60%; BTTS odds zero 1.04%; DC odds zero 3.60%.
- 2026 calendar-year aggregate is mixed historical and future data. After restricting to 12,222 rows with kickoff on/before 30 October 2026, prematch xG zero rates are home 6.41%, away 6.40%, total 5.67%; BTTS odds zero 1.19%; DC odds zero 1.24%. The 2,383 future-dated 2026 rows are excluded from these historical rates.
- 2027 is future schedule data only at the audit date (4,452 rows). It has no historical feature rows as of the audit date. Its raw all-row odds zero rate is 99.93%; these are not historical bookmaker prices and must not enter odds training or backtesting.
- A separate as-of-kickoff feature quality split is included in the audit output. On the stricter subset of `status=complete` and kickoff on/before the audit date, row counts are 2024 = 14,749; 2025 = 14,987; 2026 = 12,045. The corresponding zero rates are: 2024 xG home/away/total 5.44%/5.45%/4.85%, BTTS odds 0.45%, DC odds 1.39–1.40%; 2025 xG 5.15%/5.16%/4.62%, BTTS odds 0.87%, DC odds 3.44%; 2026 xG 6.48%/6.48%/5.75%, BTTS odds 1.06%, DC odds 1.11%. Numeric presence still does not prove point-in-time capture. Only the complete/on-or-before subset is suitable for further historical feature validation, subject to PIT provenance.

## Identity and external join status
- FootyStats selected-season identity probe #3: 50/50 exact season IDs returned a `comp_master_id`; 50 unique values. This remains provider parent-field evidence only. Semantic definition and stability are not sufficiently established to promote it into Oracle's canonical competition registry.
- Bounded endpoint probe #6: 201/201 HTTP requests succeeded; all 50 exact selected season IDs found in live catalogue; all 50 returned success for matches, teams, tables and season endpoints. This is a schema/availability probe only, not full historical ingestion. Provider request_remaining last observed = 1,599; this is not proof of subscription monthly credits.
- Cross-provider fixture audit #18: 10 exact fixture joins across 2 selected seasons; 577 historical-ledger date-only candidates across 24 seasons; zero exact kickoff joins to the historical ledger; zero approved canonical bridges; zero strong canonical code candidates. No production eligibility.

## Data and governance controls
- The archive inventory now covers 2024 onward, but this does not automatically expand the governed primary model-validation window. The existing primary validation window remains 20 March 2025–20 September 2026 unless a separate governance decision explicitly changes it. The 2024 rows are archived coverage evidence, not an automatic authorization to retrain or recalibrate on an expanded period.
- Preserve provider zeros and raw source status. No imputation, fuzzy team mapping, or fabricated fixture joins.
- Keep future-dated rows out of historical model evaluation.
- Do not treat provider `complete` status or score values as official settlement truth without a reconciled market settlement specification.
- Current model probabilities, Oracle V1.6 production benchmark, V1.6.3 development benchmark, production ledger and betting eligibility remain unchanged.
- `production_eligible=false` and `betting_eligible=false` remain in force.

## Remaining release gates
1. Establish a documented, stable provider competition identity mapping; obtain provider confirmation for `comp_master_id` semantics or an equivalent documented crosswalk.
2. Resolve canonical fixture and team identity across FootyStats, the historical Oracle ledger and any independent source. Exact kickoff timestamps are currently missing from the historical ledger used in the join audit.
3. Establish point-in-time provenance for prematch xG and odds; separate missing/zero/unavailable semantics; quantify quality using the on/before-audit subset.
4. Reconcile official settlement truth and combo market semantics to the production market specification.
5. Run historical walk-forward validation only after the above gates pass; calibrate only under existing model governance.
6. Re-run the safe current fixture pipeline after the release gates; do not promote research-only raw probabilities as production predictions.

## Verified workflow evidence
- Private archive QA run #60: success; artifact ID `13006650629`; SHA-256 `e430347585949815bd3f99d4493fbd6935638ae89d5158e081adde483398b340`.
- Safety contract tests run #505: success.
- Dry-run planner run #785: success.
- All of these are research branch runs; no production model logic was changed.

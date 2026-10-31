# Oracle Market Intelligence Report Template — v1.1
Status: LOCKED REPORTING TEMPLATE
Effective: 2026-10-31
Supersedes: v1.0
Governed branch: research/oracle-50-league-readiness-audit

## Purpose and continuity
This is the canonical reporting contract for every weekly Selected-50 Market Intelligence report. The workbook is regenerated from the governed workflow and pinned inputs; it must never be rebuilt manually from scratch. The generator, tests, workbook schema and this contract are version-controlled in this repository. Each run must retain its workflow run ID, commit SHA, artifact ID/digest, input archive digest and QA output.

## Workbook tabs
1. **Oracle V1.6 Output** — frozen source output, exactly 38 columns. Preserve production values and order. Never modify Oracle V1.6 model logic or probabilities in report generation.
2. **Market Intelligence** — executive/analyst decision view. Keep the existing 83-column layout and column order unless a separately reviewed template version is approved.
3. **H2H Intelligence** — exact prior meetings, fixture IDs, kickoff, ordered team IDs and scores.
4. **Team Form Evidence** — overall and venue-split team form, rates, source fixture IDs and cutoff.
5. **Data Quality & Risk** — exact join, schedule status, sample sizes, provenance and eligibility.
6. **Goal Intelligence** — empirical form and goal evidence; do not label empirical rates as prediction probabilities.
7. **Goal Market Research** — experimental Poisson estimates and all block reasons/eligibility flags.
8. **Market Data Coverage** — per-field population and unavailable counts.
9. **Archive Field Coverage** — source-field availability and limitations.
10. **Definitions & Governance** — definitions, restrictions and research eligibility.
11. **xG Evidence Audit** — exact-identity fixture-level raw/source/numeric prematch xG inventory, capture timestamp status, archive provenance and quarantine. All xG remains excluded from prediction and betting use until point-in-time capture and revision provenance are verified.

## Required report invariants
- 50 governed league universe; actual fixture count varies by reporting horizon.
- Exact identity joins only: provider season ID, fixture ID, ordered home team ID, ordered away team ID.
- Strict pre-kickoff cutoff. Exclude target fixture, same-kickoff and post-kickoff evidence.
- No fuzzy identity joins, silent imputation, fabricated probabilities or blank failure states.
- Production source sheet remains exactly 38 columns.
- Research fields remain separate and explicitly marked non-production/non-betting eligible.
- The xG Evidence Audit uses exact ordered composite identity only; duplicate/missing keys are blocked, timestamps are not inferred, and every row remains prediction/betting ineligible.
- Preserve schedule conflicts and all missing/blocked reasons.
- All 434 fixture rows in the 2026-10-31 reference run had Production Eligible=NO and Betting Eligible=NO; future runs must derive these fields from governance, not copy that row count.
- H2H average total goals is computed only from exact verified pre-cutoff H2H meeting details. If no verified prior H2H exists, display NO_VERIFIED_PRIOR_H2H.
- Missing venue splits must display NOT_AVAILABLE_INSUFFICIENT_VENUE_SAMPLE, not a blank.
- Goal Research Block Reason must display NONE_FORECASTABLE_RESEARCH_ONLY for forecastable rows, or a specific blocker for blocked rows.
- Historical accuracy and A+ statuses must remain explicit NOT_VALIDATED / NOT_GRADED until all chronology, settlement, odds and calibration gates pass.

## Research datapoint roadmap (not production inputs)
Prioritize adding these as separately sourced evidence when provenance exists:
1. xG home/away and xGA, including provider field, capture timestamp, revision policy, source fixture IDs and pre-kickoff availability proof. Quarantine until temporal provenance is verified.
2. Contemporaneous bookmaker odds for supported markets: bookmaker, market, selection, price, timestamp, pre-match/closing marker and margin-removed consensus. No value/edge claim without timestamped odds.
3. Confirmed injuries/suspensions and lineups with source timestamp and status confidence. Never infer absence from missing data.
4. Rest days, fixture congestion, travel distance/time zone and home/away sequence, with reproducible calculation and cutoff.
5. Team strength/opponent-adjusted attack and defence ratings calculated strictly from prior matches.
6. League/season context: promotion/relegation, format, points rules, neutral venue and season phase; official table position only when verified.
7. Market-specific historical calibration: chronological out-of-fold Brier, log loss, calibration slope/intercept, reliability/ECE, sample size and league baseline comparison.

## Weekly release gate
A weekly artifact is canonical only when the workflow completes successfully and QA verifies exact joins, locked 38-column source sheet, expanded decision view, supporting tabs, explicit unavailable states, unchanged production probabilities, research-only eligibility, archive checksum, provenance, and schedule-discordance disclosure. Failed gates block publication; do not patch the workbook manually and call it canonical.

## Reference workbook
The approved visual/structural reference is the inspected 2026-10-31 expanded workbook generated by workflow run 41201069428. The workbook layout is maintained by the report generator and regression tests, not by manual copying. Future weekly runs must regenerate the same template automatically.

# Project Oracle — Decision Workbook Specification
Date: 2026-10-31
Branch: research/oracle-50-league-readiness-audit

## Approved user decisions
- Dashboard purpose: identify market opportunities and explain the evidence behind them.
- Rankings: separate rankings for BTTS, Double Chance Home and Double Chance Away, plus a combined shortlist.
- Team information: include only information that materially influences market selection.
- All 50 leagues must be consolidated into shared tables, not separate worksheets per league.
- Historical market performance and the team-market matrix are approved.
- Seven main review tabs; detailed calculations and provenance remain in supporting research artifacts.

## Seven main review tabs

1. **Executive Dashboard**
   - Combined shortlist, strongest supported candidates by market, market mix, key risks and data coverage.
   - Clearly distinguish raw Oracle probability, calibrated research estimate (only if validated), evidence grade and eligibility.
   - No claim of betting confidence based on raw probability alone.

2. **All Leagues & Fixtures**
   - One row per exact fixture ID across the governed 50-league universe.
   - League, kickoff, teams, Oracle raw probabilities for BTTS / DC Home / DC Away, visual intelligence, recent form, home/away splits, goals for/against, H2H summary, sample reliability, risk flags, data coverage and research-only status.
   - Filterable by date, league, team, market and evidence classification.
   - Preserve exact IDs and source lineage; no fuzzy joins.

3. **Market Rankings & Shortlist**
   - Separate Top 50 lists for BTTS, DC Home and DC Away.
   - Combined shortlist across markets.
   - Top 3 overall per market and top 3 per league where an exact eligible record exists.
   - Include probability, evidence grade, calibration status, supporting signals, contradictory signals, sample size and quarantine status.
   - Do not invent replacements where no exact eligible candidate exists.

4. **League DNA & Market Suitability**
   - All 50 leagues in one table.
   - Historical scoring and market tendencies, year/window coverage, walk-forward market performance, calibration, sample size, evidence classification and strongest diagnostic market(s).
   - Distinguish 2024 descriptive/earlier-fold history from the primary governed validation window (2025-03-20 to 2026-09-20).
   - Missing league data is unavailable, never zero-filled.

5. **Team & Match Intelligence**
   - One consolidated table for teams and relevant fixture-level matchups.
   - Only decision-relevant team features: recent form, venue splits, goals scored/conceded, BTTS/clean-sheet tendencies, relevant H2H and reliability.
   - H2H is supporting context only unless effective sample and chronological validation support stronger use.
   - Keep exact team/fixture keys and evidence windows.

6. **Historical Performance & Feature Edge**
   - Historical market performance by market and league: sample sizes, Brier, log loss, AUC, calibration and walk-forward consistency.
   - Feature ablation results and coverage; clearly distinguish exploratory challenger results from incremental tests against frozen Oracle V1.6.
   - No feature is promoted based on a single fold or uncorrected multiple-testing screen.

7. **Risk, Confidence & Data Quality**
   - Missing/stale/unverified fields, source provenance, quarantines, sample warnings, calibration warnings and explicit reasons to avoid a market.
   - Confidence must reflect validated probability quality and evidence reliability, not raw probability alone.

## Optional views
- **Team-Market Matrix**: include as a compact section within Team & Match Intelligence or as a supporting view if it materially improves usability.
- **Historical Market Performance**: included in tab 6; no separate worksheet required.
- Detailed calculation ledgers, fold predictions, raw H2H, feature diagnostics and provenance remain in a separate technical evidence pack, not the user-facing review workbook.

## Governance and data rules
- Preserve Oracle V1.6 production logic and probabilities unchanged.
- V1.6.3 remains development research; no promotion without governed validation.
- Keep production_eligible=false and betting_eligible=false until all formal gates pass.
- No provider/API credit spend without explicit user authorization.
- No reruns of completed ingestion/snapshot/runtime/bridge workflows merely to refresh presentation.
- No post-kickoff leakage, fuzzy identity matching, imputed required fields or fabricated data.
- Clearly label raw probabilities as raw and uncalibrated where applicable.
- Fixture rankings must be current to the timestamp shown; stale fixtures must be excluded from future-only shortlists.
- The full 50-league archive has been identified, but the private ZIP bytes still require retrieval and independent checksum verification. Until then, the 19 unavailable groups remain unavailable in numeric league/team/fixture analysis.

## Acceptance criteria
- Exactly seven principal review tabs.
- All 50 leagues consolidated into shared tables.
- All fixtures represented where verified data exists; missing coverage explicitly labelled.
- Separate and combined market rankings with exact fixture IDs and currentness controls.
- Historical performance and team-market suitability visible without opening technical ledgers.
- Technical evidence preserved separately and traceable to immutable source artifacts.

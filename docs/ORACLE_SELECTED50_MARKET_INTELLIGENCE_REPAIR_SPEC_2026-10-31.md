# Oracle Selected-50 Market Intelligence Repair — 2026-10-31

## Objective
Produce a complete fixture-level Market Intelligence report for the governed 50-league universe using the existing pinned FootyStats archive (read-only; SHA-256 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f). No provider API calls or credits. Do not alter frozen Oracle V1.6 logic or its probability outputs.

## Report contract (38 columns)
- H:S (12 fields): retain the existing locked schema. Populate a field only from a genuine Oracle market output in the run artifact. The 31-Oct runtime exposes BTTS, DC_HOME, DC_AWAY and masked combo fields; it does not expose Over 1.5, Over 2.5, Under 4.5, team goals, M-1UP or draw probabilities. Those must remain explicitly NOT_AVAILABLE_FROM_ORACLE_OUTPUT until an approved market-specific model output exists. Never synthesize probabilities from league averages or derived goal bands.
- W:AB (6 fields): fixture-cutoff league position, home/away last-five average goals scored, conceded, points, Attacking Index, Defensive Index. Derive only from completed matches strictly before kickoff and exact selected-league/team identity. Include sample n and source status in supporting fields/metadata. If fewer than 3 prior matches, mark insufficient; 5 preferred.
- AC:AG (5 fields): TOTAL Index; H2H last-five summary; H2H average total goals; historical accuracy status; home evidence risk. H2H must be strictly pre-kickoff and exact team pair/competition identity. Historical accuracy must remain NOT_VALIDATED until genuinely pre-match predictions are joined to official settled outcomes for the same market.
- AH:AL (5 fields): away evidence risk; home/away risk rationales; A+ setup status; independent match analysis. Risk is evidence coverage, never probability of losing. A+ is NOT_GRADED until market-specific calibration, settlement truth, and odds/value gates pass.

## Calculation contract
1. Team form: latest five completed fixtures before kickoff, separately overall and home/away split where sample permits. Points: W=3, D=1, L=0. Goals for/against are role-aware. No post-kickoff rows.
2. Attacking Index = 50 * (team last-five goals-for per match / pre-fixture league goals-per-team-match); Defensive Index = 50 * (pre-fixture league goals-per-team-match / team last-five goals-against per match). Clip each to 0–100; require >=3 matches; expose sample size. A zero denominator is unavailable, not infinity. TOTAL Index = Attacking + Defensive; do not normalize silently.
3. League position: reconstruct from completed league results strictly before kickoff, unless a dated official standings snapshot exists. Tie-break order must match competition rules; otherwise mark reconstructed/provisional, not verified.
4. H2H: exact same two teams in same competition where possible, strictly before kickoff; present latest five in current home-team perspective. No cross-competition fuzzy name joins.
5. Risk Profile: weighted evidence-gap score with documented components; label HIGH/MODERATE/LOW only as data coverage risk, not outcome risk.
6. Probabilities: preserve raw Oracle V1.6 output exactly. No recalibration, blending, or derived market probabilities in reporting workflow.
7. Calibration/selection: use chronological out-of-fold predictions only; reliability curves, Brier, log loss, calibration slope/intercept, ECE, confidence intervals and market-specific sample gates. Probability bands are descriptive, not guaranteed thresholds. Selection requires positive expected value using calibrated probability and contemporaneous verified odds, after margin/commission and uncertainty. No bet where odds or calibration absent.

## Mandatory 50-league completeness gates
- 50/50 configured leagues enumerated; report fixtures reconcile to the governed schedule.
- Every fixture has exact fixture ID and exact home/away team IDs; unresolved identity quarantined.
- Every field has source, as-of cutoff, sample size and status.
- No post-kickoff leakage; no duplicate fixture rows.
- Required data columns have explicit completeness counts by league and fixture. No silent blanks.
- Report cannot be marked COMPLETE if any league is absent, any required join fails, or any required market output is unavailable. Use PARTIAL/BLOCKED with exact reason.
- All rows remain research-only; production_eligible=false and betting_eligible=false until governance gates pass.

## Current evidence and known gap
31-Oct research runtime reports 434 governed fixture rows, 410 raw research predictions, 24 feature-support-blocked rows. The weekend workbook contains 320 fixture rows and only three market probabilities populated. The existing scoring-DNA workflow is league-level aggregate only; it does not yet produce fixture-cutoff rolling team form, standings, or Visual Intelligence indices. Its workflow requires manual workflow_dispatch, read-only archive confirmation, and the private archive token. This GitHub integration can inspect and modify repository files but cannot dispatch that workflow. Do not claim the repair is executed until the workflow run and artifacts are inspected.

## Implementation sequence
A. Extend archive-derived feature script to emit fixture-level team form, league table, scoring baselines and H2H features for every governed fixture using the pinned archive.
B. Add unit tests for chronology, home/away roles, exact identity, no-home-away flags, postponed/incomplete statuses, zero goals, duplicate keys and league table tie-breaks.
C. Build deterministic exact-ID join into the 38-column report; preserve raw Oracle probabilities byte-for-byte.
D. Add 50-league and per-column completeness QA; fail report build on broken joins, wrong schema or leakage.
E. Build calibration/selection diagnostics only from chronological OOF predictions and verified market settlement/odds evidence.
F. Refresh the report only after the above QA passes; publish run IDs, archive SHA, data cutoffs and per-column coverage.

## Non-goals
No new model, no production V1.6 changes, no new provider API calls, no guessed probabilities, no fabricated standings, no unverified settlement truth, and no automatic bet recommendation from raw probabilities.
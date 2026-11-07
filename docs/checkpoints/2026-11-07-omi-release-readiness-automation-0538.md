# Project Oracle — OMI / Release Readiness Automation Checkpoint — 2026-11-07 05:38 SAST

## Scope
Research-only work on `research/oracle-50-league-readiness-audit`. No provider/API acquisition, no Selected-50 repair rerun, and no production/betting admission.

## Live HEAD
The current branch commit observed from the GitHub branch commit endpoint is:
`b15aa303c0a6af768e1d6b0768bee11bb4570ac1`
Message: `checkpoint: Selected-50 evidence and historical validation gates`.

This supersedes older checkpoint notes that recorded earlier branch heads. The latest commit is research-only and adds a historical-validation checkpoint.

## OMI baseline
The successful Selected-50 Market Intelligence Report Repair remains the downstream baseline:
- workflow run #360 / run id `42309893170`
- repair commit `f084491b95be1df95d0d59b8d2d08d16ab6dbfbc`
- artifact `oracle-selected50-market-intelligence-repair`
- artifact id `13547044125`
- artifact SHA-256 `91cf647eb7a19d2f3e263347194c76477f60a2de0cf9ff90afab38d6227e7dfc`
- 717 runtime fixtures; 717/717 exact archive joins; zero unmatched/quarantined runtime joins; zero schedule discordance rows.
The repair is not rerun because no new defect has been proven.

## Historical evidence available
Sanitized historical evidence currently records:
- 49,949 unique provider fixture IDs after deduplicating 56,407 raw observations.
- 43,618 completed/settled-status fixture observations (87.33% of unique fixtures).
- 100% valid kickoff timestamps and provider fixture/team IDs.
- Completed-match score fields structurally valid for the represented historical observations.
- Non-zero odds availability: 1X2 99.74%, BTTS 99.34%, O/U 2.5 99.85%.
- Prematch-labelled xG non-zero for both teams: 93.28%.
- Explicit home/away flag: 86.64%.
- Strict chronological five-match form for both teams: 92.60%.
- Strict chronological eight-match form for both teams: 88.23%.
- Strict pre-kickoff H2H prior meeting: 75.33%.
These are availability/structure measures only. They are not production settlement or prediction-performance metrics.

## Consolidated readiness
### READY
- 50-league governance and scope.
- Acquisition accounting is structurally accounted for in the governed control plane.
- Exact provider IDs and fixture identity where canonical joins are proven.
- Chronology/leakage rules and exact-ID H2H controls.
- Research-only feature coverage and risk accounting.
- Historical descriptive diagnostics where their limitations are explicit.

### PARTIAL
- Recent form and home/away splits where strict pre-kickoff samples exist.
- Goals and derived goal distributions.
- BTTS / O1.5 / O2.5 / O3.5 where explicit settled-score evidence exists.
- Clean sheets / failed-to-score.
- Standings/strength.
- Team DNA / League DNA.
- H2H where exact prior identity/history exists.
- Sample size, recency and risk diagnostics.
- Fixture/probability reconciliation for research candidates.

### BLOCKED
- Point-in-time xG admission: numeric xG presence does not establish capture timestamp/revision provenance.
- Timestamped odds admission: non-zero odds availability does not establish admissible pre-kickoff timestamp/bookmaker/market provenance.
- Verified actual-result settlement for production backtesting.
- Immutable prediction + feature snapshot -> official settlement chain.
- Confidence promotion: confidence is gated by validated inputs.
- Production/betting report admission.

## Actual-results/backtesting
The historical research checkpoint explicitly marks accuracy, calibration, Brier, log loss, AUC and confidence/risk-band accuracy as UNVERIFIED for production because a complete immutable prediction-to-settlement dataset is not proven on the public branch. Existing challenger/shadow diagnostics remain research-only and must not be relabelled as Oracle V1.6 production performance.

No H2H predictive lift is promoted. Exact H2H history is used only when exact identity and chronology are proven; missing history remains unavailable.

## Highest-value remaining gates
1. Reconcile canonical Oracle fixture identity to the validated historical/provider identity for each production candidate.
2. Prove strict pre-kickoff feature cutoffs and immutable snapshot provenance.
3. Obtain point-in-time xG provenance.
4. Obtain timestamped odds provenance.
5. Establish verified official settlement records.
6. Establish immutable prediction/feature snapshot -> settlement links for leakage-safe backtesting.
7. Resolve feature-family sample gaps without inference or imputation.
8. Keep quarantined/unvalidated data excluded.

## Testing / workflow decision
The public branch contains a dedicated Selected-50 governed-readiness test workflow that runs:
- `python scripts/build_selected50_governed_readiness_matrix.py`
- `python tests/test_selected50_governed_readiness_matrix.py`
- output validation.
No safe direct workflow-dispatch action is available through the connected GitHub interface in this run, and no manual dispatch is required for this research-only checkpoint. The completed repair baseline is not rerun.

## Governance
- Oracle V1.6 production probabilities: unchanged.
- Production logic/thresholds/calibration: unchanged.
- No quarantined data promoted.
- No future/unsettled result treated as settled.
- No missing feature fabricated.
- `production_eligible=false`.
- `betting_eligible=false`.

## Next actionable milestone
Build the final deterministic league × season × endpoint × feature-family release matrix from validated evidence, then reconcile only rows that pass identity, chronology, provenance and settlement gates. Production/betting admission remains fail-closed until those gates are genuinely satisfied.

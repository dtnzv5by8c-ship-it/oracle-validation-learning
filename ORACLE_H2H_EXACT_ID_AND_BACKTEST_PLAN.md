# H2H Exact-ID Integration and Market Backtest — Controlled Work Plan

**Branch:** `feature/h2h-exact-id-join-and-market-backtest`  
**Status:** implementation scaffold committed for review; not production-enabled.  
**Governance:** reporting-only. No Oracle probabilities, production logic, calibration, weights, thresholds, or promotion gates may change.

## Phase A — canonical Fixture ID
1. Add the canonical Oracle Fixture ID to the fixture-level Oracle export at the report/export boundary, sourced from the existing governed fixture record.
2. Do not synthesize an ID from team names/date when a canonical ID exists upstream.
3. Require uniqueness and nonblank IDs; fail the report build if violated.

## Phase B — exact ID H2H join
- `scripts/join_h2h_by_fixture_id.py` performs exact ID matching only.
- It fails closed on missing ID columns, blank IDs, duplicate IDs, or empty inputs.
- It preserves every Oracle input value and appends H2H fields with an `H2H |` prefix.
- It writes a JSON audit and per-league coverage rates.
- No fuzzy matching or team/date fallback is permitted.

## Phase C — leagues and source gaps
Classify every no-match by league into:
1. Oracle fixture ID absent from H2H fixture report.
2. Team alias not resolved.
3. Team absent from the league archive.
4. Candidate pair found under another league code (investigate only; never auto-reassign).
5. No historical meeting found in archive coverage.
6. Source/season coverage not verified.
A no-match is not automatically “no H2H”. Retain the separate unmatched and no-meeting lists.

## Phase D — H2H predictive value research (offline only)
Run a chronological, pre-match-only, market-specific comparison:
- Baseline: Oracle raw probabilities alone.
- Challenger: same predictions plus H2H-derived features, tested only as a research/selection layer.
- Markets: evaluate separately (BTTS Yes, Over/Under markets, 1X2/double chance, and 1UP only where event truth is verified).
- Report sample size, league and season coverage, hit rate, Brier score, log loss when probabilities are available, calibration, and uncertainty intervals.
- Split chronologically; compute H2H only from matches completed before each target kickoff. Prevent leakage from future fixtures and post-match updates.
- Compare matched fixture cohorts to avoid attributing archive coverage differences to H2H performance.
- Report per-league and pooled results. Do not pool unsupported leagues without a coverage warning.
- H2H frequencies are features, not calibrated forecast probabilities. Do not call a hit-rate lift statistically reliable without uncertainty analysis.
- No model changes or production promotion based on this experiment.

## Completion gates
- Exact-ID join test: all Oracle IDs unique/nonblank; no duplicate H2H IDs; one output row per Oracle fixture; Oracle values byte-for-byte unchanged.
- Per-league H2H coverage report produced with explicit reasons for missingness.
- Historical prediction ledger and settled outcomes verified before performance claims. If a genuinely pre-match archived probability or outcome is missing, report that market/period as untestable rather than reconstructing it.
- Research results documented and reviewed before any separate change request.

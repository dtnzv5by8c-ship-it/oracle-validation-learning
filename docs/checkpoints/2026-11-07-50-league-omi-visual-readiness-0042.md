# Project Oracle — 50-League OMI / Visual Intelligence Automation Checkpoint

**As of:** 2026-11-07 00:42 SAST  
**Scope:** research-only downstream readiness for the governed 50-league universe. No production or betting admission.

## Live state

Current branch head: `faf7f1cc3af13e122d32a6ea73fb7628f4e98332`.

The latest code change explicitly permits a historical-only snapshot orientation state to pass its accounting QA when every runtime row is accounted for, snapshot-trace rows are correctly zero, identity/duplicate/missing counts are zero, and production/betting eligibility remain false. This is a reporting/validation correction only; it does not admit historical rows as production predictions.

## Upstream handoff

The acquisition queue remains exhausted and is not reopened by this checkpoint.

- Governed leagues: 50
- Provider seasons: 182
- Endpoint tasks: 728
- Completed governed tasks: 648
- Quarantined/provider-blocked tasks: 80
- Pending tasks: 0
- Missing task IDs: 0
- Out-of-manifest task IDs: 0
- Completed/quarantine overlap: 0

Task completion is not feature readiness. Only deterministic READY evidence is eligible for downstream admission.

## Downstream feature gate

| Feature family | Status | Admission requirement |
|---|---|---|
| Fixture identity | READY* | Canonical fixture/team/league-season identity and exact join |
| Chronology | PARTIAL | Source timestamp, kickoff and strict pre-kickoff cutoff |
| Recent form | PARTIAL | Strict prior-match window, sample count and no future leakage |
| Home/away splits | PARTIAL | Role-specific prior-match window and sample gate |
| H2H | PARTIAL | Exact team/competition identity and strictly prior meetings |
| Goals for/against | PARTIAL | Settled prior scores only |
| Total-goal distributions | PARTIAL | Settled-score sample with explicit n |
| BTTS | PARTIAL | Settled-score derivation with explicit n |
| Over 1.5/2.5/3.5 | PARTIAL | Settled-score derivation with explicit n |
| Clean sheets | PARTIAL | Settled prior scores with explicit n |
| Failed-to-score | PARTIAL | Settled prior scores with explicit n |
| xG for/against | BLOCKED | Point-in-time xG provenance and timestamp |
| Standings/strength | PARTIAL | Correct competition/season snapshot at cutoff |
| Timestamped odds | BLOCKED | Pre-kickoff timestamp, market identity and provenance |
| Sample size | READY diagnostic | Explicit per-feature/team/league n |
| Recency | PARTIAL | Record-level source timestamp and cutoff test |
| Confidence | GATED | Derived only from admitted feature coverage |
| Data-quality/risk | READY reporting | Explicit missingness/provenance/chronology/risk flags |
| Actual results | PARTIAL | Exact settled fixture identity and final score |
| Prediction→settlement backtest | BLOCKED | Immutable pre-kickoff prediction plus settlement pair |
| Team risk | PARTIAL | Repeated validated pre-kickoff samples |
| League risk | PARTIAL | Sufficient validated league-level samples |

*Structural READY does not grant production admission.

## Coverage rule

The defensible upstream coverage statement remains task-level: 648/728 completed (89.01%) and 80/728 blocked (10.99%). No league, season, endpoint or feature-family coverage percentage is asserted until computed from row-level READY evidence tied to the authoritative manifest identity.

No PARTIAL or BLOCKED evidence is backfilled, proxied, fuzzy-matched or inferred.

## Actual-results and research backtesting

Research archives and challenger/shadow experiments may be used for diagnostics when their limitations are explicitly labelled. They are not treated as production Oracle accuracy unless the prediction timestamp, immutable feature snapshot/provenance and exact settled result are all present.

The latest snapshot-orientation correction preserves this distinction: historical-only rows can be fully accounted for without being represented as production predictions.

## Highest-value blockers

1. Authoritative manifest identity normalization.
2. Deterministic row-level coverage matrix by league, season, endpoint and feature family.
3. Point-in-time xG provenance.
4. Timestamped pre-kickoff odds provenance.
5. Immutable prediction-to-settlement pairs for true backtesting.
6. Resolution of the 80 quarantined tasks through deterministic evidence only.

## Minimum evidence to resolve the blockers

A feature/fixture can become READY only when canonical identity, provider/season provenance, kickoff/source timestamps, strict pre-kickoff cutoff, source/batch provenance, required sample/window, and settlement state are all verified. xG additionally requires point-in-time xG provenance; odds additionally require timestamped market provenance; backtesting additionally requires immutable pre-kickoff prediction and feature snapshots.

## Governance

No Oracle V1.6 probability, threshold, decision rule, calibration or production governance is changed by this checkpoint. Production/betting admission remains fail-closed for PARTIAL, BLOCKED, future, unsettled or otherwise unvalidated evidence.

## Next actionable milestone

Generate the deterministic READY-only row-level coverage matrix:

**league → season → endpoint → feature family → fixture/team count → sample-size coverage → chronology/freshness pass rate → provenance pass rate → settlement pass rate → READY/PARTIAL/BLOCKED → blocker → minimum evidence required.**

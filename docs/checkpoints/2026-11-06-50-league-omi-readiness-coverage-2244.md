# Project Oracle — 50-League OMI / Visual Intelligence Coverage Gate

**As of:** 2026-11-06 22:44 SAST  
**Scope:** research-only downstream readiness. Exactly 50 governed leagues / 182 provider seasons / 728 endpoint tasks. No production or betting admission.

## Upstream handoff

The acquisition queue is treated as exhausted and is not re-opened by this checkpoint.

| Control | Count | Status |
|---|---:|---|
| Governed leagues | 50 | READY control-plane |
| Provider seasons | 182 | READY control-plane |
| Endpoint tasks | 728 | READY control-plane |
| Completed tasks | 648 | PARTIAL upstream evidence |
| Quarantined/provider-blocked tasks | 80 | BLOCKED |
| Pending tasks | 0 | READY |
| Missing task IDs | 0 | READY |
| Out-of-manifest task IDs | 0 | READY |
| Completed/quarantine overlap | 0 | READY |
| Completed-task coverage | 648 / 728 = 89.01% | PARTIAL |
| Blocked-task share | 80 / 728 = 10.99% | BLOCKED |

**Admission rule:** task completion is not feature readiness. Only deterministic READY evidence can enter downstream OMI/Visual Intelligence.

## Feature-family gate

| Feature family | Classification | Minimum evidence required |
|---|---|---|
| Fixture identity | READY* | Canonical fixture/team/league-season identity and exact join |
| Chronology | PARTIAL | Source timestamp + kickoff + pre-kickoff cutoff |
| Recent form | PARTIAL | Strict prior-match window, no future leakage, sample count |
| Home/away split | PARTIAL | Role-specific prior-match window and sample gate |
| H2H | PARTIAL | Exact team + league identity; prior meetings strictly before cutoff |
| Goals for/against | PARTIAL | Settled prior scores only |
| Total-goal distributions | PARTIAL | Settled-score sample with explicit n |
| BTTS | PARTIAL | Settled-score derivation with explicit n |
| Over 1.5 / 2.5 / 3.5 | PARTIAL | Settled-score derivation with explicit n |
| Clean sheets | PARTIAL | Settled-score derivation with explicit n |
| Failed-to-score | PARTIAL | Settled-score derivation with explicit n |
| xG for/against | BLOCKED | Point-in-time xG provenance and timestamp |
| Standings/strength | PARTIAL | Correct competition/season snapshot at cutoff |
| Timestamped odds | BLOCKED | Pre-kickoff timestamp, market identity and provenance |
| Sample size | READY diagnostic | Per-feature/per-team/per-league n |
| Recency | PARTIAL | Record-level source timestamp and cutoff test |
| Confidence | GATED | Derived only from admitted feature coverage; never imputed |
| Data quality/risk | READY reporting layer | Missingness/provenance/chronology/risk flags |
| Actual results | PARTIAL | Exact settled fixture identity and final score |
| Prediction→settlement backtest | BLOCKED | Immutable pre-kickoff prediction + settlement pair |
| Team risk | PARTIAL | Repeated validated pre-kickoff samples |
| League risk | PARTIAL | Sufficient validated league-level samples |

*Structural READY does not grant production admission.

## Coverage accounting rule

The public repository currently supports a defensible **task-level** coverage statement of 648/728 (89.01%) completed and 80/728 (10.99%) blocked. A league/season/endpoint/feature-family percentage is **not asserted** unless it is computed from the validated row-level evidence set with the authoritative manifest identity.

No league is promoted merely because another endpoint or season for that league is complete. No blocked task is backfilled with proxy data, another season, fuzzy identity, or inference.

## OMI / Visual Intelligence downstream contract

Each fixture-feature record must carry:

- canonical fixture ID and exact home/away team IDs;
- governed league and provider-season identity;
- kickoff timestamp and source timestamp;
- pre-kickoff cutoff;
- source/batch provenance;
- endpoint/task ID;
- feature value or explicit unavailable state;
- sample size;
- recency;
- READY/PARTIAL/BLOCKED status;
- data-quality/risk flags.

Derived markets are calculated only from admitted settled scores. xG and odds remain unavailable until their point-in-time provenance gates pass.

## Actual-results / backtesting contract

A prediction can enter a settlement/backtest pair only when:

1. prediction timestamp is strictly before kickoff;
2. prediction identity exactly matches the fixture;
3. prediction probability is immutable;
4. feature snapshot/provenance is retained;
5. final result is verified and settled;
6. no future/unsettled information was used.

The existing challenger/H2H research assets remain research-only and are not treated as Oracle production accuracy.

## Highest-value blockers

1. Normalize the authoritative manifest identity before declaring the evidence universe immutable.
2. Produce row-level league × season × endpoint × feature coverage from the 648 completed-task evidence, rather than extrapolating from task counts.
3. Establish point-in-time xG provenance.
4. Establish timestamped pre-kickoff odds provenance.
5. Establish immutable Oracle prediction→settlement pairs for true backtesting.
6. Preserve the 80 quarantined tasks as BLOCKED until deterministic evidence satisfies their gates.

## Governance

No Oracle V1.6 probability, threshold, decision rule, calibration or production governance is changed by this checkpoint. PARTIAL, BLOCKED, future, unsettled or unvalidated evidence is excluded from production/betting admission.

## Next actionable milestone

Build the deterministic row-level coverage matrix from only validated READY evidence:

**league → season → endpoint → feature family → fixture/team count → sample-size coverage → chronology/freshness pass rate → provenance pass rate → settlement pass rate → READY/PARTIAL/BLOCKED → blocker → minimum evidence required.**


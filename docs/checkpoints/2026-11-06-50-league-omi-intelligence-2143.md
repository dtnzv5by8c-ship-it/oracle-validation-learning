# Project Oracle — 50-League OMI Intelligence Checkpoint — 2026-11-06 21:43 SAST

## Scope
Exactly 50 leagues / 182 provider seasons / 728 governed endpoint tasks. Public repository only for downstream research, validation, OMI, Visual Intelligence and backtesting. Production/betting admission remains fail-closed.

## Upstream handoff
The acquisition queue is exhausted:
- Completed governed tasks: 648
- Provider-blocked/quarantined tasks: 80
- Pending governed tasks: 0
- Completed + quarantined: 728
- Missing governed task IDs: 0
- Out-of-manifest task IDs: 0
- Completed/quarantine overlap: 0

The 80 quarantined tasks are not READY and are excluded from downstream admission.

## Manifest identity control
Two historically recorded manifest identities exist:
- Current public control-plane manifest blob SHA: 6a916c962bfbcad1cfb429e23c26e0aef9b3a611
- Earlier pinned immutable plan blob SHA: 57fe9e1184b5035327feaa78307750e129c54bf3
- Earlier pinned manifest file SHA-256: 58bd06ed9c5a6a09ed55eb833319ca09cd4f01e2b175e4ca9127a1b3a7f689d7

This discrepancy is a provenance/control-plane blocker. Neither identity is silently substituted. Downstream production admission remains blocked until the authoritative manifest identity is normalized.

## Downstream readiness matrix
| Feature family | Status | Current rule |
|---|---|---|
| Fixture identity | READY* | Exact canonical identity only |
| League/season/endpoint identity | READY* | Manifest aligned |
| Chronology | PARTIAL | Point-in-time/pre-kickoff cutoff evidence required |
| Recent-form windows | PARTIAL | Timestamp-valid required windows only |
| Home/away splits | PARTIAL | Role-specific sample/window gate |
| H2H | PARTIAL | Exact-ID history only; unresolved/no-history separate |
| Goals for/against | PARTIAL | Derived only from admitted settled fixtures |
| Total-goal distributions | PARTIAL | Validated historical sample required |
| BTTS | PARTIAL | Settled goals/sample required |
| Over 1.5/2.5/3.5 | PARTIAL | Settled goals/sample required |
| Clean sheets | PARTIAL | Settled score history required |
| Failed-to-score | PARTIAL | Settled score history required |
| xG for/against | BLOCKED | Point-in-time provenance not proven |
| Standings/strength | PARTIAL | Fixture-time league/season chronology required |
| Timestamped odds | BLOCKED | Verified pre-kickoff timestamp/provenance required |
| Sample size | READY diagnostic | Explicit per feature |
| Recency | PARTIAL | Record-level timestamp gate |
| Confidence | GATED | Must reflect admitted feature coverage |
| Data-quality/risk flags | READY reporting layer | Missingness/provenance exposed |
| Actual results | PARTIAL | Exact settled fixtures only |
| Prediction→settlement backtesting | BLOCKED | Immutable pre-kickoff prediction ledger not established |
| Team risk | PARTIAL | Sufficient repeated pre-kickoff samples required |
| League risk | PARTIAL | Sufficient validated samples required |

*Structural READY does not grant production admission.

## Coverage / missingness control
Coverage must be quantified from the 648 completed governed task outputs only. The 80 quarantined tasks are reported separately as BLOCKED and must not be backfilled by inference, proxy substitution or cross-season substitution.

The current evidence supports structural exact-ID and settled-result/goal/BTTS/Over/1X2 reporting in the validated sample, but does not establish universal feature readiness across the governed universe.

## Highest-value blockers
1. Normalize the authoritative manifest identity before declaring the acquisition evidence set immutable.
2. Establish record-level chronology/freshness/provenance for all downstream feature windows.
3. Resolve xG provenance at the required point-in-time level.
4. Establish timestamped pre-kickoff odds provenance.
5. Build immutable Oracle prediction→settlement pairs for production backtesting.
6. Keep the 80 provider-blocked tasks explicitly unavailable.

## Minimum evidence for admission
Each admitted fixture/team-season feature must have:
- canonical fixture and team IDs
- provider league/season identity
- kickoff and source timestamps
- pre-kickoff cutoff
- immutable source/batch provenance
- required window and sample count
- raw settled score evidence for derived goal markets
- validated xG source when xG is used
- exact standings snapshot for the applicable competition/season
- pre-kickoff timestamped odds when odds are used
- settlement only after completion
- deterministic READY/PARTIAL/BLOCKED classification

## Production protection
No Oracle V1.6 production probabilities, thresholds, decision logic, calibration or governance were changed. This checkpoint is research-only. PARTIAL/BLOCKED/unvalidated evidence is not admitted to production or betting.

## Next actionable checkpoint
Resolve manifest identity in public control-plane metadata, then continue row-level feature admission and generate the final 50-league OMI/Visual Intelligence coverage matrix by league, season, endpoint and feature family.

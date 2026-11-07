# Project Oracle — OMI / Release Readiness Consolidated Checkpoint
Date: 2026-11-07 04:44 SAST
Status: RESEARCH-ONLY / FAIL-CLOSED
Branch: research/oracle-50-league-readiness-audit
Live HEAD inspected: 58f237f3b6275d6cddb036e6472f22eb3d0866c6

## Scope and baseline
- Governed universe: exactly 50 leagues / 182 provider-season partitions / 728 endpoint tasks.
- Acquisition queue is treated as exhausted; this checkpoint makes no provider/API calls and does not trigger acquisition.
- Successful Selected-50 Market Intelligence Report Repair remains the completed downstream baseline; no rerun is required.
- Oracle V1.6 production probabilities, thresholds, decision logic, calibration and governance are unchanged.
- production_eligible=false; betting_eligible=false.

## Evidence reconciliation
The latest public feature-coverage checkpoint is v11 (parent 16db1cbc36a8c6cc03bb790da22a8d48eac2b7e1). It is based on sanitized provider-canonical crosswalk evidence, not on unverified assumptions.
- 50 selected-season rows are represented.
- 31 partitions have exact selected-ID-to-archive-season matches.
- 19 partitions have no exact archive join in that evidence set.
- Private archive QA previously recorded 14,051 unique season/fixture-ID pairs with zero duplicate pairs.
- The evidence does not establish official settlement truth or point-in-time production feature provenance.

## Consolidated readiness matrix
| Feature family | READY | PARTIAL | BLOCKED / UNVERIFIED | Release interpretation |
|---|---:|---:|---:|---|
| Fixture identity | 0 | 31 | 19 | Exact archive join only; current production fixture identity not fully verified |
| Chronology / kickoff | 0 | 31 | 19 | Kickoff fields exist; as-of joins remain gated |
| Recent form 3 | 0 | 0 | 50 insufficient | No dedicated governed 3-match pre-match evidence |
| Recent form 5 | 0 | 31 | 19 | Archive form exists only for exact-join population |
| Recent form 8 | 0 | 0 | 50 insufficient | No dedicated governed 8-match evidence |
| Home/away splits | 0 | 31 | 19 | Point-in-time team-state join not verified |
| Goals for/against | 0 | 31 | 19 | Settled score fields available only in exact-join population |
| Total-goal distributions | 0 | 31 | 19 | Derived only from exact-join settled-score population |
| BTTS | 0 | 0 | 50 unverified | No production admission |
| Over 1.5 | 0 | 0 | 50 insufficient | No dedicated governed market-evidence column |
| Over 2.5 | 0 | 0 | 50 insufficient | No dedicated governed market-evidence column |
| Over 3.5 | 0 | 0 | 50 insufficient | No dedicated governed market-evidence column |
| Clean sheets | 0 | 0 | 50 insufficient | Not separately evidenced |
| Failed to score | 0 | 0 | 50 insufficient | Not separately evidenced |
| Standings / strength | 0 | 31 | 19 | As-of-kickoff validity not verified |
| xG | 0 | 31 | 19 | Numeric presence is not point-in-time provenance |
| Exact H2H | 0 | 31 | 19 | Prior meetings exist only where exact identity is established |
| Timestamped odds | 0 | 31 | 19 | Odds fields exist but verified timestamp/provenance is absent |
| Sample size | 0 | 31 | 19 | Diagnostic only until fixture/team joins are fully verified |
| Recency | 0 | 31 | 19 | Snapshot freshness is not sufficient for production eligibility |
| Confidence | 0 | 0 | 50 gated | Cannot promote confidence without validated inputs |
| Data quality / provenance | 0 | 31 | 19 | Current feed joins remain unverified |
| Actual settlement | 0 | 0 | 50 blocked | Official settlement truth not verified |
| Leakage-safe backtest | 0 | 0 | 50 blocked | Immutable prediction+feature snapshot to settlement chain absent |
| Team DNA / League DNA | 0 | 31 | 19 | Diagnostic research layer only; no production promotion |
| Risk profile | 0 | 31 | 19 | Research diagnostic; not a release gate pass |

## Highest-value blockers and minimum evidence
1. Exact fixture/team/league identity: one authoritative pre-kickoff fixture key with canonical team IDs and kickoff timestamp for every production candidate.
2. Chronology/leakage: immutable as-of cutoff proving every feature existed before kickoff.
3. xG: point-in-time xG/xGA values with capture timestamp, definition/scale and source provenance.
4. Odds: bookmaker/market/price plus capture timestamp and source provenance.
5. Settlement: independently verified official final score/result with settlement timestamp/source.
6. Backtesting: immutable prediction snapshot + exact feature snapshot + model version + pre-kickoff timestamp linked to settled result.
7. Market features: explicit validated inputs for BTTS, O1.5/O2.5/O3.5, clean-sheet and failed-to-score calculations, with minimum sample-size rules.
8. H2H: exact home/away team identity and prior-meeting cutoff; never infer missing history.
9. Team/League DNA: validated historical team and league aggregates with chronology and sample-size metadata.
10. 19 unresolved archive-season partitions: deterministic exact-ID reconciliation or explicit unavailable status; never promote as complete.

## Release decision
The consolidated evidence supports research diagnostics and reporting structures, but not a data-backed betting report. Production/betting admission remains FAIL-CLOSED until the gates above are satisfied.

## Test/status note
No CI status checks were reported for HEAD at inspection time. This checkpoint is documentation-only and does not alter production code or trigger a workflow.

## Next actionable checkpoint
Use the existing repaired OMI baseline and build the league x season x endpoint x feature-family accounting directly from its sanitized coverage/evidence artifacts. Reconcile only validated fixture/probability/settlement records. Do not rerun acquisition or the completed repair absent a proven defect.

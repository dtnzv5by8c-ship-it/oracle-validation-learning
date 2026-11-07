# Oracle OMI / Visual Intelligence — Final Release Gate Register

Date: 2026-11-07
Scope: research-only OMI/release-readiness consumption of already validated upstream evidence.

## Baseline
- Selected-50 Market Intelligence Repair #360 is complete and remains the downstream baseline.
- 717 runtime fixtures; 717/717 exact archive joins; 0 unmatched/quarantined runtime joins; 0 schedule discordance.
- 45 governed leagues represented in the inspected horizon; 5 have no represented fixtures and remain UNVERIFIED.
- No new acquisition or provider/API calls were performed by OMI.
- Quarantined evidence is excluded.

## Consolidated gate register

| Gate | Required evidence | Current status | Release effect | Dependency |
|---|---|---|---|---|
| G01 Canonical fixture identity | Exact Oracle fixture ID mapped to canonical fixture/team/league/season | READY for 717 baseline joins; 5 leagues UNVERIFIED in horizon | Candidate-level only | Validation/Evidence |
| G02 Production probability bridge | Immutable Oracle V1.6 probability string/market row mapped to exact fixture ID | BLOCKED | No production scoreability | Evidence |
| G03 Chronology | Prediction timestamp and every feature cutoff strictly pre-kickoff | READY as control; candidate admission remains gated by snapshot evidence | No production admission alone | Evidence |
| G04 Feature snapshot | Actual feature vector materialized and immutably bound to prediction | BLOCKED | No production scoreability | Evidence |
| G05 Team DNA | Pre-kickoff team-state inputs with source/time/hash and sufficient sample | UNVERIFIED/PARTIAL | Candidate-specific gate | Evidence/Validation |
| G06 League DNA | Pre-kickoff league-state inputs with source/time/hash and sufficient sample | UNVERIFIED/PARTIAL | Candidate-specific gate | Validation |
| G07 Exact H2H | Exact team IDs + historical cutoff; no fuzzy/inferred joins | PARTIAL | Candidate-specific gate | Validation |
| G08 Recent form | Complete pre-kickoff window and sample-size gate | PARTIAL | Candidate-specific gate | Validation |
| G09 Home/away form | Complete venue-specific pre-kickoff window | PARTIAL / INSUFFICIENT SAMPLE | Candidate-specific gate | Validation |
| G10 Goals/markets | Derived from admitted historical matches only | PARTIAL | Candidate-specific gate | Validation |
| G11 xG provenance | Value + definition/scale + source + capture/revision timestamp before kickoff | BLOCKED | xG cannot enter production evidence | Evidence/Validation |
| G12 Standings/strength | Point-in-time table/strength snapshot | READY for represented baseline; freshness still required for live admission | Candidate-specific gate | Validation |
| G13 Odds provenance | Bookmaker + market + price + capture timestamp | BLOCKED | Odds-based admission blocked | Evidence |
| G14 Sample size | Per-feature/per-market minimum observations | PARTIAL | Candidate-specific gate | Validation/Evidence |
| G15 Recency/freshness | Current-feed timestamp and admissible freshness window | UNVERIFIED | No live prediction admission | Validation |
| G16 Confidence | Derived only from admissible production probability/evidence cohort | UNVERIFIED | No production confidence | Evidence |
| G17 Risk | Explicit data-quality/provenance/sample/risk flags | READY as diagnostic layer; not a substitute for gates | Reporting only | OMI |
| G18 Verified settlement | Official/approved result truth with provenance | BLOCKED for production cohort | No production backtest | Evidence |
| G19 Prediction→feature→settlement chain | Immutable prediction, feature snapshot and verified result linkage | BLOCKED | No production backtest/admission | Evidence |
| G20 Leakage-safe backtest | Chronological admissible production pairs meeting sample/window rules | UNVERIFIED | No production accuracy claim | Evidence |
| G21 Quarantine exclusion | Quarantined/unvalidated rows excluded from admission | READY/control | Governance preserved | OMI |
| G22 Oracle V1.6 freeze | Logic/probabilities/thresholds/calibration unchanged | READY/control | Governance preserved | OMI |

## Market readiness inherited from the validated matrix
- BTTS: 31 READY / 14 PARTIAL / 5 UNVERIFIED.
- Over 1.5: 43 READY / 2 INSUFFICIENT SAMPLE / 5 UNVERIFIED.
- Over 2.5: 42 READY / 1 BLOCKED / 2 INSUFFICIENT SAMPLE / 5 UNVERIFIED.
- Over 3.5: 45 BLOCKED / 5 UNVERIFIED.
- xG: 1 READY numeric field / 44 BLOCKED / 5 UNVERIFIED; point-in-time provenance keeps the production gate BLOCKED.
- Timestamped odds: 45 BLOCKED / 5 UNVERIFIED.
- Actual results: 45 BLOCKED / 5 UNVERIFIED in the OMI baseline.
- Leakage-safe production backtest: 50 UNVERIFIED.

## Minimum evidence needed to close OMI
1. Canonical production probability/fixture bridge from Evidence.
2. New challenger publication with actual feature vectors materialized as immutable snapshots; do not rewrite the 900 historical rows.
3. Correct model-engine revision captured separately from workflow commit.
4. Verified settlement append using the corrected provenance builder and fail-closed feeder.
5. Current-feed freshness proof for the candidate prediction horizon.
6. Per-market sample/observation-window admission evidence.
7. xG and odds provenance only where point-in-time evidence exists.

## Shortest safe path
Consume the next canonical Evidence/Validation outputs; join them to this matrix by exact fixture ID and market key; recompute only readiness classifications; then issue a final production-admission report. No acquisition, repair rerun, H2H inference, shadow-metric promotion or Oracle V1.6 model change is required.

## Decision
Production eligibility: FALSE.
Betting eligibility: FALSE.
No production probability, threshold, calibration or governance change was made.

# Oracle OMI / Visual Intelligence — Final Release Gate Register

Date: 2026-11-07 — latest evidence refresh 12:01 SAST
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


## 2026-11-07 12:01 SAST — live-source and identity-bridge update

The upstream live 50-league fixture-source gate is now canonically persisted and PASS. This supersedes the earlier OMI statement that live source validation was still pending, but it does not close downstream identity or production-evidence gates.

### Current live 50-league source evidence
- Governed registry: 50/50 league identities represented.
- Validation rows: 50/50; exact reconciliation PASS; missing IDs 0; unexpected IDs 0; duplicate IDs 0.
- Current governed window: 2026-11-07 through 2026-11-21.
- Live fixtures verified: 299 across 26 leagues classified READY.
- 24 leagues are DATA_GATED because no usable fixture evidence was returned in the governed window; these remain represented and fail-closed.
- Greece Super League is DATA_GATED because current-season source evidence is not verified; the catalogue only exposed 2024/25.
- This source gate is evidence-backed and does not imply that all 50 leagues are prediction-ready.

### Current internal identity bridge
The research-only bridge contains exactly 50 governed identities:
- 20 EVIDENCE_EXACT_UNIQUE mappings — admissible for downstream identity work.
- 4 CROSS-NAMESPACE_NAME_VARIANT — fail-closed pending explicit identity evidence.
- 1 NAME_VARIANT_UNVERIFIED — fail-closed.
- 24 UNMAPPED — fail-closed.

Therefore OMI cannot yet treat the 299 current fixtures as an Oracle V1.6 production fixture universe. The source namespace is validated, but 20/50 identities currently have an evidence-backed internal Oracle code mapping. No production ACTIVE allow-list was changed.

### Updated OMI interpretation
- G01 fixture identity: PARTIAL / gated for live production scope. The historical #360 archive joins remain READY for their 717 fixtures, while the current 50-league source board has only 19/50 identities mapped exactly into the internal namespace.
- G15 recency/freshness: PARTIAL as source freshness evidence, not production-ready. The live source artifact is timestamped and covers 2026-11-07 to 2026-11-21, but candidate-level feature freshness and prediction-time cutoffs remain unproven.
- G02/G04/G11/G13/G16/G18/G19/G20 remain unchanged and blocked/unverified as previously recorded.
- The 50-league universe remains intact: the 24 DATA_GATED leagues are not removed or silently dropped.

### Exact next OMI dependency
Consume the next validated downstream fixture/prediction evidence only after the identity bridge and prediction-engine scope controls are reconciled. Then join exact fixture ID + market key + model-engine revision + feature snapshot to this matrix. Do not reconstruct production probabilities from challenger rows and do not infer missing league mappings.

Production eligibility: FALSE.
Betting eligibility: FALSE.


## 2026-11-07 12:57 SAST — identity-bridge count reconciliation

The OMI report's earlier 12:01 bridge counts were stale relative to the live research bridge after the Serbia exact mapping repair. A read-only re-audit of the live 50-row bridge found:
- 50/50 governed identities represented exactly once.
- 20 EVIDENCE_EXACT_UNIQUE.
- 24 UNMAPPED.
- 4 CROSS-NAMESPACE_NAME_VARIANT.
- 1 NAME_VARIANT_UNVERIFIED.
- 1 CODE_NAMESPACE_CONFLICT.

The report has been corrected to reflect the live bridge. No mapping was inferred or promoted, and the CODE_NAMESPACE_CONFLICT remains fail-closed. The source-validation gate remains PASS (50/50 reconciliation; 26 READY / 24 DATA_GATED; 299 fixtures), but this does not establish production prediction eligibility.


## 2026-11-07 15:03 SAST — prospective 50-league scope dependency consumed

### Finding
The Validation lane has now established the canonical 50-league prospective source registry, but the downstream prediction scope remains a separate control-plane blocker. OMI therefore cannot classify the current prospective fixture universe as production-ready even where source evidence is current.

### Evidence
- Canonical prospective registry: `data/prospective/oracle_50_league_fixture_source_registry.csv`
- 50/50 governed league identities represented.
- 49/50 have explicit current-season OpenFoot catalogue mappings.
- Greece Super League (GRC1) is explicitly `CURRENT_SEASON_NOT_VERIFIED` because the catalogue only exposes 2024/25; no fixture availability is inferred.
- Downstream scope audit confirms `scripts/oracle_four_model_predict.py` still applies the legacy 27-league ACTIVE allow-list.
- Therefore a validated 50-league source board cannot yet flow end-to-end into prediction publication for all governed leagues.
- The existing 50-league universe remains intact; DATA_GATED/UNVERIFIED leagues are not removed.

### Root Cause
Historical 50-league identity validation, prospective source registration, and prediction-engine scope are separate controls. The source registry is now 50-league governed, while the downstream prediction scope remains on the legacy 27-league configuration.

### Impact
- Add release gate **G23 — 50-league prospective downstream scope**: **BLOCKED**.
- G01 live fixture identity remains **PARTIAL/BLOCKED for production scope** until the canonical 50-league board is reconciled through the downstream scope control.
- G15 current-feed freshness is **PARTIAL**: source-window freshness is evidenced, but prediction-time feature freshness is not.
- No current fixture is promoted into Oracle V1.6 production evidence from this registry alone.

### Fix
OMI will consume the downstream scope reconciliation once the Validation/Evidence lanes establish it. No production allow-list, prediction logic, probability, threshold, calibration or governance change is made by OMI.

### Validation
The source registry and downstream-scope audit were read from the live branch at HEAD `b1d6468c5a1e6b642c7a711bdb874d7437cfecd7`. This update is reporting/control-plane only. The 50-league universe remains represented and fail-closed.

### Current OMI release decision
Production eligibility: FALSE.
Betting eligibility: FALSE.


## 2026-11-07 16:04 SAST — OMI evidence dependency audit

### Finding
A read-only audit of the latest canonical validation/evidence handover found no newly admissible post-repair prospective cohort. OMI therefore has no safe evidence-backed promotion to perform in this cycle.

### Evidence
- Latest canonical evidence checkpoint: `docs/checkpoints/2026-11-07-evidence-validation-control-1438.md`.
- Current prediction archive remains challenger/shadow evidence with raw prediction metadata; `calibrated_probability` remains unavailable for the audited challenger population.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv` remains header-only and `archive/FEATURE_SNAPSHOT_VALUES.csv` remains absent.
- The corrected settlement-truth artifact carries explicit provenance, but the append-only settlement ledger still contains the historical 25 settled rows with blank provenance; those rows remain immutable and non-production.
- No new completed prospective execution proving non-empty immutable snapshots and exact prediction-to-snapshot linkage was found in the available canonical evidence.

### Root Cause
The remaining OMI blocker is evidence maturity, not report logic: code-level snapshot/provenance repairs exist, but an independently auditable post-repair execution artifact has not yet been demonstrated.

### Impact
G02/G04/G16/G18/G19/G20 remain blocked or unverified. OMI cannot promote challenger probabilities, shadow settlement, populated feature IDs, xG values or odds values into production evidence merely because the fields exist or the repair code exists.

### Fix
No code, provider, workflow, model, probability, threshold, calibration or governance change was made. The OMI register is explicitly synchronized to the current evidence state and continues to fail closed.

### Validation
- Canonical continuation state and lessons learned were read before action.
- Live OMI release-gate register and latest validation checkpoint were re-read.
- No duplicate workflow launched.
- No provider/API calls made.
- No quarantined evidence promoted.
- Production and betting eligibility remain false.

### Single highest-value next action
Consume the first genuinely completed prospective cycle after the snapshot/YAML/namespace repairs and verify, in one chain, non-empty immutable snapshot manifest/values, exact fixture+market+model-engine linkage, pre-kickoff chronology and corrected settlement provenance. If that evidence is absent, no OMI reconstruction is justified.


## 2026-11-07 17:04 SAST — H2H upstream dependency audit

### Finding
A new H2H reporting execution is currently in progress on the public `main` branch. OMI has not consumed or promoted its output because the run is not complete and its artifact is not yet persisted/reconciled into the governed research branch.

### Evidence
- H2H Run #57: `Oracle H2H Reporting`, GitHub Actions run `42384137240`.
- Head commit: `f73f2139a74ae3cfe1fc4d07288728041a04dac6`.
- Status at audit: `in_progress`.
- The code change under test classifies archive absence/cross-league-only history as `NO_VERIFIED_HISTORICAL_H2H`; it does not fabricate H2H or change Oracle V1.6.
- Run #56 remains the last completed H2H artifact available to OMI: exact Fixture ID join 145/145, with 110 fixtures having prior H2H and 35 having no verified same-league H2H.

### Root Cause
The latest H2H evidence is still executing on a separate public `main` path. The OMI governed branch cannot treat an in-progress run as validated evidence.

### Impact
G07 Exact H2H remains PARTIAL/candidate-level. No H2H readiness promotion or production admission is justified from Run #57 yet.

### Fix
No workflow was launched, no artifact was copied, and no H2H history was inferred. The existing OMI classifications remain fail-closed pending a completed persisted artifact.

### Validation
- Live branch artifacts were read before any write.
- Actions state was inspected and Run #57 was confirmed already in progress.
- No duplicate H2H run was launched.
- No provider/API calls were made.
- No Oracle V1.6 production logic, probability, threshold, calibration, betting eligibility or governance change was made.

### Current release decision
Production eligibility: FALSE.
Betting eligibility: FALSE.

### Single highest-value next action
When Run #57 completes, consume only its persisted/reconciled artifact and update G07/H2H market-readiness classifications. Until then, no H2H reconstruction is justified.


## 2026-11-07 17:57 SAST — H2H execution dependency refresh

### Finding
The previously observed H2H execution has advanced to Run #62 on public `main`, but it is still in progress. OMI therefore has no completed H2H artifact to consume and no release classification can be promoted from it.

### Evidence
- H2H Run #62: `Oracle H2H Reporting`, Actions run `42387447956`.
- Head SHA: `4bb9924d0ee720e812b551a40254db1a072ef1a2`.
- Current status: `in_progress`.
- Archive extension, development-only challenger settlement audit and research-only chronological H2H incremental-value experiment have passed according to the canonical continuation state.
- Final H2H build, identity classification, report/audit artifact and quality gates are not yet complete.
- The run is on public `main`; no artifact has yet been persisted/reconciled into this governed research branch.
- H2H remains supporting evidence and is non-blocking for fixture/prediction eligibility; genuine no-H2H and small-sample H2H cases remain reporting-quality states only.

### Root Cause
H2H evidence production is still executing on a separate public path. OMI cannot consume an in-progress run as validated evidence.

### Impact
G07 remains PARTIAL/candidate-level. No OMI release gate is closed by Run #62 until the final artifact is completed and reconciled.

### Fix
No workflow was launched, no duplicate run was created, no provider/API call was made, and no H2H history was inferred. OMI records the live dependency only.

### Validation
- Live H2H run inspected at 17:57 SAST.
- Run #62 confirmed `in_progress`.
- Existing OMI report and continuation state were read before update.
- Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance remain unchanged.
- Production and betting eligibility remain FALSE.

### Next OMI action
Consume Run #62 only after successful completion and persisted/reconciled artifact validation; then update G07 and affected market/league readiness classifications.
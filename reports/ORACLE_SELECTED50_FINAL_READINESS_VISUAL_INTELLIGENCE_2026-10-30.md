# Project Oracle — Selected-50 Final Readiness & Visual Intelligence Report

**Report date:** 30 October 2026  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Governed branch:** `research/oracle-50-league-readiness-audit`  
**Runtime commit:** `5aef886e2c34a2e930937830f77a8fb444eba4fa`  
**Runtime run:** `41119141526`  
**Snapshot run:** `41117910952`  
**Bridge audit run:** `41121900062`  
**Release status:** RESEARCH ONLY — production and betting eligibility not granted.

## 1. Executive decision

The Selected-50 research runtime and its snapshot-to-runtime provenance audit have passed. The bridge audit proves that the exact sanitized snapshot was consumed by the exact runtime: snapshot SHA-256, GitHub artifact digest, runtime archive-open receipt, archive input hash and downloaded prediction-report hash all reconcile. The audit has **zero failed provenance checks**.

This closes the snapshot/runtime provenance gate. It does **not** certify all 50 leagues or markets for production or betting. Canonical cross-provider identity, official settlement truth, point-in-time feature provenance, calibration and market governance remain open.

The current report contains **426 fixture rows** across **39 leagues**: **403 raw research-only predictions** and **23 fixtures blocked** for missing required features. Combo Home and Combo Away probabilities are fully masked.

## 2. Governed data scope — keep training and validation dates distinct

The selected universe contains 50 selected FootyStats season groups and 200 archived season folders.

| Measure | Result |
|---|---:|
| Retained archive match records after deduplication | 59,049 |
| Completed match records | 51,983 |
| Historical rows with all 20 required feature fields | 51,095 |
| 2024 calendar-year archive rows | 14,761 |
| 2024 completed rows with numeric scores | 14,749 |
| 2024 rows with all 20 feature fields | 13,526 |
| Governed primary validation window | 20 Mar 2025 – 20 Sep 2026 |
| Training sample before validation cutoff | 22,427 |
| Holdout sample per market | 20,878 |

**Date interpretation:** 2024 data is present in the archive and forms part of the pre-cutoff historical training pool. The governed out-of-sample evaluation window is 20 March 2025 through 20 September 2026. These are different scopes and must not be described interchangeably. Calendar-year archive rows are observed coverage, not proof of provider completeness or point-in-time feature validity. Runtime archive observations also span calendar years 2023–2027; future-dated 2027 rows are not historical training.

## 3. Holdout performance

All figures below are raw, expanding-window walk-forward outputs, not calibrated probabilities and not betting ROI.

| Market | Train N | Holdout N | Accuracy @ 0.5 | Majority baseline accuracy | Brier | Constant-prevalence Brier | AUC | Log loss | ECE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTTS | 22,427 | 20,878 | 53.59% | 54.14% | 0.24746 | 0.24870 | 0.53790 | 0.68804 | 0.01633 |
| Double Chance Home | 22,427 | 20,878 | 70.13% | 69.79% | 0.20081 | 0.21094 | 0.63519 | 0.58862 | 0.02006 |
| Double Chance Away | 22,427 | 20,878 | 60.42% | 56.28% | 0.23298 | 0.24607 | 0.63207 | 0.65789 | 0.01571 |
| Combo Home | 22,427 | 20,878 | 57.40% | 56.95% | 0.24213 | 0.24520 | 0.57054 | 0.67718 | 0.02322 |
| Combo Away | 22,427 | 20,878 | 64.93% | 64.90% | 0.22384 | 0.22787 | 0.58152 | 0.63913 | 0.02088 |

**Interpretation:** Double Chance Home and Away show lower Brier scores than their constant-prevalence baselines in this holdout. BTTS accuracy is below its majority-class baseline, although its Brier score is modestly better than the constant-prevalence baseline. These are model-quality diagnostics only. No market is approved for betting on this evidence alone.

Three expanding-window folds are available for the market-level diagnostics. Per-league results are included in the companion workbook.

## 4. League × market readiness

The runtime produced 250 league-market diagnostic rows (50 leagues × 5 markets).

| Fold stability classification | Combinations |
|---|---:|
| Insufficient fold sample or metric | 100 |
| Mixed Brier skill across folds | 75 |
| Positive Brier skill in all observed folds — diagnostic only | 71 |
| No positive Brier skill in all observed folds | 4 |
| **Total** | **250** |

The sample gate was met for 245/250 combinations, but that gate explicitly requires stability and odds validation as additional controls. It is not an approval gate. No league-market combination is production eligible or has an approved edge claim. The workbook includes the complete 250-row league-market matrix.

## 5. Current fixture intelligence

| Measure | Result |
|---|---:|
| Governed fixture rows | 426 |
| Leagues represented in prediction report | 39 of 50 |
| Raw research-only predictions | 403 |
| Feature-support blocked fixtures | 23 |
| All Combo Home probabilities masked | Yes |
| All Combo Away probabilities masked | Yes |
| Confidence score | Not calculated |
| Data-risk percentage | Not quantified |
| Production eligible | No |

The report includes source fixture/team IDs, recent form, H2H diagnostics, table-position status, input coverage, risk status and market probabilities. Confidence is blank because the model is uncalibrated. Data risk percentage is blank because no validated risk mapping exists. These fields must not be fabricated.

For table positions, 359 rows use a current provider team snapshot rather than historical as-of standings; 67 are missing or unverified. Odds and xG fields are present in the source report schema, but provenance is unverified and these inputs were not used by the model.

## 6. Snapshot-to-runtime bridge audit

Bridge audit #12 completed successfully on the governed branch.

| Control | Result |
|---|---:|
| Selected season groups | 50 |
| Snapshot fixture rows | 2,258 |
| Runtime report rows | 426 |
| Exact season/fixture-key joins | 426 |
| Duplicate runtime exact keys | 0 |
| Future research candidates in snapshot | 601 |
| Future candidates in 7-day window | 347 |
| Exact 7-day matches | 344 |
| 7-day exact match coverage | 99.14% |
| Missing exact 7-day runtime matches | 3 |
| Snapshot-to-runtime provenance checks failed | 0 |

The bridge audit status is `PASS_BRIDGE_AUDIT_WITH_RELEASE_BLOCKERS`: the technical provenance check passes, while release eligibility remains blocked by independent governance and source-safety conditions. The 99.14% measure is a fixture join-coverage metric, not model accuracy.

### 6.1 Quarantined and unmatched fixtures

Of the 426 runtime rows, 347 are exact ID/team matches and safe future research candidates; 79 are exact matches but source-quarantined:
- 71 no-home/away distinction;
- 7 suspended/nonstandard status;
- 1 non-future unsettled status.

Three future candidates in the seven-day window have no exact runtime match:
- Everton vs Coventry City — fixture ID 8558082;
- Derby County vs Bolton Wanderers — fixture ID 8566315;
- Sevilla FC vs Deportivo Alavés — fixture ID 8570347.

These remain named exceptions for targeted reconciliation. They do not justify repeating historical ingestion, the snapshot or the runtime.

## 7. Market governance

Combo markets remain masked. The existing predictor target is Double Chance **and total goals between 2 and 4 inclusive**. The current settlement helper uses Double Chance **and total goals below 5**, which also includes 0–1 goals. These are different target definitions. Neither definition may be silently rewritten. An authoritative market-owner specification and corresponding official settlement truth are required before Combo can be released.

BTTS and Double Chance are retained as raw research outputs only. Canonical fixture/team joins and official settlement truth are not approved, and the probabilities are uncalibrated.

## 8. Outstanding closure register

| Gate | Status | Required closure evidence |
|---|---|---|
| Snapshot/runtime provenance | CLOSED | Bridge audit #12 passed exact snapshot, runtime receipt and report hash checks |
| Historical archive ingestion | CLOSED FOR THIS LINEAGE | Reuse pinned 200-season archive; do not repeat absent evidence of corruption |
| Canonical fixture/team identity | OPEN | Approved exact cross-provider bridges with stable identifiers and provenance |
| Parent competition identity | OPEN | Authoritative parent competition mapping; selected season IDs are not parent IDs |
| Official settlement truth | OPEN | Exact fixture-level official results, immutable captures, trusted observation times and approved source allowlist |
| Combo market definition | BLOCKED | Market owner approval reconciling predictor and settlement target |
| Calibration | OPEN | Chronological calibration procedure and independent calibration evaluation |
| Odds/xG provenance | OPEN | Provider/source identity, observation timestamps, point-in-time semantics and field definitions |
| Historical standings | OPEN | Point-in-time table snapshots or approved exclusion from dependent features |
| League-market stability | DIAGNOSTIC | Review 100 insufficient, 75 mixed and 4 consistently negative combinations; positive-fold cases remain diagnostic |
| Three unmatched fixtures | OPEN — TARGETED TRIAGE | Exact schedule reconciliation for the three listed fixtures |
| Production release | NOT GRANTED | All required identity, settlement, provenance, calibration and governance approvals |

## 9. Execution decisions — avoid repeat loops

1. Preserve Run #176, its pinned archive lineage, snapshot and Bridge Audit #12 as the current research baseline.
2. Do not repeat historical ingestion, the current fixture snapshot, runtime build or bridge audit merely to reproduce passing evidence.
3. Work only the open rows in the closure register. Re-run a workflow only when a code change or new evidence requires a specific validation.
4. Keep Combo masked until market-owner target definition and settlement truth are reconciled.
5. Keep confidence and data-risk percentages blank until valid methodologies exist.
6. Do not change Oracle V1.6 production logic or production probabilities as part of this reporting work.
7. Keep `production_eligible=false` and `betting_eligible=false` until formal release evidence and approval exist.

## 10. Source artifacts and reproducibility

- Runtime run: [41119141526](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41119141526)
- Snapshot run: [41117910952](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41117910952)
- Bridge audit run: [41121900062](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41121900062)
- Runtime archive SHA-256: `85c13ed0956325b3d96a998e7f5e533a5cec7fa9f7e88344dbad3c7f73085321`
- Snapshot file SHA-256: `b30ec294734c287fef9d713b19adbd55e16e77400a7c17a7e03fab24e1b0d7ff`
- Snapshot artifact ZIP SHA-256: `63e76d57465f53200f1bd8a6767cff12583887dcadd8abdb50ade39f7490a137`
- Runtime prediction report SHA-256: `086af446dee2e73f5a2da00fcca11cd6ef0b431a96a22f411dd4bae1d98a5e23`
- Bridge audit artifact SHA-256: `afa5527e3a17e61886d9c3de4fa9b0373425ad377c56f939816ef3401fc967c6`

**Companion workbook:** `Oracle_Selected50_Final_Readiness_Visual_Intelligence_30Oct2026.xlsx` — includes executive summary, holdout metrics, fold metrics, all 250 league-market rows, schedule coverage, calendar-year coverage, 426 fixture rows, exceptions and definitions.

---
This report is a research evidence consolidation. It does not certify provider completeness, canonical identity, official settlement, calibration, profitability, production readiness or betting eligibility.

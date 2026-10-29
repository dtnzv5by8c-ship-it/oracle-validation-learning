# Project Oracle — Deadline Readiness Decision (2026-10-29)

## Executive decision
**NOT APPROVED FOR PRODUCTION OR BETTING RELEASE.** This is a fail-closed governance decision, not a failure of the research workflow. No production model logic, frozen probabilities, thresholds, calibration, or production ledgers were changed.

## Newly verified: FootyStats identity probe
- Workflow run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40850862599
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40850862599/artifacts/12886454030
- Sequential requests attempted: 50; HTTP 200 with provider success: 50; failures: 0.
- Selected season ID response matches: 50/50.
- Country/name matches against selected manifest: 50/50.
- Responses populated comp_master_id: 50/50; unique comp_master_id values: 50.
- Probe used 50 calls, no retries, no parallel requests.
- Research evidence CSV: reports/oracle-selected50-footystats-identity-crosswalk-probe-2026-10-29.csv

## Identity interpretation
The probe verifies selected season IDs and captures provider comp_master_id values. It does not alone establish that comp_master_id is the Oracle canonical competition key or prove the canonical Oracle team/fixture join. Therefore provider IDs are evidence only and are not promoted to production registry values. Crosswalk remains provisional until checked against Oracle's canonical registry and exact fixture/team IDs.

## Release gate matrix
| Gate | Evidence | Decision |
|---|---|---|
| Selected 50 scope | Manifest has 50 unique provider season IDs | PASS — scope only |
| FootyStats identity response | 50/50 responses, country/name match, no request failures | PASS — provider response only |
| Provider-to-Oracle canonical competition bridge | No independently verified canonical-registry crosswalk yet | BLOCKED |
| Canonical team and fixture joins | Not verified for all selected current fixtures | BLOCKED |
| Freshness and future fixture status semantics | Conservative snapshot gate; quarantines retained | BLOCKED where unverified |
| Recent form | 24/435 current future rows lack required features; no imputation | BLOCKED for affected fixtures |
| Standings as of kickoff | Point-in-time evidence not established | BLOCKED |
| Historical xG leakage safety | Actual/post-match xG fields found populated on future-dated rows in prior audit; consumption leakage not proven, but safe provenance not established | BLOCKED for historical validation |
| Point-in-time odds | No verified point-in-time odds provenance or approved ROI benchmark | BLOCKED |
| Official settlement truth | Internal status/score QA only; official settlement unverified | BLOCKED |
| Combo market | Predictor uses Double Chance AND total goals 2–4 inclusive; helper uses Double Chance AND total goals <5, including 0–1 | BLOCKED; keep Combo masked |
| BTTS edge | Raw holdout 53.588% vs 54.143% majority baseline | NO DEMONSTRATED EDGE |
| Production/betting eligibility | Gates above unresolved | NOT_GRANTED |

## Current historical diagnostic (raw / research-only)
- Deduplicated match rows: 59,049.
- 51,983 rows have finished/complete status and numeric score; 7,066 non-finished status rows also have numeric scores and must not be treated as settled truth.
- Completed matches with 0–1 total goals: 13,346.
- Combo Home predictor-vs-ledger disagreements: 9,335; Combo Away disagreements: 8,017.
- BTTS raw holdout accuracy: 53.588%, versus 54.143% majority baseline.
- Double Chance walk-forward Brier skill was positive in the three reported folds for some league groups, but scores are raw/uncalibrated and not verified profitable edge. No production promotion is justified.

## Immediate next actions (research only)
1. Compare all 50 provider comp_master_id values against the actual Oracle canonical registry, not just the FootyStats manifest.
2. Obtain authoritative settlement truth and approve one Combo market definition before rebuilding any diagnostic ledger.
3. Require pre-kickoff timestamps/snapshots for xG, standings and odds; exclude unproven fields from historical validation.
4. Build exact fixture/team join coverage and classify each of the 435 upcoming rows as eligible or blocked; keep the 24 missing-required-feature rows blocked.
5. Run existing safety and compatibility checks only after changes. Do not rerun the full runtime merely to repeat completed gates.

## Governance
- Research branch only.
- No production model or probability changes.
- No fabricated mappings, settlement outcomes, feature provenance, odds or performance claims.
- A successful API probe or green workflow is not production approval.

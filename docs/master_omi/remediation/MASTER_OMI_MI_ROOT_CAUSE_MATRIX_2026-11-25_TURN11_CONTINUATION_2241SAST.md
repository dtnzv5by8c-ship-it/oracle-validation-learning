# Master OMI MI Root-Cause Matrix — Automation Turn 11 continuation — 2026-11-25 22:41 SAST

## Release decision
RELEASE_DECISION=FAIL-CLOSED

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6: unchanged

## Latest independent QA
- QA: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_2211SAST.md
- QA decision: FAIL-CLOSED
- QA evidence identifies the current prediction ledger, current team-state and matches as missing public authoritative inputs.

## Direct current-spine validation
- Path: data/fixtures/governed_50league_current.csv
- Current blob SHA observed during this cycle: 34f11025d1b72305126e124602838826859739d3
- Rows: 368
- Unique provider fixture IDs: 368
- Duplicate IDs: 0
- Fixture dates: 2026-11-25 through 2026-12-03
- Provider: FootyStats
- Identity status: EXACT_PROVIDER_FIXTURE_ID
- No dated frozen weekly spine accepted.
- Current manifest currently records requested window_end 2026-12-02 while the persisted CSV reaches 2026-12-03. This is a persistence/provenance inconsistency and is not treated as release evidence.

## Root-cause matrix

| Field / fixture domain | Defect | Root cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Rolling fixture spine | Current spine/manifest date-bound mismatch | Manifest stored requested window bounds but did not persist/validate actual fixture date bounds | Direct GitHub scan of current CSV + current manifest | Workflow now records fixture_date_min/max and fails closed if manifest and CSV bounds differ | FIXED IN CODE; next run validation required |
| Last-5 overall vs venue | Overall sample/metrics were actually venue-only | last5_for was called only with home/away venue filters, then reused for overall fields | oracle-50league-upcoming-mi-build.yml | Added independent overall and venue Last-5 calculations with strict kickoff cutoff | FIXED IN CODE; next run validation required |
| FootyStats PPG/GF/M/GA/M/BTTS | Metrics were extracted into intel but never joined into persisted fixture-level MI | Producer wrote only the Last-5 fixture object; intel was dead/unpersisted | Same workflow, direct code inspection | Added deterministic fixture/side metric join and explicit source/status/snapshot fields | FIXED IN CODE; next run validation required |
| H2H | No current H2H output in rolling MI | Producer had season match history but no fixture-level H2H aggregation | Same workflow + FootyStats league-matches source | Added exact provider-ID H2H from completed meetings strictly before target kickoff | FIXED IN CODE; next run validation required |
| xG | Cannot certify temporal provenance | Current fixture payload lacks authoritative provider capture timestamp tied to xG | Latest QA 22:11 | Keep xG explicitly UNVERIFIED_NO_CAPTURE_TIMESTAMP; do not substitute | QA BLOCKER |
| Current prediction ledger | Missing | No public authoritative current research/four_model/outputs/omi_prediction_ledger_current.csv; Oracle V1.6 engine is not in public repo | Latest QA + direct GitHub 404 | Do not fabricate/substitute; fail closed | QA BLOCKER |
| Current team state | Missing | Public current-data workflow is disabled and private-production dependent | oracle-public-current-data.yml + direct 404 | Do not fabricate; fail closed | QA BLOCKER |
| Current matches | Missing | Same public/private dependency defect | Latest QA + direct 404 | Do not fabricate; fail closed | QA BLOCKER |
| Canonical production scope | 754 governed rows vs current rolling spine 368 | Current weekly spine is rolling 50-league input; canonical locked workbook remains a historical/locked 754-row production surface | Latest QA | Do not pad, reuse dated spine, or silently reconcile scopes | QA BLOCKER |
| Kickoff reconciliation | 67/754 mismatch | Existing canonical fixture schedule discrepancies lack authoritative event-time correction evidence | Latest QA | Leave unchanged; fail closed | QA BLOCKER |
| xG provenance | 754/754 unverified | Capture timestamp not persisted | Latest QA | Explicit UNVERIFIED only | QA BLOCKER |
| Actual review status | 41 immutable DI blanks | Review status is inside immutable A:ET | Latest QA | Do not mutate A:ET | INTENTIONALLY UNCHANGED |
| Numeric typing | 21,749 governed analytical text values | Legacy persisted numeric values outside immutable A:ET were typed as inline strings | QA/remediation evidence | Type-only conversion to native Excel numeric | REMEDIATED; independent binary QA required |
| A:ET | 15,574 numeric-looking text values | Immutable production contract | Canonical/QA | Never mutate | INTENTIONALLY UNCHANGED |
| Formula Input | BLOCKED | Upstream prediction/chronology/provenance gates unresolved | Latest QA | Fail closed | QA BLOCKER |
| Production eligibility | 0/754 | Mandatory upstream gates unresolved | Latest QA | Fail closed | QA BLOCKER |
| Betting eligibility | 0/754 | Production gate blocked | Latest QA | Fail closed | QA BLOCKER |
| CMOI | UNAVAILABLE/UNVERIFIED for production promotion | Permanent contract does not contain promoted CMOI output | Latest QA | No inference/promotion | QA BLOCKER |

## Non-negotiable controls
- No fuzzy matching.
- No timezone normalization.
- No estimation.
- No zero-fill.
- No historical backfill.
- No post-kickoff evidence.
- No stale dated weekly spine.
- No unsupported provenance substitution.
- No fixture-ID rewriting.
- A:ET immutable.
- Oracle V1.6 immutable.
- Critical enrichment failure fails closed.

## Release state
FAIL-CLOSED. The rolling producer root causes identified in this cycle are fixed in code, but the fixes require a fresh scheduled execution and independent QA. The authoritative current prediction ledger/current Team State/current matches remain absent from the public governed source, so no release workbook can be certified in this cycle.
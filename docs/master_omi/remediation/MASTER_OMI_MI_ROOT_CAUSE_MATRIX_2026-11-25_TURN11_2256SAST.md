# Master OMI MI Root-Cause Matrix — Automation Turn 11 — 2026-11-25 22:56 SAST

## Release decision
RELEASE_DECISION=FAIL-CLOSED

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6: unchanged

## Latest independent QA
- QA: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_2242SAST.md
- QA blob SHA: d0226d9e816b38a4d7ef4414619a528eed951c63
- QA decision: FAIL-CLOSED
- QA freshness finding: current persisted rolling spine generated at 2026-11-25T20:12:37.694673+00:00; no newer public current-spine commit was present at audit time.
- QA current-source blockers: current prediction ledger, current Team State, and current matches absent from the public default branch.

## Direct current-spine validation
- Path: data/fixtures/governed_50league_current.csv
- File blob SHA: 34f11025d1b72305126e124602838826859739d3
- Rows: 368
- Unique provider fixture IDs: 368
- Duplicate IDs: 0
- Fixture dates: 2026-11-25 through 2026-12-03
- Provider: FootyStats
- Identity status: EXACT_PROVIDER_FIXTURE_ID
- No dated frozen weekly spine accepted.
- Persisted generation timestamp: 2026-11-25T20:12:37.694673+00:00.
- At the 22:42 SAST audit, the persisted spine was ~2h30m old and therefore not accepted as a fresh hourly source snapshot.

## Root-cause matrix

| Field / fixture domain | Defect | Root cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Rolling fixture freshness | Master OMI could consume a current-named spine that had gone stale between producer runs | Downstream workflow had no hard age gate on the persisted rolling-spine manifest | Latest QA 22:42 + .github/workflows/oracle-master-omi-excel.yml | Added fail-closed freshness gate: manifest required, generated_utc required, max age 90 minutes, exact ID-count validation, and governance flags enforced before build | FIXED IN WORKFLOW; next scheduled cycle must validate |
| Rolling fixture spine | Current spine/manifest date-bound mismatch was previously observed | Manifest originally stored requested window bounds rather than actual persisted fixture bounds | Direct GitHub scan + prior continuation matrix | Producer now records fixture_date_min/max and validates CSV/manifest equality | FIXED IN CODE; next run validation required |
| Last-5 overall vs venue | Overall sample/metrics previously used venue-only history | Duplicate/mis-scoped Last-5 calculation path | oracle-50league-upcoming-mi-build.yml | Independent overall and venue Last-5 calculations with strict target-kickoff cutoff | FIXED IN CODE; fresh execution required |
| FootyStats PPG/GF/M/GA/M/BTTS | Provider metrics were extracted but not persisted into fixture-level MI | Intermediate intel object was not joined into final MI rows | Producer code + FootyStats source contract | Deterministic fixture/side join with source, snapshot/cutoff and status | FIXED IN CODE; fresh execution required |
| H2H | Rolling MI lacked fixture-level H2H | Season match history was available but not aggregated | FootyStats league-matches | Exact provider-ID H2H from completed meetings strictly before target kickoff | FIXED IN CODE; fresh execution required |
| xG temporal provenance | 754/754 unverified | Provider capture timestamp tied to xG is absent | Latest QA | Preserve explicit UNVERIFIED; no substitution | QA BLOCKER |
| Current prediction ledger | Missing | Public repo has no authoritative current ledger and no public V1.6 prediction engine | Latest QA + direct GitHub scan | Fail closed; no fabricated/substituted predictions | QA BLOCKER |
| Current Team State | Missing | Public current-state workflow is private-production dependent and current artifact is absent | Latest QA + workflow inspection | Fail closed; no stale/private substitution | QA BLOCKER |
| Current matches | Missing | Same current-state dependency gap | Latest QA + direct GitHub scan | Fail closed | QA BLOCKER |
| Canonical scope | 754 governed production rows vs 368 current rolling rows | Locked historical production surface and current rolling 50-league input are different governed scopes | Latest QA | Do not pad, reuse dated spine, fuzzy-match, or silently reconcile | QA BLOCKER |
| Kickoff reconciliation | 67/754 mismatch | No authoritative event-time correction evidence | Latest QA | Leave unchanged; fail closed | QA BLOCKER |
| Actual review status | 41 immutable DI blanks | DI is inside immutable A:ET | Latest QA | Do not mutate A:ET | INTENTIONALLY UNCHANGED |
| Numeric typing | 21,749 analytical numeric-looking strings outside ET | Legacy workbook type defect | QA/remediation evidence | Type-only native numeric conversion | REMEDIATED; independent binary QA required |
| A:ET numeric text | 15,574 | Immutable production contract | Canonical/QA | Never mutate | INTENTIONALLY UNCHANGED |
| Formula Input | BLOCKED | Current prediction/provenance/chronology gates unresolved | Latest QA | Fail closed | QA BLOCKER |
| Production eligibility | 0/754 | Mandatory upstream gates unresolved | Latest QA | Fail closed | QA BLOCKER |
| Betting eligibility | 0/754 | Production gate blocked | Latest QA | Fail closed | QA BLOCKER |
| CMOI | UNAVAILABLE/UNVERIFIED for production promotion | Permanent production contract has no promoted CMOI output | Latest QA | No inference/promotion | QA BLOCKER |

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
FAIL-CLOSED. Workflow-level freshness protection is now hardened, but the current rolling spine must be freshly regenerated and independently audited. The authoritative current prediction ledger, current Team State, and current matches remain absent from the public governed source. No release workbook is certified until those dependencies exist and the exhaustive independent QA gate reaches 100%.

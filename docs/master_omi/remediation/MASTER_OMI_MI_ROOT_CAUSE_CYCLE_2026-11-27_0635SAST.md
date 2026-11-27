# Master OMI MI Remediation — Automation Run 11 — 2026-11-27 06:35 SAST

## Release decision

**FAIL-CLOSED. No release workbook certified.**

This cycle continues from the live public-repository state and applies root-cause fixes only. Oracle V1.6 production logic and canonical A:ET remain protected.

## Authoritative baseline

- Canonical V2.1.1 SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Protected canonical A:ET SHA-256: `b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564`
- Latest independently available QA in the public repository at cycle start: `docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-27_0127SAST.md`
- QA decision: **FAIL-CLOSED**
- Latest persisted rolling spine at cycle start: 392 fixtures / 50 leagues / 392 unique FootyStats Fixture IDs.

## Live current-data evidence at cycle start

- Rolling manifest: 392 fixtures, 50 governed leagues, 392 unique provider Fixture IDs.
- Rolling window: 2026-11-27 through 2026-12-04.
- Rolling spine generated: 2026-11-27T01:44:18.279672Z.
- Current reconciliation artifact: 392/392 exact provider-ID matches, 0 unmatched, 100% coverage, generated 2026-11-27T01:32:23.322258Z.
- Current FootyStats manifest: 2,733 current match rows and 6,788 goal-event rows, source errors 0.
- Venue is not present in the current governed spine/current FootyStats staging schema. It is therefore **UNAVAILABLE_SOURCE_SCHEMA** and must not be guessed or substituted.
- Current Team State and prediction-ledger durable public files were not independently certified at cycle start.

## Root-cause matrix

| Field / scope | Fixture / scope | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Fixture identity | Rolling 50-league universe | Downstream ledger reconciliation previously used composite league/date/team keys after prediction generation | `governed_50league_current.csv` + FootyStats Fixture ID | Prediction engine now preserves `fixture_id`; public workflow requires exact governed-vs-ledger Fixture-ID set equality | FIXED IN CODE |
| Fixture snapshot consistency | All current fixtures | Reconciliation only compared row count against a later live spine read; same-count fixture drift could pass | Rolling spine raw bytes + manifest | Reconciliation now persists spine SHA-256 and Fixture-ID-set SHA-256; public gate compares both against a fresh live read | FIXED IN CODE |
| Kickoff datetime | All exact matches | Provider identity was verified, but kickoff metadata was not independently asserted field-by-field | Rolling spine `kickoff_utc` vs current FootyStats `date_utc` | Exact field comparison; any mismatch fails closed | FIXED IN CODE |
| League/season | All exact matches | Provider Fixture ID match did not itself prove season identity | Rolling spine `league_season_id` vs current FootyStats `league_id` | Exact field comparison; any mismatch fails closed | FIXED IN CODE |
| Provider team source IDs | All exact matches | Provider Fixture ID match did not independently assert home/away provider IDs | Rolling spine `provider_home_id` / `provider_away_id` | Exact field comparison; any mismatch fails closed | FIXED IN CODE |
| Venue | All current fixtures | Venue/stadium is not exposed in the current governed spine or persisted FootyStats staging schema | Current rolling spine + FootyStats current schema | Explicit `UNAVAILABLE_SOURCE_SCHEMA`; no unsupported provider substitution or guess | UNAVAILABLE — release blocker only if canonical formula/mandatory field requires it |
| Team identity | Current Team State / prediction | Fuzzy identity resolvers and historical/cross-league fallbacks existed in integration adapters | Current governed Team State + provider IDs | Removed fuzzy matching and fallback admission; unresolved identity becomes NO_BET/DATA_GATED | FIXED IN CODE |
| Prediction ledger identity | Current ledger | Ledger output did not preserve governed Fixture ID as a first-class field | Rolling 50-league spine | Prediction engine now carries exact Fixture ID through output | FIXED IN CODE |
| Regression protection | Current/prediction paths | Identity hardening could regress without a dedicated executable test | Source code + workflow | Added exact-identity regression suite and public workflow execution gate | FIXED IN CODE |
| Persistence | Current Team State | Prior runs could validate a non-empty local artifact while durable public state remained absent | Current Team State manifest + CSV | Existing size/hash/row checks retained; fresh public current-data cycle now re-executes against current spine | EXECUTION REQUIRED |
| MI schema | Master OMI | Current FootyStats artifact is narrower than locked V2.1.1 canonical surface | Canonical V2.1.1 workbook | No padding or fabricated values; canonical 264-column assembly remains blocked until authoritative ledger/state are available | BLOCKED |
| xG PIT | Canonical MI | Current source rows do not carry verified capture timestamps sufficient for PIT certification | FootyStats source manifest / row provenance | Classify `UNVERIFIED_NO_CAPTURE_TIMESTAMP`; never infer timestamp | UNVERIFIED |
| H2H | Canonical MI | No authoritative H2H evidence for some fixtures | Authoritative H2H evidence only | Explicit `UNAVAILABLE_NO_AUTHORITATIVE_H2H` | UNAVAILABLE where applicable |
| Last-3/Last-5 / venue metrics | Canonical MI | Full canonical candidate cannot yet be regenerated from fresh durable current state | Current Team State + governed spine | Rebuild after current-state publication; missing sample remains explicit and fail-closed | BLOCKED |
| A:ET | Canonical workbook | Protected columns must not be mutated | Canonical V2.1.1 | No write path introduced; hash remains protected | PROTECTED |
| Oracle V1.6 | Production model | Remediation could accidentally alter model behaviour | Production source + locked governance | No threshold/probability/calibration/eligibility changes | PROTECTED |

## Code changes committed this cycle

### Private production source
- `7dd5e255b1b56d3116891887e452bcc491cdad39` — exact current Team-State identity admission.
- `2cbbde61dc9612b9b7c56c61d03508dfedc02e16` — exact current prediction-state identity admission.
- `5438f3ccd848d55a1509a902ec04977ba75f18f2` — remove compatibility fallback admission.
- `02be42c96aeebf85f59d1c36b944926891aa2388` — persist rolling-spine snapshot and Fixture-ID-set hashes.
- `336ceea235ef61043e4a709434d38c4c740bb9c1` — preserve governed Fixture IDs through prediction output.
- `bccc4f5afa44925ab66ae112a8b2e4ebe3117b35` — exact-identity regression suite.

### Public governed repository
- `093f072986fe5dd45b3c354849aad7d644c465d6` — rolling-spine drift and exact ledger reconciliation.
- `5a2fd942ac7eabac4479527b99c2699c40d73923` — exact identity regression + kickoff/season/provider-ID metadata gate.

## Release gate

**Not releasable yet.**

Required next evidence:

1. Fresh rolling 50-league rebuild after the current code changes.
2. Exact snapshot hash and Fixture-ID-set hash match between reconciliation and the live rolling spine.
3. 100% exact kickoff / league-season / provider-ID metadata reconciliation.
4. Durable current Team State on the governed public repository with verified hash, size and row count.
5. Current prediction ledger with exact Fixture-ID set parity.
6. Canonical 755-row × 264-column MI rebuild without A:ET mutation.
7. Cell-level coverage/type/provenance/PIT/chronology/leakage audit.
8. Native XLSX/XML/hash certification.
9. Independent QA = **100%**.

No release workbook is produced until every gate passes.

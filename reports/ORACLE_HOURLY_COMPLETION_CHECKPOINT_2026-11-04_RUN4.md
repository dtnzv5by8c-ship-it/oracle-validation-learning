# Project Oracle hourly completion checkpoint — 2026-11-04, run 4

**Pre-checkpoint research branch HEAD:** `31cca3cdfc7824b01923b9ea054418b84c2261ce`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** non-conflicting OMI output compatibility and offline ingestion-receipt validation. No main/private repository writes, no provider calls and no production model changes.

## 1. OMI / Oracle V1.6 output compatibility resolved at the schema-builder level

Inspection of the actual Library reference workbook `MASTER_OMI_REPORT_06_to_24_NOV_2026_ALL_50_LEAGUES_RUN183.xlsx` showed that the `Oracle V1.6 Output` sheet has 68 columns (A:BP), while the previous research builder labelled a separate 38-column derived analyst view with the same sheet name. These are different schemas and must not be treated as interchangeable.

Implemented:
- Exact 68-column ordered schema locked in `config/oracle_v1_6_output_schema_v1.json`.
- Header-sequence SHA-256: `4899b305eda7e156e3e1b2d398b02cac869b1df21e378fecaf991074012c22f7`.
- Builder now mirrors the runtime CSV into `Oracle V1.6 Output` without recalculating probabilities.
- Runtime CSV header order must match the locked 68-column sequence exactly. Missing, extra, duplicate or reordered headers fail closed.
- The previous 38-column derived view is now `Oracle V1.6 Analyst Summary`.
- The 95-column Book4 `OMI Report` and `Market Intelligence` sheets remain separate schemas.
- Structural reference workbook rows were not copied into public repo or used as current fixture data.

Details: `reports/OMI_ORACLE_V1_6_OUTPUT_SCHEMA_RECONCILIATION_2026-11-04.md`.

## 2. Ingestion receipt trust gap hardened offline

The prior planner treated SHA-shaped fields and boolean claims as evidence. It now requires two separately signed HMAC-SHA256 attestations for every successful receipt:

1. Private archive read-back verifier: independently confirms object bytes, immutable object version, private receipt bytes, writer receipt signature, private visibility, no public raw write and a digest binding all response/page metadata.
2. Central budget-ledger verifier: resolves the actual reservation and unique request event, exact task identity, one request, request timestamp, rolling-hour count, 1,800 hard ceiling, operational limit no greater than 1,500, at least 300 headroom and lower provider-limit enforcement.

Legacy boolean-only success receipts are rejected. The keys are read only from protected environment variables and are not logged or stored in the public repository. The dry-run summary explicitly states that authenticated archive and ledger attestations are required.

Contract: `docs/FOOTYSTATS_SIGNED_INGESTION_RECEIPT_CONTRACT_V2.md`.

Important limitation: no trusted production verifier keys have been provisioned, and the private writer/central ledger has not been modified to emit these attestations. This workstream is not authorized to modify the private repository. Therefore this is a tested consumer-side fail-closed verifier, not a completed live archive trust integration. No ingestion dispatch is allowed.

## 3. CI evidence on the latest code

- OMI Book4 Schema Contract Tests [41903897603](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41903897603): **PASS**, 8 tests, including exact 68-column schema/hash contract.
- Oracle Selected-50 Safety Contract Tests [41904496170](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41904496170): **PASS**. The Market Intelligence report suite ran 43 tests, including exact 68-column source mirroring, unchanged raw probability strings, and fail-closed schema drift/missing-field cases.
- FootyStats Budgeted Preflight Contract Tests [41904495658](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41904495658): **PASS**. The resumable-ingestion receipt suite ran 11 tests, including missing/invalid signatures, metadata tampering, legacy boolean-only receipts and valid signed test receipts.
- Oracle Selected-50 Dry-Run Planner [41904495647](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41904495647): **PASS**; sanitized artifact ID `13358954296`, ZIP SHA-256 `05ceedf1a3d1ec3130a3b819a3f137f8e83ab94788d8e7e1566282eae9a0903f`.

## 4. Current ingestion position

The dry-run remains:
- Planned tasks: 728
- Completed: 0
- Pending: 728
- Blocked: 0
- Dispatch allowed: false
- Production eligible: false
- Betting eligible: false

The 182-season preflight (Run 41869437030) is not repeated. It remains pagination metadata, not archived/validated historical data. No new FootyStats API calls were made in this continuation.

## 5. Coordination with league-mapping automation

The separate mapping automation's latest completed run is `53914e52-6570-8329-b2e6-a517f2f0bea0`. Its latest findings remain in its own mapping-owned files and were not edited here:
- 44 of 49 current leagues have exact country/competition corroboration from the prior provider probe.
- Five new catalogue leagues still need identity evidence.
- Six legacy-50 leagues are absent from the current selected 49 catalogue.
- 22 canonical candidates still require human approval; none are promoted.
- Fourteen calendar-2023 season partitions remain date-boundary review items because postponed 2024 fixtures cannot be inferred from season labels alone.
- The 6,398 legacy-parser no-home-away flags remain aggregate evidence only; fixture-level IDs and venue semantics are unresolved.

No mapping-owned path was changed. The shared execution protocol was not edited during this run to avoid concurrent changes.

## 6. Remaining gates

1. The private `oracle-football-data` writer and direct API workflow must be retired or centrally budget-gated by an authorized owner, outside this workstream.
2. Trusted private archive read-back and central budget verifier must issue v2 attestations; protected key provisioning and signer identity must be independently reviewed.
3. The actual runtime CSV must pass the exact 68-header check before any workbook build.
4. Protected private archive storage and read-back must be validated before any raw ingestion.
5. Only then may the 728 planned requests be executed in checkpointed batches under the shared rolling-hour ledger.
6. Historical match spine, exact team identity, H2H chronology, recent/home-away form and fixture-time standings must be independently validated. xG remains quarantined.
7. Data-backed OMI/Visual Intelligence output must wait for verified archived source data.

## Governance

Work remained on the governed research branch. No changes were made to `main` or the private `oracle-football-data` repository. No raw provider payloads or secrets were committed. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility remain unchanged. All research outputs remain `production_eligible=false` and `betting_eligible=false`.

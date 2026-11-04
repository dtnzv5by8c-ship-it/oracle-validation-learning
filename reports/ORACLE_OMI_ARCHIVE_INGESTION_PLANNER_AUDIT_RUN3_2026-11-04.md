# Project Oracle — OMI, archive and ingestion-planner validation (run 3)

Date: 2026-11-04  
Governed branch: `research/oracle-50-league-readiness-audit`  
Branch HEAD inspected before this report: `482337a0c2b68638bed95b0601e2c0166acdb628`  
Scope: offline validation only. No provider calls, private-repository writes, raw payload downloads or production changes.

## 1. OMI builder and schema verification

Current code inspected:
- `scripts/build_selected50_market_intelligence_report.py` blob SHA `c41dc64972519329f60de9a5f3bc748960f69d90`
- `config/omi_market_intelligence_schema_v1.json` blob SHA `3d5cceaf02c3b6a169d34f1567b8ef6108ea4ec4`
- `tests/test_selected50_market_intelligence_report.py` blob SHA `52db1c2e5d1c300a5d88c8ef3b19aa6e18170df5`

The builder reads the governed 95-header schema and creates:
- `Market Intelligence`: exactly 95 columns A:CQ, in schema header order;
- `OMI Report`: summary/control sheet;
- `Visual Intelligence`;
- `H2H Intelligence` and `Team Form Evidence`, plus supporting evidence and QA tabs;
- `Oracle V1.6 Output`: currently preserved as the tested 38-column sheet.

The report-builder test suite explicitly checks the 95-column Market Intelligence sheet against the schema JSON, the OMI Report and Visual Intelligence tabs, H2H/team-form tabs, exact-ID actuals, and NO production/betting eligibility. The dedicated schema contract checks the 95 unique headers, identity/time fields, governance fields and reserved CR:CS / append-only CT policy.

Verified CI:
- OMI Book4 Schema Contract Tests run 41876481840: PASS, 6 tests.
- Oracle Selected-50 Safety Contract Tests run 41892010984: PASS; the log includes the 41-test Market Intelligence report suite and confirms the 95-column Market Intelligence workbook contract plus 38-column Oracle V1.6 output contract.

### OMI compatibility blocker

The earlier master-template compatibility audit records that the inspected user master workbook's `Oracle V1.6 Output` sheet had 68 columns, whereas the current builder/test contract preserves 38 columns. The 95-column Market Intelligence schema is verified, but the separate Oracle V1.6 Output width/header discrepancy is not resolved by these tests. Before describing the generated workbook as fully compatible with the user's complete master workbook, reconcile the authoritative Oracle V1.6 Output header set against the frozen production output and lock that mapping without changing any probabilities or model logic.

## 2. Data-backed workbook remains correctly gated

Market Intelligence Report Repair run 41887608026 completed successfully as a CI/diagnostic run, but all private-archive-dependent steps were skipped:
- explicit private archive consent and token check;
- pinned private archive download and checksum verification;
- runtime artifact verification;
- archive-wide pre-kickoff features and xG provenance;
- H2H/recent-form rebuild;
- workbook rebuild and report upload.

The only completed report-repair tests included 41 Market Intelligence report tests and report-only diagnostics. The resulting diagnostics identified 24 blocked fixture rows and 25 blocked team-side rows; they are not a replacement for the data-backed workbook.

The read-only private archive QA workflow requires explicit manual confirmation and downloads a pinned existing private release, but no run of that workflow appears in the inspected branch Actions history. This run did not read or write the private repository. Therefore, no current protected private archive receipt or end-to-end archive access proof was established.

## 3. Offline resumable ingestion planner

Current files:
- `scripts/footystats_ingestion_checkpoint.py` blob SHA `253646683984422f216a87d215cd1d757c00b1a3`
- `tests/test_footystats_ingestion_checkpoint.py` blob SHA `5cd9fea0b908e65b06fcf21abe54f74095aa4a99`

FootyStats Budgeted Preflight Contract Tests run 41891767718: PASS. The log explicitly shows all 9 ingestion-checkpoint tests passing, including:
- deterministic pending-plan generation with `dispatch_allowed=false`;
- exact task identity and page-count checks;
- short-page rejection;
- 429 stop without retry;
- conflicting and orphan receipt quarantine;
- raw-payload field rejection;
- mandatory central-budget and private-archive attestations;
- sanitized research-only outputs.

The offline planner summary from that run was:
- planned tasks: 728;
- completed verified private-archive tasks: 0;
- pending tasks: 728;
- blocked tasks: 0;
- next batch tasks: 728;
- execution gate: `READY_FOR_CENTRAL_BUDGET_RESERVATION`;
- `dispatch_allowed=false`;
- `production_eligible=false`;
- `betting_eligible=false`;
- full history ingested: false.

This is a planning result only. It does not mean any provider request or private archive write occurred.

### Receipt trust-boundary gap

The current receipt validator enforces exact task/season/endpoint/page identity, timestamps, HTTP/provider success, page completeness, field presence, pagination totals and unique IDs, a central-gateway reservation ID, budget/headroom claims, private-write booleans, public-raw prohibition and SHA-256 string shape.

However, it does not independently verify that:
- `private_archive_receipt_sha256` matches a retrieved protected receipt object;
- `payload_sha256` matches the archived object;
- the archive receipt was signed by, or fetched from, the authorized private archive writer;
- the budget reservation ID resolves to the authoritative shared ledger entry and actual request timestamps.

The helper `receipt_signature` canonicalizes JSON for detecting conflicting receipts; it is not a cryptographic signature verifier. Consequently, the planner validates receipt structure and declared attestations, not authenticity of the private write or budget evidence. Before any ingestion, the trusted private writer must emit a verifiable receipt, and the consumer must independently resolve/verify the receipt and archive object hashes against the protected private destination and central ledger. Do not treat a boolean attestation or a well-formed SHA-256 string as proof of a write.

## 4. Latest related workflow evidence

- FootyStats Budgeted Preflight Contract Tests: [41891767718](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41891767718) — PASS; 9 ingestion checkpoint tests passed.
- Oracle Selected-50 Safety Contract Tests: [41892010984](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41892010984) — PASS.
- Oracle Selected-50 Dry-Run Planner: [41892011148](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41892011148) — PASS; separate 50-ID compatibility/readiness audit, not proof of the 49-league FootyStats history ingestion.
- OMI Book4 Schema Contract Tests: [41876481840](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41876481840) — PASS, 6 tests.
- OMI/report repair diagnostic: [41887608026](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41887608026) — workflow success, but all archive-dependent build steps skipped.

## 5. Next permitted actions

1. Reconcile the 38-versus-68 Oracle V1.6 Output header discrepancy against the actual frozen production output, without editing its logic or values.
2. Define and test a trusted private-writer receipt contract: signed or otherwise independently authenticated receipt, archive object key/version, exact payload SHA-256, receipt SHA-256, task identity, and a resolvable central ledger reservation/request record.
3. Run the existing read-only private archive QA only after the workflow's explicit private-read consent is supplied; preserve the pinned checksum and upload sanitized QA only.
4. Keep the 728-task ingestion planner offline until the private direct-API bypass is retired/centrally gated and the protected writer/receipt path is validated.
5. After those gates, run a small controlled batch, verify actual receipt/object/ledger joins, then checkpoint before scaling.
6. Rebuild OMI/Visual Intelligence/H2H/recent-form only from the verified archive and exact chronological match spine.

## Governance

No FootyStats API requests were made in this run. No private repository was modified. No raw provider payloads or secrets were added to the public repository. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility remain unchanged. All research outputs remain `production_eligible=false` and `betting_eligible=false`.
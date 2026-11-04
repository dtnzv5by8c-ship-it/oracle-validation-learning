# Project Oracle — offline ingestion and OMI schema checkpoint

Date: 2026-11-04  
Governed branch: `research/oracle-50-league-readiness-audit`  
Branch HEAD at checkpoint: `f2fcb4cc5fb523b8a19b55c27c4d6b4d651f6592`

## 1. Historical ingestion plan and pagination

The FootyStats selected catalogue remains the source of truth: 49 selected provider leagues and 756 catalogue season rows. The 2024-01-01 through 2026-11-04 history window maps to 182 provider-season partitions.

The saved preflight evidence for Run 41869437030 reports:
- 182/182 provider-season endpoint preflights completed.
- 910 API requests attempted against a 1,000-request reservation.
- 54,546 league-matches rows returned in preflight samples.
- 3,117 league-team rows reported.
- One match page and one team page reported for each of the 182 seasons; the per-season match returned-row counts equal provider total_results.
- 6,398 no_home_away rows across 73 seasons; 14 seasons have every sampled row flagged no_home_away.

This is pagination metadata evidence, not historical ingestion. The 54,546 rows have not been archived, cross-season deduplicated, exact-window admitted or validated into a chronological match spine. H2H chronology, recent form, venue form and fixture-time standings remain unverified. xG remains quarantined for missing point-in-time capture/revision provenance.

The 728-task manifest has been reconciled so league-teams tasks now carry exact `max_per_page`, `expected_total_results` and `expected_page_count` from the matching provider-season coverage row. No API request was made to make this correction.

## 2. Resumable ingestion checkpoint planner

Added `scripts/footystats_ingestion_checkpoint.py` and its offline tests. The planner consumes the task manifest and sanitized receipts only; it does not call FootyStats or read credentials. A successful receipt must attest:
- exact provider season, endpoint, page and task ID;
- HTTP 200, provider success, verified response shape, complete page and required fields;
- exact page totals, page count and unique IDs;
- central gateway use, durable budget reservation ID and ledger attestation;
- hard 1,800-request rolling-hour limit and at least 300 requests of headroom;
- verified protected private archive write and private raw-payload storage;
- SHA-256 payload and private archive receipt hashes;
- no raw payload written to the public repository.

429, 401, 403, provider failure, transport failure, malformed response, required-field gaps, private archive failures, orphan receipts and conflicting receipts block the next batch. There are no automatic retries. The output is always `dispatch_allowed=false`; the central budget gateway must reserve requests before any external executor runs.

The offline dry-run against the committed manifest verified:
- planned tasks: 728;
- completed private-archive receipts: 0;
- pending tasks: 728;
- blocked tasks: 0;
- next batch plan: 728;
- dispatch allowed: false;
- production and betting eligibility: false.

The plan is ready for central budget reservation only; no ingestion was dispatched.

## 3. Rolling-hour budget hardening

The shared request-budget helper now:
- rejects any configured global limit above 1,800;
- requires at least 300 requests of reserved headroom;
- rejects provider request limits at or below the headroom requirement;
- preserves a larger headroom value if one is already recorded;
- checks the provider-reported request limit immediately after the first preflight response, before reserving or issuing further calls.

The provider's `request_remaining` value is not treated as monthly-credit evidence. The user has attested sufficient credits; no further monthly-credit confirmation is requested. Any lower provider limit or permission still takes precedence.

The central workflow now uses up to five safe fetch/rebase/push attempts for both reservation and sanitized-output commits. It never force-pushes. If reservation publication cannot be made safely, execution stops before provider access.

## 4. OMI and Visual Intelligence schema integration

The report builder now reads `config/omi_market_intelligence_schema_v1.json` as the authoritative Book4 schema and writes exactly 95 unique `Market Intelligence` columns A:CQ, preserving the locked header order. Explicit alias mappings preserve the exact template headers, including the numbered duplicate fields.

The workbook builder now includes:
- `OMI Report` summary sheet;
- `Market Intelligence` (95-column Book4 baseline);
- `Visual Intelligence` sheet;
- existing H2H and team-form evidence tabs;
- existing 38-column `Oracle V1.6 Output` sheet unchanged.

Actual goals and settlement fields are populated only from an exact composite archive join with settled status and valid scores. No-home/away fixtures do not populate home/away goals or a home/away result. H2H uses exact unordered provider team-ID pairs only; display-name joins are not used. Naive kickoff timestamps are rejected. Exact duplicate archive rows are deduplicated; conflicting fixture identities are quarantined. No-home/away rows are excluded from venue-specific recent form. An empty or wholly invalid archive history now blocks the archive-index gate rather than reporting PASS.

This validates the builder and its contract; it does not mean a new OMI workbook has been generated from verified live historical data. The private archive read/build path remains gated pending a verified protected archive receipt.

## 5. Workflow evidence

Successful GitHub Actions runs:
- FootyStats Budgeted Preflight Contract Tests: [41887006445](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41887006445)
- Oracle Selected-50 Safety Contract Tests: [41887006611](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41887006611)
- Oracle Selected-50 Dry-Run Planner: [41887006771](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41887006771)
- OMI Book4 Schema Contract Tests: [41885332620](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41885332620)
- Oracle Selected-50 Market Intelligence Report Repair contract: [41887384395](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41887384395)
- Latest Oracle Selected-50 Safety Contract Tests: [41887384486](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41887384486)

The budgeted contract run includes the resumable planner dry-run and asserts all 728 tasks remain pending, no dispatch is allowed, and research/betting eligibility remain false.

## 6. External provider-workflow safety audit — blocker

The six legacy FootyStats workflows on the public `oracle-validation-learning` default branch were rechecked. They are now fail-closed, read-only stubs with manual dispatch only; they contain no direct provider host or API secret use.

The private repository `dtnzv5by8c-ship-it/oracle-football-data` has 74 GitHub Actions workflows. A read-only scan of all 74 workflow files found one direct FootyStats access workflow:
- `.github/workflows/footystats-private-historical-ingestion.yml`
- current file SHA: `e4a951f2366f713088e06c96ef007afecafb5de8`
- active `workflow_dispatch` and `push` triggers;
- reads `FOOTYSTATS_API_KEY` and calls `api.football-data-api.com` directly;
- uses three automatic retries;
- has no shared rolling-hour ledger or 300-request headroom enforcement;
- hardcodes a 27-league universe and page size 1,000;
- writes raw payloads to a private workflow artifact without the new central-gateway receipt contract.

This remains a hard blocker for all further FootyStats requests. The user's current-turn scope is research-branch-only, so this automation did not modify the private repository. No FootyStats request was made to test or bypass this workflow.

## 7. Governance state

- Frozen Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility: unchanged.
- Research outputs: `production_eligible=false`, `betting_eligible=false`.
- Full historical ingestion: not completed.
- Verified private raw archive receipts: 0.
- H2H/recent/home-away/fixture-time standings: not yet certified.
- xG: quarantined.
- Master OMI workbook: schema-compatible builder validated; no new data-backed workbook published.

Next permitted work is offline implementation, tests and sanitized audits. Provider ingestion must remain stopped until the private direct-API workflow is retired or centrally gated and the protected private archive receipt path is validated.

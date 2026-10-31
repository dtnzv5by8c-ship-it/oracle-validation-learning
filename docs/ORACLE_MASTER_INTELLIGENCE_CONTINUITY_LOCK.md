# Master Intelligence Report — Continuity Lock

Date: 2026-10-31
Status: GOVERNED CONTINUITY INSTRUCTION
Branch: research/oracle-50-league-readiness-audit

## Canonical template — do not rebuild

The canonical weekly workbook is governed by:
- Template: `reports/templates/ORACLE_MARKET_INTELLIGENCE_TEMPLATE_V1.md` — v1.2, LOCKED REPORTING TEMPLATE.
- Generator: `scripts/build_selected50_market_intelligence_report.py`.
- Workflow: `.github/workflows/oracle-selected50-market-intelligence-repair.yml`.
- Field dictionary: `docs/ORACLE_MASTER_INTELLIGENCE_DATA_DICTIONARY_V1.md` — v1.0.

The v1.2 contract preserves 12 tabs, the 38-column Oracle V1.6 Output sheet, the 83-column Market Intelligence view, fixture-context supporting tabs, and the dedicated Schedule Reconciliation queue.

**Mandatory weekly rule:** Never recreate the workbook manually or start again from a blank workbook. Regenerate from the existing version-controlled template and generator. Carry forward the same sheet order, headers, calculations, supporting evidence, coverage summaries, definitions, exception queue and governance flags. If schema or calculations change, update the template, dictionary, tests and generator together, then verify the governed workflow before declaring the change complete.

## Run record and release control

Every weekly report must preserve:
- report workflow run ID and source runtime run ID;
- governed branch and commit SHA;
- artifact ID and artifact digest;
- pinned archive release and SHA-256;
- QA JSON, evidence trace and workbook output.

A green workflow alone is not final sign-off. Inspect the workbook and QA. Failed or incomplete gates remain PARTIAL/BLOCKED with explicit reasons. Do not manually patch a failed workbook and call it canonical.

## Frozen governance

- Oracle V1.6 remains unchanged.
- No production probabilities, thresholds or logic may be changed by report enrichment.
- Research outputs remain production-ineligible and betting-ineligible.
- Exact identity and strict pre-kickoff chronology remain mandatory.
- No fuzzy joins, imputation, fabricated probabilities or silent missing values.
- No additional provider API calls, paid credits, purchases or archive mutations without fresh explicit approval.

## Known open items carried forward

- 19 schedule kickoff discordances from the 31-Oct report: REVIEW_REQUIRED.
- xG capture timestamps/revision provenance unverified; xG quarantined.
- League positions provisional pending competition-specific rules/tie-break verification.
- Cross-season H2H not verified.
- Historical accuracy/calibration/A+ and value not validated pending immutable pre-match predictions, official settlements and contemporaneous odds.
- Numeric confidence is not a validated metric; evidence risk is not match-outcome probability.

## Verified reference report

- Report run: 41223119793.
- Artifact: 13050950126.
- Output: 12-tab workbook, 434 fixture records, exact archive identity joins 434/434.
- QA: PARTIAL_RESEARCH_ONLY; production and betting eligibility remain false.
- Template v1.2 blob SHA at inspection: `a3ecb07805c1f4a6bf6beec52f355a10d1852c83`.

## Next operational step

Continue the field-level audit against the dictionary and implementation. Inspect actual workflow runs and artifacts; do not infer run success from YAML. The full report workflow is manually dispatched by the user with the pinned archive confirmation and runtime run ID recorded in `docs/PROJECT_ORACLE_EXECUTION_PROTOCOL.md`. This integration cannot dispatch that workflow. No new manual run is claimed here.


## FootyStats identity resolver review — 2026-10-31

- Static review record: `docs/ORACLE_FOOTYSTATS_IDENTITY_RESOLVER_REVIEW_2026-10-31.md`.
- PR #31 remains a draft and is not mergeable (1,526 commits / 608 changed files); do not merge or synchronize the accumulated research branch wholesale.
- Identity & Settlement Evidence workflow run #20 (41222551893) passed on commit 92710c5dc2de4c022d6949d0df204cc4ad0e8a16: 7 resolver tests, 15 adapter tests, 10 identity/settlement register tests, 15 blocker-diagnostic tests, 18 snapshot/runtime coverage tests and 25 offline current-snapshot tests.
- That run is an offline regression result on its recorded commit, not proof of production integration or approved mappings.
- Static review identified three resolver gaps requiring correction before further integration: no approved competition-bridge gate; no explicit quarantine for multiple reference candidates; and timezone-naive ISO kickoff values are currently interpreted as UTC.
- Keep the resolver research-only, all mappings NOT_APPROVED, no API calls/credits, no production writes and no Oracle V1.6 changes. Correct these gaps with regression tests in a narrowly scoped research-only change and verify the exact commit before integration.
- Continue weekly Market Intelligence reports from the locked v1.2 template and existing generator. Identity resolver work must not alter report schemas or production probabilities.

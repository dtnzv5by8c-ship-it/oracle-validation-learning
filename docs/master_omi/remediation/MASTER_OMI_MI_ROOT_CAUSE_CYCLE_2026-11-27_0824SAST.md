# Master OMI MI Root-Cause Cycle — 2026-11-27 08:24 SAST

## Release posture
FAIL-CLOSED. No release workbook is admissible.

## Fresh-cycle evidence
- Rolling governed universe remains the sole current weekly spine.
- Latest public validation cycle observed the rolling spine at 392 fixtures / 50 leagues / 392 unique FootyStats fixture IDs.
- Current-data workflow run 45947611240 failed after the live-spine gate passed with 392 rows and 100% coverage.
- Failure occurred in current Team State construction before durable publication.
- No dated frozen spine was substituted.

## Root-cause matrix

| Field / scope | Fixture / scope | Root cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Current Team State | 392 governed fixtures | Builder still depended on name/alias resolution and cross-provider historical replay; it crashed when an unresolved history key contained None and sorted mixed None/string values. This also violated exact-provider identity policy. | FootyStats current_matches.csv + governed rolling spine | Rebuilt builder around exact (league_id, provider_team_id) history from FootyStats current_matches only; exact fixture_id; strict kickoff-before-target PIT; no aliases/name admission; explicit unavailable classification. | FIXED IN CODE |
| Regression control | Weekly recurrence | Existing persistence test still asserted the removed UPCOMING_CODE_TO_LEAGUE mapping, so the new exact-ID implementation could not pass the old test contract. | Repository test suite | Replaced mapping assertion with exact provider-ID contract assertions; added dedicated exact-identity regression test. | FIXED |
| Workflow dependency | Current Data | Current-data workflow did not trigger on Team State builder/test changes. | .github/workflows/oracle_current_data.yml | Added builder and regression-test paths to push trigger. | FIXED |
| Cross-source reconciliation | 2,733 current rows | FotMob/SofaScore reconciliation returned 0 matches and 2,733 UNVERIFIED because SofaScore retrieval is HTTP 403. | reconcile_current_sources.py | Keep fail-closed/unverified; do not substitute unsupported provider. Primary FootyStats chain remains authoritative for governed MI. | UNVERIFIED / NON-SUBSTITUTED |
| Venue | 392 governed fixtures | Current FootyStats staging schema does not expose venue/stadium fields. | Current FootyStats staging + governed spine schema | Explicit UNAVAILABLE_SOURCE_SCHEMA; no inference or alternate provider substitution. | BLOCKER if canonical venue input is mandatory |
| xG PIT | Current MI | xG is admissible only where capture timestamp and pre-kickoff provenance are present. | FootyStats source payload provenance | Keep unverified where capture timestamp is absent; never backfill from post-kickoff data. | BLOCKER where mandatory |
| Canonical MI | Full release | Current source surface remains narrower than locked Master OMI schema. | V2.1.1 canonical contract | Build canonical append-only ET+ intelligence layer only from authoritative fields; missing mandatory inputs remain blockers. | BLOCKED |
| Persistence | Current Team State | Prior workflow had durable publication races/drift gates. | Current-data workflow | Existing hash/size/row-count remote verification retained; fresh exact-ID builder now feeds it. | AWAITING FRESH EXECUTION |
| Final QA | Full workbook | Independent 100% cell/type/provenance/chronology/leakage audit cannot pass until current Team State + prediction ledger + canonical MI candidate exist. | Independent QA gate | Run only after fresh chain completes; no green-workflow shortcut. | BLOCKED |

## Controls
- Oracle V1.6 production logic unchanged.
- A:ET immutable.
- No fuzzy matching.
- No estimates/guesses.
- No missing-to-zero.
- No stale fallback.
- No historical substitution across providers.
- No timezone normalization.
- No post-kickoff leakage.
- No unsupported provider substitution.
- Mandatory formula inputs fail closed.

## Next admissible chain
Fresh rolling 50-league spine -> exact FootyStats reconciliation -> exact provider-ID Team State -> durable persistence/hash verification -> exact current prediction ledger -> canonical Master OMI MI assembly -> exhaustive cell/type/provenance/PIT/chronology/leakage QA -> native XLSX/XML/hash certification -> independent 100%.

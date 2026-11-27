# Master OMI MI Root Cause Matrix — 2026-11-27 12:23 SAST

## Historical-first evidence
- Live rolling manifest: data/fixtures/governed_50league_current_manifest.json
- governed_leagues=50
- fixture_rows=392
- unique_provider_fixture_ids=392
- season_ids_with_fixtures=41
- generated_utc=2026-11-27T08:33:39.602844Z
- Current independent QA: docs/master_omi/qa/MASTER_OMI_MI_AUTOMATION_TURN11_CURRENT_2026-11-27_1119SAST.md
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e (reference contract remains unchanged)

## Root-cause matrix

| Field / workflow domain | Fixture / scope | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Current FootyStats intelligence fixture count | Current rolling 50-league set | Workflow hard-coded 385 current fixture rows, contradicting the rolling governed fixture contract and failing when the current set became 392 | Live rolling manifest + live workflow source | Commit c183a070214105616f3e35e43d3e3a7ca562f80f; derive count from current reconciliation input, reject empty input, assert summary/input parity | FIXED IN CODE; fresh runtime validation pending |
| Current reconciliation certificate | Current rolling set | Persisted reconciliation is older than the current 08:33 rolling spine and therefore cannot certify the current snapshot | current_reconciliation_status.json + current rolling manifest | Existing exact hash/Fixture-ID-set controls remain binding; do not promote stale certificate | BLOCKED PENDING FRESH RUN |
| Current prediction ledger | Current rolling set | Authoritative omi_prediction_ledger_current.csv absent at inspected public HEAD | Live public repository | Existing exact row/Fixture-ID parity gate; build from governed rolling spine | BLOCKED |
| Current Team State | Current rolling set | database/current_prematch_team_state.csv present but empty | Live public QA | Existing fail-closed persistence controls | BLOCKED |
| Canonical MI surface | Current rolling set | Upstream artifact 392x139 versus locked 264-column MI schema | Live current MI artifact + canonical V2.1.1 | Downstream canonical rebuild only; never pad/zero-fill | BLOCKED |
| xG PIT provenance | Current fixtures | 392/392 UNVERIFIED_NO_CAPTURE_TIMESTAMP | Current MI QA | Admit xG only with capture timestamp <= fixture PIT | BLOCKED |
| Provider completeness | Current fixtures | provider_status incomplete for 390/392 | Current MI QA | Resolve authoritative provider evidence or explicit unavailable/unverified classification | BLOCKED |
| Venue / H2H / LTSS / actuals / derived inputs | Current fixtures | Required fields absent or not certified in current upstream artifact | Current MI QA | Populate only from authoritative evidence; otherwise explicit status/reason/provenance | BLOCKED |
| Candidate workbook | Current release | No admissible current XLSX/XML candidate | Current independent QA | Build only after ledger + canonical MI exist; certify native types, formulas, A:ET, XML and hashes | BLOCKED |

## Regression controls
- Rolling fixture count must always be derived from the live governed reconciliation input; no fixed weekly fixture count.
- governed_leagues=50 is distinct from fixture-bearing season-ID count.
- Exact provider Fixture ID identity only.
- Exact rolling-spine and Fixture-ID-set hashes are authoritative; independent process timestamps need not match.
- No stale snapshot, fuzzy matching, historical fallback, estimation, zero-fill, timezone normalization or post-kickoff evidence.
- Missing mandatory inputs remain release blockers.
- Oracle V1.6 and A:ET remain immutable.

## Validation update — 2026-11-27 12:47 SAST
- Remediation commit c183a070214105616f3e35e43d3e3a7ca562f80f was exercised by workflow run 45966547927 (run 72), which completed successfully at 2026-11-27T08:33:46Z.
- The resulting current MI artifact is 392 rows × 139 columns and matches the live rolling spine at 392/392 exact provider Fixture IDs.
- This closes the fixed-fixture-count root cause. The release gate does not reopen it.
- The current rolling snapshot is nevertheless stale at this audit point because its generation time is 2026-11-27T08:33:39Z; freshness must be re-established by a later rolling rebuild before release.

## Release decision
FAIL-CLOSED. No release workbook is certified.

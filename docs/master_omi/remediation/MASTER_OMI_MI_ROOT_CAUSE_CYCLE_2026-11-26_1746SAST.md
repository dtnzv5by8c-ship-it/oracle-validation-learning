# Master OMI MI Root-Cause Cycle — 2026-11-26 17:46 SAST

## Gate status
FAIL-CLOSED. No release workbook certified.

## New root cause
The authoritative current-data workflow successfully ingested FootyStats and built a fresh current Team State, but the regression suite failed before persistence because the test still asserted the obsolete V4 branch/PR persistence contract.

Observed run:
- Public current-data run: 45851769421
- Failed job: 140019839509
- Fresh FootyStats ingestion: 2,594 matches; 198 upcoming; 2,594 prematch xG; 2,594 1X2 odds; 1 retrieval error.
- Current Team State: 14,001 rows; CSV/manifest integrity PASS.
- Current staging freshness: FRESH at 2026-11-26T15:43:48Z.
- Governed upcoming fixture identities matched: 0/429; therefore current staging was correctly NOT_READY.
- Independent current-source reconciliation: 0 matched; 2,594 unverified; source retrieval returned HTTP 403 errors.

### Root cause
The persistence regression test still required the obsolete run-specific persistence branch, PERSIST_PR_MODE=CONNECTOR_REQUIRED, and V4 branch persistence markers.

The production workflow has already moved to V5 direct-main persistence after validation, with rebase/hash/size/row verification. The test contract had not been updated.

### Fix
Updated private production repository test:
- Commit: 691aa243ce53bdd2636fd3d431dc4134aca0bdd7
- Changed test to assert the V5 direct-main contract:
  - rebase onto origin/main;
  - push HEAD:main;
  - remote size/hash/row verification;
  - PERSIST_MAIN_READY=true;
  - reject obsolete branch/PR contract.

### Verification action
Reran failed jobs for public current-data run 45851769421 after the private test fix. The rerun was accepted; completion evidence is still pending.

## Current weekly fixture spine
Only the rolling 50-league spine is admissible. No dated frozen spine was used. The public current-data reconciliation independently reported 429 governed upcoming identities absent from the fresh private FootyStats staging, so it correctly failed closed rather than fuzzy-matching or substituting stale data.

## Mandatory MI controls
A:ET unchanged. Oracle V1.6 unchanged. No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, post-kickoff evidence, or stale/frozen weekly spine substitution.

## Next gate
1. Complete rerun of current-data workflow.
2. If current staging remains NOT_READY, trace the 429 exact-identity gap to provider ingestion/mapping rather than bypassing the gate.
3. Resolve FootyStats retrieval error(s) and independent-source 403 handling where authoritative evidence is required.
4. Refresh/reconcile rolling 50-league spine again.
5. Generate current prediction ledger only after authoritative current state is READY.
6. Rebuild canonical 264-column MI.
7. Run exhaustive cell/type/provenance/chronology/leakage QA.
8. Native XLSX/XML/hash certification.
9. Release only at 100%.

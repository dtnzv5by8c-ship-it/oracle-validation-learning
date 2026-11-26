# Master OMI MI Root Cause — 2026-11-27 00:26 SAST

## Root causes
1. Rolling 50-league current spine is not fresh enough at audit time despite being fresh when generated.
2. Current FootyStats staging contains 2,672 match rows but none of the 429 governed upcoming fixture identities reconcile exactly to the governed spine.
3. Current Team State is populated (14,027 rows) but cannot be promoted because the governed fixture join is 0/429.
4. Authoritative current prediction ledger is not certified in the current persisted evidence.
5. Candidate XLSX/XML binary is not exposed for independent native-type/formula/hash/A:ET certification.

## Controls
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, or post-kickoff evidence accepted. Static checks already passed in prior evidence are not reopened as outstanding defects.

## Release decision
FAIL-CLOSED. Do not release Master OMI until the fresh-source and exact-identity gates pass, followed by current ledger/team state, fresh 754x264 rebuild, and independent candidate binary certification.

# FootyStats signed ingestion receipt contract v2

**Status:** consumer-side verifier implemented; trusted signer/key provisioning and private-writer integration remain pending.  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** offline contract and validation only. No provider calls, private repository writes, raw payloads or secrets.

## Why v1 receipts are no longer sufficient

The prior receipt contract accepted SHA-256-shaped strings and boolean claims such as `budget_ledger_attested=true` and `private_archive_write_verified=true`. Canonical JSON in `receipt_signature` was only used to detect conflicting receipts; it was not a cryptographic signature. Those fields cannot prove that an archive object exists, that its bytes match the supplied digest, or that a request was consumed in the authoritative global ledger.

The offline planner now rejects legacy boolean-only success receipts. A successful receipt must carry two independently authenticated attestations.

## 1. Private archive read-back attestation

The archive verifier signs canonical JSON claims using HMAC-SHA256.

- Signer ID: `oracle-private-archive-readback-verifier`
- Key ID: `private-archive-readback-v1`
- Protected environment key: `FOOTYSTATS_ARCHIVE_VERIFIER_HMAC_KEY`
- Minimum key length: 32 UTF-8 bytes

Required claims include exact task identity (task ID, provider, provider-season ID, endpoint and page); private archive object ID, immutable object version and byte size; payload SHA-256; archive receipt object ID and SHA-256; confirmation that the verifier independently read back and hashed both objects; confirmation that the private writer receipt signature was authenticated; private visibility and private raw-storage confirmation; explicit confirmation that no raw payload was written publicly; response-metadata SHA-256; and a timezone-aware verification timestamp.

The archive attestation's `response_metadata_sha256` binds the following receipt fields: HTTP status, provider success, response shape, page completeness, total results, page number/count, returned-row count, unique-ID count, required fields present/missing, completed-match count, goal-field gaps, no-home-away count and xG missing fields.

## 2. Central budget-ledger attestation

The central budget verifier signs canonical JSON claims using a separate HMAC-SHA256 key.

- Signer ID: `oracle-central-budget-ledger-verifier`
- Key ID: `central-budget-ledger-v1`
- Protected environment key: `FOOTYSTATS_BUDGET_VERIFIER_HMAC_KEY`
- Minimum key length: 32 UTF-8 bytes

Required claims include exact task identity; reservation ID; resolved authoritative ledger-entry ID; unique request-event ID; exactly one request; request timestamp; rolling-60-minute request count after the event; hard limit exactly 1,800; operational limit no greater than 1,500; at least 300 reserved headroom; confirmation that lower provider limits were enforced; successful resolution of both the ledger record and request event; and a timezone-aware verification timestamp.

The planner also checks that the signed reservation ID, request timestamp, hard limit and headroom match the receipt's top-level fields.

## 3. Verification and failure behavior

The planner canonicalizes each `claims` object using UTF-8 JSON with sorted keys and compact separators, then verifies the HMAC with constant-time comparison. The archive and budget keys are separate and are loaded only from protected environment variables. They are never logged or written to public output.

A success receipt is blocked when either key is missing, either signature is invalid, task identity differs, archive object/receipt hashes are not independently verified, response metadata digest differs, the private writer receipt is not authenticated, the central ledger event cannot be resolved, the request count is not exactly one, or any limit/headroom invariant fails.

Failed provider receipts remain stop signals; they cannot mark a task complete. Existing 429/401/403/provider-failure handling remains fail-closed and has no automatic retry.

## 4. Integration prerequisites

This is a consumer-side verifier only. The protected private archive writer must emit a read-back attestation after independently verifying the actual object bytes and signed writer receipt. The central budget ledger verifier must emit a separate attestation after resolving the authoritative reservation and actual request event. The protected keys must be provisioned only in the trusted execution environment and must not be committed to this public repository.

This workstream is not authorized to modify the private `oracle-football-data` repository. Therefore the existing private writer has not been changed to emit v2 attestations, and no real v2 receipt/key has been provisioned or tested. **No historical ingestion may be dispatched until that trusted integration exists and is independently validated.**

## 5. Current dry-run and governance

The planner still reports 728 planned tasks, 0 completed, 728 pending, `dispatch_allowed=false`, and research/betting eligibility false. The new summary explicitly reports that HMAC-authenticated archive read-back and central ledger attestations are required. No provider API calls were made by this work.

Oracle V1.6 production logic, probabilities, thresholds, calibration and ledgers remain unchanged. Raw provider payloads and secrets remain prohibited from the public repository.

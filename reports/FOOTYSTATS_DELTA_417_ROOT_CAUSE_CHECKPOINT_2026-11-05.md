# Project Oracle — FootyStats Delta 417 Checkpoint

Date: 2026-11-05

## Observed run
- Workflow run: 42070473567
- Head commit: 668b875dcd337f1b877ecdc5e89613927aa238bd
- Result: failed closed
- Provider requests observed: 1
- Pre-provider gates: confirmation, exact 20-season delta, and 100-request reservation all passed.
- Provider step: HTTP 417.
- Finalization: passed and sanitized evidence was preserved.

## Related evidence
- Prior run 42055869598 recorded HTTP 401 after one provider request.
- Prior 910-request preflight is not rerun.
- Rolling ledger records the one-request abort; no raw provider payload is persisted publicly.

## Repair committed on main
- Commit: 928f2c72e203fd41408090cfe9bf2e80f8502732
- Transport now mirrors the documented FootyStats GET contract: HTTP/1.1, explicit empty Expect header, standard query-string encoding, and sanitized non-200 classification.
- HTTP 417 is classified as UPSTREAM_EXPECTATION_OR_PROXY; 401/403 or explicit invalid-key/authentication responses are classified as AUTHENTICATION_OR_ENTITLEMENT.
- Provider response bodies are never published to the public repository.

## Governance
- 50/50 governed leagues preserved.
- 182 provider seasons preserved.
- 728-task historical ingestion plan preserved.
- Oracle V1.6 production logic, probabilities, thresholds, calibration and governance unchanged.
- Private oracle-football-data ingestion remains blocked until public gateway/preflight gates pass.

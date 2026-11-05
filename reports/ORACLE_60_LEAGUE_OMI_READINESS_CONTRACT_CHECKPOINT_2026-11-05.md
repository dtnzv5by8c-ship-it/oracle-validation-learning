# Oracle 60-League OMI Readiness Contract Checkpoint — 2026-11-05

## Scope
The governed target is now the **60-League Universe**, with historical football data from **2024 through current**.

This checkpoint extends the existing OMI/Market Intelligence reporting architecture without changing Oracle V1.6 production logic, probabilities, thresholds or calibration.

## Work completed
- Added `scripts/validate_omi_universe_readiness.py`.
- Added `tests/test_omi_universe_readiness.py`.
- Added `.github/workflows/oracle-omi-60-league-readiness-contract.yml`.
- The validator is research-only, fail-closed and does not calculate or modify Oracle probabilities.
- It validates:
  - exact governed league-count admission;
  - unique canonical league IDs;
  - 2024+ season boundary;
  - OMI required headers;
  - exact composite fixture identity (provider season + fixture + home team + away team);
  - provider-season membership;
  - pre-kickoff history cutoff;
  - probability range 0–100;
  - required recent-form / league-position / H2H / xG fields;
  - UTC retrieval timestamp;
  - actual-score integrity;
  - settlement status consistency.

## Reuse / governance
The contract deliberately reuses the locked OMI Market Intelligence schema and existing report-builder field names. It does not replace the existing 95-column Book4 baseline, Visual Intelligence logic, H2H logic, recent-form logic, actual-result/backtesting logic or Oracle V1.6 output.

## Admission state
No upstream provider data is fabricated or admitted by this contract. The existing provider gateway/ingestion gate remains authoritative. Once a validated 60-league manifest and admitted OMI dataset are available, this contract can be run against them before downstream report release.

## Next bounded step
1. Validate the canonical 60-league manifest when admitted.
2. Run the OMI readiness contract against the first bounded historical ingestion batch.
3. Reconcile exact IDs and chronology before adding rows to downstream OMI/Visual Intelligence.
4. Promote only rows passing provenance/settlement gates.
5. Continue batch-by-batch through 2024-current.

## Production safety
- Oracle V1.6 production logic: unchanged.
- Oracle probabilities: unchanged.
- Provider transport gate: unchanged.
- Fail-closed behavior: preserved.

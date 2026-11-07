# Project Oracle — FootyStats Receipt / Manifest Reconciliation — 2026-11-07

## Major milestone

The previously reported FootyStats manifest-hash discrepancy has now been independently resolved at the **content and task-ID level**.

### Verified evidence

Private provider checkpoint:
- Batch/run: `42255401046`
- Completed tasks: 100
- Rows requested/received: 8,367 / 8,367
- Provider requests: 100
- Manifest blob recorded by provider: `57fe9e1184b5035327feaa78307750e129c54bf3`
- Manifest file SHA-256: `58bd06ed9c5a6a09ed55eb833319ca09cd4f01e2b175e4ca9127a1b3a7f689d7`

### Deterministic reconciliation

The provider workflow explicitly references:

`oracle-validation-learning/57fe9e.../data/footystats/selected50-full-ingestion-manifest.csv`

Fetching that exact historical manifest and the current governed manifest produced:
- Historical manifest blob SHA returned by GitHub: `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`
- Current governed manifest blob SHA: `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`
- Content length: 116,108 bytes for both
- Content comparison: **EXACT MATCH**
- Governed task count: 728

The earlier `57fe9e...` value is the provider workflow's recorded plan/ref identifier, while the actual GitHub blob for the referenced manifest resolves to `6a916c...`. This is a reference/version-label distinction, not a manifest-content discrepancy.

The private completion checkpoint for run `42255401046` contains 100 explicit task IDs. Deterministic comparison against the current 728-task manifest shows:
- Receipt task IDs: 100
- Matched current manifest task IDs: **100**
- Missing task IDs: **0**

## Admission decision

The 100-task receipt is **admissible as private evidence for those 100 exact governed tasks**.

It is a subset of the 728-task plan and must not be double-counted.

This does **not** by itself prove all 728 tasks are evidenced, nor does it make production/betting eligible.

## Corrected accounting

The acquisition control-plane accounting remains:
- 728 governed tasks
- 648 completed
- 80 quarantined/provider-blocked
- 0 pending
- 648 + 80 + 0 = 728

The 100-task receipt is evidence within that governed population; it is not an additional 100 tasks.

## Next blocker — now clearly isolated

The remaining acquisition problem is no longer manifest compatibility.

The next work is:
1. reconcile the evidence supporting the 648 completed-task population;
2. enumerate and root-cause the 80 HTTP-417 quarantined tasks;
3. validate whether the completed evidence satisfies identity, pagination, chronology and freshness;
4. separately close point-in-time provenance for xG and odds;
5. build immutable prediction → fixture → pre-kickoff feature snapshot → verified settlement linkage;
6. then advance OMI/release gates.

### Governance

- Oracle V1.6 production logic unchanged.
- Production probabilities/thresholds/calibration unchanged.
- Production eligible: false.
- Betting eligible: false.
- No public provider transport used.
- No raw private payloads exposed.
- No research metric promoted to production.
- No ingestion workflow rerun.

This checkpoint supersedes the earlier interpretation that the manifest hashes represented incompatible manifests.

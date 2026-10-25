# Selected-50 Archive Evidence-Layer Reconciliation — 2026-10-26

**Status:** PASS for inventory reconciliation only; research-only; production eligibility remains `NO`.

## Verification evidence

- Branch at execution: `917ae479fa8d4b720d11cdb3cdfd28388511043d`
- Dry-run workflow: [40247101627 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40247101627)
- Artifact: [12618679274 — oracle-selected50-dry-run-plan](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40247101627/artifacts/12618679274)
- Artifact digest: `sha256:7ad4a60923efb6693fad64d5cec82c2281d198342117adf070b042b3995c5c5d`
- New no-network builder: `scripts/build_selected50_archive_evidence_reconciliation.py`
- Regression test: `tests/test_selected50_archive_evidence_reconciliation.py`

## Findings

| Evidence class | Selected groups | Reported match rows | Interpretation |
|---|---:|---:|---|
| Exact Run 56 selected-season-ID manifest match | 31 | 9,708 | Exact selected ID is present in the Run 56 manifest evidence. |
| Run 56 manifest gap reconciled to retained private-package row-level QA | 19 | 4,343 | The ID is absent from the Run 56 manifest snapshot but has a row-level private-package QA record in the separate gap-triage evidence. |
| Total selected IDs accounted for | 50 | Not summed | The two row-count fields come from distinct evidence fields and are not asserted to form a deduplicated archive total. |

For the 19 gap-triage groups, the retained evidence reports:
- 2,822 rows in the primary window (2025-03-20 through 2026-09-20, as recorded by the source field).
- 3,476 fixture rows with recent-five form available for both teams.
- 2,251 rows with a prior H2H meeting.
- Two groups with zero primary-window rows: Australia A-League (selected ID `17326`) and India Indian Super League (selected ID `17964`). Do not fill their history from guesses; verify prior-season evidence or quarantine them from markets requiring sufficient form.

The matrix explicitly retains unresolved/blocked statuses for all 50:
- Parent provider competition ID: `UNRESOLVED`.
- Canonical fixture join: `NOT_VERIFIED`.
- Canonical team join: `NOT_VERIFIED`.
- Official settlement truth: `NOT_VERIFIED`.
- Historical standings as of kickoff and point-in-time xG/odds provenance: `NOT_VERIFIED`.
- `production_eligible=NO`.

## Output files

- `audit-output/selected50_archive_evidence_reconciliation.csv` — 50-row sanitized matrix.
- `audit-output/selected50_archive_evidence_reconciliation.json` — summary and explicit limitations.

These are included in the dry-run artifact. Raw provider payloads are not included.

## Safety and next action

The new workflow steps passed:
1. Build the reconciliation without network calls.
2. Validate the 50-row matrix and status invariants.
3. Upload only sanitized audit outputs.

No FootyStats requests or credits were used. No private-repository Actions workflow was dispatched. The diagnostic does not infer parent competition IDs from season IDs and does not claim canonical fixture/team joins or official settlement truth.

**Next action:** reconcile canonical competition/team/fixture identity and settlement truth using existing private evidence. Only consider the bounded live `league-teams` probe after the existing explicit provider-credit confirmation gate is satisfied. Keep Combo blocked until its market definition and settlement ledger are reconciled. Production remains `NOT_GRANTED`; M-1UP remains blocked.

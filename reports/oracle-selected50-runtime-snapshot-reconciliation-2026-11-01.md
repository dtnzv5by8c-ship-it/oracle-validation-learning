# Project Oracle — Selected-50 runtime/snapshot reconciliation

**Evidence cutoff:** 1 November 2026 (SAST)  
**Lane:** Research/reporting only. No production writes, model changes, provider API calls or betting approval.

## Exact source artifacts

- Current-fixture snapshot run: `41174900415`; artifact: `13031728960`.
- Research runtime run: `41175230838`; artifact: `13032880970`.
- Snapshot retrieved: `2026-10-31T06:02:13.776050+00:00`.
- Runtime generated: `2026-10-31T06:11:36.951760+00:00`.
- Snapshot artifact and runtime ZIP were downloaded and inspected. Runtime ZIP SHA-256: `e4bca38c8ab8e6afd5c23d241e4b55fe3ce6277e656172e8cda910718c897ae0`.

## Reconciliation results

- Runtime report: 434 rows / 434 unique fixture IDs.
- Current snapshot: 2,262 rows.
- Current snapshot within seven days after the 15-minute minimum lead-time cutoff: 441 rows (432 `incomplete`, 9 `suspended`).
- All 434 runtime fixture IDs are present in the snapshot trace and all 434 have exact ordered provider home/away team-ID matches.
- Runtime-vs-snapshot kickoff values differ on 27 of the 434 shared fixture IDs.
- 66 runtime rows carry provider `no_home_away=1`.
- 7 runtime rows are marked `suspended` in the current snapshot.
- 10 runtime rows now fall outside the snapshot's seven-day future window or are historical.
- 17 current-snapshot future rows are absent from the runtime report.

### Disjoint runtime-row states

| State | Rows |
|---|---:|
| Runtime/snapshot exact schedule match | 351 |
| Runtime included while provider `no_home_away` flag is set | 66 |
| Runtime included while current snapshot status is suspended | 7 |
| Runtime included but current snapshot kickoff is now historical or outside seven days | 10 |
| **Runtime rows** | **434** |

### Snapshot-only future rows

- 15 are quarantined because `no_home_away=1`.
- 2 are quarantined because status is suspended/nonstandard.

The detailed 451-row reconciliation CSV is preserved as a separate local deliverable. Its SHA-256 is `bf03320f372d3019e94104977d39e6b869802a87fcbef2a989c5d4e6327a48f3`.

## Interpretation and root-cause leads

1. The current runtime report is not a complete reflection of the later snapshot's schedule/status state. The 27 kickoff disagreements and 17 snapshot-only rows need manual event-level reconciliation; no automatic correction is authorised.
2. The runtime and snapshot preserve exact ordered provider team IDs for all 434 runtime fixtures, so the observed disagreement is not an ordered team-ID join failure in this artifact pair.
3. The `no_home_away` field requires provider clarification. FootyStats' public API overview lists it in the **League Variable Description** section but does not define its semantics. Do not interpret it as a match-level neutral-venue flag or assume it can safely be ignored. Confirm whether it is a season/competition-wide format flag and how it should affect fixture home/away orientation.
4. The runtime report records `xg_named_field_count=6` and `odds_xg_provenance_status=UNVERIFIED_NOT_USED_IN_MODEL` for all 434 fixtures. This is field-presence/provenance status only; it does not approve xG. The historical archive still has no capture manifest/timestamp evidence.

## Required next actions

1. Add a report-only reconciliation state to the recurring Market Intelligence output so stale, suspended, outside-horizon and provider-flagged fixtures are visible without changing model probabilities.
2. Obtain a written FootyStats definition for `no_home_away` and its fixture-orientation consequences.
3. Re-run the report repair workflow against a fresh successful runtime artifact after the snapshot/runtime discrepancies are resolved.
4. Continue xG provenance work under the existing evidence contract. Keep all pre-match-labelled xG quarantined until immutable pre-kickoff capture/revision evidence is supplied.

## Governance

No Oracle V1.6 production logic, thresholds or probabilities were changed. The research runtime itself marks all 434 fixtures production-ineligible and betting-ineligible. The 434 xG-bearing rows remain unapproved; no xG feature was introduced. This report does not grant production or betting eligibility.

# Selected-50 Pre-Batch-5 Private-Archive Coverage & Provenance Snapshot — 2026-10-26

**Snapshot status:** `PRE_BATCH5_QA_SNAPSHOT_SUPERSEDED_FOR_CURRENT_ARCHIVE_COVERAGE`. The QA evidence below is retained for provenance, but it is **not the current historical-archive coverage view**.

The source QA run [40183451811](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183451811) was created at 2026-10-25 10:07:11 UTC. The later 200-season historical ingestion [40375285207](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40375285207) completed at 2026-10-26 18:12:52 UTC. This report's source predates that ingestion; its 14,051-row selected-season snapshot and status counts must not be treated as QA of the later 200-season archive.

The historical snapshot remains useful for its documented checks, but current archive coverage must be taken from a QA artifact generated against the exact batch-5 archive tag. All results remain research-only; production eligibility is **NOT GRANTED**.

## Verification

- Private archive QA source run: [40183451811 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183451811)
- Sanitized QA artifact: [12594568810](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183451811/artifacts/12594568810)
- Sanitized QA artifact SHA-256: `713ed63ed5dd6e6902a2e152367500386d5037dd6dc8bbc82fa87c831d10c375`
- Current no-network validation run: [40247504417 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40247504417)
- Current dry-run artifact: [12619680465](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40247504417/artifacts/12619680465)
- Dry-run artifact SHA-256: `05bd352bc01be7d557c70f0123888fc917502840b5f6501a4ec47fde112d426b`
- Matrix: `selected50_latest_private_archive_coverage_matrix.csv` (50 rows, 41 columns)
- Summary: `selected50_latest_private_archive_coverage_summary.json`

The artifact contains sanitized aggregate/season-level QA only. Raw provider match payloads were not published.

## Coverage established by this pre-batch-5 selected-season snapshot

| Check | Verified result |
|---|---:|
| Selected season IDs in manifest | 50 |
| Exact selected ID set match | 50/50 |
| Manifest metadata matches | 50/50 |
| Country + competition composite label matches | 50/50 |
| Season folders audited / files OK | 50/50 |
| Match records retained in private archive | 14,051 |
| Unique season-fixture ID pairs | 14,051 |
| Duplicate season-fixture pairs | 0 |
| Fixture-ID, kickoff-like, team-ID pair, team-name pair and score-pair field presence | 100% each |
| Rows in the locked primary window (2025-03-20–2026-09-20) | 5,637 |
| Recent-five prior-form rows available for both teams | 11,744 |
| Seasons with any recent-five form for both teams | 48/50 |
| Prior H2H meeting rows | 5,294 |
| Nonempty table payloads | 50/50 |

The pre-batch-5 selected-season snapshot therefore had evidence for all 50 selected season IDs. It does not certify the later 200-season historical archive ingested by run 40375285207. The earlier Run 56 split of 31 direct manifest matches and 19 manifest gaps is an older manifest snapshot; it must not be used to claim that 19 seasons are absent from the latest private archive. The latest QA reconciles private season-folder presence for all 50 IDs. **This still does not establish parent competition IDs or canonical Oracle fixture/team joins.**

## Important data-quality limitations

- **Parent competition IDs:** 0 populated. The source catalogue exposes season IDs, not a verified parent competition ID. Do not infer one.
- **Separate country metadata:** 0 retained as a separate field. The country + competition composite label matches all 50, but the country field itself is not retained in the audited payload.
- **Result truth:** the score-pair fields are present for all rows, including future/incomplete records. This is field-presence evidence, not proof that a match is settled or its result is valid for market settlement.
- **Status/date discrepancy:** provider status counts are 6,916 `complete`, 7,083 `incomplete`, and 52 `suspended`; the completed-status candidate and past-kickoff counts are 6,912. That leaves a four-record difference to reconcile. Another 135 records have neither past nor future kickoff-date classification in this snapshot.
- **Primary-window limitations:** the current season archive's observed date range is 2026-01-16 to 2027-06-06. Its 5,637 primary-window rows do not prove complete coverage of the full 18-month validation window.
- **Recent form:** Australia A-League (selected ID `17326`) and India Indian Super League (`17964`) have zero primary-window rows and zero recent-five prior-form rows in this season snapshot. Verify approved prior-season history or keep affected markets blocked.
- **Season-year labels:** 33 raw values are the nonstandard eight-digit token `20262027`; 17 are `2026`. Preserve the raw value and resolve the provider schema before normalising season labels.
- **Standings:** all 50 seasons have nonempty table payloads, but historical standings as of kickoff are not verified.
- **xG:** nonempty prematch xG fields are present on 14,051 rows, but no as-of timestamp provenance is established.
- **Odds:** nonempty odds values are present on 7,330 rows (52.17%), but zero odds timestamps are observed. No odds-based ROI benchmark is approved.
- **Current feed and canonical mapping:** current-feed identity is blocked across all 50 groups; 22 canonical-code candidates require human review and 28 remain unresolved. Candidate codes are not approved mappings.

## Release and market gates

- Canonical Oracle fixture join: `NOT_VERIFIED` for all 50.
- Canonical Oracle team join: `NOT_VERIFIED` for all 50.
- Official settlement truth: `NOT_VERIFIED` for all 50.
- Historical standings-as-of-kickoff: `NOT_VERIFIED`.
- Point-in-time xG/odds: `NOT_VERIFIED`.
- BTTS and Double Chance: research outputs only; not production-ready.
- Combo: blocked until predictor target and settlement comparator are reconciled.
- M-1UP: blocked; independent event-truth gate not passed.
- Production eligibility: `NOT_GRANTED`.

## Next action

Do not use this pre-batch-5 report as the latest archive-coverage view. The live provider first-page audit is run 40391540391; the multi-year historical runtime used the batch-5 private archive and completed successfully in run 40400232375. A fresh private-archive QA run against the exact batch-5 archive is still needed to reconcile row-level status/date exceptions with that archive. Next reconcile canonical Oracle fixture/team IDs and completed-result settlement truth from approved evidence. Resolve the season-year encoding and status/date discrepancies. Do not use xG/odds as point-in-time features or ROI benchmarks without timestamps and provenance. Do not dispatch private Actions or make provider calls until the existing spending/credit gates permit them.

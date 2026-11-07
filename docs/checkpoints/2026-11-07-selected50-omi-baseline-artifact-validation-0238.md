# Project Oracle — Selected-50 OMI Baseline Artifact Validation — 2026-11-07

## Scope
Governed research lane: `research/oracle-50-league-readiness-audit`. Exactly 50 selected leagues only.

## Baseline
Selected-50 Market Intelligence Report Repair workflow run **#360** completed successfully on 2026-11-06:
- run_id: `42309893170`
- head commit: `f084491b95be1df95d0d59b8d2d08d16ab6dbfbc`
- workflow: `Oracle Selected-50 Market Intelligence Report Repair`
- conclusion: `success`
- artifact: `oracle-selected50-market-intelligence-repair`
- artifact id: `13547044125`
- artifact SHA-256: `91cf647eb7a19d2f3e263347194c76477f60a2de0cf9ff90afab38d6227e7dfc`

The live research branch is now ahead of the repair commit by two research-only checkpoint commits; the repair commit is therefore an ancestor of the current branch state and is a valid downstream OMI baseline.

## Artifact inspection
The workflow artifact was downloaded and inspected before any new work. It contains the rebuilt Market Intelligence workbook and the associated QA/evidence outputs, including:
- 717 runtime fixture rows
- exact archive joins: 717/717
- unmatched/quarantined runtime joins: 0
- schedule discordance rows: 0
- 50 selected league groups
- archive index rows: 59,049
- retained completed H2H meetings: 51,983
- field-by-field coverage matrix: 18,000 league-field rows
- field audit exceptions: 1,622
- actual-results register: 717 rows, but all settlement states are `NOT_RETRIEVED_NO_CREDIT_APPROVAL`
- xG numeric values exist for all 717 rows, but verified capture timestamps are 0; xG remains audit-only
- runtime snapshot trace rows: 0; the artifact explicitly marks this as historical-only orientation and does not infer home/away from absent snapshot evidence.

## Readiness interpretation
The successful repair proves the downstream research artifact is internally constructed and QA'd; it does **not** make every feature production-ready.

### READY
- 50-league scope control
- fixture identity and exact archive joins
- archive index integrity
- chronology rule enforcement (history strictly before fixture kickoff)
- recent-form fields where the artifact reports usable values
- report/evidence trace assignment with no unmapped source rows
- field-level coverage accounting
- research-only risk/data-quality reporting

### PARTIAL
- BTTS and 1X/X2 research values: usable on 678/717 rows (94.56%)
- recent-form goal/points/index fields: usable on 705/717 rows (98.33%)
- H2H: available only where exact prior history exists; no inference is allowed
- goal-market research: report-only/experimental and explicitly blocked where unavailable
- standings/strength: present but some rows are provisional
- venue/home-away evidence: research coverage exists, but absent snapshot overlay prevents pre-kickoff snapshot qualification
- five selected leagues have no fixture rows in the current report horizon; this is a schedule-window state, not evidence of missing historical data.

### BLOCKED
- xG production/prediction admission: 717/717 rows have numeric xG, but **0/717 have verified capture timestamps**; policy is `AUDIT_ONLY_UNTIL_POINT_IN_TIME_CAPTURE_AND_REVISION_PROVENANCE_VERIFIED`.
- timestamped odds: no admissible point-in-time provenance is established in this artifact baseline.
- actual-result settlement/backtesting: 717/717 are `NOT_RETRIEVED_NO_CREDIT_APPROVAL`; no provider result calls were made.
- production/betting eligibility: explicitly false.
- historical accuracy grading: not validated against an immutable official settlement join.
- snapshot-linked pre-kickoff prediction provenance: 0 snapshot trace rows.

## Quantified exception picture
Field audit QA reports:
- 360 field occurrences audited
- 1,622 exception rows
- 160 partial-value coverage
- 881 explicitly unavailable/blocked
- 581 with no usable values
- 0 unmapped source rows
- 0 production-model changes
- 0 production-probability changes

## Safety decision
- No acquisition triggered.
- No provider/API calls made.
- No PARTIAL/BLOCKED/unvalidated evidence promoted.
- No future/unsettled data treated as settled.
- No missing feature fabricated.
- Oracle V1.6 production probabilities, thresholds, decision logic, calibration and governance unchanged.
- Production and betting admission remain fail-closed.

## Next actionable checkpoint
Build the research-only READY/PARTIAL/BLOCKED matrix at league × season × endpoint × feature-family level from the artifact's field coverage and evidence-trace tables. Prioritize resolution of:
1. point-in-time xG capture/revision provenance;
2. timestamped odds provenance;
3. immutable prediction/feature snapshot to official settlement linkage;
4. feature-family gaps identified by the 1,622 audited exceptions.

No manual workflow dispatch is required for this research lane.

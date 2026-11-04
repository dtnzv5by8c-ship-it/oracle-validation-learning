# Project Oracle — Historical Feature Admission Gate Matrix
## Research-only checkpoint — 2026-11-05

Scope: offline governance/audit only. No provider API calls. No private-repository access. No production Oracle V1.6 changes.

## Decision

The current evidence supports a fail-closed historical feature admission matrix, but does not support promoting any historical feature to production or betting eligibility.

| Feature | Admission requirement | Current evidence | Status |
|---|---|---|---|
| Fixture identity | Exact provider fixture ID plus verified competition/season and unique key | 10-row sample has unique FootyStats IDs, but no complete fixture-ID archive | BLOCKED |
| Team identity | Exact provider home/away team IDs with cross-season continuity evidence | Aggregate archive reports team-ID completeness, but no fixture-level team IDs in sanitized evidence | BLOCKED |
| Kickoff chronology | Exact UTC kickoff at fixture level; strictly pre-kickoff history | Season plan has 182 partitions and exact global date window, but no complete fixture spine | BLOCKED |
| Results/goals | Verified final result and score tied to exact fixture ID | Aggregate archive reports complete score fields, but not fixture-level IDs | BLOCKED |
| H2H | Same verified competition; exact unordered team pair; completed prior matches strictly before target kickoff | Existing H2H research implementation uses strict earlier-date selection, but source identity/coverage is not complete | BLOCKED |
| Recent form | Exact team identity plus completed matches strictly before cutoff, no same-day leakage | No complete exact-ID chronological spine | BLOCKED |
| Home/away form | Exact ordered home/away IDs plus venue semantics; no_home_away rows quarantined | 6,398 legacy-parser flags; fixture-level semantics unresolved | BLOCKED |
| Fixture-time standings | Reconstruct standings from completed matches strictly before kickoff | No verified fixture-time standings spine | BLOCKED |
| xG | Point-in-time capture timestamp/provenance and revision policy proving value existed before kickoff | Existing xG evidence lacks sufficient point-in-time provenance | QUARANTINED |
| OMI/reporting | All required inputs pass the above gates | Schema/tests pass, but verified historical source receipt is absent | BLOCKED |

## Existing evidence

- Current FootyStats catalogue: 49 selected leagues / 756 catalogue season rows.
- Historical plan: 182 provider-season partitions intersecting 2024-01-01 through 2026-11-04.
- Provider preflight: 182/182 partitions, 910 requests; this is endpoint/pagination metadata, not historical ingestion.
- Preflight match rows: 54,546; team rows: 3,117.
- No-home-away audit: 6,398 explicit flags recognised by the legacy parser across 73 seasons / 31 leagues; the count is not retroactively revalidated against fixture rows.
- Existing Run56 archive evidence: 31/49 current leagues have selected-season snapshots; 18/49 have no Run56 evidence.
- Run56 aggregate evidence: 9,708 match records with complete team-ID fields, kickoff parsing and score pairs, but no fixture-level IDs in the aggregate CSV.
- Separate settlement register: 10 unique FootyStats fixture IDs and 10 unique FotMob fixture IDs; exact ordered team-name + UTC-kickoff joins, but no home/away team-ID columns and no canonical bridge approvals.
- Existing H2H research audit: 75,104 historical rows and strict earlier-date H2H selection in its research implementation, but production incremental-value testing remains unproven because canonical historical prediction/settlement pairing is absent.

## Non-negotiable chronology rules

1. A fixture cannot contribute to its own features.
2. Same-day fixtures cannot contribute to one another unless an independently verified event-time cutoff proves the source existed before the target kickoff.
3. Only completed, identity-verified matches may enter H2H, recent form, home/away form or standings.
4. Season labels never substitute for fixture-level kickoff dates.
5. Cross-year season partitions remain acquisition partitions; individual fixtures are admitted only when their exact UTC kickoff is inside the governed date window.
6. Unknown, duplicate or conflicting fixture identity fails closed.
7. no_home_away never means neutral venue by inference.
8. Absence of a no_home_away flag is not venue certification.
9. xG is excluded until point-in-time provenance and revision semantics are independently demonstrated.
10. Research metrics must not be converted into production accuracy claims or betting eligibility.

## Current hard gates

Historical dispatch remains disabled until:
- the private direct FootyStats API bypass is retired or centrally budget-gated;
- the protected private raw archive receipt path is validated;
- the shared request ledger is authoritative across all Oracle workflows.

Budget controls remain:
- hard maximum: 1,800 requests / rolling 60 minutes;
- operational maximum: 1,500;
- reserved headroom: 300.

## Governance

All outputs from this checkpoint are production_eligible=false and betting_eligible=false.

Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and eligibility were not changed.

## Next exact-ID work

The next research implementation should produce a sanitized fixture-level identity contract containing, at minimum:

provider_season_id, provider_fixture_id, kickoff_utc, home_team_id, away_team_id, competition_id, result_status, home_goals, away_goals

It must reject duplicates/conflicts, preserve raw provider IDs, and never infer identity from team names alone. That contract is the prerequisite for chronological H2H/form/standings reconstruction.

# FootyStats 49-league feature provenance and chronology gates

**Evidence date:** 4 November 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** current selected 49-league / 182-season acquisition plan; offline review of sanitized preflight metadata and existing endpoint/H2H/xG specifications. No provider calls, raw payload reads, private-repository writes or production changes.

## Current evidence boundary

The current selected catalogue contains 49 leagues and 756 provider-season rows. The 2024-01-01 through 2026-11-04 plan contains 182 exact provider-season IDs. The earlier FootyStats preflight (Run 41869437030) reported 54,546 match rows and 3,117 team rows across 182 season samples. Every season reported one matches page and one teams page, with returned match rows equal to provider `total_results`.

This is pagination-metadata evidence only. The 54,546 match rows have not been ingested into the protected private archive, cross-season deduplicated, admitted by exact kickoff UTC, or validated into a chronological current-49 match spine. The 728-task ingestion plan remains pending. Do not use older Selected-50 archive metrics as current-49 coverage.

## Feature readiness matrix

| Feature | Current 49 / 182 preflight evidence | Required acceptance gate | Current disposition |
|---|---|---|---|
| Fixtures | Match ID, ordered home/away team IDs, Unix kickoff and status fields observed in endpoint samples | Exact unique provider fixture ID; exact season ID; timezone-aware kickoff; inclusive UTC filter; reconcile duplicate fixture IDs across seasons | Not ingested / not certified |
| Results and goals | Preflight reports 47,641 completed rows in page samples and zero completed-match goal-field gaps | Explicit completed status; non-boolean integer home/away scores; consistent total goals; no score/status conflicts; exact fixture identity | Sample fields only; not historical coverage |
| Team identity | 3,117 team rows reported; team IDs unique on sampled season pages | Exact provider team ID, season membership, name/alias evidence; audit reuse/collision across seasons; never join by display name alone | Sample-page identity only |
| H2H | H2H field present in one match-detail sample for each of 182 seasons | Derive from exact completed match spine; same approved competition scope; exact stable team IDs; target fixture excluded; prior kickoff strictly less than target kickoff; duplicate/self-match/score conflict quarantine | Field present; chronology and coverage unverified |
| Recent form | No complete current-49 history reconstruction | Last 5/8 eligible completed matches per team, strictly before target kickoff; fixed settlement/status policy; exact match IDs; no look-ahead; explicit sample count and missing-feature reason | Not reconstructed |
| Home/away form | 6,398 explicit no-home-away flags were counted by the legacy parser across 73 seasons; 14 seasons had every sampled row flagged. The legacy parser did not count missing flag values. | Preserve ordered `homeID`/`awayID`; quarantine true, missing and unknown orientation; require validated venue semantics; no side reassignment or imputation | Quarantined / not reconstructed |
| Standings | `league-tables` returned current table shapes; timestamp/as-of behaviour not established for fixture-time positions | Use an independently validated as-of snapshot or reconstruct standings from completed results before kickoff, preserving rounds, groups, split phases, points and competition-specific tie-breakers | Current snapshot only; fixture-time standings unverified |
| xG | Match-detail sample exposes pre-match-labelled xG fields | Per-fixture point-in-time capture before kickoff, immutable raw-response hash, exact match/season/team IDs, capture timestamps and provider revision/effective-time semantics | Quarantined |

## 1. Fixture and result spine

The documented primary source is `league-matches` with exact `season_id`. Required match identity fields are `id`, `homeID`, `awayID`, `date_unix` and status. Goal fields include `homeGoalCount`, `awayGoalCount` and `totalGoalCount`.

Acceptance requirements:

1. Preserve provider match ID and provider season ID as separate keys.
2. Convert `date_unix` to an explicit UTC instant; do not derive kickoff from local display strings.
3. Apply `2024-01-01T00:00:00Z <= kickoff_utc <= 2026-11-04T23:59:59.999999Z` to every fixture, regardless of season label.
4. Validate page number, `total_results`, page size, expected page count and exact returned rows for every page.
5. Detect exact fixture-ID duplicates and conflicting copies across adjacent season partitions. Same team pair/date is not a substitute for exact fixture ID.
6. Admit a result only when status and score fields agree under one explicit completed-status policy. Reject booleans, non-integers, negative scores, missing scores and inconsistent total goals; quarantine rather than impute.

The preflight's zero goal-field gaps apply only to the 47,641 completed rows in its page samples. They do not establish completeness of the 182-season historical spine.

## 2. Team identity and cross-season continuity

The documented `league-teams` endpoint supplies team IDs and season membership. The current preflight only established unique IDs on each sampled page. It did not establish that a provider team ID is globally stable across seasons or that IDs are never reused after club renames, mergers, reserve-team changes or competition reconfiguration.

Required checks before cross-season H2H or recent-form joins:

- exact team ID retained with provider season ID and competition context;
- duplicate team IDs within a season quarantined unless the provider contract explicitly defines the duplication;
- same ID with materially conflicting names/aliases across seasons placed in a review queue, not automatically merged or split;
- team-pair/date and display-name matches remain candidate evidence only;
- home and away roles remain ordered, never sorted or inferred.

The prior Selected-50 identity runtime reported repeated team IDs across seasons, but that is an older scope and does not certify continuity for the current 49-league / 182-season plan.

## 3. H2H chronology and competition scope

The match-detail endpoint exposes an H2H field, but a field's presence does not establish chronological correctness. The lower-cost, auditable design is to derive H2H from the complete exact-ID match spine, with optional match-detail calls used only when specifically justified and budgeted.

For target fixture (F) at kickoff (t_F), only prior completed matches (M) satisfying (t_M < t_F) may contribute. Equality is excluded conservatively. The join must use exact team IDs and an explicit competition policy; cross-competition cup matches must not enter a league-only H2H feature unless the feature definition explicitly allows them.

Required diagnostics per target fixture:

- number of eligible prior H2H meetings;
- exact source match IDs and kickoff timestamps for the selected meetings;
- ordered home/away orientation and target-home perspective;
- same-competition mapping status and cross-season team-ID continuity;
- duplicate fixture-ID/signature exclusions, self-match exclusions and score/status conflicts;
- last prior meeting date and age at target kickoff;
- explicit `NO_VERIFIED_PRIOR_H2H` when no eligible meeting exists.

Older Selected-50 runtime reviews found H2H diagnostics were calculated/exported but not included in the active 20-feature baseline. That older research result is not a reason to add H2H to Oracle V1.6 or to this current 49-league workstream. Any H2H predictive experiment must remain separate from the frozen production model and use chronological paired evaluation.

## 4. Recent and home/away form

Recent form must be derived from the same admitted match spine, not current `league-season` aggregates or a precomputed team summary whose observation cutoff is unknown.

For each target fixture and team:

- select only eligible completed matches with kickoff strictly before the target;
- sort by exact UTC kickoff and exact match ID as a deterministic tie-breaker only after duplicate/collision review;
- report N and source fixture IDs for last 5 and last 8;
- preserve goals, BTTS, failed-to-score, clean-sheet and other field-specific denominators;
- require each input field to pass its own coverage and chronology gate;
- leave a feature unavailable when the required sample or identity evidence is insufficient.

Venue-specific form additionally requires an unambiguous ordered home/away assignment. The current 6,398 no-home-away count is subject to the parser missingness caveat: it is the legacy parser's recognized explicit-flag count, not proof that all flag values were populated or all encodings captured. The research parser has since been hardened to count missing flags and fail closed on unknown values, but the old 910-request preflight was not rerun. True, missing or unknown orientation must be excluded from home/away splits; non-flagged rows are not automatically certified.

A prior Selected-50 report also identified different descriptive `SETTLED` versus runtime `FINISHED` status policies and a five-match runtime feature gate. Keep these concepts distinct and do not relax the frozen production gate.

## 5. Fixture-time standings

A `league-tables` response may be a current snapshot, and the `max_time` parameter is documented for time-fenced league/team statistics. Neither fact alone proves that the returned table is a correct historical table immediately before every target fixture.

Preferred evidence hierarchy:

1. immutable provider table snapshot explicitly captured at or before the target kickoff, with request/response timestamps and exact competition/season/round identity; or
2. independent reconstruction from the validated completed-match spine, using only matches finished before the target kickoff and the competition's actual points, goal-difference, head-to-head, split-phase and tie-break rules.

A simple season-total reconstruction is insufficient for competitions with split rounds, groups, playoff phases or special tie-breakers. If the format or ruleset is not verified for a season, mark standings `UNVERIFIED`; do not infer table position from a current table.

## 6. xG provenance decision

The documented match-detail example exposes `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch` on a completed historical match alongside actual-match xG. The response does not provide field-level capture time or revision history. The `prematch` suffix is a field label, not proof that the value was frozen before kickoff. `max_time` is documented for league/team statistics, not as an immutable per-fixture xG snapshot.

To qualify any xG field for a pre-match feature, require:

- `response_received_at_utc < kickoff_utc` (a request started before kickoff but received after kickoff fails);
- exact provider match ID, season ID and ordered team IDs;
- exact raw response bytes stored only in the approved private archive;
- SHA-256 of those bytes and immutable object/version reference;
- request endpoint/parameters with credentials removed;
- capture client version and request-start/response-received timestamps;
- provider `updated_at`, effective timestamp or revision ID only when actually returned;
- documented provider field definition, historical availability and revision/correction semantics.

A client timestamp proves when Oracle received a value; it does not prove when the provider originally calculated it. Never fabricate provider timestamps or reconstruct historical pre-match xG from a current completed-match response. Until these conditions are met, all xG remains quarantined.

## 7. Current gates and governance

- Current 49-league selected catalogue: 49 leagues / 756 catalogue season rows.
- Current historical plan: 182 provider-season partitions / 2024-01-01 to 2026-11-04.
- Prior preflight: 910 requests, 182/182 endpoint preflights; do not rerun merely for Git reconciliation.
- Full ingestion: 728 tasks pending; no current-49 historical archive admission is certified.
- H2H, recent form, home/away form and fixture-time standings: not verified for current 49.
- xG: quarantined.
- Provider request dispatch: blocked until the separate private direct-API bypass is retired or centrally budget-gated and the protected private archive receipt path is independently validated.
- Global budget: hard cap 1,800 per rolling 60 minutes, operational maximum 1,500, at least 300 headroom; shared durable ledger and no uncontrolled retries.
- All research outputs remain `production_eligible=false` and `betting_eligible=false`.

No raw data, secrets, provider credits or production model logic were used or changed in this audit.

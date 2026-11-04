# FootyStats no_home_away aggregate audit — 2026-11-04

## Scope and evidence

This is an offline audit of the sanitized file `data/footystats/full-ingestion-manifest/season-ingestion-coverage.csv`. It does not read provider raw payloads, call FootyStats, or infer fixture identity or home/away assignments.

- Source CSV SHA-256: `1de6de240b1e2bd3e134850477198d8fcaf3159c40d03f7c0c8fe3c28ee92789`
- Source rows: 182 provider-season partitions across 49 selected provider leagues.
- Workflow: 41892011156 — completed successfully.
- Artifact: 13352979859 — `footystats-no-home-away-aggregate-audit`.
- Artifact SHA-256: `384dbe03ca0b5da3626229cb9b590f83700124d8179e6d7b3346c043cae5d133`
- Workflow verified the committed season and league rollups exactly match the offline builder.
- Provider API requests in this audit: 0.

## Aggregate findings

| Measure | Verified count |
|---|---:|
| Selected provider leagues | 49 |
| Provider-season partitions | 182 |
| Match rows in page-1 preflight samples | 54,546 |
| Explicit `no_home_away` flags reported | 6,398 |
| Page-1 rows carrying the flag | 11.73% |
| Seasons with at least one reported flag | 73 |
| Leagues with at least one reported flag | 31 |
| Seasons where every page-1 row is flagged | 14 |
| Fixture-level records inspected by this audit | 0 |

All 182 seasons reported one match page and one team page, and the returned match-row count equalled the provider-reported match total in each season. This remains pagination-metadata evidence, not historical ingestion or validation of a chronological match spine.

## Highest aggregate flag counts by league

Rates below use all page-1 rows in the league's planned seasons, including seasons with zero reported flags.

| Provider league | Seasons | Flagged / returned | Rate |
|---|---:|---:|---:|
| Argentina Primera División | 3 | 903 / 1,383 | 65.29% |
| Colombia Categoria Primera A | 3 | 825 / 1,278 | 64.55% |
| Paraguay Division Profesional | 3 | 792 / 792 | 100.00% |
| Peru Primera División | 3 | 652 / 958 | 68.06% |
| Mexico Liga MX | 4 | 558 / 1,170 | 47.69% |
| Uruguay Primera División | 3 | 470 / 878 | 53.53% |
| Poland Ekstraklasa | 4 | 306 / 1,224 | 25.00% |
| Saudi Arabia Professional League | 4 | 306 / 1,224 | 25.00% |
| Ukraine Ukrainian Premier League | 4 | 240 / 960 | 25.00% |
| Scotland Premiership | 4 | 198 / 882 | 22.45% |
| Ecuador Primera Categoría Serie A | 3 | 146 / 866 | 16.86% |
| Denmark Superliga | 4 | 123 / 711 | 17.30% |

## Fully flagged provider-season partitions

Every page-1 match row was marked `no_home_away` in these 14 partitions:

| Provider league | Season label | Provider season ID | Rows flagged |
|---|---|---:|---:|
| Argentina Primera División | 2024 | 11212 | 378 |
| Argentina Primera División | 2026 | 16571 | 495 |
| Colombia Categoria Primera A | 2026 | 16614 | 394 |
| Mexico Liga MX | 20252026 | 15234 | 337 |
| Mexico Liga MX | 20262027 | 17099 | 153 |
| Paraguay Division Profesional | 2024 | 11141 | 264 |
| Paraguay Division Profesional | 2025 | 16333 | 264 |
| Paraguay Division Profesional | 2026 | 16533 | 264 |
| Peru Primera División | 2025 | 14912 | 346 |
| Peru Primera División | 2026 | 16905 | 306 |
| Poland Ekstraklasa | 20252026 | 15031 | 306 |
| Saudi Arabia Professional League | 20242025 | 12772 | 306 |
| Scotland Premiership | 20262027 | 17148 | 198 |
| Ukraine Ukrainian Premier League | 20242025 | 12483 | 240 |

The committed machine-readable rollups are:

- `data/footystats/no-home-away-audit-2026-11-04/season-summary.csv` — 182 provider-season rows.
- `data/footystats/no-home-away-audit-2026-11-04/league-summary.csv` — 49 league rollups.
- `data/footystats/no-home-away-audit-2026-11-04/summary.json` — aggregate counts and source provenance.

## Important parser limitation and hardening

The preflight run 41869437030 used the earlier parser, which counted `no_home_away` only when the stringified value was exactly one of `1`, `true` or `True`. That run did not record per-row missingness for the flag field. Therefore, 6,398 is the count of values recognized by that earlier parser; it is not proof that the flag field was populated or interpreted consistently on every row. The sanitized preflight artifact does not contain the underlying fixture rows, so this audit cannot retroactively recompute the count.

The preflight parser has since been hardened on the research branch:
- explicit boolean and numeric 0/1 values are accepted;
- string boolean values are parsed case-insensitively;
- missing values are counted separately and never silently treated as false;
- unrecognized values stop validation with `MATCH_NO_HOME_AWAY_FLAG_UNRECOGNIZED`.

Regression tests for explicit values, missingness and unknown-value fail-closed behaviour passed in FootyStats Budgeted Preflight Contract Tests run 41891767718. No new provider request was made to apply this code change to the earlier run.

## Data-quality policy and outstanding work

- No fixture-level IDs are present in the sanitized coverage file, so the 6,398 rows cannot yet be individually reconciled.
- Root cause and provider semantics of `no_home_away` remain unresolved; do not assume the flag means neutral venue.
- Quarantine flagged fixtures from home/away and venue-specific form. Do not infer or reassign sides.
- A row without a reported flag is not automatically certified for venue features; exact ordered team IDs, fixture chronology and source completeness are still required.
- H2H chronology, recent form, home/away form and fixture-time standings remain unverified.
- xG remains quarantined until point-in-time capture and revision provenance are demonstrated.
- The 728-task historical ingestion manifest remains planned, not executed. The offline resume planner remains `728 pending / 0 completed / 0 blocked`, with `dispatch_allowed=false`.
- Provider calls remain prohibited until the private direct-API bypass is retired or centrally budget-gated and the protected private archive receipt path is validated.

## Governance

All audit outputs remain research-only: `production_eligible=false`, `betting_eligible=false`. No production model code, Oracle V1.6 probabilities, thresholds, calibration, ledgers or eligibility were changed.

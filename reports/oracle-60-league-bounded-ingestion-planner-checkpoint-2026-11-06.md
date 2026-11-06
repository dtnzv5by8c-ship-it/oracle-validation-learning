# Oracle 60-League Bounded Ingestion Planner Checkpoint — 2026-11-06

Governed target: 60-League Universe, historical football data from 2024 through current.

Hardened the offline bounded-ingestion planner to require exactly 60 league rows, unique canonical league IDs, unique provider season IDs, a 2024 season start, valid season-end chronology, a maximum batch size of 20 provider seasons, and a deterministic SHA-256 manifest for every bounded batch.

The planner remains offline-only. It does not call providers, create credentials, create gateway receipts, or modify Oracle V1.6 probabilities or logic.

Regression coverage includes:
- valid 60-row manifest -> 3 batches of 20;
- deterministic batch digest;
- duplicate provider season -> BLOCK;
- duplicate league -> BLOCK;
- 59-league scope -> BLOCK;
- missing provider season -> BLOCK;
- non-2024 start -> BLOCK;
- batch size greater than 20 -> BLOCK.

CI workflow added:
.github/workflows/oracle-60-league-bounded-ingestion-planner.yml

Broad historical ingestion remains blocked until the approved private 60-league gateway/archive receipt is proven. No public FootyStats HTTP 417/Cloudflare bypass was attempted and no provider-sensitive data was added.

Next action: when a verified private 60-league receipt exists, submit only deterministic 20/20/20 batches, validate each returned batch for identity, pagination, chronology, freshness and feature readiness, then checkpoint before advancing.

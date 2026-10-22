# Oracle 44-League Expansion and Visual Intelligence Readiness
Date: 2026-10-22
Status: research-only readiness plan; production eligibility not granted.

## Executive position
The user goal is to resume Oracle predictions across a 44-league universe and deliver the established markets plus Visual Intelligence (recent form, H2H, standings, team-level risk and market-level probabilities). The checked production canonical registry contains **27 leagues**, not 44: 13 are marked CONTROLLED and 14 NOT_INGESTED. The 44-league research scope therefore must be reconciled to the canonical 27-league universe before claiming coverage. League membership is not proof that a league is ingested, that upcoming fixtures are current, or that predictions are eligible to publish.

## Evidence checked
- Production registry: `config/oracle_major_league_registry_v1.json`, version ORACLE_MAJOR_LEAGUE_REGISTRY_V1.0, status DEVELOPMENT_CONTROLLED, research window 2025-03-20 through 2026-09-20.
- Current registry count: 27 leagues; CONTROLLED 13; NOT_INGESTED 14.
- Existing fixture CSV in production repository currently contains historical 9–12 October 2026 rows and only base columns `league_code,date,home_team,away_team,kickoff_time`. It is not evidence of a fresh upcoming fixture feed for 22 October.
- Most recent historical fixture-identity audit: 42 distinct source fixtures, zero verified fixture identities, zero eligible scoring rows.
- Canonical production prediction/settlement evidence is insufficient to calculate production accuracy; do not report accuracy as 0% or invent a hit rate.
- Public regression workflow is configured for a six-hour heartbeat and manual dispatch. Successful runs #4, #5, #6 verified targeted unit tests only; they do not establish full pipeline readiness.
- The private autonomous league-expansion workflow has repeated failures at its prepare gate, and available job logs did not expose the underlying error. Do not make speculative workflow changes.

## 44-league scope reconciliation (required)
Create a controlled mapping table for every requested league with:
1. User-universe name and stable internal league code.
2. Canonical registry competition name/code.
3. Provider competition ID and source namespace.
4. Season and timezone conventions.
5. Ingestion status and last successful retrieval timestamp.
6. Fixture count for next requested date window.
7. Team-ID mapping coverage and fixture-ID provenance coverage.
8. Historical results and standings coverage.
9. Recent-form coverage (last 5 and last 3, home/away split where available).
10. H2H coverage and sample size.
11. xG / odds availability and pre-kickoff provenance status.
12. Markets supported, settlement rules, evaluation sample size and readiness state.

Any one of these 44 leagues absent from the canonical 27 must remain a research candidate until explicitly reconciled. Do not expand or edit the production registry as part of this research-only PR.

## Market and Visual Intelligence publication contract
For each fixture, preserve the existing Oracle prediction outputs unchanged and attach only evidence-backed intelligence:
- Identity: source fixture ID, canonical fixture ID if independently verified, provider namespace, competition ID, home/away team IDs, UTC kickoff, retrieval timestamp, raw-source fingerprint.
- Recent form: last 5 and last 3 results; goals for/against; home/away split; explicit match count and data cutoff. Show N/A if not supported.
- H2H: prior meetings only, sorted before kickoff, with sample size and latest meeting date; no future or post-kickoff leakage.
- League position: verified season standings snapshot as-of a timestamp before kickoff; no inference from another season.
- Team-level risk profile and confidence: define inputs, output scale and missing-data behavior; never imply these are calibrated probabilities unless validation supports calibration.
- Market probabilities: preserve production probability and version. Display only markets the current governed model actually emits; do not create new predictions in the visual layer.
- Settlement: final score and fixture status from an approved independent source; exact market settlement rules; exclude abandoned/postponed/ambiguous fixtures from scoring until resolved.
- Audit: each field has source, as-of time, coverage status and evidence reference.

## Readiness gates before live publication
A fixture is publishable only when:
1. Upcoming fixture feed is fresh and its kickoff is future-dated in the fixture's local competition timezone, normalized to UTC.
2. Home/away team identity and competition identity are resolved without fuzzy auto-approval.
3. Production model output exists with version, timestamp before kickoff, preserved probability and source/feature cutoff metadata.
4. Visual Intelligence fields are joined by exact fixture identity and are explicitly marked VERIFIED / PARTIAL / UNAVAILABLE.
5. Unsupported markets, missing inputs and low-sample H2H are disclosed rather than filled with invented values.
6. The report can be reproduced from frozen input snapshots.
7. Historical evaluation uses only verified pre-kickoff predictions and approved final results.

## Prioritized build sequence
### P0 — establish visible execution
- Keep public six-hour fixture identity regression workflow; inspect its status and artifacts each iteration.
- Keep production workflows unchanged while their prepare/predict/settle failures lack diagnostic logs.
- Publish a short checkpoint after each verified milestone.

### P1 — repair and test ingestion provenance
- Expand unit tests for Football Charts and OpenFoot payload variants, null IDs, nested team objects, numeric IDs, empty IDs and duplicate fixtures.
- Test final CSV and manifest exports, including deduplication that must not discard the richer provenance record.
- Test all downstream readers against the additional columns.
- Run an approved non-production fixture-ingestion sample and record per-provider/league ID coverage before merging the private PR.

### P2 — rebuild identity audit
- Re-ingest fixtures only when permitted by existing provider access; no paid API calls without approval.
- Join source IDs to archive IDs only with independent evidence for provider namespace, competition, teams and kickoff.
- Rebuild review queue; retain unresolved fixtures as blocked.

### P3 — 44-league inventory and freshness
- Export the canonical 27-league registry into an audit table.
- Obtain the exact additional 17 league names/codes from the established 44-league list already in project records/repository.
- Reconcile league-by-league data feeds, seasons, team aliases, fixture coverage and current date window.
- Do not claim 44-league predictions until the missing 17 are identified and the registry scope is reconciled.

### P4 — Visual Intelligence report
- Produce one row per fixture, with source/provenance and market columns; exact fixture ID join only.
- Add recent form, home/away form, H2H, verified standings, xG where sourced, team risk profile, model confidence, market probabilities, data completeness and expert analysis.
- Distinguish model probability from confidence/risk and from bookmaker implied probability.
- Keep unavailable evidence explicit and use no fabricated values.

### P5 — validation and publication
- Score historical predictions only when prediction timestamp is pre-kickoff, exact fixture identity is verified, market settlement rules are approved, and final result is independently sourced.
- Report hit rate with numerator/denominator, coverage, exclusions, league and market sample sizes, plus calibration metrics only when justified.
- Keep challenger/research results separate from production and require explicit approval for promotion.

## Current blockers and what would unblock them
- **44-league universe list:** canonical registry has 27. Reuse the saved 44-league scope from repository/project records; if it is not retrievable, ask Nolan for the exact list rather than inventing 17 leagues.
- **Production ingestion fix:** private PR #20 is a draft. Required tests include CSV/manifest/downstream compatibility and per-provider coverage. Do not merge without passing evidence.
- **Live workflow failures:** latest autonomous expansion prepare failure and live prediction/settlement failures have no retrievable diagnostic logs via current connector. The actual log or a run artifact is required before fixing the true cause.
- **Historical accuracy:** canonical production settlement rows are empty in the last audit. Accuracy remains NOT CALCULABLE, not zero.
- **Provider limits:** no paid API plan changes or new provider API spend without explicit approval.

## Non-negotiable controls
No model redesign, production probability changes, new thresholds, weights, calibration, synthetic IDs, fuzzy auto-approval, guessed league mapping, or unverified prediction claims. Keep this document and all associated experiments research-only.


## Additional legacy universe evidence found (2026-10-22)
The private repository's `ORACLE_BTTS_YES_MEMORY_PACK.json` defines a legacy list of 10 named MAJOR leagues and 25 named MINOR leagues (35 named leagues total), plus an `EXOTIC_DISCOVERY` section consisting of category placeholders rather than individually named leagues. This is not a reproducible, exact 44-league manifest. It must not be padded by guessing the remaining ten.
- Legacy pack: https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/ORACLE_BTTS_YES_MEMORY_PACK.json
- Canonical production registry: 27 leagues, 13 CONTROLLED / 14 NOT_INGESTED.
- Another readiness matrix search result states a separate baseline of 22/30 Major leagues connected, with partial results for six gated leagues; that matrix uses a different scope/status vocabulary and must be reconciled rather than merged blindly into the canonical 27.
- Action: derive the intended 44 only from a governed list/artifact already used by the current 44-league prediction workflow. If no exact list is found, the scope remains UNRECONCILED and no missing leagues are invented.


## Executed inventory milestone (2026-10-22 04:20 UTC)
- Added `scripts/oracle_league_readiness_inventory.py` and public workflow `.github/workflows/oracle-league-readiness-inventory.yml`.
- Workflow run #1 completed successfully: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39721747262
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39721747262/artifacts/12401815585
- The job fetched the three retained source files through the existing private-repository token and made no provider API calls.
- Measured inventory: 27 canonical leagues (13 CONTROLLED, 14 NOT_INGESTED); 35 named entries in the legacy memory pack; 80 rows in the retained fixture CSV.
- The 80 retained fixture rows are not proof of current upcoming fixtures. The inventory intentionally labels current/future status and Visual Intelligence coverage as unaudited. No predictions were generated and no production eligibility was granted.
- The scheduled inventory workflow runs every six hours and produces a downloadable artifact with a CSV per canonical league, the legacy named-universe list, a JSON summary and README.


## Freshness/provenance gate added and executed (2026-10-22 04:22 UTC)
- Updated the public inventory script to parse retained fixture kickoffs against current UTC and list required provider provenance columns.
- Latest successful run #5: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39721989515
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39721989515/artifacts/12401621444
- Observed: 80 retained rows; **0 future fixtures**; latest retained kickoff is 2026-10-17 13:30 UTC; all eight source provenance columns are absent from the current CSV (source name, provider fixture ID, slug, competition ID, home/away team IDs, retrieval time, record fingerprint).
- This is a concrete upstream blocker: the retained fixture file is stale for upcoming predictions and cannot prove provider identity. The proposed private PR #20 addresses preserving provenance on future ingestion but remains draft and unmerged.
- Do not produce live predictions from these 80 rows. Next safe step is validate the draft ingestion change against actual provider payload examples and final CSV/manifest/downstream readers, then request approval before any production merge or provider-backed refresh.

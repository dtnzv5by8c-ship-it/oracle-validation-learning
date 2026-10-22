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


## Ingestion code review — additional defects corrected in draft PR #20 (2026-10-22 04:38 UTC)
A deeper review of the draft ingestion code found two downstream correctness issues beyond the original missing-ID export:
1. Duplicate fixture rows were deduplicated by keeping the first occurrence, which could discard the row with richer provider identity/provenance. The draft now prefers records with more source identity fields and sorts output duplicates by provenance completeness before deduplication.
2. The fixture manifest was written before fields such as admitted league count, per-league fixture counts and status counts were populated. The draft now writes the manifest after all summary fields are set, so the retained JSON should match the printed summary.
3. Added regression cases for duplicate fixtures where only one record carries provider IDs and for numeric provider IDs/team IDs.

Code/test changes are on private draft PR #20 (not merged): https://github.com/dtnzv5by8c-ship-it/oracle-football-data/pull/20
The public regression workflow was triggered against the updated private branch, run #17: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39723499279
At checkpoint time, run #17 was queued/in progress; its result has not yet been verified. The original three tests passed, but the expanded suite must pass before claiming this milestone complete.

## Scope and live prediction gate
Repository search found a legacy 30-league readiness matrix and multiple other historical scopes, but the current canonical production registry and expansion workflow govern 27 active leagues. These different scopes must not be silently conflated into the requested 44. The exact approved 44 list remains unresolved in a governed artifact.
No live predictions are generated from the retained fixture CSV because the latest audit confirms zero future fixtures and missing source provenance fields. No model probabilities or production settings have been changed.


## Latest build continuation — exact approved 44-league list recovered (2026-10-22)
Prior conversation retrieval recovered the explicit approved 44-league scope. It contains the following names, with no canonical IDs supplied in that earlier specification:

SA Premiership; EPL; Championship; La Liga; Bundesliga; Serie A; Ligue 1; Eredivisie; Primeira Liga; Belgium; Turkey; Denmark; Sweden; Norway; Finland; Switzerland; Austria; Greece; Poland; Czech; Croatia; Serbia; Romania; Ukraine; Russia; Ireland; Scotland; MLS; CPL; Liga MX; Brazil Serie A; Argentina Primera; Colombia Primera A; Chile Primera; Uruguay Primera; Paraguay Primera; Ecuador Liga Pro; Peru Liga 1; Venezuela Primera; Australia A-League; Japan J1; K League 1; China CSL; India ISL.

A research-only reconciliation was added to `scripts/oracle_league_readiness_inventory.py`. It writes `oracle_approved_44_scope_reconciliation.csv`, comparing exact normalized names against the current 27-league canonical registry. It intentionally does not infer IDs or automatically map broad country/region labels to provider competitions.
- Change commit: `38946f64e2cfb140c16e7c085fe614317a6b7c55`
- Inventory workflow #12: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39734670630
- Inventory workflow #13: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39734676596
- Regression workflow #20: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39734676469
These three runs were still in progress at the time of this checkpoint; do not mark them successful until completed.

Latest confirmed regression run #19 passed all **5** tests in 0.71 seconds, including duplicate-fixture provenance preference and numeric provider-ID preservation: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39723534417

## Next technical gates
1. Confirm runs #12/#13/#20 and inspect the generated exact-44 reconciliation artifact.
2. Add isolated tests for CSV/manifest output and compatibility with downstream readers; never call provider APIs inside unit tests.
3. Before any live refresh, inspect existing ingestion workflow and provider rate/credit constraints. Do not dispatch paid or credit-consuming calls without explicit approval.
4. Once the ingestion code passes static/output tests, request approval before merging private PR #20 or refreshing the production fixture file.
5. Build Visual Intelligence joins from already available historical source snapshots first; exact fixture identity and pre-kickoff as-of cutoffs are mandatory.
6. Keep prediction publication blocked until a fresh future-dated fixture snapshot and existing governed model outputs are available. No production model logic has changed.


## Exact 44-scope inventory result (2026-10-22 06:35 UTC)
- The readiness inventory now emits `oracle_approved_44_scope_reconciliation.csv` for all 44 approved names recovered from the September 2026 conversation.
- Successful run #15: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39734761612
- Artifact ID 12406776729; 44 rows in the scope reconciliation.
- Exact normalized competition-name matches: **7/44**. Remaining **37/44** need a controlled alias/competition mapping review. Even the seven exact-name matches are marked `NOT_GRANTED` pending stable-ID and readiness review; exact text match alone is not enough to enable production.
- Inventory reconfirms 27 canonical leagues (13 CONTROLLED, 14 NOT_INGESTED), 80 retained fixture rows, zero future fixtures, and all eight source-provenance columns missing from the retained production CSV.
- Regression workflow #21 passed after the inventory changes: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39734713834
- Inventory workflow runs #12–#14 failed due to an accidentally literal escaped newline in the script. This was corrected in commit `abc6f128a8f8924ea235c1bfbe1ef1065f495d48`; run #15 succeeded. Earlier failures are retained in run history and are not presented as passes.

## Remaining hard blockers
- No verified fresh future fixture feed is available from the current retained production CSV.
- No live ingestion was run because that would invoke external providers and could consume API quota; no approval to spend new credits was given.
- Private PR #20 remains open and draft. Its 5 targeted regression tests pass in public run #19; this still does not test the full network-backed ingestion workflow or all downstream consumers.
- Exact 44-league mappings are not complete: 37 names need review; do not add guessed IDs to the production registry.
- Visual Intelligence source joins and current production market probabilities have not yet been rebuilt into a publishable report because the fixture slate is stale and fixture IDs are not verified.


## Downstream CSV compatibility review (2026-10-22)
A static source review was completed against the current production-branch consumer `scripts/oracle_four_model_live_predict.py`.
- It loads the fixture file with pandas `read_csv` and accesses the existing base columns `league_code`, `date`, `kickoff_time`, `home_team`, and `away_team` by name.
- Adding extra provenance columns should not, by itself, break this consumer because it does not require an exact five-column schema in the reviewed path.
- This is a **static compatibility review only**, not an executed integration test against the proposed branch or an actual generated CSV. Other consumers still require audit, and a full live ingestion run remains unverified.
- Source: https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/cb89e5bd1c24810fe821a6b2c3c2c1c19272b381/scripts/oracle_four_model_live_predict.py
- PR #20 remains draft and unmerged; no production fixture file was refreshed.


## Latest live workflow check (2026-10-22 09:50 SAST)
- Public research regression workflow run 39740437745: completed successfully.
- Public research 44-league inventory run 39740437741: completed successfully.
- Private production repo latest autonomous league expansion run 39742184987: failed in `prepare`; all downstream jobs skipped; no fixture refresh or expansion output from that run.
- Private production readiness run 39723492326: failed in its `readiness` job. The connector exposes no step summaries/logs for these jobs, so the precise exception is not confirmed and should not be guessed.
- Private PR #20 is still draft/unmerged; branch head observed as `f20ed60c8d23684c9c00ab82fc6f1e7fd915f4f0`.
- These failed production workflows mean the successful public research checks must not be interpreted as a live production prediction pass.


## Latest continuation update (2026-10-22)
- Confirmed from the production readiness workflow file that the fixture fallback step hard-codes `2026-10-09` through `2026-10-12`, a historical window as of 22 October. This is a concrete workflow defect independent of the ingestion PR.
- Opened draft production workflow PR #21 to calculate the next Friday-to-Monday fixture window at runtime and pass it to the existing fallback ingester. No model logic/probabilities/calibration changed. Do not merge until GitHub Actions run validates syntax, non-empty future fixtures, and governance assertions.
- PR: https://github.com/dtnzv5by8c-ship-it/oracle-football-data/pull/21
- Expansion run #193 (39742184987) fails at `prepare`; readiness run #156 (39723492326) fails at `readiness`. Job-log retrieval returns GitHub's `BlobNotFound`, so exact exceptions remain unconfirmed. Expansion prepare code queries prior workflow artifacts via `GITHUB_TOKEN`; this is a diagnostic lead, not a confirmed cause.
- Existing ingestion PR #20 remains draft/unmerged. Public regression and inventory workflows pass, but that does not establish production readiness or live prediction availability.


## Follow-up check after draft PR #21 (2026-10-22)
- PR #21 remains open/draft/unmerged: https://github.com/dtnzv5by8c-ship-it/oracle-football-data/pull/21 (head `33ace30da62c3eccb332c00e6ab1de9893606a9e`).
- The new PR commit triggered Oracle Final 27-League Assessment run 153 (ID `39744286178`) and Oracle 27 League Prediction Readiness run 157 (ID `39744286213`); both completed with failure. The available connector returns no step summaries and job-log download endpoints return `BlobNotFound`, so the failing command cannot be identified from the current evidence.
- Therefore the dynamic-window change is proposed but not validated. Do not merge PR #21 yet. Next diagnostic requirement: open each failed job in GitHub Actions and expand its step output, or add a separate minimal diagnostics workflow that prints step names and errors without secrets. Do not print tokens or environment secrets.
- No production model logic was changed. No fresh fixture CSV or Visual Intelligence output has been verified. The 44-league publication gate remains blocked.

# Oracle 44-League Pipeline — Autonomous Continuation Checkpoint
Date: 2026-10-23
Branch: research/oracle-crosswalk-isolation-2026-10-22
Governance: research-only; no production repository changes; no merge performed.

## Work completed in this checkpoint
1. Executed the committed structural validator against the uploaded sanitized audit artifact. It returned exit code 0, zero structural errors, 88 warnings, 44 target leagues, 7,216 fixture rows, 86 page-provenance rows, 24 short-page terminations, 20 targets not retrieved, and 44 targets without verified cutoff provenance.
2. Added `scripts/oracle_44_catalogue_discovery.py`. It queries the broader provider catalogue (`chosen_leagues_only=false`), emits only sanitized league/season metadata and a candidate crosswalk for the fixed 44-target research universe, records a catalogue hash, and deliberately leaves all candidate mappings as review-required. It does not fetch match data or create predictions.
3. Added `.github/workflows/oracle-44-league-catalogue-discovery.yml`. It supports manual dispatch, research-branch pushes touching the discovery code, and a weekly Monday schedule. It checks that `FOOTYSTATS_API_KEY` exists without printing its value and uploads a sanitized artifact with 30-day retention.

## Verification boundary
The new discovery script and workflow have been committed, but their first GitHub Actions execution has not yet been observed. API-secret presence and provider access have therefore not been verified for this new job. The weekly schedule is configured in the file, but GitHub scheduled workflows run from the repository's default branch; this schedule will not be active for the research branch alone until the workflow is accepted into the default branch. Do not claim recurring automation is live before that is confirmed.

## Remaining hard gates
- Run the new discovery workflow and inspect its artifact. Reconcile the 20 alias misses against the full catalogue and candidate season metadata. Do not auto-map ambiguous matches.
- Validate candidate season IDs against actual season start/end dates and the requested target period.
- Improve match-fetch pagination: use provider-documented pagination/count semantics and independent official fixture counts; a short page alone is not proof of completeness.
- Replace goal-null `upcoming_rows` logic with explicit status normalization for completed, upcoming, postponed, abandoned, in-play, and unresolved/unknown statuses.
- Validate source field semantics and types. Separate observed in-match xG from any pre-match expectation fields, and verify odds timestamps/meaning.
- Implement timestamped as-of-kickoff provenance and reject any feature/odds value without defensible pre-kickoff availability for historical backtests.
- Integrate the structural validator into the full-season audit workflow and make structural failures fail the run.
- Retrieve actual verified historical Oracle prediction records and settlements; then calculate league-by-market and team-level accuracy/calibration only on matched, settled, leakage-safe records.
- Verify a successful scheduled run and artifact retention after the workflow is merged to the default branch by an authorized maintainer.

## Safety and interpretation
No production model logic, weights, thresholds, probabilities, selection rules, market definitions, or governed 27-league registry were changed. No production predictions were created. Catalogue matches are candidates, not validated mappings. This checkpoint does not claim the 44-league pipeline or historical validation is complete.

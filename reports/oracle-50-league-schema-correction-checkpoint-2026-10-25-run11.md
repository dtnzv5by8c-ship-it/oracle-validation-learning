# Project Oracle — FootyStats 50-ID Schema Correction Checkpoint (Run 11)

Date: 2026-10-25
Branch: `research/oracle-50-league-readiness-audit`
Status: **RESEARCH TOOLING IMPROVED; LIVE ACCOUNT RECONCILIATION PENDING**
Scope: exactly the owner-selected 50 IDs recovered from the saved FootyStats settings page.
Governance: research-only; no production Oracle changes.

## Source schema confirmed

Official documentation: https://footystats.org/api/documentations/league-list

- Endpoint: `GET https://api.football-data-api.com/league-list?key=YOURKEY`
- `chosen_leagues_only=true` filters the response to leagues chosen by the account.
- The documented sample exposes a competition `name` and nested `season[]` entries with `id` and `year`.
- The documentation explicitly says each season of a competition has a unique ID.
- The published example does not show a top-level parent competition ID.

This confirms that the API's documented season identifier is `season[].id`. It does **not**, by itself, prove that every numeric ID extracted from the saved checkbox page has the same semantics. That must be verified by comparing the actual selected IDs with the account-specific response.

## Research-only utility committed

Added:
`scripts/reconcile_footystats_selected_seasons.py`

Commit: `23b722d9531a3588d6a92ddb79d28a05039ac987`

The utility:
- accepts a sanitized `league-list` JSON response and a selected-ID CSV;
- indexes the nested `season[].id` values rather than assuming a parent competition ID;
- reports ID match, exact competition-name match, candidate season years, and country/name discrepancies separately;
- fails closed on blank/duplicate selected IDs and malformed input;
- labels all mappings unapproved and never declares production readiness.

It deliberately does not make provider calls or accept API credentials, so the key cannot be logged by this script. The script has been committed to the research branch; it has **not yet been executed against a fresh account-specific response**.

## Remaining blocker and evidence limits

The connected execution tools in this session do not expose the FootyStats account secret or a way to dispatch the repository workflow. Therefore I did not make a live API request, did not inspect account-specific catalogue results, and did not claim the 50-row comparison passed. The existing audit evidence still says the catalogue artifact has 43 league rows with blank parent IDs, the archive manifest has 126 rows with blank parent IDs, and exact selected-ID-to-fixture/canonical-team joins are 0/50 verified.

## Next validation sequence

1. Run the existing catalogue workflow in GitHub Actions using the configured `FOOTYSTATS_API_KEY` secret. It already calls `league-list` with `chosen_leagues_only=true` and outputs a season-level CSV.
2. Download the catalogue artifact. Do not paste or upload the API key; the artifact must contain only the response fields used for the audit.
3. Prepare a selected manifest CSV with columns `selected_id,country,competition_name` from the saved 50-row manifest and run the new script against the downloaded JSON response.
4. Review every row marked other than `EXACT_ID_AND_NAME`; do not approve mappings automatically based on names, numerical coincidence, or fuzzy matches.
5. After ID reconciliation, build and validate selected-ID → season → fixture → canonical home/away team joins, then audit current fixtures, recent form, standings, xG and odds timestamps/provenance, H2H chronology, and each market separately.
6. Refresh stale data and establish immutable feature snapshots before considering any readiness decision.

## Current readiness decision

- Selected IDs reconciled against live account response: **NOT YET VERIFIED**
- Exact selected ID to fixture and canonical-team joins: **0/50 verified in prior audit**
- Approved canonical mappings: **0**
- Verified as-of-kickoff xG provenance: **0 rows**
- Verified pre-match odds provenance: **0 rows**
- M-1UP: blocked by stale event truth and missing selected-ID joins
- BTTS Yes, Double Chance, Double Chance + Under 4.5: not verified for selected-50 scope
- Production eligibility: **NOT GRANTED**

No production model logic, weights, probabilities, thresholds, calibration, model version, protected registry, or canonical ledgers were changed. No draft PR was merged, no gate was bypassed, and no paid provider change was made.

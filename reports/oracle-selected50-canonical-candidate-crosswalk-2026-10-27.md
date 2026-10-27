# Selected-50 Identity Reconciliation — Canonical Registry Candidate Pass

**Evidence date:** 2026-10-27  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Provider evidence:** successful read-only schema diagnostic run #9 (`40548721202`), sanitized artifact digest `sha256:a993aa11e7de8aa1b4415c9a564c843cb3180bbb6754670f0f45c81426ca52c5`  
**Canonical reference:** protected production registry `config/oracle_major_league_registry_v1.json`, blob `81d6db487e498fc84a87a7457b0de7215537f15c` (read only; not modified)  
**Status:** `CANDIDATE CROSSWALK ONLY — NO APPROVAL OR PRODUCTION ELIGIBILITY`

## Results

The provider schema diagnostic matched **50/50 selected IDs to `season.id`**, and **0/50 to direct league-level ID fields**. The provider catalogue returned 50 catalogue rows and 766 season objects. It did not return a direct parent competition ID field in the examined league objects.

The current protected Oracle canonical registry contains **27 leagues** (active universe count 27), while the selected provider manifest contains 50 leagues. Name/country crosswalk is therefore a candidate-only bridge, not a 50-league canonical registry expansion.

Candidate pass counts using the repository's explicit alias policy and country-constrained name matching:

- `NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY`: **28**
- `CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW`: **22**

## Interpretation

- A candidate canonical ID is populated only where country-constrained normalized provider naming matched exactly one current registry league, using only explicit aliases already defined in the research crosswalk script.
- Every candidate remains `human_approval_required=TRUE`; none is approved or production eligible.
- The provider season ID is preserved as a season identifier. The parent competition ID remains blank because the diagnostic did not provide it.
- The 50 selected groups not represented in the current 27-league registry are labelled `NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY`, not assigned invented canonical IDs.
- The FootyStats League List documentation says each season of a competition has a unique ID and documents `season.id` / `season.year` as the relevant fields. It does not document a separate parent competition ID in the sample response. See [FootyStats League List documentation](https://footystats.org/api/documentations/league-list).

## Next controlled steps

1. Review the candidate CSV row by row; confirm country, provider name and intended Oracle competition.
2. Decide the governance route for the 23 leagues outside the current canonical registry: separate research-only extension proposal, not a production registry edit.
3. If parent competition IDs are a hard requirement, request clarification from FootyStats or identify an explicitly documented provider field/endpoint before spending another API request. Do not infer parent IDs from season IDs.
4. Keep production model logic, probabilities, thresholds, calibration and canonical registry unchanged until approval through the existing governance process.

## Safety and eligibility

The successful diagnostic was read-only, performed no full match ingestion, and did not change production files. The artifact records `monthly_credit_budget_verified=false`; the user's confirmation that the balance was checked is not independently validated by the workflow. Production and betting eligibility remain **NOT GRANTED**.

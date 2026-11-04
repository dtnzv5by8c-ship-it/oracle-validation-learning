# FootyStats preflight pagination reconciliation — 2026-11-04

Read-only audit of the committed 182-row season-ingestion coverage CSV.

Verified: 182 seasons; all 182 report matches_page_count=1 and teams_page_count=1. Sum matches_total_results=54,546 and sum page_1_match_rows_returned=54,546; the values match for every season. Sum teams_total_results=3,117. The manifest reports unique match IDs and team IDs on each sampled page.

The 6,398 no_home_away rows occur in 73 seasons; in 14 seasons every returned match row is flagged no_home_away.

Interpretation: provider pagination metadata indicates one complete page for league-matches and league-teams in every planned season, with match returned-row counts matching provider totals. This supports a single-page pagination-completeness claim for those endpoint responses, subject to provider total_results accuracy and source-artifact integrity. It does not mean the 54,546 rows have been ingested, archived, deduplicated across seasons, filtered to the exact history window, or validated into a chronological match spine. The 728-request ingestion manifest is still only a plan.

Investigate no_home_away rows by exact provider fixture/team IDs and competition semantics. Do not infer or reassign home/away sides; quarantine unresolved rows from venue-split features. Validate cross-season duplicate IDs and kickoff UTC boundaries 2024-01-01 through 2026-11-04 inclusive. Before ingestion, validate the protected private archive and provider limits; checkpoint each batch and keep raw payloads out of the public repository. H2H/recent/home-away features require the admitted exact-ID chronological match spine. xG remains quarantined and fixture-time standings unverified.

Research only: production_eligible=false, betting_eligible=false. Oracle V1.6 production logic, probabilities, thresholds, calibration and ledgers remain unchanged.
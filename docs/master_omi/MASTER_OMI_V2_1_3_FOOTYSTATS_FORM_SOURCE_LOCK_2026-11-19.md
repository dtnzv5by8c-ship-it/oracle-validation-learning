# PROJECT ORACLE — MASTER OMI V2.1.3 FOOTYSTATS FORM SOURCE LOCK

## Date
2026-11-19

## Root cause identified
The previous Master OMI form block was not reliable because the extraction path mixed provider venue-form fields with the intended overall Last-5 form fields. This produced cases such as Manchester City vs Fulham where the workbook showed the home team's venue form in the overall Home Last-5 field.

Example independently verified against FootyStats:
- Manchester City overall Last 5: provider league table shows W W L L L for the league-only view; the FootyStats team page can also expose cross-competition recent matches. The Master OMI must use the dedicated Last-X team endpoint for the provider's Last-5 form, because FootyStats explicitly states that Last-5 Form can include matches from different leagues.
- Manchester City Home Form: W W W W L.
- The workbook's prior Home Last-5 Form = W W W W L was therefore a venue-form value in the wrong field.

## Permanent source rule
Master OMI Last-5 provider form must be sourced from FootyStats API endpoint:
`https://api.football-data-api.com/lastx?key=YOURKEY&team_id=TEAM_ID`

The endpoint is specifically documented by FootyStats as the Team Last 5 / 6 / 10 Stats endpoint and returns Last-X team statistics. The exact 5-match node must be selected using `seasonMatchesPlayed_overall = 5`.

Required provider fields:
- formRun_overall -> FootyStats Home/Away Last 5 Form field for the scheduled home/away team.
- formRun_home -> Home Venue Last 5 Form for the scheduled home team.
- formRun_away -> Away Venue Last 5 Form for the scheduled away team.
- seasonPPG_overall/home/away.
- seasonScoredAVG_overall/home/away.
- seasonConcededAVG_overall/home/away.
- seasonAVG_overall/home/away.
- seasonMatchesPlayed_overall/home/away.

## Form order
FootyStats form strings are locked as **OLDEST -> NEWEST, left-to-right**.
Example: `LLLWL` = Loss, Loss, Loss, Win, Loss; the final L is the most recent result.

## Fixture/report snapshot rule
The provider form snapshot must be timestamped in UTC.
All form fields in a weekly report must come from the same provider snapshot unless a fixture-specific refresh is explicitly recorded.
The snapshot timestamp is appended to Market Intelligence.

## QA requirements
Before promotion of a new Master OMI report:
1. Exact 5-match provider node must be available for each team where possible.
2. Form length must equal sample N.
3. Form-derived PPG must equal provider PPG to provider rounding tolerance.
4. Overall form must come from `formRun_overall`, never `currentFormHome` or `currentFormAway`.
5. Scheduled-home venue form must come from `formRun_home`.
6. Scheduled-away venue form must come from `formRun_away`.
7. No stale prior report values may survive a failed refresh.
8. If provider coverage is below 95% for the report's unique teams, the rebuild must fail closed rather than publish partial provider form.

## Workflow
`oracle-footystats-form-rebuild.yml`
`scripts/oracle_footystats_form_rebuild.py`

The workflow rebuilds the Master OMI form block from the dedicated FootyStats Last-X endpoint and uploads a QA artifact. It does not modify Oracle V1.6.

## Governance
- Oracle V1.6 unchanged.
- Market Intelligence A:ET unchanged.
- Form fields after ET may be corrected in place because they are provider-intelligence extensions.
- Future intelligence remains append-only after the existing block.
- No post-kickoff results.
- No fuzzy identity matching.
- No provider substitution without explicit status.
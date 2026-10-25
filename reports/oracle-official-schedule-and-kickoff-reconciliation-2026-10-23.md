# Project Oracle — Official Schedule and Kickoff Reconciliation

**Date:** 23 October 2026  
**Scope:** Research-only schedule reconciliation, kickoff timestamp enrichment and cutoff traceability.  
**Production status:** BLOCKED — no production model logic, probabilities, calibration, thresholds, or eligibility rules are changed.

## Official fixture corrections

### Paris Saint-Germain vs Lyon
The French Professional Football League (LFP) announced on 23 October that the match originally scheduled for Sunday 25 October at 20:45 was moved to Monday 26 October at 20:30 France local time. The research schedule canonicalises this fixture to **26 October 2026, 18:30 UTC** (20:30 CEST). This overrides the earlier club fixture page and the stale date in the Run 108 baseline.

Sources:
- LFP rescheduling notice: https://www.lfp.fr/article/paris-saint-germain-olympique-lyonnais-decale-au-lundi-26-octobre-a-20-h-30
- PSG fixture page (historical pre-change schedule): https://www.psg.fr/en/matches/mens-football/20262027/paris-vs-lyon-2026-10-25

### FC Botoșani vs Petrolul Ploiești
The Romanian league and both clubs list this fixture for Friday 23 October at 18:00 Romania local time, equivalent to **15:00 UTC**. The research schedule restores it if the run's window includes 23 October and that date has not passed. The comparison canonicalises short team labels (e.g. “Petrolul”) to the official fixture names so the baseline and replay can be compared on the same identity.

Sources:
- Liga Profesionistă de Fotbal (LPF) calendar: https://lpf.ro/cluburi/fc-botosani/8/calendar
- FC Petrolul fixture page: https://fcpetrolul.ro/meci/fc-botosani-vs-fc-petrolul-ploiesti-6/
- FC Botoșani fixture calendar: https://fcbt.ro/calendar/superliga-2026-2027/

## Common-list reconciliation rule

The comparison must apply these source-backed corrections to both the Run 108 baseline and the current research schedule, then compare the full fixture keys (league code, date, home team, away team). It writes a common fixture list only if the corrected key sets match exactly. Any unmatched or extra fixture blocks the comparison rather than silently treating the fixture sets as equivalent.

## Kickoff enrichment root cause and safeguard

The research ingestion already enriches missing kickoffs from the archived FotMob current_matches.csv only when date, competition, home team and away team identify one unique row with an explicit timezone-qualified timestamp. The source review identified two normalisation gaps:
- competition display labels differ for Austrian Bundesliga (Bundesliga) and Italian Serie B (Serie B);
- accented names such as Pogoń and Südtirol did not normalise to their ASCII fixture labels.

The research-only ingestion branch now applies accent-insensitive comparison and a small explicit competition-label alias list. It still requires the exact date, both ordered teams, and exactly one source match; it accepts only a complete timezone-qualified timestamp. Ambiguous matches and date-only values remain unverified. This is a metadata join only and does not change prediction features or model logic.

## Mandatory cutoff audit

Every research replay now executes a separate cutoff traceability audit even when the live runner fails. It requires cutoff date, cutoff UTC, prediction timestamp and fixture date, checks for invalid/missing timestamps, and compares a cutoff against the verified kickoff where available. If kickoff is unknown, the audit conservatively requires the cutoff date to precede the fixture date. A failed or unavailable audit blocks the run's reconciliation/promotion path.

## Validation gates

1. Confirm the official correction step passes and the fixture manifest agrees with the corrected schedule.
2. Require exact equality of the corrected baseline and research fixture keys before writing the common list.
3. Report every remaining kickoff without a verified timezone-qualified source timestamp as missing; never infer one.
4. Require zero missing/invalid cutoff timestamps and zero cutoff-after-kickoff violations.
5. Keep research changes on the research branch / draft PR until reviewed. Production promotion remains blocked.

#!/usr/bin/env python3
"""Add a machine-readable field dictionary and durable run configuration to the workbook.

This is a report-only post-processing step. It does not alter fixture values,
probabilities, model logic, or eligibility decisions.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

SHEET_PURPOSE = {
    "Oracle V1.6 Output": "Human-readable presentation of the source Oracle V1.6 fixture output. Values are copied from the verified runtime report or explicitly labelled derived/report-only fields.",
    "Market Intelligence": "Combined fixture-level market, form, H2H, goal-research, provenance and eligibility evidence. Raw Oracle probabilities are preserved; research estimates are separate.",
    "xG Evidence Audit": "Fixture-level xG values and their source, timestamp, hash and point-in-time provenance status. Numeric presence does not establish pre-kickoff availability.",
    "H2H Intelligence": "Individual qualifying prior head-to-head meetings, strictly before the fixture cutoff and matched under the exact Selected-50 identity rules.",
    "Team Form Evidence": "Per-fixture, per-team historical form evidence using completed prior matches and explicit overall/venue samples.",
    "Data Quality & Risk": "Fixture-level identity, schedule, feature support, provenance and eligibility controls. Evidence risk is not outcome risk.",
    "Schedule Reconciliation": "Runtime versus archive kickoff comparison and evidence needed for manual schedule resolution.",
    "Goal Intelligence": "Descriptive historical scoring rates and samples derived from prior completed matches; not prediction probabilities.",
    "Goal Market Research": "Experimental, research-only goal-market forecasts and baselines. Not Oracle production probabilities and not betting eligible.",
    "Market Data Coverage": "Coverage counts for key market output fields in the fixture report.",
    "Archive Field Coverage": "Presence of raw fields in the pinned archive. Presence alone is not proof of validity or point-in-time availability.",
    "Definitions & Governance": "Core business definitions and non-negotiable research/production governance rules.",
    "50-League Coverage": "One row per governed Selected-50 season with fixture, feature, market, H2H, xG and eligibility coverage counts.",
    "Coverage Audit Summary": "Top-level field coverage audit metrics and their interpretations.",
    "xG Provenance Decision": "Summary of xG provenance findings and the resulting permitted-use decision.",
    "50-League Field Coverage": "League-by-field presence, usability and explicit-unavailability audit for each source sheet and field.",
    "Field Coverage Summary": "Aggregated field coverage and completeness states across selected leagues.",
    "Field Coverage Exceptions": "League-level field coverage exceptions requiring interpretation or remediation.",
    "Field Coverage QA": "Control checks for the field-by-field coverage audit.",
    "LLM Data Dictionary": "Machine-readable definitions for every column heading in every report sheet, including purpose, source/calculation, units and limitations.",
    "Report Configuration": "Persistent configuration and repeatability instructions for producing this report weekly."
}

EXACT = {
    "Fixture Date": ("Scheduled fixture date/time as represented in the runtime output.", "Copied from the verified runtime fixture record; timezone semantics follow the source field.", "Source timestamp; do not reinterpret without timezone evidence."),
    "League": ("Competition label for the fixture.", "Copied from the runtime report; exact selected-season mapping is separately recorded by selected_id/provider_season_id.", "Display label, not a unique identifier."),
    "Fixture": ("Home team versus away team display string.", "Concatenation of runtime home_team and away_team.", "Display label; use fixture_id and team IDs for joins."),
    "BTTS Yes": ("Oracle probability for both teams to score at least one goal.", "Copied unchanged from the supported runtime BTTS_probability_pct field.", "Percentage points, 0–100; source prediction, not recalculated here."),
    "Home 1X": ("Oracle double-chance probability that the home team wins or the match is drawn.", "Copied unchanged from runtime DC_HOME_probability_pct.", "Percentage points, 0–100; source prediction."),
    "Away X2": ("Oracle double-chance probability that the away team wins or the match is drawn.", "Copied unchanged from runtime DC_AWAY_probability_pct.", "Percentage points, 0–100; source prediction."),
    "Over 1.5": ("Oracle probability that total match goals are at least 2.", "Copied from runtime only when a supported source field exists; otherwise explicitly unavailable.", "Percentage points, 0–100; not inferred from empirical rates."),
    "Over 2.5": ("Oracle probability that total match goals are at least 3.", "Copied from runtime only when supported; otherwise explicitly unavailable.", "Percentage points, 0–100."),
    "Under 4.5": ("Oracle probability that total match goals are fewer than 5.", "Copied from runtime only when supported; otherwise explicitly unavailable.", "Percentage points, 0–100."),
    "Home over 1.5 goals": ("Oracle probability that the home team scores at least 2 goals.", "Copied from runtime only when supported; otherwise explicitly unavailable.", "Percentage points, 0–100."),
    "Away over 1.5 goals": ("Oracle probability that the away team scores at least 2 goals.", "Copied from runtime only when supported; otherwise explicitly unavailable.", "Percentage points, 0–100."),
    "Home 1X + Over 1.5": ("Combined-market probability for home-or-draw and at least 2 total goals.", "Source runtime value if explicitly supplied; no independent calculation is performed by this report.", "Percentage points; unavailable unless sourced."),
    "Away X2 + Over 1.5": ("Combined-market probability for away-or-draw and at least 2 total goals.", "Source runtime value if explicitly supplied; no independent calculation is performed by this report.", "Percentage points; unavailable unless sourced."),
    "Home 1X + Under 4.5": ("Combined-market probability for home-or-draw and fewer than 5 total goals.", "Source runtime value if explicitly supplied; no independent calculation is performed by this report.", "Percentage points; unavailable unless sourced."),
    "Away X2 + Under 4.5": ("Combined-market probability for away-or-draw and fewer than 5 total goals.", "Source runtime value if explicitly supplied; no independent calculation is performed by this report.", "Percentage points; unavailable unless sourced."),
    "M-1UP Home": ("Oracle M-1UP home-side market probability or output.", "Copied only from the runtime output; no M-1UP model is run by this report.", "Source-defined value; not recalculated."),
    "M-1UP Away": ("Oracle M-1UP away-side market probability or output.", "Copied only from the runtime output; no M-1UP model is run by this report.", "Source-defined value; not recalculated."),
    "Draw Probability (derived)": ("Derived draw probability where the source Oracle home/away/draw probability components support it.", "Report-level derivation from the source runtime probability components; inspect the source builder for exact guards. Not a newly trained estimate.", "Percentage points; treat as derived, not a raw source probability."),
    "Goal Line Call (O/U 2.5)": ("Categorical goal-line selection for over/under 2.5 goals.", "Presentation derived from the supported Oracle goal-line output where available.", "Categorical; not a separate probability."),
    "Most Likely Total-Goals Band (derived)": ("Most likely total-goals range label.", "Presentation derivation from available Oracle goal-distribution outputs; not an independently fitted model.", "Categorical derived field."),
    "Recent Form (5)": ("Recent five-match form string, typically W/D/L sequence.", "Derived from up to five qualifying completed prior matches; strictly before the fixture cutoff.", "Chronological form sequence; sample size must be checked separately."),
    "Recent Form Points (Last 5)": ("Points earned across the qualifying recent-form sample.", "Sum of 3 points for a win, 1 for a draw and 0 for a loss across the available sample.", "Points; not normalized unless explicitly stated."),
    "League Position": ("Provisional reconstructed league-table position.", "Reconstructed within exact provider season using 3-1-0 points, then goal difference, goals scored and deterministic team-name/ID tie-breaks.", "Ordinal position; provisional, not official where competition-specific rules are unverified."),
    "Avg. Goals Scored (Last 5)": ("Mean goals scored by the team in its latest qualifying overall matches.", "Sum of team goals scored divided by the qualifying sample count, up to five completed matches.", "Goals per match; inspect sample N."),
    "Avg. Goals Conceded (Last 5)": ("Mean goals conceded by the team in its latest qualifying overall matches.", "Sum of opponent goals divided by the qualifying sample count, up to five completed matches.", "Goals per match; inspect sample N."),
    "Avg. Points (Last 5)": ("Average league points earned per match in the qualifying recent sample.", "Total 3-1-0 points divided by the qualifying sample count.", "Points per match."),
    "Attacking Index": ("Descriptive relative attacking index.", "Capped 0–100 index: 50 × team goals-for average ÷ league goals-per-team baseline, when inputs exist.", "Index, not probability; depends on sample and league baseline."),
    "Defensive Index": ("Descriptive relative defensive index.", "Capped 0–100 inverse-conceding index: 50 × league goals-per-team baseline ÷ team goals-against average; undefined for zero conceded average.", "Index, not probability; inspect missing values."),
    "TOTAL Index": ("Combined descriptive team index.", "Source presentation field combining the available attack/defence indices; not a probability. Exact implementation is source-code-defined.", "Index; not a prediction probability."),
    "H2H Last 5 Summary": ("Summary of the latest qualifying head-to-head meetings.", "Uses up to five completed exact-pair meetings strictly before fixture cutoff; no fuzzy aliases.", "Descriptive summary; check H2H N and match basis."),
    "H2H Avg Total Goals": ("Average total goals across qualifying prior H2H meetings.", "Mean of home_goals + away_goals across the included H2H meeting rows; no meetings yields NO_VERIFIED_PRIOR_H2H.", "Goals per meeting; check H2H sample N."),
    "Historical Accuracy Status": ("Whether the source Oracle prediction has been historically graded.", "Copied status from runtime/report evidence; no accuracy is calculated if no verified settled outcome and grading record exist.", "Status, not accuracy percentage."),
    "Home Evidence Risk": ("Home-side evidence/data-quality risk indicator.", "Report-only risk indicator based on evidence completeness/provenance; not the probability the home team loses.", "Percentage/status per source; do not interpret as outcome risk."),
    "Away Evidence Risk": ("Away-side evidence/data-quality risk indicator.", "Report-only risk indicator based on evidence completeness/provenance; not the probability the away team loses.", "Percentage/status per source; do not interpret as outcome risk."),
    "Home Risk Rationale": ("Explanation of home-side evidence risk.", "Rule/status rationale generated from the evidence and missing-feature checks.", "Text rationale; not a model prediction."),
    "Away Risk Rationale": ("Explanation of away-side evidence risk.", "Rule/status rationale generated from the evidence and missing-feature checks.", "Text rationale; not a model prediction."),
    "A+ Setup Status": ("Source-defined premium setup status.", "Copied from runtime/report status; no new threshold or model decision is introduced here.", "Categorical status; inspect supporting gates."),
    "Gem's Independent Match Analysis": ("Narrative commentary field.", "Text field from the report process; not an independent probability or verified source record.", "Qualitative only; never override numeric source evidence."),
    "fixture_id": ("Provider/runtime fixture identifier used for exact fixture identity.", "Copied from the runtime/archive identity; combined with provider season and ordered home/away team IDs for exact joins.", "Identifier; do not join on display name alone."),
    "selected_id": ("Governed Selected-50 competition/season mapping identifier.", "Exact mapping through the selected-season manifest and pinned archive ingestion manifest.", "Identifier; not interchangeable with league display name."),
    "provider_season_id": ("Provider season identifier.", "Copied from archive/runtime; used as an exact join component.", "Identifier."),
    "home_team_id": ("Provider identifier for the home team.", "Copied from the archive/runtime exact fixture record.", "Identifier."),
    "away_team_id": ("Provider identifier for the away team.", "Copied from the archive/runtime exact fixture record.", "Identifier."),
    "history_cutoff_utc": ("UTC timestamp defining the latest permitted historical evidence time for this fixture.", "Set from the fixture's runtime kickoff timestamp; history rows must be strictly earlier than this cutoff.", "UTC timestamp; records at or after cutoff are excluded."),
    "h2h_n": ("Number of qualifying prior H2H meetings included.", "Count of exact matched, completed, valid-score meetings strictly before cutoff; generally capped to latest five for fixture-level summary.", "Integer sample size; zero means no verified qualifying pair in this archive, not proof teams never met."),
    "h2h_scope": ("Scope used to identify eligible H2H meetings.", "Selected-50 country scope from the pinned ingestion manifest; no cross-country matching.", "Scope label; inspect h2h_scope_id."),
    "h2h_scope_id": ("Exact identifier for the H2H country scope.", "Mapped from the archive ingestion manifest and selected-season mapping.", "Identifier."),
    "home_form_n": ("Number of qualifying completed overall matches in the home team's form sample.", "Count of valid, completed, strictly pre-cutoff matches for the exact team ID in the exact provider competition; up to five.", "Integer sample size."),
    "away_form_n": ("Number of qualifying completed overall matches in the away team's form sample.", "Same rule as home_form_n for the away team.", "Integer sample size."),
    "home_at_home_form_n": ("Number of qualifying home-at-home matches.", "Count of qualifying completed matches where the home team played at home, strictly pre-cutoff; up to five.", "Integer sample size."),
    "away_away_form_n": ("Number of qualifying away-away matches.", "Count of qualifying completed matches where the away team played away, strictly pre-cutoff; up to five.", "Integer sample size."),
    "home_evidence_risk_pct": ("Home-side evidence risk percentage.", "Report-only evidence completeness/provenance calculation; never a match-loss probability.", "Percentage points."),
    "away_evidence_risk_pct": ("Away-side evidence risk percentage.", "Report-only evidence completeness/provenance calculation; never a match-loss probability.", "Percentage points."),
    "production_eligible": ("Whether this row is permitted in production model/prediction use.", "Governance control. In this research-only workflow the value must remain false/NO.", "Boolean/status; YES is not permitted by this report workflow."),
    "betting_eligible": ("Whether this row is approved for betting use.", "Governance control. In this research-only workflow the value must remain false/NO.", "Boolean/status; YES is not permitted by this report workflow."),
    "capture_time_utc": ("Verified xG data capture timestamp, if available.", "Must be supported by fixture-linked source capture metadata; archive match kickoff is not a substitute.", "UTC timestamp; blank/unverified means xG is not point-in-time verified."),
    "temporal_provenance_status": ("Assessment of whether xG can be proven available at the relevant pre-kickoff time.", "Derived from fixture-linked capture/revision/hash evidence and cutoff comparison.", "Status; numeric xG without verified provenance remains quarantined."),
    "prediction_use_status": ("Whether xG is allowed as a prediction feature.", "Governance decision based on temporal provenance and evidence completeness.", "Status; do not use quarantined xG."),
    "prediction_eligible": ("Whether this xG record is permitted for prediction use.", "Boolean governance output from the xG provenance audit.", "Boolean; numeric presence alone does not qualify."),
    "betting_eligible": ("Whether this record is permitted for betting use.", "Boolean governance output; report remains research-only.", "Boolean."),
}

def describe(sheet, header):
    if header in EXACT:
        purpose, calc, limits = EXACT[header]
        return purpose, calc, limits
    h = str(header)
    low = h.casefold()
    if low.endswith("_utc") or "kickoff" in low or "timestamp" in low or "retrieved_utc" in low:
        return ("Time or cutoff field used to establish chronology and provenance.",
                "Copied from the named runtime/archive/source field; timestamps are normalized or compared as UTC only where the audit explicitly does so.",
                "Never substitute archive kickoff for capture time; chronology is strict pre-kickoff.")
    if low.endswith("_id") or low.endswith("_fixture_ids") or low in {"fixture_identity","fixture"}:
        return ("Identifier or exact identity trace used to connect records.",
                "Copied from the corresponding provider/runtime/manifest record or assembled from exact identity components.",
                "Use exact IDs and declared composite keys; display names are not sufficient for joins.")
    if low.endswith("_n") or "sample_n" in low or low.endswith("_count") or low.endswith("_rows"):
        return ("Count of records, matches, rows or observations in the named scope.",
                "Count supplied by the source audit or calculated as the number of qualifying records in the explicitly named sample.",
                "Always interpret with its denominator, scope and status; a count does not prove feature completeness.")
    if "probability" in low or low.endswith("_pct") or "rate_pct" in low or low.endswith("_rate"):
        return ("Probability, percentage or empirical rate for the market/feature named in the heading.",
                "Copied from source where identified as a runtime prediction; otherwise an empirical rate is computed as qualifying positive outcomes divided by qualifying sample N. Check the sheet's evidence label and source status.",
                "Do not equate empirical historical rate with a forecast probability; inspect sample size and provenance.")
    if "status" in low or "state" in low or "gate" in low or "eligible" in low or "resolution_action" in low:
        return ("Categorical control, availability, validation or eligibility result.",
                "Copied from or derived by the named QA/governance rule; see the relevant sheet's QA record and source script.",
                "Status values are not numeric predictions; BLOCKED/REVIEW/NOT_AVAILABLE must not be treated as PASS.")
    if "reason" in low or "interpretation" in low or "limitation" in low or "remediation" in low:
        return ("Human-readable explanation of a status, exception, limitation or remediation.",
                "Generated by the corresponding report/audit rule or copied from source evidence.", "Descriptive text; not a prediction.")
    if "sha256" in low or "hash" in low or "source_file" in low or "source_row" in low:
        return ("Source provenance locator or integrity value.", "Copied from the archive, snapshot, manifest or source artifact metadata.", "Use for traceability; a hash does not establish semantic correctness or pre-kickoff availability.")
    if any(x in low for x in ("avg", "average", "lambda", "goals_for", "goals_against", "points_per_game")):
        return ("Numeric historical feature or expected-goals parameter for the named team/side/sample.",
                "Derived from qualifying prior completed matches or copied from the research model output; see the source sample count and status.", "Inspect sample N, cutoff and source; lambda is an experimental model parameter, not an Oracle production probability.")
    if "form" in low:
        return ("Recent results sequence or venue/overall form feature for the named team/side.",
                "Derived from completed qualifying prior matches in the named scope, strictly before the fixture cutoff.", "Check sample N and whether this is overall or venue-restricted form.")
    if "league" in low or "country" in low or "competition" in low or "season" in low:
        return ("Competition, country or season grouping/label used for reporting and coverage.", "Copied from the selected-season manifest, provider archive or runtime fixture record.", "Use selected_id/provider_season_id for exact joins; labels may not be unique.")
    if "field" in low or "column" in low or "role" in low or "denominator" in low or "coverage" in low or "records" in low:
        return ("Field-level coverage audit descriptor or count.", "Calculated by the field coverage audit from the named source sheet and denominator basis.", "Presence, usable-value coverage and explicit unavailable states are distinct; consult Coverage State.")
    if sheet == "Definitions & Governance":
        return ("Governance term and its definition.", "Authored report governance definition.", "Normative control; does not alter production model logic.")
    return (f"Field named '{h}' describing {sheet}.",
            "Source value is copied from the corresponding runtime, archive, evidence, coverage or QA output unless the heading and sheet explicitly identify a derived measure. No additional calculation is introduced by the dictionary.",
            "Refer to the source sheet's status, sample size, exact identity and provenance columns before interpreting. Unknown or unavailable values must not be inferred.")

def style_sheet(ws, widths):
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="333F50")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for idx, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--workbook", required=True)
    ap.add_argument("--config", required=True)
    args=ap.parse_args()
    path=Path(args.workbook)
    config=json.loads(Path(args.config).read_text(encoding="utf-8"))
    wb=load_workbook(path)
    if "LLM Data Dictionary" in wb.sheetnames:
        del wb["LLM Data Dictionary"]
    if "Report Configuration" in wb.sheetnames:
        del wb["Report Configuration"]
    dictionary=wb.create_sheet("LLM Data Dictionary")
    dictionary.append(["Sheet", "Sheet Purpose", "Column #", "Column Heading", "Purpose / Meaning", "Source / Calculation", "Units / Format", "Interpretation / Limitations"])
    count=0
    for source in list(wb.worksheets):
        if source.title in {"LLM Data Dictionary","Report Configuration"}:
            continue
        if source.max_row < 1:
            continue
        sheet_purpose=SHEET_PURPOSE.get(source.title, f"Additional report audit sheet '{source.title}'.")
        for col in range(1, source.max_column+1):
            header=source.cell(1,col).value
            if header is None or str(header).strip()=="":
                continue
            purpose, calc, limits=describe(source.title, str(header))
            units="See field semantics; identifiers/status/text are non-numeric."
            if any(k in str(header).casefold() for k in ("probability","_pct","rate_pct","coverage_pct")):
                units="Percentage points (0–100), unless the source explicitly uses a fraction."
            elif str(header).casefold().endswith("_n") or "count" in str(header).casefold() or "rows" in str(header).casefold():
                units="Integer count."
            elif "utc" in str(header).casefold() or "kickoff" in str(header).casefold() or "timestamp" in str(header).casefold():
                units="UTC ISO-8601 timestamp, where supplied."
            elif any(k in str(header).casefold() for k in ("avg","average","lambda","goals_for","goals_against")):
                units="Numeric feature; typically goals/match or model lambda. Check exact field and sample."
            dictionary.append([source.title, sheet_purpose, col, str(header), purpose, calc, units, limits])
            count+=1
    if count==0:
        raise SystemExit("No report headings found; dictionary cannot be generated.")
    style_sheet(dictionary,[25,48,11,38,58,76,32,76])
    cfg=wb.create_sheet("Report Configuration")
    cfg.append(["Configuration Key","Value / Instruction"])
    cfg_rows=[
        ("report_name",config.get("report_name","Oracle Selected-50 Market Intelligence Report")),
        ("configuration_version",config.get("configuration_version","")),
        ("governed_league_universe",config.get("governed_league_universe","")),
        ("selected_league_count",config.get("selected_league_count","")),
        ("production_benchmark",config.get("production_benchmark","")),
        ("pinned_archive_release_tag",config.get("pinned_archive_release_tag","")),
        ("pinned_archive_sha256",config.get("pinned_archive_sha256","")),
        ("history_minimum_matches",config.get("history_minimum_matches","")),
        ("history_cutoff_rule",config.get("history_cutoff_rule","")),
        ("h2h_matching_policy",config.get("h2h_matching_policy","")),
        ("xg_policy",config.get("xg_policy","")),
        ("production_and_betting_policy",config.get("production_and_betting_policy","")),
        ("weekly_workflow",config.get("weekly_workflow","")),
        ("weekly_run_instructions",config.get("weekly_run_instructions","")),
        ("required_inputs",config.get("required_inputs","")),
        ("output_artifact",config.get("output_artifact","")),
        ("reproducibility_rule",config.get("reproducibility_rule","")),
        ("dictionary_columns_included",count),
        ("dictionary_scope","Every non-empty column heading in every other workbook sheet, generated dynamically from the actual workbook schema."),
        ("generation_policy","This step only adds explanatory tabs. It does not modify fixture rows, Oracle probabilities, feature values, eligibility or production logic.")
    ]
    for row in cfg_rows: cfg.append(list(row))
    style_sheet(cfg,[36,120])
    wb.save(path)
    print(json.dumps({"status":"PASS_DICTIONARY_AND_CONFIGURATION_ADDED","dictionary_entries":count,"sheets":wb.sheetnames},indent=2))

if __name__=="__main__":
    main()

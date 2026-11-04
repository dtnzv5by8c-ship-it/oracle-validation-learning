#!/usr/bin/env python3
"""Write an explicit no-query actual-results register when provider credits are not approved.

This is a report-only placeholder. It makes zero network/API calls and never infers scores.
A later approved FootyStats reconciliation replaces the Actual Results sheet and these files.
"""
import argparse
import csv
import json
from pathlib import Path
from openpyxl import load_workbook

FIELDS = [
    "fixture_date_utc", "league", "fixture", "provider_season_id", "fixture_id",
    "home_team_provider_id", "away_team_provider_id", "actual_home_goals",
    "actual_away_goals", "actual_total_goals", "actual_match_result",
    "actual_btts", "actual_over_1_5", "actual_over_2_5", "actual_under_4_5",
    "settlement_status", "provider_match_status", "results_source",
    "retrieved_utc", "provider_date_unix", "production_eligible", "betting_eligible"
]


def build_rows(runtime_rows):
    rows = []
    for item in runtime_rows:
        rows.append({
            "fixture_date_utc": item.get("date_utc", ""),
            "league": item.get("league", ""),
            "fixture": f"{item.get('home_team', '')} vs {item.get('away_team', '')}",
            "provider_season_id": item.get("provider_season_id", ""),
            "fixture_id": item.get("fixture_id", ""),
            "home_team_provider_id": item.get("home_team_provider_id", ""),
            "away_team_provider_id": item.get("away_team_provider_id", ""),
            "actual_home_goals": "",
            "actual_away_goals": "",
            "actual_total_goals": "",
            "actual_match_result": "",
            "actual_btts": "",
            "actual_over_1_5": "",
            "actual_over_2_5": "",
            "actual_under_4_5": "",
            "settlement_status": "NOT_RETRIEVED_NO_CREDIT_APPROVAL",
            "provider_match_status": "",
            "results_source": "NOT_QUERIED",
            "retrieved_utc": "",
            "provider_date_unix": "",
            "production_eligible": "NO",
            "betting_eligible": "NO",
        })
    return rows


def write_placeholder(runtime_report, workbook_path, out_dir):
    runtime_report = Path(runtime_report)
    workbook_path = Path(workbook_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with runtime_report.open(encoding="utf-8-sig", newline="") as handle:
        runtime_rows = list(csv.DictReader(handle))
    if not runtime_rows:
        raise ValueError("Runtime report is empty; refusing to create an empty results register.")
    rows = build_rows(runtime_rows)
    csv_path = out_dir / "oracle_selected50_actual_results.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    wb = load_workbook(workbook_path)
    if "Actual Results" in wb.sheetnames:
        del wb["Actual Results"]
    ws = wb.create_sheet("Actual Results")
    ws.append(FIELDS)
    for row in rows:
        ws.append([row.get(field, "") for field in FIELDS])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for col in ws.columns:
        letter = col[0].column_letter
        ws.column_dimensions[letter].width = min(
            34, max(14, max(len(str(cell.value or "")) for cell in col[:200]) + 2)
        )
    wb.save(workbook_path)

    qa = {
        "status": "NOT_RUN_CREDIT_APPROVAL_NOT_GRANTED",
        "runtime_fixture_rows": len(runtime_rows),
        "results_rows": len(rows),
        "provider_seasons_requested": 0,
        "provider_seasons_failed": [],
        "settlement_status_counts": {"NOT_RETRIEVED_NO_CREDIT_APPROVAL": len(rows)},
        "provider_api_calls": 0,
        "retrieved_utc": "",
        "source": "NOT_QUERIED_NO_CREDIT_APPROVAL",
        "provider_credit_authorized": False,
        "identity_policy": "EXACT_PROVIDER_SEASON_FIXTURE_ID_ORDERED_HOME_AWAY_TEAM_IDS; NO RESULTS JOIN ATTEMPTED",
        "production_eligible": False,
        "betting_eligible": False,
        "prediction_probabilities_modified": False,
    }
    (out_dir / "oracle_selected50_actual_results_qa.json").write_text(
        json.dumps(qa, indent=2) + "\n", encoding="utf-8"
    )
    return qa


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-report", required=True)
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(write_placeholder(args.runtime_report, args.workbook, args.out_dir), indent=2))


if __name__ == "__main__":
    main()

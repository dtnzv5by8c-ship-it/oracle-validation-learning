#!/usr/bin/env python3
"""Enforce the user-approved 95-column OMI Market Intelligence layout.

This is a reporting-only compatibility step. It never recalculates Oracle
probabilities or creates evidence. It copies the already-enriched OMI Report
values to the Market Intelligence view by exact Fixture ID.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from openpyxl import load_workbook

def header_index(ws):
    return {str(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1)
            if ws.cell(1, c).value is not None}

def fixture_rows(ws, fixture_id_col):
    rows = {}
    for row_num in range(2, ws.max_row + 1):
        fixture_id = ws.cell(row_num, fixture_id_col).value
        if fixture_id in (None, ""):
            continue
        key = str(fixture_id).strip()
        if key in rows:
            raise ValueError(f"Duplicate Fixture ID in {ws.title}: {key}")
        rows[key] = row_num
    return rows

def enforce(workbook_path: Path, schema_path: Path) -> dict:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    headers = schema["headers"]
    if len(headers) != 95 or schema.get("baseline_columns") != "A:CQ":
        raise ValueError("Canonical OMI schema must contain exactly 95 A:CQ headers")
    wb = load_workbook(workbook_path)
    if "OMI Report" not in wb.sheetnames or "Market Intelligence" not in wb.sheetnames:
        raise ValueError("Workbook must contain OMI Report and Market Intelligence sheets")
    omi, market = wb["OMI Report"], wb["Market Intelligence"]
    omi_idx, market_idx = header_index(omi), header_index(market)
    if "Fixture ID" not in omi_idx or "Fixture ID" not in market_idx:
        raise ValueError("Both report sheets must contain Fixture ID")
    omi_rows = fixture_rows(omi, omi_idx["Fixture ID"])
    market_rows = fixture_rows(market, market_idx["Fixture ID"])
    if not omi_rows or omi_rows.keys() != market_rows.keys():
        raise ValueError("OMI Report and Market Intelligence Fixture ID sets do not match")
    for col, header in enumerate(headers, start=1):
        omi.cell(1, col).value = header
        market.cell(1, col).value = header
    for fixture_id, target_row in market_rows.items():
        source_row = omi_rows[fixture_id]
        for col in range(1, 96):
            market.cell(target_row, col).value = omi.cell(source_row, col).value
    for ws in (omi, market):
        ws.freeze_panes = "D2"
        ws.auto_filter.ref = f"A1:CQ{ws.max_row}"
        ws.sheet_view.showGridLines = False
    # CR:CS are reserved; this step must not create values there.
    for ws in (omi, market):
        if any(ws.cell(r, c).value not in (None, "") for r in range(1, ws.max_row + 1) for c in (96, 97)):
            raise ValueError(f"Reserved columns CR:CS must remain empty in {ws.title}")
    wb.save(workbook_path)
    # Re-open after save and verify the complete immutable schema.
    check = load_workbook(workbook_path, read_only=True, data_only=False)
    for name in ("OMI Report", "Market Intelligence"):
        ws = check[name]
        actual = [ws.cell(1, c).value for c in range(1, 96)]
        if actual != headers or ws.max_column > 97:
            raise ValueError(f"Post-save schema verification failed for {name}")
    return {"fixture_rows": len(omi_rows), "columns": 95, "baseline": "A:CQ",
            "reserved": "CR:CS", "first_extension": "CT", "status": "PASS"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--schema", default="config/omi_market_intelligence_schema_v1.json")
    args = parser.parse_args()
    result = enforce(Path(args.workbook), Path(args.schema))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

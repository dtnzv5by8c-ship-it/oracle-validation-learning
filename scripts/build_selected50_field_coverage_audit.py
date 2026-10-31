#!/usr/bin/env python3
"""Build a report-only per-league field coverage audit from the Selected-50 workbook."""
from __future__ import annotations
import argparse, csv, json, hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

SOURCE_SHEETS = {
    "Market Intelligence": "Provider Season ID",
    "xG Evidence Audit": "selected_id",
    "Goal Intelligence": "selected_id",
    "H2H Intelligence": "selected_id",
    "Team Form Evidence": "selected_id",
    "Data Quality & Risk": "selected_id",
    "Schedule Reconciliation": "selected_id",
    "Goal Market Research": "provider_season_id",
    "50-League Coverage": "Selected Season ID",
}
EXCLUDED_SHEETS = [
    "Oracle V1.6 Output", "Market Data Coverage", "Archive Field Coverage",
    "Definitions & Governance", "Coverage Audit Summary", "xG Provenance Decision",
]
STATUS_PREFIXES = (
    "NOT_AVAILABLE", "NOT_VALIDATED", "NOT_GRADED", "NO_VERIFIED", "NO_FIXTURE",
    "NO_FIXTURES", "NO_RECORDS", "BLOCKED", "QUARANTINED", "REVIEW_REQUIRED",
    "UNAVAILABLE", "UNKNOWN", "NOT_APPLICABLE", "NOT_REQUIRED", "NOT_ASSESSED",
    "UNVERIFIED", "INSUFFICIENT", "MISSING", "PENDING", "MASKED", "FAIL_",
)
MATRIX_HEADERS = [
    "Selected Season ID", "Country", "League", "Source Sheet", "Source Column #",
    "Field", "Field Occurrence", "Field Role", "Denominator Basis", "Scope Records",
    "Nonblank Records", "Usable Value Records", "Explicit Status / Unavailable Records",
    "Blank Records", "Presence %", "Usable Value %", "Coverage State",
    "Common Values / Statuses", "Interpretation / Limitation",
]
SUMMARY_HEADERS = [
    "Source Sheet", "Source Column #", "Field", "Field Occurrence", "Field Role",
    "Denominator Basis", "Total Records", "Nonblank Records", "Usable Value Records",
    "Explicit Status / Unavailable Records", "Blank Records", "Presence %", "Usable Value %",
    "Groups Full", "Groups Partial", "Groups Status Only", "Groups Explicitly Blocked",
    "Groups Missing", "Groups No Records",
]

def blank(v):
    return v is None or (isinstance(v, str) and not v.strip())

def norm(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()

def role_for(field):
    s = str(field).lower()
    if any(x in s for x in ("status", "reason", "eligible", "gate", "decision", "state", "block")):
        return "STATUS"
    if any(x in s for x in ("probability", "_pct", "percent", "lambda", "risk_pct")):
        return "PROBABILITY_OR_RATE"
    if any(x in s for x in ("_n", "count", "sample", "rank", "rows", "fixtures", "meetings")):
        return "COUNT_OR_SAMPLE"
    if any(x in s for x in ("id", "league", "country", "fixture", "date", "kickoff", "source_file", "source_row", "sha256", "url")):
        return "IDENTITY_OR_PROVENANCE"
    return "VALUE_OR_DESCRIPTION"

def is_explicit_status(value, role):
    if blank(value):
        return False
    if role == "STATUS":
        return True
    if isinstance(value, str):
        u = value.strip().upper()
        return u.startswith(STATUS_PREFIXES) or (u in {"YES", "NO", "PASS", "FAIL", "TRUE", "FALSE"} and role != "VALUE_OR_DESCRIPTION")
    return False

def parse_utc(value):
    if blank(value):
        return None
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None

def normalize_report_statuses(wb):
    """Fill explicit report-layer NOT_REQUIRED states; never alter model values."""
    counts = {
        "goal_market_nonblocked_reason_filled": 0,
        "goal_market_blocked_reason_still_missing": 0,
        "schedule_no_mismatch_reason_filled": 0,
        "schedule_exact_match_zero_delta_filled": 0,
        "schedule_review_reason_still_missing": 0,
    }
    if "Goal Market Research" in wb.sheetnames:
        ws = wb["Goal Market Research"]
        headers = [c.value for c in ws[1]]
        idx = {h:i+1 for i,h in enumerate(headers)}
        if all(k in idx for k in ("forecast_status", "blocked_reason")):
            for row in range(2, ws.max_row + 1):
                status = str(ws.cell(row, idx["forecast_status"]).value or "").strip().upper()
                reason = ws.cell(row, idx["blocked_reason"])
                if status == "EXPERIMENTAL_UNCALIBRATED" and blank(reason.value):
                    reason.value = "NONE_FORECASTABLE_RESEARCH_ONLY"
                    counts["goal_market_nonblocked_reason_filled"] += 1
                elif status.startswith("BLOCKED") and blank(reason.value):
                    counts["goal_market_blocked_reason_still_missing"] += 1
    if "Data Quality & Risk" in wb.sheetnames:
        ws = wb["Data Quality & Risk"]
        headers = [c.value for c in ws[1]]
        idx = {h:i+1 for i,h in enumerate(headers)}
        if all(k in idx for k in ("schedule_reconciliation_status", "schedule_reconciliation_reason")):
            for row in range(2, ws.max_row + 1):
                status = str(ws.cell(row, idx["schedule_reconciliation_status"]).value or "").strip().upper()
                reason = ws.cell(row, idx["schedule_reconciliation_reason"])
                if status == "MATCH" and blank(reason.value):
                    reason.value = "NOT_REQUIRED_NO_KICKOFF_MISMATCH"
                    counts["schedule_no_mismatch_reason_filled"] += 1
                elif status == "REVIEW_REQUIRED" and blank(reason.value):
                    counts["schedule_review_reason_still_missing"] += 1
                if status == "MATCH" and "schedule_delta_minutes_archive_minus_runtime" in idx and blank(ws.cell(row, idx["schedule_delta_minutes_archive_minus_runtime"]).value):
                    rt = parse_utc(ws.cell(row, idx["runtime_kickoff_utc"]).value) if "runtime_kickoff_utc" in idx else None
                    ar = parse_utc(ws.cell(row, idx["archive_kickoff_utc"]).value) if "archive_kickoff_utc" in idx else None
                    if rt and ar and rt == ar:
                        ws.cell(row, idx["schedule_delta_minutes_archive_minus_runtime"]).value = 0
                        counts["schedule_exact_match_zero_delta_filled"] += 1
    return counts

def interpretation(sheet, field, role):
    s, f = sheet.lower(), str(field).lower()
    if "xg" in s or "xg" in f:
        return "Field presence only; point-in-time capture and revision provenance are unverified. Keep xG quarantined from forecasts and betting."
    if "h2h" in f:
        return "No verified prior H2H may mean no qualifying meeting under exact identity, competition scope and pre-kickoff cutoff."
    if "schedule" in s or "kickoff" in f:
        return "Schedule discrepancies require authoritative event-time review; no automatic correction."
    if "historical accuracy" in f or "a+ setup" in f:
        return "Not graded; requires exact historical prediction ledger, point-in-time inputs and authoritative settlement evidence."
    if "goal market" in s or "lambda" in f or "forecast" in f:
        return "Experimental, uncalibrated research only; insufficient baselines or missing estimates are not production/betting eligible."
    if role == "STATUS":
        return "Status-field presence is audited separately from value availability; inspect explicit status semantics."
    return "Presence/value coverage only; semantic validity and point-in-time provenance require separate validation."

def style_sheet(ws):
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    ws.row_dimensions[1].height = 42
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="333366")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, cell in enumerate(ws[1], 1):
        ws.column_dimensions[get_column_letter(i)].width = min(48, max(14, len(str(cell.value or "")) + 3))
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

def write_csv(path, headers, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbook", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    workbook_path = Path(args.workbook)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    wb = load_workbook(workbook_path)
    normalizations = normalize_report_statuses(wb)
    if "50-League Coverage" not in wb.sheetnames:
        raise SystemExit("FAIL: workbook has no 50-League Coverage sheet")
    cov = wb["50-League Coverage"]
    cov_headers = [c.value for c in cov[1]]
    cov_idx = {h:i for i,h in enumerate(cov_headers)}
    sid_col = cov_idx.get("Selected Season ID")
    country_col = cov_idx.get("Country")
    league_col = cov_idx.get("League")
    if sid_col is None:
        raise SystemExit("FAIL: Selected Season ID missing from coverage sheet")
    groups = {}
    for vals in cov.iter_rows(min_row=2, values_only=True):
        sid = norm(vals[sid_col]) if vals[sid_col] is not None else ""
        if not sid:
            continue
        if sid in groups:
            raise SystemExit(f"FAIL: duplicate selected season ID in coverage sheet: {sid}")
        groups[sid] = {
            "Country": norm(vals[country_col]) if country_col is not None and vals[country_col] is not None else "",
            "League": norm(vals[league_col]) if league_col is not None and vals[league_col] is not None else "",
        }
    if len(groups) != 50:
        raise SystemExit(f"FAIL: expected 50 unique selected season IDs, found {len(groups)}")
    matrix, unmapped = [], Counter()
    row_counts, field_counts = {}, {}
    for sheet_name, key_name in SOURCE_SHEETS.items():
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        headers = [c.value if c.value is not None else f"__UNNAMED_COLUMN_{i+1}" for i,c in enumerate(ws[1])]
        positions = [i for i,h in enumerate(headers) if h == key_name]
        if not positions:
            raise SystemExit(f"FAIL: {sheet_name} has no exact grouping key column '{key_name}'")
        key_pos = positions[0]
        rows_by_group = defaultdict(list)
        for vals in ws.iter_rows(min_row=2, values_only=True):
            if not any(v is not None for v in vals):
                continue
            sid = norm(vals[key_pos]) if key_pos < len(vals) and vals[key_pos] is not None else ""
            if not sid or sid not in groups:
                unmapped[sheet_name] += 1
                continue
            rows_by_group[sid].append(vals)
        row_counts[sheet_name] = sum(len(v) for v in rows_by_group.values())
        occurrences = Counter()
        for col_idx, field in enumerate(headers):
            occurrences[field] += 1
            occurrence = occurrences[field]
            role = role_for(field)
            for sid, meta in groups.items():
                recs = rows_by_group.get(sid, [])
                denom = len(recs)
                vals = [r[col_idx] if col_idx < len(r) else None for r in recs]
                nonblank = [v for v in vals if not blank(v)]
                explicit = [v for v in nonblank if is_explicit_status(v, role)]
                usable = [v for v in nonblank if not is_explicit_status(v, role)]
                blanks = denom - len(nonblank)
                if denom == 0:
                    state = "NO_RECORDS_IN_SCOPE"
                elif blanks == 0 and len(explicit) == 0:
                    state = "FULL_VALUE_COVERAGE"
                elif blanks == 0 and len(usable) == 0:
                    state = "STATUS_PRESENT_ALL_RECORDS" if role == "STATUS" else "EXPLICITLY_UNAVAILABLE_OR_BLOCKED"
                elif blanks == 0:
                    state = "PARTIAL_VALUE_COVERAGE"
                elif role == "STATUS" and len(nonblank) == 0:
                    state = "STATUS_MISSING"
                elif len(nonblank) == 0:
                    state = "NO_USABLE_VALUES"
                elif role == "STATUS":
                    state = "STATUS_PARTIAL"
                else:
                    state = "PARTIAL_VALUE_COVERAGE"
                counts = Counter(norm(v) for v in nonblank)
                common = " | ".join(f"{k} ({n})" for k,n in counts.most_common(3))
                matrix.append({
                    "Selected Season ID": sid, "Country": meta["Country"], "League": meta["League"],
                    "Source Sheet": sheet_name, "Source Column #": col_idx+1, "Field": field,
                    "Field Occurrence": occurrence, "Field Role": role,
                    "Denominator Basis": "record_count_in_source_sheet_for_selected_season",
                    "Scope Records": denom, "Nonblank Records": len(nonblank),
                    "Usable Value Records": len(usable), "Explicit Status / Unavailable Records": len(explicit),
                    "Blank Records": blanks,
                    "Presence %": round(100*len(nonblank)/denom,2) if denom else 0.0,
                    "Usable Value %": round(100*len(usable)/denom,2) if denom else 0.0,
                    "Coverage State": state, "Common Values / Statuses": common,
                    "Interpretation / Limitation": interpretation(sheet_name, field, role),
                })
        field_counts[sheet_name] = len(headers)
    if not matrix:
        raise SystemExit("FAIL: no field coverage rows generated")
    by_field = defaultdict(list)
    for row in matrix:
        key = (row["Source Sheet"], row["Source Column #"], row["Field"], row["Field Occurrence"], row["Field Role"])
        by_field[key].append(row)
    summary = []
    for key, recs in by_field.items():
        denom = sum(r["Scope Records"] for r in recs)
        nonblank = sum(r["Nonblank Records"] for r in recs)
        usable = sum(r["Usable Value Records"] for r in recs)
        explicit = sum(r["Explicit Status / Unavailable Records"] for r in recs)
        blanks = sum(r["Blank Records"] for r in recs)
        states = Counter(r["Coverage State"] for r in recs)
        summary.append(dict(zip(
            ["Source Sheet", "Source Column #", "Field", "Field Occurrence", "Field Role"], key
        ), **{
            "Denominator Basis": "sum_of_record_counts_across_selected_seasons",
            "Total Records": denom, "Nonblank Records": nonblank,
            "Usable Value Records": usable, "Explicit Status / Unavailable Records": explicit,
            "Blank Records": blanks, "Presence %": round(100*nonblank/denom,2) if denom else 0.0,
            "Usable Value %": round(100*usable/denom,2) if denom else 0.0,
            "Groups Full": states["FULL_VALUE_COVERAGE"],
            "Groups Partial": states["PARTIAL_VALUE_COVERAGE"],
            "Groups Status Only": states["STATUS_PRESENT_ALL_RECORDS"],
            "Groups Explicitly Blocked": states["EXPLICITLY_UNAVAILABLE_OR_BLOCKED"],
            "Groups Missing": states["STATUS_MISSING"] + states["NO_USABLE_VALUES"],
            "Groups No Records": states["NO_RECORDS_IN_SCOPE"],
        }))
    exceptions = [r for r in matrix if r["Coverage State"] not in {
        "FULL_VALUE_COVERAGE", "STATUS_PRESENT_ALL_RECORDS", "NO_RECORDS_IN_SCOPE"
    }]
    for name in ("50-League Field Coverage", "Field Coverage Summary", "Field Coverage Exceptions", "Field Coverage QA"):
        if name in wb.sheetnames:
            del wb[name]
    for name, headers, rows in (
        ("50-League Field Coverage", MATRIX_HEADERS, matrix),
        ("Field Coverage Summary", SUMMARY_HEADERS, summary),
        ("Field Coverage Exceptions", MATRIX_HEADERS, exceptions),
    ):
        ws = wb.create_sheet(name)
        ws.append(headers)
        for row in rows:
            ws.append([row.get(h, "") for h in headers])
        style_sheet(ws)
    qa = {
        "status": "PASS_FIELD_BY_FIELD_SELECTED50_REPORT_AUDIT",
        "selected_league_groups": len(groups),
        "selected_season_ids": sorted(groups),
        "source_sheets_audited": list(field_counts),
        "source_sheet_row_counts": row_counts,
        "source_sheet_field_counts": field_counts,
        "field_occurrences_audited": len(summary),
        "league_field_matrix_rows": len(matrix),
        "exception_rows": len(exceptions),
        "exception_states": dict(Counter(r["Coverage State"] for r in exceptions)),
        "unmapped_rows_by_sheet": dict(unmapped),
        "report_only_status_normalizations": normalizations,
        "skipped_non_league_sheets": EXCLUDED_SHEETS,
        "production_model_logic_changed": False,
        "production_probabilities_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
        "xg_policy": "QUARANTINED_UNTIL_POINT_IN_TIME_CAPTURE_AND_REVISION_PROVENANCE_VERIFIED",
    }
    ws = wb.create_sheet("Field Coverage QA")
    ws.append(["Control", "Result"])
    for k,v in qa.items():
        ws.append([k, json.dumps(v, ensure_ascii=False) if isinstance(v,(dict,list)) else v])
    style_sheet(ws)
    wb.save(workbook_path)
    matrix_path = out_dir / "oracle_selected50_field_coverage_by_league.csv"
    summary_path = out_dir / "oracle_selected50_field_coverage_summary.csv"
    exceptions_path = out_dir / "oracle_selected50_field_coverage_exceptions.csv"
    qa_path = out_dir / "oracle_selected50_field_coverage_qa.json"
    write_csv(matrix_path, MATRIX_HEADERS, matrix)
    write_csv(summary_path, SUMMARY_HEADERS, summary)
    write_csv(exceptions_path, MATRIX_HEADERS, exceptions)
    qa["workbook_sha256"] = hashlib.sha256(workbook_path.read_bytes()).hexdigest()
    qa["matrix_csv_sha256"] = hashlib.sha256(matrix_path.read_bytes()).hexdigest()
    qa["summary_csv_sha256"] = hashlib.sha256(summary_path.read_bytes()).hexdigest()
    qa["exceptions_csv_sha256"] = hashlib.sha256(exceptions_path.read_bytes()).hexdigest()
    qa["workbook_size_bytes"] = workbook_path.stat().st_size
    qa_path.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k:qa[k] for k in ("status","selected_league_groups","field_occurrences_audited","league_field_matrix_rows","exception_rows","unmapped_rows_by_sheet","report_only_status_normalizations")}, indent=2))

if __name__ == "__main__":
    main()

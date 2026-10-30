#!/usr/bin/env python3
"""Exact calendar-year coverage from the pinned private Selected-50 archive.

Outputs aggregate counts only. Never exports raw provider match rows or treats
numeric score/price presence as settlement truth.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, json, os, zipfile
from collections import Counter, defaultdict
from pathlib import Path
try:
    from scripts.qa_selected50_private_archive import read_json, as_list, date_value
except ModuleNotFoundError:
    from qa_selected50_private_archive import read_json, as_list, date_value

ARCHIVE = Path(os.environ.get("ORACLE_ARCHIVE", "private-download/oracle-selected50-footystats-private-ingestion.zip"))
MANIFEST = Path("data/oracle-footystats-selected-50-season-id-manifest.csv")
YEARS = (2024, 2025, 2026, 2027)
FIELDS = (
    "team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch",
    "odds_btts_yes", "odds_btts_no", "odds_doublechance_1x", "odds_doublechance_x2",
)

def numeric(v):
    if v in (None, "") or isinstance(v, bool): return None
    try:
        x = float(v)
    except (TypeError, ValueError, OverflowError): return None
    return x if x == x and abs(x) != float("inf") else None

def summarize(rows, audit_date):
    out = {"match_rows": len(rows), "unique_provider_match_ids": 0, "duplicate_provider_match_id_rows": 0,
           "undated_rows": 0, "kickoff_date_min": "", "kickoff_date_max": "",
           "kickoff_on_or_before_audit_date_rows": 0, "kickoff_after_audit_date_rows": 0,
           "status_counts": {}, "field_quality": {}}
    ids = []
    statuses = Counter()
    dates = []
    for row in rows:
        rid = row.get("id", row.get("match_id", row.get("fixture_id", row.get("game_id", ""))))
        if rid not in (None, ""): ids.append(str(rid).strip())
        status = str(row.get("status", "")).strip().lower() or "MISSING"
        statuses[status] += 1
        day = date_value(row)
        if not day:
            out["undated_rows"] += 1
        else:
            parsed = dt.date.fromisoformat(day)
            dates.append(day)
            if parsed <= audit_date: out["kickoff_on_or_before_audit_date_rows"] += 1
            else: out["kickoff_after_audit_date_rows"] += 1
    id_counts = Counter(ids)
    out["unique_provider_match_ids"] = len(id_counts)
    out["duplicate_provider_match_id_rows"] = sum(n - 1 for n in id_counts.values() if n > 1)
    out["status_counts"] = dict(sorted(statuses.items()))
    out["kickoff_date_min"] = min(dates) if dates else ""
    out["kickoff_date_max"] = max(dates) if dates else ""
    for field in FIELDS:
        values = [numeric(row.get(field)) for row in rows]
        numeric_values = [v for v in values if v is not None]
        out["field_quality"][field] = {
            "numeric_rows": len(numeric_values),
            "missing_or_nonnumeric_rows": len(rows) - len(numeric_values),
            "zero_rows": sum(v == 0 for v in numeric_values),
            "positive_rows": sum(v > 0 for v in numeric_values),
            "negative_rows": sum(v < 0 for v in numeric_values),
        }
    return out

def load_selected(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 50 or len({r["selected_id"] for r in rows}) != 50:
        raise ValueError("Selected-50 manifest must contain exactly 50 unique season IDs")
    groups = {}
    for r in rows:
        key = (r["country"].strip(), r["competition_name"].strip())
        if not all(key) or key in groups: raise ValueError(f"Duplicate or blank selected league group: {key}")
        groups[key] = r["selected_id"].strip()
    return groups

def run(archive, manifest, out):
    groups = load_selected(manifest)
    audit_date = dt.datetime.now(dt.timezone.utc).date()
    group_rows = defaultdict(list)
    season_rows = defaultdict(list)
    group_undated = Counter()
    season_undated = Counter()
    season_meta = {}
    unmatched = []
    with zipfile.ZipFile(archive) as z:
        names = set(z.namelist())
        manifest_name = next((n for n in names if n.endswith("ingestion_manifest.json")), None)
        if not manifest_name: raise ValueError("Archive ingestion_manifest.json missing")
        raw = read_json(z, manifest_name)
        if not isinstance(raw, list): raise ValueError("Archive season manifest is not a list")
        season_ids = [str(m.get("season_id", "")).strip() for m in raw]
        if len(season_ids) != len(set(season_ids)) or "" in season_ids:
            raise ValueError("Archive season manifest has blank/duplicate IDs")
        selected_ids = set(groups.values())
        missing_selected_ids = sorted(selected_ids - set(season_ids))
        if missing_selected_ids:
            raise ValueError("Selected season IDs missing from archive manifest: " + ",".join(missing_selected_ids))
        for meta in raw:
            sid = str(meta["season_id"]).strip()
            group = (str(meta.get("selected_country", "")).strip(), str(meta.get("selected_competition_name", "")).strip())
            if group not in groups:
                unmatched.append({"season_id": sid, "reason": "NO_EXACT_SELECTED_COUNTRY_COMPETITION_MATCH"})
                continue
            base = f"seasons/{sid}/"
            file = next((n for n in names if n.endswith(base + "matches.json")), None)
            if not file:
                unmatched.append({"season_id": sid, "reason": "MATCHES_FILE_MISSING"})
                continue
            matches = as_list(read_json(z, file))
            season_meta[sid] = {"country": group[0], "competition_name": group[1], "ingestion_status": meta.get("status", "UNKNOWN")}
            for row in matches:
                if not isinstance(row, dict): continue
                day = date_value(row)
                if not day:
                    group_undated[group] += 1
                    season_undated[sid] += 1
                    continue
                year = int(day[:4])
                if year in YEARS:
                    group_rows[(group[0], group[1], year)].append(row)
                    season_rows[(sid, year)].append(row)
    group_out, season_out = [], []
    for (country, competition), selected_sid in sorted(groups.items()):
        seasons_for_group = [sid for sid, m in season_meta.items() if (m["country"], m["competition_name"]) == (country, competition)]
        for year in YEARS:
            rows = group_rows[(country, competition, year)]
            s = summarize(rows, audit_date)
            rows_asof = [row for row in rows if date_value(row) and dt.date.fromisoformat(date_value(row)) <= audit_date]
            rows_future = [row for row in rows if date_value(row) and dt.date.fromisoformat(date_value(row)) > audit_date]
            rows_complete_asof = [row for row in rows_asof if str(row.get("status", "")).strip().lower() == "complete"]
            asof_summary = summarize(rows_asof, audit_date)
            future_summary = summarize(rows_future, audit_date)
            complete_asof_summary = summarize(rows_complete_asof, audit_date)
            group_out.append({
                "country": country, "competition_name": competition, "selected_current_season_id": selected_sid,
                "calendar_year": year, "archive_season_folders_for_group": len(seasons_for_group),
                "season_ids_in_archive": ";".join(sorted(seasons_for_group)),
                **{k: s[k] for k in ("match_rows","unique_provider_match_ids","duplicate_provider_match_id_rows","kickoff_date_min","kickoff_date_max","kickoff_on_or_before_audit_date_rows","kickoff_after_audit_date_rows")},
                "undated_rows_in_group_across_archive_seasons": group_undated[(country, competition)],
                "rows_on_or_before_audit_date": len(rows_asof),
                "rows_after_audit_date": len(rows_future),
                "status_counts_json": json.dumps(s["status_counts"], sort_keys=True),
                "status_counts_on_or_before_audit_date_json": json.dumps(asof_summary["status_counts"], sort_keys=True),
                "status_counts_after_audit_date_json": json.dumps(future_summary["status_counts"], sort_keys=True),
                "field_quality_json": json.dumps(s["field_quality"], sort_keys=True),
                "field_quality_on_or_before_audit_date_json": json.dumps(asof_summary["field_quality"], sort_keys=True),
                "field_quality_after_audit_date_json": json.dumps(future_summary["field_quality"], sort_keys=True),
                "complete_status_rows_on_or_before_audit_date": len(rows_complete_asof),
                "field_quality_complete_status_on_or_before_audit_date_json": json.dumps(complete_asof_summary["field_quality"], sort_keys=True),
                "complete_status_rows_on_or_before_audit_date": len(rows_complete_asof),
                "field_quality_complete_status_on_or_before_audit_date_json": json.dumps(complete_asof_summary["field_quality"], sort_keys=True),
                "official_settlement_truth_verified": "NO", "canonical_fixture_team_joins_verified": "NO",
                "production_eligible": "NO",
            })
    for sid, meta in sorted(season_meta.items()):
        for year in YEARS:
            rows = season_rows[(sid, year)]
            s = summarize(rows, audit_date)
            rows_asof = [row for row in rows if date_value(row) and dt.date.fromisoformat(date_value(row)) <= audit_date]
            rows_future = [row for row in rows if date_value(row) and dt.date.fromisoformat(date_value(row)) > audit_date]
            rows_complete_asof = [row for row in rows_asof if str(row.get("status", "")).strip().lower() == "complete"]
            asof_summary = summarize(rows_asof, audit_date)
            future_summary = summarize(rows_future, audit_date)
            complete_asof_summary = summarize(rows_complete_asof, audit_date)
            season_out.append({
                "season_id": sid, **meta, "calendar_year": year,
                **{k: s[k] for k in ("match_rows","unique_provider_match_ids","duplicate_provider_match_id_rows","kickoff_date_min","kickoff_date_max","kickoff_on_or_before_audit_date_rows","kickoff_after_audit_date_rows")},
                "undated_rows_in_season": season_undated[sid],
                "rows_on_or_before_audit_date": len(rows_asof),
                "rows_after_audit_date": len(rows_future),
                "status_counts_json": json.dumps(s["status_counts"], sort_keys=True),
                "status_counts_on_or_before_audit_date_json": json.dumps(asof_summary["status_counts"], sort_keys=True),
                "status_counts_after_audit_date_json": json.dumps(future_summary["status_counts"], sort_keys=True),
                "field_quality_json": json.dumps(s["field_quality"], sort_keys=True),
                "field_quality_on_or_before_audit_date_json": json.dumps(asof_summary["field_quality"], sort_keys=True),
                "field_quality_after_audit_date_json": json.dumps(future_summary["field_quality"], sort_keys=True),
            })
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in (("selected50_calendar_year_coverage_by_league.csv", group_out),
                       ("selected50_calendar_year_coverage_by_season.csv", season_out),
                       ("selected50_calendar_year_unmatched_seasons.csv", unmatched)):
        with (out/name).open("w", newline="", encoding="utf-8") as f:
            fields = list(rows[0]) if rows else ["season_id", "reason"]
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    season_counts_by_group = {key: sum(1 for m in season_meta.values() if (m["country"], m["competition_name"]) == key) for key in groups}
    all_groups_have_four_seasons = all(count == 4 for count in season_counts_by_group.values())
    summary = {
        "status": "RESEARCH_ONLY_CALENDAR_YEAR_COVERAGE_COMPLETE" if len(group_out) == 200 and len(groups) == 50 and len(season_meta) == 200 and all_groups_have_four_seasons else "REVIEW_REQUIRED",
        "audit_date_utc": audit_date.isoformat(),
        "selected_league_groups": len(groups), "league_year_rows": len(group_out),
        "archive_season_folders_matched_exactly": len(season_meta),
        "league_groups_with_exactly_four_archive_seasons": sum(count == 4 for count in season_counts_by_group.values()),
        "archive_season_folder_counts_by_group": {f"{k[0]}::{k[1]}": v for k, v in sorted(season_counts_by_group.items())},
        "season_year_rows": len(season_out), "unmatched_or_missing_season_folders": len(unmatched),
        "undated_match_rows": sum(group_undated.values()),
        "calendar_years": list(YEARS),
        "total_rows_by_year": {str(y): sum(r["match_rows"] for r in group_out if r["calendar_year"] == y) for y in YEARS},
        "kickoff_rows_on_or_before_audit_date_by_year": {str(y): sum(r["kickoff_on_or_before_audit_date_rows"] for r in group_out if r["calendar_year"] == y) for y in YEARS},
        "kickoff_rows_after_audit_date_by_year": {str(y): sum(r["kickoff_after_audit_date_rows"] for r in group_out if r["calendar_year"] == y) for y in YEARS},
        "limitations": [
            "Calendar-year counts are provider archive rows grouped by exact selected country and competition labels; they are not canonical fixture counts.",
            "Provider status is reported, not converted into official settlement truth.",
            "Numeric xG/odds values are descriptive; zero is not recoded and field presence is not PIT provenance.",
            "No model logic, probabilities, production ledgers or betting eligibility are changed."
        ],
    }
    (out/"selected50_calendar_year_coverage_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    if summary["status"] != "RESEARCH_ONLY_CALENDAR_YEAR_COVERAGE_COMPLETE":
        raise SystemExit("Calendar-year coverage is incomplete; see unmatched season output.")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive", type=Path, default=ARCHIVE)
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    p.add_argument("--out-dir", type=Path, default=Path("selected50_calendar_year_coverage"))
    a=p.parse_args()
    run(a.archive, a.manifest, a.out_dir)

if __name__ == "__main__": main()

#!/usr/bin/env python3
"""Fail-closed, research-only scope check for Oracle's owner-selected 50 leagues.

This validates identifiers and reports readiness blockers. It never approves mappings,
changes production configuration, or treats season IDs as competition/provider IDs.
"""
import argparse
import csv
import json
import re
from pathlib import Path

ID_COLUMNS = (
    "footystats_provider_id",
    "provider_league_id",
    "provider_competition_id",
    "league_id",
    "leagueid",
    "competition_id",
    "competitionid",
    "id",
)


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_selected_manifest(path):
    text = Path(path).read_text(encoding="utf-8")
    ids = re.findall(r"^\|\s*\d+\s*\|\s*(\d+)\s*\|", text, flags=re.M)
    return ids


def norm_id(value):
    value = str(value or "").strip()
    if not value:
        return ""
    # Provider IDs in this manifest are integer identifiers; do not coerce arbitrary text.
    return str(int(value)) if value.isdigit() else value


def id_column(rows, source_name):
    if not rows:
        return None, {"status": "EMPTY_SOURCE", "candidate_columns": []}
    available = set(rows[0].keys())
    candidates = []
    for key in ID_COLUMNS:
        for col in available:
            if col.strip().lower() == key and any(norm_id(r.get(col)) for r in rows):
                candidates.append(col)
    # Keep only the highest-priority column when the columns agree. If they disagree,
    # the source is ambiguous and must not silently select one.
    sets = {col: {norm_id(r.get(col)) for r in rows if norm_id(r.get(col))} for col in candidates}
    nonempty_sets = {tuple(sorted(v)) for v in sets.values()}
    if len(nonempty_sets) > 1:
        return None, {"status": "AMBIGUOUS_ID_COLUMNS", "candidate_columns": candidates,
                      "distinct_id_counts": {k: len(v) for k, v in sets.items()}}
    if not candidates:
        return None, {"status": "NO_PROVIDER_ID_COLUMN", "candidate_columns": []}
    return candidates[0], {"status": "ID_COLUMN_FOUND", "candidate_columns": candidates,
                           "distinct_id_count": len(sets[candidates[0]])}


def compare_ids(expected, observed):
    return {
        "expected_count": len(expected),
        "observed_unique_count": len(observed),
        "missing_ids": sorted(expected - observed),
        "extra_ids": sorted(observed - expected),
        "exact_set_match": expected == observed,
    }


def audit(manifest_path, crosswalk_path, catalogue_path, archive_manifest_path):
    issues = []
    selected_list = read_selected_manifest(manifest_path)
    selected = set(selected_list)
    if len(selected_list) != 50:
        issues.append(f"selected manifest has {len(selected_list)} parsed rows; expected exactly 50")
    if len(selected) != len(selected_list):
        issues.append("selected manifest contains duplicate provider IDs")
    if not selected:
        issues.append("no selected provider IDs parsed from manifest")

    crosswalk = read_csv(crosswalk_path)
    crosswalk_ids = [norm_id(r.get("footystats_provider_id")) for r in crosswalk]
    crosswalk_set = {x for x in crosswalk_ids if x}
    crosswalk_check = compare_ids(selected, crosswalk_set)
    if len(crosswalk) != 50 or len(crosswalk_set) != 50 or not crosswalk_check["exact_set_match"]:
        issues.append("crosswalk does not contain the exact 50 selected provider IDs once each")
    if len(crosswalk_ids) != len(crosswalk_set):
        issues.append("crosswalk contains blank or duplicate provider IDs")
    for i, row in enumerate(crosswalk, start=1):
        status = str(row.get("crosswalk_status") or "").strip().upper()
        eligibility = str(row.get("production_eligibility") or "").strip().upper()
        if status.startswith("APPROVED") or eligibility not in {"NOT_GRANTED", "NOT GRANTED"}:
            issues.append(f"crosswalk row {i} contains an approval/eligibility state that this research audit cannot grant")

    catalogue = read_csv(catalogue_path)
    cat_col, cat_col_info = id_column(catalogue, "provider catalogue")
    catalogue_check = None
    if cat_col is None:
        issues.append("provider catalogue has no unambiguous populated competition/provider ID column")
    else:
        cat_ids = {norm_id(r.get(cat_col)) for r in catalogue if norm_id(r.get(cat_col))}
        catalogue_check = compare_ids(selected, cat_ids)
        if not catalogue_check["exact_set_match"]:
            issues.append("provider catalogue ID set does not exactly match the owner-selected 50 IDs")

    archive_rows = read_csv(archive_manifest_path)
    archive_col = next((c for c in (archive_rows[0].keys() if archive_rows else [])
                        if c.strip().lower() == "provider_league_id"), None)
    blank_archive_ids = 0
    archive_check = None
    if archive_col is None:
        issues.append("archive manifest lacks a provider_league_id column; season_id is not an acceptable substitute")
    else:
        blank_archive_ids = sum(not norm_id(r.get(archive_col)) for r in archive_rows)
        archive_ids = {norm_id(r.get(archive_col)) for r in archive_rows if norm_id(r.get(archive_col))}
        archive_check = compare_ids(selected, archive_ids)
        if blank_archive_ids:
            issues.append(f"archive manifest has {blank_archive_ids} rows with blank provider_league_id")
        if not archive_check["exact_set_match"]:
            issues.append("archive manifest provider_league_id set does not exactly match the selected 50 IDs")

    return {
        "schema_version": "ORACLE_SELECTED50_SCOPE_GUARD_V1.0",
        "status": "PASS_SCOPE_MATCH" if not issues else "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE",
        "production_eligibility": "NOT_GRANTED",
        "scope": "owner-approved FootyStats selected 50; no substitution by the 27-league registry",
        "selected_manifest_rows": len(selected_list),
        "selected_unique_provider_ids": len(selected),
        "crosswalk_rows": len(crosswalk),
        "crosswalk_id_check": crosswalk_check,
        "provider_catalogue_row_count": len(catalogue),
        "provider_catalogue_id_column": cat_col,
        "provider_catalogue_id_column_check": cat_col_info,
        "provider_catalogue_id_check": catalogue_check,
        "archive_manifest_rows": len(archive_rows),
        "archive_provider_id_column": archive_col,
        "archive_blank_provider_id_rows": blank_archive_ids,
        "archive_provider_id_check": archive_check,
        "blockers": issues,
        "interpretation": "PASS_SCOPE_MATCH validates only the identifier set and does not establish data freshness, fixture/team joins, feature provenance, market readiness, or production eligibility.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--crosswalk", required=True)
    p.add_argument("--catalogue", required=True)
    p.add_argument("--archive-manifest", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    result = audit(args.manifest, args.crosswalk, args.catalogue, args.archive_manifest)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    # This is a reporting-only workflow: preserve the diagnostic artifact even when blocked.
    # Downstream consumers must gate on result.status, never on process exit alone.


if __name__ == "__main__":
    main()

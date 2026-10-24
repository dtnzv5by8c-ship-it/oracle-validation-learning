#!/usr/bin/env python3
"""Create a conservative per-target readiness view from the sanitized Oracle audit.

This is a research/reporting-only artifact. It never creates predictions, changes
model logic, approves fuzzy mappings, or treats pagination termination as season
completeness. Usage: python scripts/build_oracle_44_readiness.py <audit-dir>
"""
import csv
import json
import sys
from pathlib import Path

CORE_FIELDS = ("match_id", "homeID", "awayID", "date_unix", "status")


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def truthy_id(value):
    return str(value or "").strip() not in ("", "0", "None", "null")


def build(root):
    coverage_path = root / "oracle_44_league_full_season_coverage.csv"
    crosswalk_path = root / "oracle_44_league_candidate_crosswalk.csv"
    fixtures_path = root / "oracle_44_league_sanitized_fixture_audit.csv"
    for path in (coverage_path, crosswalk_path, fixtures_path):
        if not path.is_file():
            raise FileNotFoundError(f"Required audit input missing: {path.name}")

    coverage = read_csv(coverage_path)
    crosswalk = read_csv(crosswalk_path)
    fixtures = read_csv(fixtures_path)
    fixture_by_code = {}
    for row in fixtures:
        fixture_by_code.setdefault(row.get("target_code", ""), []).append(row)
    crosswalk_by_code = {r.get("target_code", ""): r for r in crosswalk}

    readiness = []
    for cov in coverage:
        code = cov.get("target_code", "")
        cw = crosswalk_by_code.get(code, {})
        rows = fixture_by_code.get(code, [])
        catalogue_status = cov.get("catalogue_status", "")
        fetch_status = cov.get("match_fetch_status", "")
        notes = []
        missing_core = sum(
            not all(truthy_id(row.get(field)) for field in CORE_FIELDS)
            for row in rows
        )
        duplicates = int(cov.get("duplicate_match_ids") or 0)
        if catalogue_status in ("NO_EXACT_ALIAS_MATCH", "AMBIGUOUS_ALIAS", "NO_SEASON_ID"):
            status = "PARKED_UNVERIFIED"
            notes.append("Competition/season identity is not safely established; no fuzzy mapping auto-approved.")
        elif fetch_status != "PAGINATION_STOPPED_SHORT_PAGE":
            status = "BLOCKED"
            notes.append("Fixture retrieval did not end normally; inspect failure diagnostics.")
        elif not rows or missing_core or duplicates:
            status = "PARTIAL"
            notes.append("Fixture rows are absent or core identity fields/uniqueness checks need repair.")
        else:
            status = "PARTIAL"
            notes.append("Fixture retrieval and core-field checks pass; season completeness and point-in-time provenance remain unverified.")
        if cov.get("cutoff_provenance") != "VERIFIED":
            notes.append("Not cleared for historical backtesting or pre-kickoff prediction evaluation.")
        readiness.append({
            "target_code": code,
            "country": cov.get("country", ""),
            "target_competition": cov.get("target_competition", ""),
            "provider_name": cw.get("provider_name", cov.get("provider_name", "")),
            "provider_season_id": cw.get("provider_season_id", cov.get("provider_season_id", "")),
            "season_label": cw.get("season_label", cov.get("season_label", "")),
            "fixture_rows": len(rows),
            "core_field_missing_rows": missing_core,
            "duplicate_match_ids": duplicates,
            "retrieval_status": fetch_status,
            "readiness_status": status,
            "prediction_ready": "NO",
            "reason": " ".join(notes),
        })
    return readiness


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/build_oracle_44_readiness.py <audit-dir>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    rows = build(root)
    if len(rows) != 44 or len({r["target_code"] for r in rows}) != 44:
        raise SystemExit(f"Expected 44 unique target rows; found {len(rows)}")
    output = root / "oracle_44_league_readiness.csv"
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    counts = {}
    for row in rows:
        counts[row["readiness_status"]] = counts.get(row["readiness_status"], 0) + 1
    summary = {
        "target_leagues": len(rows),
        "readiness_counts": counts,
        "prediction_ready_targets": sum(r["prediction_ready"] == "YES" for r in rows),
        "season_completeness_proven": False,
        "point_in_time_provenance_established": False,
        "model_logic_changed": False,
        "production_registry_changed": False,
        "production_predictions_created": False,
        "interpretation": "Readiness is fixture-ingestion/reporting status only. PARTIAL does not mean season-complete or prediction-ready.",
    }
    (root / "oracle_44_league_readiness_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

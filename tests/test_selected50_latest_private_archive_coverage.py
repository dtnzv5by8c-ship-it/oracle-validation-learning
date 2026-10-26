#!/usr/bin/env python3
"""Regression test for the latest sanitized Selected-50 private-archive coverage snapshot."""
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_selected50_latest_private_archive_coverage.py"


def rows(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        subprocess.run([sys.executable, str(SCRIPT), "--out-dir", str(out)],
                       cwd=ROOT, check=True, capture_output=True, text=True)
        matrix = rows(out / "selected50_latest_private_archive_coverage_matrix.csv")
        summary = json.loads((out / "selected50_latest_private_archive_coverage_summary.json").read_text(encoding="utf-8"))
        assert len(matrix) == 50 and len({r["selected_id"] for r in matrix}) == 50
        assert summary["status"] == "PASS_SANITIZED_SELECTED50_ARCHIVE_COVERAGE_CONTRACT_RESEARCH_ONLY"
        assert summary["snapshot_freshness_status"] == "PRE_BATCH5_QA_SNAPSHOT_SUPERSEDED_FOR_CURRENT_ARCHIVE_COVERAGE"
        assert summary["source_snapshot_qa_created_at_utc"] == "2026-10-25T10:07:11Z"
        assert summary["superseding_historical_ingestion_run_id"] == "40375285207"
        assert summary["superseding_historical_ingestion_created_at_utc"] == "2026-10-26T18:09:53Z"
        assert summary["current_historical_archive_coverage_verified_by_snapshot"] is False
        assert summary["selected_groups"] == summary["unique_selected_ids"] == 50
        assert summary["all_50_manifest_rows_ingested"] is True
        assert summary["all_50_private_season_folders_ok"] is True
        assert summary["metadata_matches"] == summary["country_competition_composite_matches"] == 50
        assert summary["parent_competition_ids_populated"] == 0
        assert summary["separate_country_values_retained"] == 0
        assert summary["total_private_season_fixture_rows"] == 14051
        assert summary["total_unique_season_fixture_pairs"] == 14051
        assert summary["duplicate_season_fixture_pairs"] == 0
        assert summary["total_primary_window_rows_2025_03_20_to_2026_09_20"] == 5637
        assert summary["both_teams_recent5_prior_counts_sum"] == 11744
        assert summary["h2h_prior_meeting_rows_sum"] == 5294
        assert summary["date_unclassified_rows"] == 135
        assert summary["complete_status_vs_past_date_candidate_difference"] == 4
        assert summary["odds_timestamp_rows"] == 0
        assert summary["provider_xg_odds_point_in_time_provenance_verified"] is False
        assert summary["canonical_fixture_team_joins_verified"] is False
        assert summary["official_settlement_truth_verified"] is False
        assert summary["production_eligible"] is False and summary["betting_eligible"] is False
        assert summary["network_calls_made"] == summary["paid_provider_calls_made"] == 0
        assert sum(r["season_label_format_status"] == "NONSTANDARD_8_DIGIT_TOKEN_UNVERIFIED" for r in matrix) == 33
        assert {r["selected_id"] for r in matrix if r["provider_primary_window_fixture_rows"] == "0"} == {"17326", "17964"}
        assert all(r["production_eligible"] == "NO" for r in matrix)
        assert all(r["archive_coverage_snapshot_freshness_status"] == summary["snapshot_freshness_status"] for r in matrix)
        assert all(r["archive_coverage_source_qa_run_id"] == "40183451811" for r in matrix)
        assert all(r["archive_coverage_superseding_ingestion_run_id"] == "40375285207" for r in matrix)
        print("PASS: 50-season sanitized coverage reconciles to the verified QA artifact; identity, settlement, standings, xG/odds provenance and production remain blocked.")


if __name__ == "__main__":
    main()

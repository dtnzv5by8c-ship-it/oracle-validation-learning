#!/usr/bin/env python3
"""Build a sanitized 50-row matrix from the latest verified private-archive QA snapshot.

Reads only the already-published sanitized crosswalk/QA summary. No API or network
calls. Does not infer parent competition IDs, official settlement truth, or
canonical Oracle fixture/team joins.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv"
MANIFEST = ROOT / "data/oracle-footystats-selected-50-season-id-manifest.csv"
OUT = ROOT / "audit-output"
EXPECTED_QA_RUN = "40183451811"
EXPECTED_QA_ARTIFACT = "12594568810"
EXPECTED_QA_SHA256 = "713ed63ed5dd6e6902a2e152367500386d5037dd6dc8bbc82fa87c831d10c375"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def unique_by(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        value = str(row.get(key, "")).strip()
        if not value:
            raise ValueError(f"{label}: blank {key}")
        if value in out:
            raise ValueError(f"{label}: duplicate {key}={value}")
        out[value] = row
    return out


def number(row: dict[str, str], key: str) -> int:
    value = str(row.get(key, "")).strip()
    if not re.fullmatch(r"\d+", value):
        raise ValueError(f"{key}: expected non-negative integer, got {value!r}")
    return int(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--out-dir", type=Path, default=OUT)
    args = parser.parse_args()

    source_rows = read_csv(args.source)
    manifest_rows = read_csv(args.manifest)
    source = unique_by(source_rows, "footystats_provider_id", "crosswalk snapshot")
    manifest = unique_by(manifest_rows, "selected_id", "selected-50 manifest")
    if len(source) != 50 or len(manifest) != 50 or set(source) != set(manifest):
        raise ValueError("Crosswalk snapshot and selected manifest must match the same 50 unique season IDs")

    # Verify the source snapshot actually points to the inspected sanitized QA artifact.
    for sid, row in source.items():
        checks = {
            "latest_private_archive_qa_run_id": EXPECTED_QA_RUN,
            "latest_private_archive_qa_conclusion": "success",
            "latest_private_archive_qa_artifact_id": EXPECTED_QA_ARTIFACT,
            "latest_private_archive_qa_artifact_sha256": EXPECTED_QA_SHA256,
            "latest_private_archive_selected_id_set_match": "PASS_50_OF_50",
            "latest_private_archive_fixture_rows": "14051",
            "latest_private_archive_unique_season_fixture_pairs": "14051",
            "latest_private_archive_duplicate_pairs": "0",
            "latest_private_archive_parent_competition_id_rows": "0",
            "provider_parent_competition_id_status": "NOT_EXPOSED_BY_CATALOGUE",
            "provider_xg_point_in_time_provenance": "NOT_VERIFIED; NO_AS_OF_TIMESTAMP_PROVENANCE",
            "provider_odds_point_in_time_provenance": "NOT_VERIFIED; NO_ODDS_TIMESTAMP_FIELD_OBSERVED",
            "production_eligibility": "NOT_GRANTED",
        }
        for field, expected in checks.items():
            if row.get(field, "") != expected:
                raise ValueError(f"{sid}: source provenance invariant failed for {field}: {row.get(field)!r}")

    out_fields = [
        "selected_id", "country", "competition", "provider_season_year_raw",
        "season_label_format_status", "manifest_status", "selected_id_semantics_status",
        "crosswalk_candidate_code", "crosswalk_status", "provider_season_fixture_records",
        "provider_season_team_records", "provider_primary_window_fixture_rows",
        "provider_past_date_fixture_rows", "provider_future_date_fixture_rows",
        "provider_recent_form5_home_prior_count", "provider_recent_form5_away_prior_count",
        "provider_recent_form5_both_teams_prior_count", "provider_h2h_prior_meeting_rows",
        "provider_fixture_id_field_presence_pct", "provider_kickoff_field_presence_pct",
        "provider_team_id_pair_field_presence_pct", "provider_team_name_pair_field_presence_pct",
        "provider_score_pair_field_presence_pct_not_settlement_truth",
        "provider_standings_payload_status", "provider_parent_competition_id_status",
        "provider_country_field_value_status", "provider_country_competition_composite_label_status",
        "provider_xg_nonempty_global_coverage_pct", "provider_odds_nonempty_global_coverage_pct",
        "provider_xg_point_in_time_provenance", "provider_odds_point_in_time_provenance",
        "provider_selected_season_id_to_private_fixture_join_status",
        "current_feed_identity_join_status", "BTTS_YES_readiness",
        "DOUBLE_CHANCE_readiness", "DC_UNDER_4_5_readiness", "M1UP_readiness",
        "canonical_fixture_join_status", "canonical_team_join_status",
        "official_settlement_truth_status", "production_eligible",
    ]
    out_rows: list[dict[str, str]] = []
    for sid, m in manifest.items():
        row = source[sid]
        raw_year = str(row.get("provider_season_year_raw", "")).strip()
        year_status = (
            "NONSTANDARD_8_DIGIT_TOKEN_UNVERIFIED"
            if re.fullmatch(r"\d{8}", raw_year)
            else "RAW_PROVIDER_YEAR_TOKEN"
        )
        out_rows.append({
            "selected_id": sid,
            "country": m.get("country", ""),
            "competition": m.get("competition_name", ""),
            "provider_season_year_raw": raw_year,
            "season_label_format_status": year_status,
            "manifest_status": row.get("provider_ingestion_run_status", ""),
            "selected_id_semantics_status": row.get("provider_selected_id_semantics", ""),
            "crosswalk_candidate_code": row.get("canonical_code_candidate", ""),
            "crosswalk_status": row.get("crosswalk_status", ""),
            "provider_season_fixture_records": row.get("provider_season_fixture_records", ""),
            "provider_season_team_records": row.get("provider_season_team_records", ""),
            "provider_primary_window_fixture_rows": row.get("provider_primary_window_fixture_rows", ""),
            "provider_past_date_fixture_rows": row.get("provider_past_date_fixture_rows", ""),
            "provider_future_date_fixture_rows": row.get("provider_future_date_fixture_rows", ""),
            "provider_recent_form5_home_prior_count": row.get("provider_recent_form5_home_prior_count", ""),
            "provider_recent_form5_away_prior_count": row.get("provider_recent_form5_away_prior_count", ""),
            "provider_recent_form5_both_teams_prior_count": row.get("provider_recent_form5_both_teams_prior_count", ""),
            "provider_h2h_prior_meeting_rows": row.get("provider_h2h_prior_meeting_rows", ""),
            "provider_fixture_id_field_presence_pct": row.get("provider_fixture_id_coverage_pct", ""),
            "provider_kickoff_field_presence_pct": row.get("provider_kickoff_field_coverage_pct", ""),
            "provider_team_id_pair_field_presence_pct": row.get("provider_team_id_pair_coverage_pct", ""),
            "provider_team_name_pair_field_presence_pct": row.get("provider_team_name_pair_coverage_pct", ""),
            "provider_score_pair_field_presence_pct_not_settlement_truth": row.get("provider_score_pair_field_coverage_pct", ""),
            "provider_standings_payload_status": row.get("provider_standings_payload_status", ""),
            "provider_parent_competition_id_status": row.get("provider_parent_competition_id_status", ""),
            "provider_country_field_value_status": row.get("provider_country_field_value_status", ""),
            "provider_country_competition_composite_label_status": row.get("provider_country_competition_composite_label_status", ""),
            "provider_xg_nonempty_global_coverage_pct": row.get("provider_xg_nonempty_global_coverage_pct", ""),
            "provider_odds_nonempty_global_coverage_pct": row.get("provider_odds_nonempty_global_coverage_pct", ""),
            "provider_xg_point_in_time_provenance": row.get("provider_xg_point_in_time_provenance", ""),
            "provider_odds_point_in_time_provenance": row.get("provider_odds_point_in_time_provenance", ""),
            "provider_selected_season_id_to_private_fixture_join_status": row.get("provider_selected_season_id_to_private_fixture_join_status", ""),
            "current_feed_identity_join_status": row.get("current_feed_identity_join_status", ""),
            "BTTS_YES_readiness": row.get("BTTS_YES_readiness", ""),
            "DOUBLE_CHANCE_readiness": row.get("DOUBLE_CHANCE_readiness", ""),
            "DC_UNDER_4_5_readiness": row.get("DC_UNDER_4_5_readiness", ""),
            "M1UP_readiness": row.get("M1UP_readiness", ""),
            "canonical_fixture_join_status": "NOT_VERIFIED",
            "canonical_team_join_status": "NOT_VERIFIED",
            "official_settlement_truth_status": "NOT_VERIFIED",
            "production_eligible": "NO",
        })

    total_matches = sum(number(r, "provider_season_fixture_records") for r in source.values())
    total_primary = sum(number(r, "provider_primary_window_fixture_rows") for r in source.values())
    total_past = sum(number(r, "provider_past_date_fixture_rows") for r in source.values())
    total_future = sum(number(r, "provider_future_date_fixture_rows") for r in source.values())
    total_home_form = sum(number(r, "provider_recent_form5_home_prior_count") for r in source.values())
    total_away_form = sum(number(r, "provider_recent_form5_away_prior_count") for r in source.values())
    total_both_form = sum(number(r, "provider_recent_form5_both_teams_prior_count") for r in source.values())
    total_h2h = sum(number(r, "provider_h2h_prior_meeting_rows") for r in source.values())
    raw_years = [str(r.get("provider_season_year_raw", "")).strip() for r in source.values()]
    nonstandard_years = [sid for sid, r in source.items()
                         if re.fullmatch(r"\d{8}", str(r.get("provider_season_year_raw", "")).strip())]
    zero_primary = sorted(sid for sid, r in source.items() if number(r, "provider_primary_window_fixture_rows") == 0)
    odds_values = number(next(iter(source.values())), "latest_private_archive_odds_nonempty_rows")
    odds_timestamp_rows = number(next(iter(source.values())), "latest_private_archive_odds_timestamp_rows")
    xg_values = number(next(iter(source.values())), "latest_private_archive_xg_nonempty_rows")
    status_counts = json.loads(next(iter(source.values())).get("latest_private_archive_provider_status_counts", "{}"))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / "selected50_latest_private_archive_coverage_matrix.csv"
    json_path = args.out_dir / "selected50_latest_private_archive_coverage_summary.json"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(sorted(out_rows, key=lambda r: (r["country"], r["competition"], r["selected_id"])))

    summary = {
        "status": "PASS_SANITIZED_SELECTED50_ARCHIVE_COVERAGE_CONTRACT_RESEARCH_ONLY",
        "source": {
            "private_archive_qa_run_id": EXPECTED_QA_RUN,
            "private_archive_qa_artifact_id": EXPECTED_QA_ARTIFACT,
            "private_archive_qa_artifact_sha256": EXPECTED_QA_SHA256,
            "source_crosswalk_path": str(args.source.relative_to(ROOT)),
            "source_crosswalk_blob_sha": "2c23ac9d42f0b8cf85111ea5e431b234cc164ab4",
        },
        "selected_groups": len(out_rows),
        "unique_selected_ids": len({r["selected_id"] for r in out_rows}),
        "all_50_manifest_rows_ingested": all(r.get("provider_ingestion_run_status") == "SUCCESS_50_OF_50_SEASONS_INGESTED" for r in source.values()),
        "all_50_private_season_folders_ok": all(r.get("provider_selected_season_id_to_private_fixture_join_status", "").startswith("EXACT_SELECTED_ID_TO_PROVIDER_SEASON_ID") for r in source.values()),
        "metadata_matches": sum(r.get("selected_manifest_metadata_match_status") == "EXACT_LABEL_MATCH" for r in source.values()),
        "country_competition_composite_matches": sum(r.get("provider_country_competition_composite_label_status") == "EXACT_COUNTRY_PLUS_COMPETITION_LABEL_MATCH" for r in source.values()),
        "parent_competition_ids_populated": sum(bool(r.get("provider_parent_competition_id_status") == "POPULATED") for r in source.values()),
        "separate_country_values_retained": sum(bool(r.get("provider_country_field_value_status") == "RETAINED") for r in source.values()),
        "total_private_season_fixture_rows": total_matches,
        "total_unique_season_fixture_pairs": number(next(iter(source.values())), "latest_private_archive_unique_season_fixture_pairs"),
        "duplicate_season_fixture_pairs": number(next(iter(source.values())), "latest_private_archive_duplicate_pairs"),
        "total_primary_window_rows_2025_03_20_to_2026_09_20": total_primary,
        "past_kickoff_date_rows": total_past,
        "future_kickoff_date_rows": total_future,
        "date_unclassified_rows": total_matches - total_past - total_future,
        "provider_status_value_counts": status_counts,
        "complete_status_vs_past_date_candidate_difference": status_counts.get("complete", 0) - total_past,
        "home_recent5_prior_counts_sum": total_home_form,
        "away_recent5_prior_counts_sum": total_away_form,
        "both_teams_recent5_prior_counts_sum": total_both_form,
        "h2h_prior_meeting_rows_sum": total_h2h,
        "nonempty_table_payload_seasons": number(next(iter(source.values())), "latest_private_archive_table_payload_seasons"),
        "xg_nonempty_rows": xg_values,
        "odds_nonempty_rows": odds_values,
        "odds_nonempty_pct": next(iter(source.values())).get("latest_private_archive_odds_nonempty_pct", ""),
        "odds_timestamp_rows": odds_timestamp_rows,
        "xg_point_in_time_provenance": next(iter(source.values())).get("latest_private_archive_xg_pit_provenance", ""),
        "odds_point_in_time_provenance": next(iter(source.values())).get("latest_private_archive_odds_pit_provenance", ""),
        "raw_provider_payload_published": False,
        "canonical_fixture_team_joins_verified": False,
        "official_settlement_truth_verified": False,
        "historical_standings_as_of_kickoff_verified": False,
        "provider_xg_odds_point_in_time_provenance_verified": False,
        "nonstandard_8_digit_season_year_tokens": len(nonstandard_years),
        "nonstandard_8_digit_season_year_selected_ids": sorted(nonstandard_years),
        "selected_ids_with_zero_primary_window_rows": zero_primary,
        "network_calls_made": 0,
        "paid_provider_calls_made": 0,
        "production_eligible": False,
        "betting_eligible": False,
        "limitations": [
            "The selected IDs are season IDs; parent competition IDs are not exposed and are never inferred.",
            "Field-presence percentages are not proof of correct IDs, completed-result truth, or settlement eligibility.",
            "The provider's status 'complete' count differs from past-date candidate rows; 135 rows have neither past nor future date classification in this snapshot.",
            "A score pair field on an incomplete/future fixture is not settled-result truth.",
            "Nonempty xG fields lack as-of timestamps; odds fields lack odds timestamps. Neither is approved for point-in-time model inputs or ROI benchmarking.",
            "Table payloads are nonempty but historical standings as-of kickoff are not verified.",
            "Current feed identity, canonical Oracle fixture/team joins, and production market readiness remain blocked."
        ],
        "csv_output": str(csv_path),
    }
    if len(out_rows) != 50 or len({r["selected_id"] for r in out_rows}) != 50:
        raise ValueError("Output matrix does not contain 50 unique selected IDs")
    if total_matches != 14051 or total_primary != 5637 or total_both_form != 11744 or total_h2h != 5294:
        raise ValueError("Per-season aggregates do not match the verified sanitized QA artifact totals")
    if odds_timestamp_rows != 0 or summary["parent_competition_ids_populated"] != 0:
        raise ValueError("Critical provenance gate unexpectedly changed; review source before publishing")
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

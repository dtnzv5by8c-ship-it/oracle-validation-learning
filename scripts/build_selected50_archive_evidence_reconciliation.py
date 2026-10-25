#!/usr/bin/env python3
"""Reconcile selected-50 archive evidence layers without network/API calls.

This is a sanitized inventory audit. It does not infer parent competition IDs,
canonical team/fixture joins, settlement truth, or production eligibility.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data/oracle-footystats-selected-50-season-id-manifest.csv"
DEFAULT_RUN56 = ROOT / "data/run56_selected50_archive_evidence.csv"
DEFAULT_TRIAGE = ROOT / "data/run56_selected50_manifest_gap_triage.csv"
DEFAULT_OUT = ROOT / "audit-output"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def unique_by_id(rows: list[dict[str, str]], label: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        sid = str(row.get("selected_id", "")).strip()
        if not sid:
            raise ValueError(f"{label}: blank selected_id")
        if sid in out:
            raise ValueError(f"{label}: duplicate selected_id {sid}")
        out[sid] = row
    return out


def integer(value: str, label: str, *, blank_ok: bool = True) -> int | None:
    value = str(value or "").strip()
    if not value and blank_ok:
        return None
    try:
        n = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label}: expected integer, got {value!r}") from exc
    if n < 0:
        raise ValueError(f"{label}: negative count {n}")
    return n


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--run56", type=Path, default=DEFAULT_RUN56)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    manifest_rows = read_csv(args.manifest)
    run56_rows = read_csv(args.run56)
    triage_rows = read_csv(args.triage)
    manifest = unique_by_id(manifest_rows, "selected manifest")
    run56 = unique_by_id(run56_rows, "Run 56 evidence")
    triage = unique_by_id(triage_rows, "manifest-gap triage")

    if len(manifest) != 50:
        raise ValueError(f"Expected 50 selected groups, got {len(manifest)}")
    if set(manifest) != set(run56):
        missing = sorted(set(manifest) - set(run56))
        extra = sorted(set(run56) - set(manifest))
        raise ValueError(f"Run 56 evidence scope mismatch; missing={missing}, extra={extra}")

    direct_ids = {
        sid for sid, row in run56.items()
        if row.get("run56_manifest_status") == "MANIFEST_RECORD_PRESENT"
    }
    gap_ids = {
        sid for sid, row in run56.items()
        if row.get("run56_manifest_status") == "NO_MANIFEST_RECORD_IN_RUN56"
    }
    unexpected = set(run56) - direct_ids - gap_ids
    if unexpected:
        raise ValueError(f"Unexpected Run 56 statuses for IDs: {sorted(unexpected)}")
    if set(triage) != gap_ids:
        missing_triage = sorted(gap_ids - set(triage))
        stale_triage = sorted(set(triage) - gap_ids)
        raise ValueError(
            "Gap-triage scope must exactly equal current Run 56 manifest gaps; "
            f"missing_triage={missing_triage}, stale_triage={stale_triage}"
        )

    output: list[dict[str, str]] = []
    direct_match_rows = 0
    triage_match_rows = 0
    primary_window_rows = 0
    recent_form_rows = 0
    h2h_rows = 0
    no_primary_window_history = []
    for sid, m in manifest.items():
        a = run56[sid]
        status = a.get("run56_manifest_status", "")
        row: dict[str, str] = {
            "selected_id": sid,
            "country": m.get("country", ""),
            "competition_name": m.get("competition_name", ""),
            "selected_id_semantics": "SEASON_ID_NOT_PARENT_COMPETITION_ID",
            "run56_manifest_status": status,
            "evidence_layer": "",
            "row_count_source": "",
            "reported_match_rows": "",
            "reported_team_count": "",
            "primary_window_rows_2025_03_20_to_2026_09_20": "",
            "fixtures_with_recent5_both_teams": "",
            "fixtures_with_h2h_prior_meeting": "",
            "structural_qa_status": "",
            "provider_parent_competition_id_status": "UNRESOLVED",
            "canonical_fixture_join_status": "NOT_VERIFIED",
            "canonical_team_join_status": "NOT_VERIFIED",
            "official_settlement_truth_status": "NOT_VERIFIED",
            "historical_standings_as_of_kickoff_status": "NOT_VERIFIED",
            "xg_and_odds_point_in_time_provenance": "NOT_VERIFIED",
            "production_eligible": "NO",
            "next_action": "",
        }
        if status == "MANIFEST_RECORD_PRESENT":
            count = integer(a.get("match_count", ""), f"{sid} match_count")
            team_count = integer(a.get("team_count", ""), f"{sid} team_count")
            if count is None or team_count is None:
                raise ValueError(f"{sid}: direct manifest row lacks match_count/team_count")
            direct_match_rows += count
            row.update({
                "evidence_layer": "RUN56_EXACT_SEASON_ID_MANIFEST_MATCH",
                "row_count_source": "run56_selected50_archive_evidence.csv:match_count",
                "reported_match_rows": str(count),
                "reported_team_count": str(team_count),
                "structural_qa_status": "NOT_ESTABLISHED_BY_THIS_SANITIZED_MATRIX",
                "next_action": (
                    "Use retained Run 56 evidence; verify parent competition ID and canonical "
                    "fixture/team joins, then reconcile settlement truth and point-in-time inputs."
                ),
            })
        else:
            t = triage[sid]
            package_status = t.get("private_package_row_level_status", "")
            if t.get("evidence_status") != "PRIVATE_PACKAGE_ROW_LEVEL_CONFIRMED_RUN56_GAP_RECONCILED":
                raise ValueError(f"{sid}: gap row lacks confirmed row-level reconciliation")
            if package_status != "CONFIRMED_PRESENT_QA_FILE_OK":
                raise ValueError(f"{sid}: private package row-level QA is not confirmed")
            count = integer(t.get("private_package_match_count", ""), f"{sid} private_package_match_count", blank_ok=False)
            if count is None:
                raise ValueError(f"{sid}: private package match count is missing")
            primary = integer(t.get("primary_window_rows_2025_03_20_to_2026_09_20", ""), f"{sid} primary window")
            recent = integer(t.get("fixture_rows_with_recent_form5_both_teams", ""), f"{sid} recent-form coverage")
            h2h = integer(t.get("fixture_rows_with_h2h_prior_meeting", ""), f"{sid} H2H coverage")
            triage_match_rows += count
            primary_window_rows += primary or 0
            recent_form_rows += recent or 0
            h2h_rows += h2h or 0
            if primary == 0:
                no_primary_window_history.append(sid)
            gate_text = t.get("remaining_data_gate", "").lower()
            qa_status = (
                "STRUCTURAL_QA_PASS_REPORTED; CANONICAL_IDENTITY_AND_SETTLEMENT_STILL_UNVERIFIED"
                if "no missing/duplicate fixture ids" in gate_text
                else "ROW_LEVEL_QA_STATUS_REQUIRES_REVIEW"
            )
            row.update({
                "evidence_layer": "RUN56_GAP_RECONCILED_TO_RETAINED_PRIVATE_PACKAGE",
                "row_count_source": "run56_selected50_manifest_gap_triage.csv:private_package_match_count",
                "reported_match_rows": str(count),
                "primary_window_rows_2025_03_20_to_2026_09_20": "" if primary is None else str(primary),
                "fixtures_with_recent5_both_teams": "" if recent is None else str(recent),
                "fixtures_with_h2h_prior_meeting": "" if h2h is None else str(h2h),
                "structural_qa_status": qa_status,
                "next_action": (
                    "Do not re-ingest solely to repair the Run 56 manifest gap. Complete canonical "
                    "fixture/team joins, settlement and point-in-time QA; assess season-history sufficiency."
                ),
            })
        output.append(row)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / "selected50_archive_evidence_reconciliation.csv"
    json_path = args.out_dir / "selected50_archive_evidence_reconciliation.json"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)

    summary = {
        "status": "PASS_ARCHIVE_EVIDENCE_LAYERS_RECONCILED_RESEARCH_ONLY",
        "selected_group_count": len(manifest),
        "unique_selected_ids": len({r["selected_id"] for r in output}),
        "run56_direct_manifest_matches": len(direct_ids),
        "run56_manifest_gaps_reconciled_to_private_package": len(gap_ids),
        "rows_accounted_for_across_evidence_layers": len(output),
        "run56_direct_match_reported_rows_sum": direct_match_rows,
        "gap_triage_private_package_reported_rows_sum": triage_match_rows,
        "gap_triage_primary_window_rows_sum": primary_window_rows,
        "gap_triage_recent5_both_team_coverage_sum": recent_form_rows,
        "gap_triage_h2h_prior_meeting_rows_sum": h2h_rows,
        "gap_triage_selected_ids_with_zero_primary_window_rows": no_primary_window_history,
        "parent_competition_ids_verified": 0,
        "parent_competition_ids_inferred_from_season_ids": False,
        "canonical_fixture_team_joins_verified": False,
        "official_settlement_truth_verified": False,
        "point_in_time_standings_xg_odds_verified": False,
        "network_calls_made": 0,
        "paid_provider_calls_made": 0,
        "production_eligible": False,
        "betting_eligible": False,
        "limitations": [
            "The 31 direct manifest rows and 19 gap-triage rows come from distinct evidence fields; their row-count sums are not asserted as a deduplicated total archive size.",
            "Run 56 manifest absence is reconciled to retained private-package row-level QA for the 19 listed IDs; it does not prove a provider request failed or was never attempted.",
            "Season-ID/archive evidence does not establish parent competition IDs or canonical Oracle fixture/team identity.",
            "Structural QA statements do not establish official market settlement truth or point-in-time feature provenance.",
            "All outputs are sanitized research-only inventory evidence; production eligibility remains NO."
        ],
        "csv_output": str(csv_path),
    }
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Offline, research-only validator for the selected-50 identity/settlement evidence register.

This tool never calls providers, changes Oracle model outputs, or writes production data.
It deliberately treats public result pages as corroboration rather than a settlement ledger.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "oracle-identity-settlement-evidence-register-2026-10-28.csv"
EXPECTED_FOOTYSTATS_IDS = {
    "8465230", "8465240", "8465202", "8465167",
    "8565639", "8565337", "8565333", "8565677", "8565598", "8565602",
}
EXPECTED_EFL_POSTPONED = {
    ("8565639", "5837184"),
    ("8565337", "5837186"),
    ("8565333", "5837191"),
}
EXPECTED_CANADA_CONFLICT = ("8465167", "1000008675")
FINAL_FS_STATUSES = {"complete"}
FINAL_FOTMOB_STATUSES = {"ft", "finished", "full time", "full_time"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_rows(rows: Iterable[dict[str, str]]) -> dict[str, object]:
    rows = list(rows)
    errors: list[str] = []
    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    require(len(rows) == 10, "EXPECTED_EXACTLY_10_FIXTURE_ROWS")
    fs_ids = [r.get("footystats_fixture_id", "") for r in rows]
    fotmob_ids = [r.get("fotmob_fixture_id", "") for r in rows]
    require(set(fs_ids) == EXPECTED_FOOTYSTATS_IDS, "FOOTYSTATS_FIXTURE_ID_SET_CHANGED")
    require(len(set(fs_ids)) == len(fs_ids), "DUPLICATE_FOOTYSTATS_FIXTURE_ID")
    require(len(set(fotmob_ids)) == len(fotmob_ids), "DUPLICATE_FOTMOB_FIXTURE_ID")

    by_fs = {r.get("footystats_fixture_id", ""): r for r in rows}
    canada = [r for r in rows if r.get("league_name", "").startswith("Canada —")]
    england = [r for r in rows if r.get("league_name", "").startswith("England —")]
    require(len(canada) == 4, "EXPECTED_4_CANADIAN_FIXTURES")
    require(len(england) == 6, "EXPECTED_6_ENGLISH_FIXTURES")

    for r in rows:
        fid = r.get("footystats_fixture_id", "")
        try:
            kickoff = r.get("kickoff_utc", "")
            require(kickoff.endswith("Z"), f"KICKOFF_NOT_EXPLICIT_UTC:{fid}")
            parsed = datetime.fromisoformat(kickoff.replace("Z", "+00:00"))
            require(parsed.utcoffset() is not None and parsed.utcoffset().total_seconds() == 0,
                    f"KICKOFF_OFFSET_NOT_UTC:{fid}")
        except (ValueError, TypeError):
            errors.append(f"KICKOFF_INVALID:{fid}")

        require(r.get("join_precision") == "EXACT_ORDERED_TEAM_NAMES_AND_UTC_KICKOFF",
                f"JOIN_PRECISION_NOT_EXACT:{fid}")
        require(r.get("provider_comp_master_id_semantics") == "UNRESOLVED_NO_PUBLIC_FIELD_CONTRACT",
                f"COMP_MASTER_ID_SEMANTICS_OVERCLAIMED:{fid}")
        require(r.get("settlement_truth_verified") == "NO", f"SETTLEMENT_TRUTH_PROMOTED:{fid}")
        require(r.get("combo_probability_masked") == "YES", f"COMBO_NOT_MASKED:{fid}")
        require(r.get("canonical_bridge_approved") == "NO", f"CANONICAL_BRIDGE_PROMOTED:{fid}")
        require(r.get("production_eligible") == "NO", f"PRODUCTION_ELIGIBILITY_PROMOTED:{fid}")
        require(r.get("betting_eligible") == "NO", f"BETTING_ELIGIBILITY_PROMOTED:{fid}")
        require(r.get("provenance_gate_status") == "INCOMPLETE_NO_IMMUTABLE_CAPTURE_OR_APPROVED_ALLOWLIST",
                f"PROVENANCE_GAP_HIDDEN:{fid}")
        require(not r.get("independent_source_observed_at_utc", "").strip(),
                f"UNSUPPORTED_SOURCE_OBSERVATION_TIME_ADDED:{fid}")
        require(not r.get("source_snapshot_sha256", "").strip(),
                f"UNSUPPORTED_SOURCE_SNAPSHOT_HASH_ADDED:{fid}")
        require(not r.get("approved_source_allowlist_id", "").strip(),
                f"UNAPPROVED_SOURCE_ALLOWLIST_CLAIMED:{fid}")

        for col in ("independent_source_url", "league_official_context_url"):
            url = r.get(col, "").strip()
            require(not url or url.startswith("https://"), f"NON_HTTPS_SOURCE_URL:{fid}:{col}")

        fs_status = r.get("footystats_status", "").strip().lower()
        fm_status = r.get("fotmob_status", "").strip().lower()
        nonfinal = fs_status not in FINAL_FS_STATUSES or fm_status not in FINAL_FOTMOB_STATUSES
        if nonfinal:
            disposition = r.get("settlement_disposition", "")
            if fid == EXPECTED_CANADA_CONFLICT[0]:
                require(disposition.startswith("QUARANTINE"), "CANADA_SOURCE_CONFLICT_NOT_QUARANTINED")
            else:
                require(disposition.startswith("EXCLUDE_NON_FINAL"),
                        f"NONFINAL_FIXTURE_NOT_EXCLUDED:{fid}")
            require(r.get("market_label_eligible") == "NO", f"NONFINAL_MARKET_LABEL_ELIGIBLE:{fid}")

    conflict = by_fs.get(EXPECTED_CANADA_CONFLICT[0])
    require(conflict is not None, "CANADA_CONFLICT_ROW_MISSING")
    if conflict:
        require(conflict.get("fotmob_fixture_id") == EXPECTED_CANADA_CONFLICT[1],
                "CANADA_CONFLICT_FOTMOB_ID_CHANGED")
        require(conflict.get("footystats_status") == "complete"
                and conflict.get("footystats_home_goals") == "3"
                and conflict.get("footystats_away_goals") == "0",
                "CANADA_FOOTYSTATS_SCORE_STATUS_CHANGED")
        require(conflict.get("fotmob_status", "").lower() == "unfinished"
                and conflict.get("fotmob_home_goals") == "0"
                and conflict.get("fotmob_away_goals") == "0",
                "CANADA_FOTMOB_PLACEHOLDER_CHANGED")
        require(conflict.get("settlement_disposition", "").startswith("QUARANTINE"),
                "CANADA_SOURCE_CONFLICT_NOT_QUARANTINED")
        require(conflict.get("market_label_eligible") == "NO",
                "CANADA_CONFLICT_MARKET_LABEL_NOT_BLOCKED")
        require(conflict.get("independent_source_match_id") == "342abe9561194411b419b4a4443c74b5",
                "CANADA_OFFICIAL_MATCH_CENTRE_ID_CHANGED")

    efl_nonfinal = {
        (r.get("footystats_fixture_id", ""), r.get("fotmob_fixture_id", ""))
        for r in rows
        if r.get("league_name", "").startswith("England —")
        and r.get("settlement_disposition") == "EXCLUDE_NON_FINAL_ZERO_ZERO_PLACEHOLDER"
    }
    require(efl_nonfinal == EXPECTED_EFL_POSTPONED, "EFL_POSTPONED_FIXTURE_SET_CHANGED")
    for fs_id, fm_id in EXPECTED_EFL_POSTPONED:
        r = by_fs.get(fs_id)
        if not r:
            errors.append(f"EFL_POSTPONED_ROW_MISSING:{fs_id}")
            continue
        require(r.get("fotmob_fixture_id") == fm_id, f"EFL_POSTPONED_FOTMOB_ID_CHANGED:{fs_id}")
        require(r.get("footystats_status", "").lower() == "suspended",
                f"EFL_POSTPONED_FS_STATUS_CHANGED:{fs_id}")
        require("postponed" in r.get("fotmob_status", "").lower() or "pp" in r.get("fotmob_status", "").lower(),
                f"EFL_POSTPONED_FOTMOB_STATUS_CHANGED:{fs_id}")
        require((r.get("footystats_home_goals"), r.get("footystats_away_goals")) == ("0", "0"),
                f"EFL_NONFINAL_FS_PLACEHOLDER_NOT_ZERO_ZERO:{fs_id}")
        require((r.get("fotmob_home_goals"), r.get("fotmob_away_goals")) == ("0", "0"),
                f"EFL_NONFINAL_FOTMOB_PLACEHOLDER_NOT_ZERO_ZERO:{fs_id}")
        require(r.get("settlement_disposition") == "EXCLUDE_NON_FINAL_ZERO_ZERO_PLACEHOLDER",
                f"EFL_NONFINAL_PLACEHOLDER_NOT_EXCLUDED:{fs_id}")

    if errors:
        raise ValueError("IDENTITY_SETTLEMENT_EVIDENCE_INVALID:" + ";".join(errors))

    score_agreements = sum(
        r.get("footystats_home_goals") == r.get("fotmob_home_goals")
        and r.get("footystats_away_goals") == r.get("fotmob_away_goals")
        and r.get("footystats_status", "").lower() == "complete"
        and r.get("fotmob_status", "").strip().lower() in FINAL_FOTMOB_STATUSES
        for r in rows
    )
    return {
        "schema_version": "oracle-identity-settlement-evidence-register-v1",
        "evidence_rows": len(rows),
        "canada_candidate_rows": len(canada),
        "england_candidate_rows": len(england),
        "exact_ordered_team_utc_kickoff_joins": len(rows),
        "completed_cross_provider_score_agreements": score_agreements,
        "canada_material_conflicts_quarantined": 1,
        "england_postponed_or_suspended_zero_zero_rows_excluded": len(efl_nonfinal),
        "official_settlement_truth_verified_rows": 0,
        "canonical_bridges_approved": 0,
        "combo_probability_unmasked_rows": 0,
        "production_eligible_rows": 0,
        "betting_eligible_rows": 0,
        "provider_api_calls_made": 0,
        "production_writes_made": 0,
        "result": "PASS_RESEARCH_ONLY_RELEASE_NOT_GRANTED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    summary = validate_rows(read_rows(args.input))
    rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

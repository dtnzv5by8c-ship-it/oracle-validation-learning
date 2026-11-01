#!/usr/bin/env python3
"""Research-only audit of raw no_home_away flag coverage in the pinned Run 8 archive.

This script emits aggregate coverage only. It never writes raw provider records.
Missing no_home_away values remain UNKNOWN and are never treated as non-neutral.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zipfile
from collections import defaultdict
from datetime import date
from pathlib import Path, PurePosixPath

from scripts.build_footystats_archive_features import (
    DATE_KEYS, HG_KEYS, AG_KEYS, as_date, first, score, settled,
    map_archive_seasons_to_selected_ids,
)


def parse_no_home_away(value) -> str:
    """Return NEUTRAL, NON_NEUTRAL, UNKNOWN, or INVALID without coercion."""
    if value is None or not str(value).strip():
        return "UNKNOWN"
    token = str(value).strip().lower()
    if token in {"1", "true", "yes"}:
        return "NEUTRAL"
    if token in {"0", "false", "no"}:
        return "NON_NEUTRAL"
    return "INVALID"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _counts():
    return defaultdict(int)


def _add(target, source):
    for key, value in source.items():
        target[key] += value


def _write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def audit_archive(
    archive_path: Path,
    selected_manifest_path: Path,
    primary_start: str = "2025-03-20",
    primary_end: str = "2026-09-20",
):
    start = date.fromisoformat(primary_start)
    end = date.fromisoformat(primary_end)
    if start > end:
        raise ValueError("primary window start must not exceed end")

    with selected_manifest_path.open(encoding="utf-8-sig", newline="") as handle:
        selected_rows = list(csv.DictReader(handle))
    if not selected_rows:
        raise ValueError("selected-50 manifest is empty")

    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        match_files = sorted(
            name for name in names
            if PurePosixPath(name).name == "matches.json"
        )
        manifest_files = [
            name for name in names
            if PurePosixPath(name).name == "ingestion_manifest.json"
        ]
        if not match_files:
            raise ValueError("archive contains no matches.json files")
        if len(manifest_files) != 1:
            raise ValueError(
                f"expected exactly one ingestion_manifest.json, got {len(manifest_files)}"
            )
        ingestion_manifest = json.loads(archive.read(manifest_files[0]))
        season_ids = [PurePosixPath(name).parent.name for name in match_files]
        season_to_selected, mapping_qa, crosswalk = map_archive_seasons_to_selected_ids(
            selected_rows, ingestion_manifest, season_ids
        )

        labels = {
            str(row.get("selected_id") or "").strip(): {
                "country": str(row.get("country") or "").strip(),
                "competition_name": str(row.get("competition_name") or "").strip(),
            }
            for row in selected_rows
        }
        season_counts = {}
        group_counts = defaultdict(_counts)
        parse_error_files = 0
        total_records = 0

        for filename in match_files:
            season_id = PurePosixPath(filename).parent.name
            selected_id = season_to_selected.get(season_id, "UNMAPPED")
            group = group_counts[selected_id]
            counts = season_counts.setdefault((selected_id, season_id), _counts())
            try:
                records = json.loads(archive.read(filename))
                if not isinstance(records, list):
                    raise ValueError("matches.json root is not a list")
            except Exception:
                parse_error_files += 1
                counts["file_parse_errors"] += 1
                group["file_parse_errors"] += 1
                continue

            for record in records:
                if not isinstance(record, dict):
                    continue
                total_records += 1
                counts["records"] += 1
                group["records"] += 1

                kickoff = as_date(first(record, DATE_KEYS))
                in_window = bool(kickoff and start <= kickoff.date() <= end)
                if kickoff:
                    counts["kickoff_parseable_records"] += 1
                    group["kickoff_parseable_records"] += 1
                if in_window:
                    counts["primary_window_records"] += 1
                    group["primary_window_records"] += 1

                state = parse_no_home_away(record.get("no_home_away"))
                counts[f"no_home_away_{state.lower()}_records"] += 1
                group[f"no_home_away_{state.lower()}_records"] += 1
                if in_window:
                    counts[f"primary_window_{state.lower()}_records"] += 1
                    group[f"primary_window_{state.lower()}_records"] += 1

                home_goals, _ = score(record, HG_KEYS, "homeGoals")
                away_goals, _ = score(record, AG_KEYS, "awayGoals")
                has_score = home_goals is not None and away_goals is not None
                is_settled_score = settled(record) and has_score
                if is_settled_score:
                    counts["settled_score_records"] += 1
                    group["settled_score_records"] += 1
                if in_window and is_settled_score:
                    counts["primary_window_settled_score_records"] += 1
                    group["primary_window_settled_score_records"] += 1
                    counts[f"primary_window_{state.lower()}_settled_score_records"] += 1
                    group[f"primary_window_{state.lower()}_settled_score_records"] += 1
                    if state == "NON_NEUTRAL":
                        counts["primary_window_verified_non_neutral_targets"] += 1
                        group["primary_window_verified_non_neutral_targets"] += 1

        season_rows = []
        for (selected_id, season_id), counts in sorted(season_counts.items()):
            label = labels.get(selected_id, {})
            row = {
                "selected_id": selected_id,
                "country": label.get("country", ""),
                "competition_name": label.get("competition_name", ""),
                "provider_season_id": season_id,
            }
            row.update(dict(counts))
            season_rows.append(row)

        group_rows = []
        for selected_id, counts in sorted(group_counts.items()):
            label = labels.get(selected_id, {})
            row = {
                "selected_id": selected_id,
                "country": label.get("country", ""),
                "competition_name": label.get("competition_name", ""),
            }
            row.update(dict(counts))
            group_rows.append(row)

    primary = _counts()
    for row in group_rows:
        _add(primary, row)
    primary_records = primary["primary_window_records"]
    explicit_primary = (
        primary["primary_window_non_neutral_records"]
        + primary["primary_window_neutral_records"]
    )
    summary = {
        "status": (
            "PASS_EXACT_SELECTED50_MAPPING"
            if mapping_qa.get("status") == "PASS_EXACT_SELECTED_MANIFEST_LABEL_MAPPING"
            else "REVIEW_REQUIRED_SELECTED50_MAPPING"
        ),
        "archive_sha256": sha256_file(archive_path),
        "archive_bytes": archive_path.stat().st_size,
        "archive_match_files": len(match_files),
        "archive_total_records": total_records,
        "archive_file_parse_errors": parse_error_files,
        "primary_window": {"start": start.isoformat(), "end_inclusive": end.isoformat()},
        "selected_groups_expected": len({str(r.get("selected_id") or "").strip() for r in selected_rows}),
        "selected_groups_mapped": len(set(season_to_selected.values())),
        "selected_groups_with_records": sum(1 for row in group_rows if row.get("records", 0) > 0),
        "provider_seasons_with_records": len(season_rows),
        "primary_window_records": primary_records,
        "primary_window_settled_score_records": primary["primary_window_settled_score_records"],
        "primary_window_no_home_away": {
            "explicit_non_neutral": primary["primary_window_non_neutral_records"],
            "explicit_neutral": primary["primary_window_neutral_records"],
            "unknown_or_blank": primary["primary_window_unknown_records"],
            "invalid": primary["primary_window_invalid_records"],
            "explicit_coverage_pct": round(100 * explicit_primary / primary_records, 4) if primary_records else None,
            "settled_score_non_neutral": primary["primary_window_non_neutral_settled_score_records"],
            "settled_score_neutral": primary["primary_window_neutral_settled_score_records"],
            "settled_score_unknown_or_blank": primary["primary_window_unknown_settled_score_records"],
            "settled_score_invalid": primary["primary_window_invalid_settled_score_records"],
        },
        "mapping_qa": mapping_qa,
        "venue_flag_policy": {
            "missing_or_blank_is": "UNKNOWN",
            "unknown_is_never_treated_as_non_neutral": True,
            "only_explicit_no_home_away_false_is_venue_eligible": True,
        },
        "source_publication_timestamps_verified": False,
        "official_settlement_truth_verified": False,
        "production_eligible": False,
        "betting_eligible": False,
        "provider_api_credits_used": 0,
        "raw_provider_rows_exported": False,
    }
    return summary, group_rows, season_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--selected-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--primary-start", default="2025-03-20")
    parser.add_argument("--primary-end", default="2026-09-20")
    args = parser.parse_args()

    summary, groups, seasons = audit_archive(
        args.archive, args.selected_manifest, args.primary_start, args.primary_end
    )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    group_fields = [
        "selected_id", "country", "competition_name", "records",
        "kickoff_parseable_records", "primary_window_records",
        "settled_score_records", "primary_window_settled_score_records",
        "primary_window_non_neutral_records", "primary_window_neutral_records",
        "primary_window_unknown_records", "primary_window_invalid_records",
        "primary_window_non_neutral_settled_score_records",
        "primary_window_neutral_settled_score_records",
        "primary_window_unknown_settled_score_records",
        "primary_window_invalid_settled_score_records", "file_parse_errors",
    ]
    season_fields = [
        "selected_id", "country", "competition_name", "provider_season_id",
        "records", "kickoff_parseable_records", "primary_window_records",
        "settled_score_records", "primary_window_settled_score_records",
        "no_home_away_non_neutral_records", "no_home_away_neutral_records",
        "no_home_away_unknown_records", "no_home_away_invalid_records",
        "primary_window_non_neutral_records", "primary_window_neutral_records",
        "primary_window_unknown_records", "primary_window_invalid_records",
        "primary_window_non_neutral_settled_score_records",
        "primary_window_neutral_settled_score_records",
        "primary_window_unknown_settled_score_records",
        "primary_window_invalid_settled_score_records", "file_parse_errors",
    ]
    _write_csv(args.out / "group_coverage.csv", groups, group_fields)
    _write_csv(args.out / "season_coverage.csv", seasons, season_fields)
    (args.out / "archive_sha256.txt").write_text(
        summary["archive_sha256"] + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()

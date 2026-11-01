#!/usr/bin/env python3
"""Inventory FootyStats archive manifest/record metadata relevant to xG provenance.

This is a research-only schema inventory. It emits field names and counts only;
it never emits raw values, credentials, xG features, predictions or eligibility.
Presence of a timestamp/hash-like key is a candidate for investigation, not proof
of point-in-time availability or revision semantics.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import zipfile
from collections import Counter
from pathlib import Path

XG_FIELDS = {
    "team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch",
}
CAPTURE_KEYS = {
    "capture_time_utc", "xg_capture_time_utc", "captured_at", "capture_timestamp",
    "retrieved_at", "retrieved_at_utc", "fetched_at", "fetched_at_utc",
    "request_started_at", "request_started_at_utc", "response_received_at",
    "response_received_at_utc", "ingested_at", "ingested_at_utc",
    "ingestion_time_utc", "snapshot_time_utc", "collected_at", "observed_at",
    "downloaded_at", "download_time_utc",
}
REVISION_KEYS = {
    "revision", "revision_id", "version", "updated_at", "updated_at_utc",
    "provider_updated_at", "modified_at", "effective_at", "last_updated",
    "last_updated_utc",
}
HASH_KEYS = {
    "sha256", "raw_response_sha256", "response_sha256", "payload_sha256",
    "content_sha256", "digest", "checksum",
}
FIXTURE_KEYS = {"match_id", "fixture_id", "game_id"}
SEASON_KEYS = {"season_id"}


def leaf(path: str) -> str:
    return path.rsplit(".", 1)[-1].strip().lower()


def key_paths(value, prefix=""):
    """Yield nested JSON key paths, never values."""
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield path
            if isinstance(child, (dict, list)):
                yield from key_paths(child, path)
    elif isinstance(value, list):
        for child in value:
            if isinstance(child, (dict, list)):
                yield from key_paths(child, prefix)


def record_paths(record):
    return set(key_paths(record))


def has_key(paths, aliases):
    return any(leaf(path) in aliases for path in paths)


def nonblank(value):
    return value is not None and value != ""


def numeric_xg(value):
    if isinstance(value, bool):
        return False
    try:
        number = float(value)
        return math.isfinite(number) and number >= 0
    except (TypeError, ValueError, OverflowError):
        return False


def field_classification(path):
    name = leaf(path)
    if name in XG_FIELDS:
        return "PREMATCH_XG_VALUE_FIELD_NOT_TEMPORALLY_VERIFIED"
    if name in CAPTURE_KEYS:
        return "CAPTURE_TIMESTAMP_CANDIDATE_NOT_SEMANTICALLY_VERIFIED"
    if name in REVISION_KEYS:
        return "REVISION_METADATA_CANDIDATE_NOT_SEMANTICALLY_VERIFIED"
    if name in HASH_KEYS:
        return "HASH_OR_DIGEST_CANDIDATE_NOT_LINKED_TO_RAW_RESPONSE"
    if name in FIXTURE_KEYS:
        return "FIXTURE_ID_CANDIDATE"
    if name in SEASON_KEYS:
        return "SEASON_ID"
    return "OTHER_METADATA"


def audit_archive(archive_path: Path, expected_sha256: str = ""):
    archive_path = Path(archive_path)
    archive_sha = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    if expected_sha256 and archive_sha.lower() != expected_sha256.lower():
        raise ValueError("Pinned archive SHA-256 mismatch")

    with zipfile.ZipFile(archive_path) as archive:
        names = sorted(archive.namelist())
        manifest_names = [name for name in names if name.endswith("ingestion_manifest.json")]
        manifest_name = manifest_names[0] if len(manifest_names) == 1 else "|".join(manifest_names)
        manifest_status = "VALID"
        manifest_error = ""
        manifest_rows = []
        if len(manifest_names) == 0:
            manifest_status = "MISSING"
            manifest_error = "No ingestion_manifest.json found in pinned archive"
        elif len(manifest_names) > 1:
            manifest_status = "AMBIGUOUS"
            manifest_error = f"Expected one ingestion_manifest.json, found {len(manifest_names)}"
        else:
            try:
                manifest = json.loads(archive.read(manifest_name).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                manifest = None
                manifest_status = "INVALID"
                manifest_error = "ingestion_manifest.json is not valid UTF-8 JSON"
            if manifest_status == "VALID" and not isinstance(manifest, list):
                manifest_status = "INVALID"
                manifest_error = "ingestion_manifest.json does not contain a JSON list"
            if manifest_status == "VALID":
                manifest_rows = [row for row in manifest if isinstance(row, dict)]
                if len(manifest_rows) != len(manifest):
                    manifest_rows = []
                    manifest_status = "INVALID"
                    manifest_error = "ingestion_manifest.json contains non-object rows"

        match_files = [name for name in names if name.endswith("/matches.json")]
        if not match_files:
            raise ValueError("No season matches.json files found")
        match_records = []
        for name in match_files:
            data = json.loads(archive.read(name).decode("utf-8"))
            if not isinstance(data, list):
                raise ValueError(f"{name} must contain a JSON list")
            for index, record in enumerate(data):
                if isinstance(record, dict):
                    match_records.append((name, index, record))

    manifest_paths = [record_paths(row) for row in manifest_rows]
    match_paths = [record_paths(record) for _, _, record in match_records]

    manifest_counts = Counter()
    for paths in manifest_paths:
        manifest_counts.update(paths)
    match_counts = Counter()
    for paths in match_paths:
        match_counts.update(paths)

    manifest_fixture_rows = sum(has_key(paths, FIXTURE_KEYS) for paths in manifest_paths)
    manifest_season_rows = sum(has_key(paths, SEASON_KEYS) for paths in manifest_paths)
    if manifest_fixture_rows and manifest_season_rows:
        manifest_grain = "FIXTURE_AND_SEASON_FIELDS_PRESENT"
    elif manifest_fixture_rows:
        manifest_grain = "FIXTURE_LEVEL_CANDIDATE"
    elif manifest_season_rows:
        manifest_grain = "SEASON_LEVEL"
    else:
        manifest_grain = "UNKNOWN"

    manifest_capture_rows = sum(has_key(paths, CAPTURE_KEYS) for paths in manifest_paths)
    manifest_revision_rows = sum(has_key(paths, REVISION_KEYS) for paths in manifest_paths)
    manifest_hash_rows = sum(has_key(paths, HASH_KEYS) for paths in manifest_paths)
    manifest_fixture_capture_hash_rows = sum(
        has_key(paths, FIXTURE_KEYS) and has_key(paths, CAPTURE_KEYS) and has_key(paths, HASH_KEYS)
        for paths in manifest_paths
    )

    xg_rows = []
    xg_numeric_counts = Counter()
    xg_with_capture = xg_with_revision = xg_with_hash = xg_with_capture_hash = 0
    for (_, _, record), paths in zip(match_records, match_paths):
        present = {key for key in XG_FIELDS if nonblank(record.get(key))}
        if present:
            xg_rows.append(record)
            for key in present:
                xg_numeric_counts[key] += int(numeric_xg(record.get(key)))
        if present and has_key(paths, CAPTURE_KEYS):
            xg_with_capture += 1
        if present and has_key(paths, REVISION_KEYS):
            xg_with_revision += 1
        if present and has_key(paths, HASH_KEYS):
            xg_with_hash += 1
        if present and has_key(paths, CAPTURE_KEYS) and has_key(paths, HASH_KEYS):
            xg_with_capture_hash += 1

    inventory = []
    for scope, counts, denominator in (
        ("INGESTION_MANIFEST_JSON", manifest_counts, len(manifest_rows)),
        ("MATCH_RECORDS_JSON", match_counts, len(match_records)),
    ):
        for path, count in sorted(counts.items()):
            inventory.append({
                "source_scope": scope,
                "field_path": path,
                "records_with_field": count,
                "total_records": denominator,
                "presence_pct": round(100 * count / denominator, 4) if denominator else 0,
                "classification": field_classification(path),
            })

    summary = {
        "status": "PASS_RESEARCH_ONLY_MANIFEST_SCHEMA_INVENTORY" if manifest_status == "VALID" else f"BLOCKED_MANIFEST_{manifest_status}",
        "archive_sha256": archive_sha,
        "manifest_path": manifest_name,
        "manifest_file_count": len(manifest_names),
        "manifest_status": manifest_status,
        "manifest_error": manifest_error,
        "manifest_rows": len(manifest_rows),
        "manifest_grain_candidate": manifest_grain,
        "manifest_rows_with_fixture_id_candidate": manifest_fixture_rows,
        "manifest_rows_with_season_id": manifest_season_rows,
        "manifest_rows_with_capture_timestamp_candidate": manifest_capture_rows,
        "manifest_rows_with_revision_metadata_candidate": manifest_revision_rows,
        "manifest_rows_with_hash_metadata_candidate": manifest_hash_rows,
        "manifest_rows_with_fixture_capture_and_hash_candidates": manifest_fixture_capture_hash_rows,
        "match_files": len(match_files),
        "match_records": len(match_records),
        "match_records_with_any_prematch_xg_field": len(xg_rows),
        "numeric_prematch_xg_field_counts": dict(sorted(xg_numeric_counts.items())),
        "xg_match_records_with_capture_timestamp_candidate": xg_with_capture,
        "xg_match_records_with_revision_metadata_candidate": xg_with_revision,
        "xg_match_records_with_hash_metadata_candidate": xg_with_hash,
        "xg_match_records_with_capture_and_hash_candidates": xg_with_capture_hash,
        "xg_point_in_time_provenance_verified": False,
        "xg_quarantine_required": True,
        "provider_api_calls": 0,
        "production_eligible": False,
        "betting_eligible": False,
        "interpretation": (
            "This inventory reports metadata field-name presence and counts only. "
            "It does not validate timestamp values, provider semantics, fixture-level "
            "linkage, raw-response integrity, xG calculation time or revision history. "
            "A JSON ingestion manifest may be season-level and is not automatically an "
            "xG capture manifest. Keep all pre-match-labelled xG quarantined."
        ),
    }
    return summary, inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--expected-archive-sha256", default="")
    args = parser.parse_args()

    summary, inventory = audit_archive(args.archive, args.expected_archive_sha256)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "oracle_selected50_xg_manifest_field_inventory.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_scope", "field_path", "records_with_field", "total_records",
                "presence_pct", "classification",
            ],
        )
        writer.writeheader()
        writer.writerows(inventory)
    (args.out_dir / "oracle_selected50_xg_manifest_provenance_qa.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Research-only fail-closed validation for result snapshot provenance.

Hashes establish byte identity, not provider authenticity. The expected hashes
must be pinned independently of the snapshot package being evaluated.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc(value):
    if not isinstance(value, str) or not value:
        raise ValueError("MISSING_OR_INVALID_UTC_TIMESTAMP")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("MISSING_OR_INVALID_UTC_TIMESTAMP") from exc
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("TIMEZONE_REQUIRED")
    return dt.astimezone(timezone.utc)


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_snapshot(snapshot_path, manifest_path, allowlist_path,
                      expected_snapshot_sha256, expected_manifest_sha256,
                      expected_allowlist_sha256, now_utc=None):
    for label, digest in (("SNAPSHOT", expected_snapshot_sha256),
                          ("MANIFEST", expected_manifest_sha256),
                          ("ALLOWLIST", expected_allowlist_sha256)):
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest.lower()):
            raise ValueError(label + "_EXPECTED_SHA256_REQUIRED")
    actual_snapshot = sha256_file(snapshot_path)
    actual_manifest = sha256_file(manifest_path)
    actual_allowlist = sha256_file(allowlist_path)
    if actual_snapshot.lower() != expected_snapshot_sha256.lower():
        raise ValueError("RESULT_SNAPSHOT_HASH_MISMATCH")
    if actual_manifest.lower() != expected_manifest_sha256.lower():
        raise ValueError("MANIFEST_HASH_MISMATCH")
    if actual_allowlist.lower() != expected_allowlist_sha256.lower():
        raise ValueError("ALLOWLIST_HASH_MISMATCH")

    manifest = load_json(manifest_path)
    allowlist = load_json(allowlist_path)
    if manifest.get("schema_version") != "oracle-result-acquisition-manifest-v1":
        raise ValueError("UNSUPPORTED_MANIFEST_SCHEMA")
    if manifest.get("snapshot_sha256") != actual_snapshot:
        raise ValueError("MANIFEST_SNAPSHOT_HASH_MISMATCH")
    for key in ("snapshot_id", "acquired_at_utc", "acquisition_run_id", "acquisition_method", "source_id", "source_uri"):
        if not manifest.get(key):
            raise ValueError("MANIFEST_MISSING_" + key.upper())
    acquired = utc(manifest["acquired_at_utc"])
    now = utc(now_utc) if now_utc else datetime.now(timezone.utc)
    if acquired > now:
        raise ValueError("ACQUISITION_TIMESTAMP_IN_FUTURE")
    if not isinstance(allowlist.get("approved_sources"), list):
        raise ValueError("ALLOWLIST_APPROVED_SOURCES_REQUIRED")
    source_ids = {str(x.get("source_id")) for x in allowlist["approved_sources"]
                  if isinstance(x, dict) and x.get("source_id") and x.get("status") == "approved"}
    source_id = str(manifest["source_id"])
    if source_id not in source_ids:
        raise ValueError("SOURCE_NOT_IN_INDEPENDENT_ALLOWLIST")

    rows = load_jsonl(snapshot_path)
    accepted, rejected = 0, []
    required = ("fixture_id", "competition_id", "scheduled_kickoff_utc",
                "home_team_id", "away_team_id", "home_score", "away_score",
                "match_status", "result_observed_at_utc", "result_source")
    for i, row in enumerate(rows, start=1):
        missing = [k for k in required if row.get(k) in (None, "")]
        if missing:
            rejected.append({"row": i, "reason": "MISSING_FIELDS:" + ",".join(missing)})
            continue
        if str(row["result_source"]) != source_id:
            rejected.append({"row": i, "reason": "ROW_SOURCE_DIFFERS_FROM_MANIFEST"})
            continue
        try:
            kickoff = utc(row["scheduled_kickoff_utc"])
            observed = utc(row["result_observed_at_utc"])
        except ValueError as exc:
            rejected.append({"row": i, "reason": str(exc)})
            continue
        if observed < kickoff:
            rejected.append({"row": i, "reason": "RESULT_OBSERVED_BEFORE_KICKOFF"})
            continue
        if str(row["match_status"]).upper() not in {"FT", "AET", "PEN", "FINISHED"}:
            rejected.append({"row": i, "reason": "MATCH_NOT_FINAL"})
            continue
        try:
            hs, aws = int(row["home_score"]), int(row["away_score"])
            if hs < 0 or aws < 0:
                raise ValueError()
        except (TypeError, ValueError):
            rejected.append({"row": i, "reason": "INVALID_FINAL_SCORE"})
            continue
        accepted += 1
    return {
        "status": "RESEARCH_ONLY_SOURCE_PROVENANCE_VALIDATION",
        "snapshot_sha256": actual_snapshot,
        "manifest_sha256": actual_manifest,
        "allowlist_sha256": actual_allowlist,
        "source_id": source_id,
        "snapshot_id": manifest["snapshot_id"],
        "rows_total": len(rows),
        "rows_structurally_accepted": accepted,
        "rows_rejected": len(rejected),
        "rejected": rejected,
        "provider_authenticity_independently_proven": False,
        "production_eligibility": "NOT_GRANTED",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--allowlist", required=True)
    p.add_argument("--expected-snapshot-sha256", required=True)
    p.add_argument("--expected-manifest-sha256", required=True)
    p.add_argument("--expected-allowlist-sha256", required=True)
    p.add_argument("--now-utc")
    args = p.parse_args()
    result = validate_snapshot(args.snapshot, args.manifest, args.allowlist,
        args.expected_snapshot_sha256, args.expected_manifest_sha256,
        args.expected_allowlist_sha256, args.now_utc)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["rows_rejected"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

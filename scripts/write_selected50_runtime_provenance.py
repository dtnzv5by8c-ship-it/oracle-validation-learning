#!/usr/bin/env python3
"""Create a fail-closed provenance manifest for the exact archive used by the research runtime."""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


PASS_OVERLAY_STATUSES = {"PASS_RESEARCH_ONLY_STAGED", "PARTIAL_RESEARCH_ONLY_UNSUPPORTED_LEAGUES"}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_provenance(*, snapshot_path, overlay_qa_path, source_archive_path,
                     selected_archive_path, runtime_report_path,
                     include_current_snapshot, snapshot_run_id, runtime_run_id,
                     runtime_run_number, runtime_run_attempt, runtime_sha,
                     runtime_ref, archive_release_tag, runtime_archive_env,
                     selected_archive_sha256_before_runtime,
                     snapshot_artifact_metadata_path=None):
    selected_path = Path(selected_archive_path)
    runtime_env_path = Path(runtime_archive_env)
    if selected_path.resolve() != runtime_env_path.resolve():
        raise SystemExit("FAIL: ORACLE_ARCHIVE path does not resolve to the selected runtime input archive")

    selected_sha = sha256_file(selected_path)
    before_sha = str(selected_archive_sha256_before_runtime or "").strip().lower()
    if len(before_sha) != 64 or any(ch not in "0123456789abcdef" for ch in before_sha):
        raise SystemExit("FAIL: pre-runtime selected archive SHA-256 is missing or invalid")
    if selected_sha != before_sha:
        raise SystemExit("FAIL: selected runtime input archive changed between pre-runtime fingerprint and provenance capture")
    provenance = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_run_id": str(runtime_run_id),
        "runtime_run_number": str(runtime_run_number),
        "runtime_run_attempt": str(runtime_run_attempt),
        "runtime_commit_sha": str(runtime_sha),
        "runtime_ref": str(runtime_ref),
        "runtime_archive_env": str(runtime_archive_env),
        "selected_runtime_input_archive": selected_path.name,
        "selected_runtime_input_archive_sha256": selected_sha,
        "selected_runtime_input_archive_sha256_before_runtime": before_sha,
        "runtime_report_file": Path(runtime_report_path).name,
        "runtime_report_sha256": sha256_file(runtime_report_path),
        "private_archive_release_tag": str(archive_release_tag),
        "snapshot_run_id": str(snapshot_run_id),
        "snapshot_artifact_id": None,
        "snapshot_artifact_name": "oracle-selected50-current-fixture-snapshot",
        "snapshot_artifact_digest": None,
        "snapshot_artifact_metadata_sha256": None,
        "snapshot_artifact_size_bytes": None,
        "snapshot_artifact_created_at": None,
        "snapshot_artifact_expires_at": None,
        "snapshot_artifact_workflow_run_id": None,
        "snapshot_artifact_head_branch": None,
        "snapshot_artifact_head_sha": None,
        "snapshot_consumption_verified": False,
        "snapshot_consumption_status": "NOT_CONSUMED_OVERLAY_DISABLED",
        "snapshot_file_sha256": None,
        "snapshot_retrieved_utc": None,
        "source_archive_sha256": sha256_file(source_archive_path),
        "overlay_qa_sha256": None,
        "overlay_archive_sha256": None,
        "selected_input_matches_overlay": False,
        "production_eligible": False,
        "betting_eligible": False,
        "model_logic_changed": False,
    }

    if not include_current_snapshot:
        return provenance

    if not snapshot_path or not Path(snapshot_path).is_file():
        raise SystemExit("FAIL: snapshot overlay enabled but snapshot artifact file is missing")
    if not overlay_qa_path or not Path(overlay_qa_path).is_file():
        raise SystemExit("FAIL: snapshot overlay enabled but overlay QA file is missing")

    if not snapshot_artifact_metadata_path or not Path(snapshot_artifact_metadata_path).is_file():
        raise SystemExit("FAIL: snapshot overlay enabled but exact GitHub artifact metadata is missing")
    metadata_path = Path(snapshot_artifact_metadata_path)
    metadata_sha = sha256_file(metadata_path)
    metadata = load_json(metadata_path)
    artifact_name = str(metadata.get("artifact_name") or "")
    artifact_id = str(metadata.get("artifact_id") or "")
    artifact_digest = str(metadata.get("artifact_digest") or "")
    artifact_run_id = str(metadata.get("artifact_workflow_run_id") or "")
    if artifact_name != "oracle-selected50-current-fixture-snapshot":
        raise SystemExit("FAIL: snapshot artifact metadata name does not match the expected artifact")
    if not artifact_id or not artifact_digest.startswith("sha256:"):
        raise SystemExit("FAIL: snapshot artifact ID or GitHub SHA-256 digest is missing")
    if artifact_run_id != str(snapshot_run_id):
        raise SystemExit("FAIL: snapshot artifact metadata run ID does not match the requested snapshot run")
    if metadata.get("artifact_expired") is not False:
        raise SystemExit("FAIL: snapshot artifact metadata is expired or expiry status is unknown")

    snapshot_sha = sha256_file(snapshot_path)
    overlay_qa_sha = sha256_file(overlay_qa_path)
    snapshot = load_json(snapshot_path)
    overlay_qa = load_json(overlay_qa_path)
    source_sha = sha256_file(source_archive_path)
    overlay_sha = str(overlay_qa.get("overlay_archive_sha256") or "")
    qa_snapshot_sha = str(overlay_qa.get("snapshot_file_sha256") or "")
    qa_source_sha = str(overlay_qa.get("source_archive_sha256") or "")
    overlay_status = str(overlay_qa.get("status") or "")

    if overlay_status not in PASS_OVERLAY_STATUSES:
        raise SystemExit(f"FAIL: overlay QA status is not an accepted research staging status: {overlay_status or 'MISSING'}")
    if not qa_snapshot_sha or qa_snapshot_sha != snapshot_sha:
        raise SystemExit("FAIL: snapshot SHA-256 does not match overlay QA")
    if not qa_source_sha or qa_source_sha != source_sha:
        raise SystemExit("FAIL: source archive SHA-256 does not match overlay QA")
    if not overlay_sha:
        raise SystemExit("FAIL: overlay QA does not record overlay_archive_sha256")
    if selected_sha != overlay_sha:
        raise SystemExit("FAIL: selected runtime input archive SHA-256 does not match overlay archive SHA-256")
    if str(snapshot.get("retrieved_utc") or "") != str(overlay_qa.get("snapshot_retrieved_utc") or ""):
        raise SystemExit("FAIL: snapshot retrieval timestamp does not match overlay QA")

    provenance.update({
        "snapshot_consumption_verified": True,
        "snapshot_consumption_status": "PASS_SNAPSHOT_TO_RUNTIME_INPUT_HASH_VERIFIED",
        "snapshot_file_sha256": snapshot_sha,
        "snapshot_artifact_id": artifact_id,
        "snapshot_artifact_name": artifact_name,
        "snapshot_artifact_digest": artifact_digest,
        "snapshot_artifact_metadata_sha256": metadata_sha,
        "snapshot_artifact_size_bytes": metadata.get("artifact_size_bytes"),
        "snapshot_artifact_created_at": metadata.get("artifact_created_at"),
        "snapshot_artifact_expires_at": metadata.get("artifact_expires_at"),
        "snapshot_artifact_workflow_run_id": artifact_run_id,
        "snapshot_artifact_head_branch": metadata.get("artifact_head_branch"),
        "snapshot_artifact_head_sha": metadata.get("artifact_head_sha"),
        "snapshot_retrieved_utc": snapshot.get("retrieved_utc"),
        "overlay_qa_sha256": overlay_qa_sha,
        "overlay_archive_sha256": overlay_sha,
        "selected_input_matches_overlay": True,
        "overlay_status": overlay_status,
        "snapshot_fixture_rows": len(snapshot.get("fixture_rows", [])),
        "overlay_candidate_rows_added": overlay_qa.get("candidate_rows_added"),
        "overlay_refreshed_present_exact_fixture_ids": overlay_qa.get("refreshed_present_exact_fixture_ids"),
        "overlay_quarantined_or_invalid_rows": overlay_qa.get("quarantined_or_invalid_rows"),
    })
    return provenance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--overlay-qa", required=True, type=Path)
    parser.add_argument("--source-archive", required=True, type=Path)
    parser.add_argument("--selected-archive", required=True, type=Path)
    parser.add_argument("--runtime-report", required=True, type=Path)
    parser.add_argument("--include-current-snapshot", action="store_true")
    parser.add_argument("--snapshot-run-id", required=True)
    parser.add_argument("--runtime-run-id", required=True)
    parser.add_argument("--runtime-run-number", required=True)
    parser.add_argument("--runtime-run-attempt", required=True)
    parser.add_argument("--runtime-sha", required=True)
    parser.add_argument("--runtime-ref", required=True)
    parser.add_argument("--archive-release-tag", required=True)
    parser.add_argument("--runtime-archive-env", required=True)
    parser.add_argument("--selected-archive-sha256-before-runtime", required=True)
    parser.add_argument("--snapshot-artifact-metadata", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    result = build_provenance(
        snapshot_path=args.snapshot,
        overlay_qa_path=args.overlay_qa,
        source_archive_path=args.source_archive,
        selected_archive_path=args.selected_archive,
        runtime_report_path=args.runtime_report,
        include_current_snapshot=args.include_current_snapshot,
        snapshot_run_id=args.snapshot_run_id,
        runtime_run_id=args.runtime_run_id,
        runtime_run_number=args.runtime_run_number,
        runtime_run_attempt=args.runtime_run_attempt,
        runtime_sha=args.runtime_sha,
        runtime_ref=args.runtime_ref,
        archive_release_tag=args.archive_release_tag,
        runtime_archive_env=args.runtime_archive_env,
        selected_archive_sha256_before_runtime=args.selected_archive_sha256_before_runtime,
        snapshot_artifact_metadata_path=args.snapshot_artifact_metadata,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

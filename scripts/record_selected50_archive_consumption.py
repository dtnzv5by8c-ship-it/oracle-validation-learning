#!/usr/bin/env python3
"""Record the exact archive file handle opened by the isolated research runtime."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def sha256_open_file_handle(handle):
    """Hash bytes from the already-open ZIP handle without leaving its cursor changed."""
    if not hasattr(handle, "seek") or not hasattr(handle, "read"):
        raise SystemExit("FAIL: opened runtime archive handle is not seekable/readable")
    position = handle.tell()
    digest = hashlib.sha256()
    try:
        handle.seek(0)
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    finally:
        handle.seek(position)
    return digest.hexdigest()


def write_archive_consumption_receipt(archive_path, opened_archive, output_path, runtime_commit_sha=None):
    """Write a receipt from the same ZipFile object the runtime is reading."""
    path = Path(archive_path)
    opened_name = getattr(opened_archive, "filename", None)
    if opened_name is None or Path(str(opened_name)).resolve() != path.resolve():
        raise SystemExit("FAIL: opened ZIP handle path does not match runtime archive path")
    handle = getattr(opened_archive, "fp", None)
    if handle is None:
        raise SystemExit("FAIL: runtime ZIP handle is not open")
    archive_sha = sha256_open_file_handle(handle)
    try:
        archive_size = os.fstat(handle.fileno()).st_size
    except (AttributeError, OSError, ValueError):
        archive_size = path.stat().st_size
    receipt = {
        "schema_version": 1,
        "archive_open_confirmed": True,
        "consumed_archive_path": str(path),
        "consumed_archive_resolved_path": str(path.resolve()),
        "consumed_archive_sha256_at_open": archive_sha,
        "consumed_archive_size_bytes": archive_size,
        "archive_member_count": len(opened_archive.namelist()),
        "runtime_commit_sha": str(runtime_commit_sha if runtime_commit_sha is not None else os.environ.get("GITHUB_SHA", "")),
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
    }
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt

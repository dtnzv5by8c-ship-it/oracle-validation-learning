#!/usr/bin/env python3
"""Fetch the latest successful Oracle completion-run fixture schedule artifact."""
import io, json, os, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path
import requests

API = "https://api.github.com"
REPO = os.getenv("GITHUB_REPOSITORY", "dtnzv5by8c-ship-it/oracle-validation-learning")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUT = Path("oracle_upcoming_fixtures.csv")
MANIFEST = Path("artifacts/opta_power_rankings/fixture_source_manifest.json")

def main():
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN_missing")
    headers = {"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    r = requests.get(f"{API}/repos/{REPO}/actions/runs?per_page=30", headers=headers, timeout=30)
    r.raise_for_status()
    runs = r.json().get("workflow_runs", [])
    candidates = [x for x in runs if x.get("name") == "Oracle Completion Run"
                  and x.get("status") == "completed" and x.get("conclusion") == "success"
                  and x.get("head_branch") == "main"]
    if not candidates:
        raise RuntimeError("No_successful_Oracle_Completion_Run_found")
    run = max(candidates, key=lambda x: x.get("created_at", ""))
    ar = requests.get(f"{API}/repos/{REPO}/actions/runs/{run['id']}/artifacts",
                      headers=headers, timeout=30)
    ar.raise_for_status()
    artifacts = ar.json().get("artifacts", [])
    artifact = next((x for x in artifacts if x.get("name") == "oracle-fixture-level-predictions" and not x.get("expired")), None)
    if not artifact:
        raise RuntimeError("Latest_successful_completion_run_has_no_fixture_predictions_artifact")
    download = requests.get(artifact["archive_download_url"], headers=headers, timeout=90)
    download.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(download.content)) as archive:
        members = [n for n in archive.namelist() if n.endswith("oracle/data/fixtures/oracle_upcoming_fixtures.csv")]
        if len(members) != 1:
            raise RuntimeError("Expected_exactly_one_fixture_schedule_in_artifact; found=" + str(len(members)))
        data = archive.read(members[0])
    if not data.startswith(b"league_code,date,home_team,away_team"):
        raise RuntimeError("Fixture_schedule_header_unexpected")
    OUT.write_bytes(data)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "status": "PASS",
        "source_repository": REPO,
        "source_workflow": run.get("name"),
        "source_run_id": run.get("id"),
        "source_run_url": run.get("html_url"),
        "source_run_created_at": run.get("created_at"),
        "source_head_sha": run.get("head_sha"),
        "source_artifact_id": artifact.get("id"),
        "source_artifact_name": artifact.get("name"),
        "fixture_rows": max(0, len(data.splitlines()) - 1),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "fixture_schedule_sha256": __import__("hashlib").sha256(data).hexdigest(),
        "policy": "Use only the fixture schedule from the latest successful governed completion run; fail closed rather than silently falling back to a stale schedule."
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(json.dumps({"status": "FAILED", "error_class": type(exc).__name__, "message": str(exc)[:240]}))
        sys.exit(1)

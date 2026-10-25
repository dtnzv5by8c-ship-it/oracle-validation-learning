#!/usr/bin/env python3
"""Regression test for Selected-50 archive evidence-layer reconciliation."""
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_selected50_archive_evidence_reconciliation.py"


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        subprocess.run(
            [sys.executable, str(SCRIPT), "--out-dir", str(out)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        matrix = read_csv(out / "selected50_archive_evidence_reconciliation.csv")
        summary = json.loads((out / "selected50_archive_evidence_reconciliation.json").read_text(encoding="utf-8"))
        assert len(matrix) == 50
        assert len({r["selected_id"] for r in matrix}) == 50
        assert {r["evidence_layer"] for r in matrix} == {
            "RUN56_EXACT_SEASON_ID_MANIFEST_MATCH",
            "RUN56_GAP_RECONCILED_TO_RETAINED_PRIVATE_PACKAGE",
        }
        assert sum(r["evidence_layer"] == "RUN56_EXACT_SEASON_ID_MANIFEST_MATCH" for r in matrix) == summary["run56_direct_manifest_matches"]
        assert sum(r["evidence_layer"] == "RUN56_GAP_RECONCILED_TO_RETAINED_PRIVATE_PACKAGE" for r in matrix) == summary["run56_manifest_gaps_reconciled_to_private_package"]
        assert summary["rows_accounted_for_across_evidence_layers"] == 50
        assert summary["parent_competition_ids_verified"] == 0
        assert summary["parent_competition_ids_inferred_from_season_ids"] is False
        assert summary["canonical_fixture_team_joins_verified"] is False
        assert summary["official_settlement_truth_verified"] is False
        assert summary["network_calls_made"] == summary["paid_provider_calls_made"] == 0
        assert summary["production_eligible"] is False and summary["betting_eligible"] is False
        assert all(r["production_eligible"] == "NO" for r in matrix)
        assert all(r["provider_parent_competition_id_status"] == "UNRESOLVED" for r in matrix)
        assert all(r["official_settlement_truth_status"] == "NOT_VERIFIED" for r in matrix)
        print("PASS: all 50 selected IDs are accounted for across direct manifest and gap-triage evidence; identity/settlement remain blocked; no network calls.")


if __name__ == "__main__":
    main()

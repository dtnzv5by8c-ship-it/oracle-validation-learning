import csv
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_selected50_row_level_history_provenance import audit, fixture_id, finished, load_archive, main, match_score, team_ids  # noqa: E402


def archive_row(fid, kickoff, home="H", away="X", status="complete",
                hg=1, ag=0, source_row=0, competition="L", season="S", raw=None):
    raw = raw if raw is not None else {
        "team_a_shots": 10, "team_b_shots": 7,
        "team_a_shotsOnTarget": 4, "team_b_shotsOnTarget": 2,
    }
    return {
        "competition_id": competition, "season_id": season, "country": "Test",
        "league": "League", "source_file": f"seasons/{season}/matches.json",
        "source_row": source_row, "fixture_id": fid, "kickoff_unix": kickoff,
        "home_id": home, "away_id": away,
        "home_name": "Home Team" if home == "H" else "Other Home",
        "away_name": "Away Team" if away == "A" else "Other Away",
        "home_goals": hg, "away_goals": ag,
        "finished": status.lower() in {"complete", "completed", "finished", "full time", "full-time", "ft", "ended", "played", "after extra time", "aet", "penalties"} and hg is not None and ag is not None,
        "status_raw": status, "raw": raw, "raw_record_sha256": f"hash-{source_row}",
    }


def runtime_row(**overrides):
    row = {
        "fixture_id": "TARGET", "selected_id": "L", "country": "Test",
        "league": "League", "date_utc": "1970-01-01T00:16:40Z",
        "home_team": "Home Team", "away_team": "Away Team",
        "home_team_provider_id": "H", "away_team_provider_id": "A",
        "home_recent5_n": "2", "away_recent5_n": "5",
        "feature_support_status": "BLOCKED_MISSING_REQUIRED_FEATURES",
        "missing_required_features": "home_gf5",
    }
    row.update(overrides)
    return row


class RowLevelHistoryProvenanceTests(unittest.TestCase):
    def test_reconstructs_oriented_history_and_strict_cutoff(self):
        rows = [
            archive_row("H1", 100, home="H", away="X", source_row=1),
            archive_row("H2", 200, home="H", away="Y", source_row=2),
            archive_row("H3", 300, home="Z", away="H", source_row=3),
            archive_row("H4", 1000, home="H", away="Q", source_row=4),
            archive_row("H5", 400, home="H", away="R", status="incomplete", source_row=5),
        ]
        sides, details, qa = audit([runtime_row(home_recent5_n="3")], rows, {"L"})
        side = sides[0]
        self.assertEqual(side["reconstructed_history_count"], 3)
        self.assertEqual(side["runtime_history_count"], "3")
        self.assertEqual(side["history_count_reconciles"], "YES")
        self.assertEqual(side["included_history_match_ids"], "H1;H2;H3")
        decisions = {d["historical_fixture_id"]: d["history_decision"] for d in details}
        self.assertEqual(decisions["H3"], "INCLUDED_IN_RUNTIME_HISTORY")
        self.assertEqual(decisions["H4"], "AFTER_CUTOFF")
        self.assertEqual(decisions["H5"], "REQUIRED_FEATURE_MISSING")
        self.assertTrue(qa["all_side_history_counts_reconcile"])

    def test_exact_duplicate_fixture_id_extra_row_is_excluded(self):
        rows = [
            archive_row("DUP", 100, source_row=1),
            archive_row("DUP", 100, source_row=2),
        ]
        sides, details, _ = audit([runtime_row(home_recent5_n="1")], rows, {"L"})
        self.assertEqual(sides[0]["reconstructed_history_count"], 1)
        duplicate = [d for d in details if d["source_record_index"] == 2][0]
        self.assertEqual(duplicate["history_decision"], "DUPLICATE_RECORD")
        self.assertEqual(duplicate["exclusion_detail"], "EXACT_DUPLICATE_FIXTURE_ID_EXTRA_ROW")

    def test_duplicate_completed_signature_quarantines_all_matching_rows(self):
        rows = [
            archive_row("SIG1", 100, home="H", away="X", source_row=1),
            archive_row("SIG2", 100, home="H", away="X", source_row=2),
        ]
        sides, details, qa = audit([runtime_row(home_recent5_n="0")], rows, {"L"})
        self.assertEqual(sides[0]["reconstructed_history_count"], 0)
        self.assertTrue(all(d["history_decision"] == "DUPLICATE_RECORD" for d in details))
        self.assertEqual(qa["history_decision_counts"]["DUPLICATE_RECORD"], 2)

    def test_runtime_count_mismatch_is_review_required(self):
        rows = [archive_row("ONE", 100, source_row=1)]
        sides, _, qa = audit([runtime_row(home_recent5_n="4")], rows, {"L"})
        self.assertEqual(sides[0]["audit_status"], "REVIEW_REQUIRED_COUNT_MISMATCH")
        self.assertFalse(qa["all_side_history_counts_reconcile"])
        self.assertEqual(len(qa["runtime_archive_history_count_mismatches"]), 1)

    def test_exact_name_diagnostic_identifies_provider_team_id_drift_without_imputing_history(self):
        rows = [archive_row("OLD-ID", 100, home="OLD-H", away="X", source_row=1)]
        rows[0]["home_name"] = "Home Team"
        sides, _, qa = audit([runtime_row(home_recent5_n="1")], rows, {"L"})
        side = sides[0]
        self.assertEqual(side["considered_source_rows"], 0)
        self.assertEqual(side["exact_name_candidate_rows"], 1)
        self.assertEqual(side["exact_name_completed_prior_matches"], 1)
        self.assertEqual(side["root_cause"], "PROVIDER_TEAM_ID_DRIFT_EXACT_NAME_CANDIDATES_FOUND")
        self.assertEqual(side["reconstructed_history_count"], 0)
        self.assertEqual(side["features_imputed"], 0)
        self.assertFalse(qa["all_side_history_counts_reconcile"])

    def test_feature_completeness_does_not_claim_five_match_sample(self):
        rows = [archive_row(f"M{i}", 100 + i, source_row=i) for i in range(1, 4)]
        sides, _, _ = audit([runtime_row(home_recent5_n="3")], rows, {"L"})
        for feature in ("home_gf5", "home_ga5", "home_shots5", "home_sot5"):
            self.assertEqual(sides[0][feature], "NO_FIVE_MATCH_SAMPLE")

    def test_source_aliases_match_archive_feature_builder(self):
        source = {
            "match_id": "ALIAS-1",
            "team_a_id": "H",
            "team_b_id": "A",
            "homeGoalsCount": "2",
            "awayGoalsCount": "1",
            "match_status": "AET",
        }
        self.assertEqual(fixture_id(source), "ALIAS-1")
        self.assertEqual(team_ids(source), ("H", "A"))
        self.assertEqual(match_score(source), (2.0, 1.0))
        self.assertTrue(finished(source))

    def test_shots_and_sot_require_all_five_numeric_values(self):
        rows = []
        for i in range(1, 6):
            raw = {
                "team_a_shots": 10 if i <= 2 else "",
                "team_b_shots": 7 if i <= 2 else "",
                "team_a_shotsOnTarget": 4 if i <= 2 else "",
                "team_b_shotsOnTarget": 2 if i <= 2 else "",
            }
            rows.append(archive_row(f"M{i}", 100 + i, source_row=i, raw=raw))
        sides, _, _ = audit(
            [runtime_row(home_recent5_n="5", date_utc="1970-01-01T00:16:40Z")],
            rows,
            {"L"},
        )
        side = sides[0]
        self.assertEqual(side["reconstructed_history_count"], 5)
        self.assertEqual(side["home_shots5_numeric_count"], 2)
        self.assertEqual(side["home_shots5_numeric_denominator"], 5)
        self.assertEqual(side["home_shots5"], "PARTIAL_NUMERIC_SOURCE_VALUES_2_OF_5")
        self.assertEqual(side["home_sot5_numeric_count"], 2)
        self.assertEqual(side["home_sot5"], "PARTIAL_NUMERIC_SOURCE_VALUES_2_OF_5")


    def test_csv_writer_accepts_feature_columns_varying_by_side(self):
        import csv
        import tempfile
        from pathlib import Path
        from audit_selected50_row_level_history_provenance import write_csv

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "side_rows.csv"
            write_csv(path, [{"fixture_id": "1", "home_gf5": "COMPLETE"},
                             {"fixture_id": "2", "away_gf5": "NO_FIVE_MATCH_SAMPLE"}])
            with path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(set(rows[0]), {"fixture_id", "home_gf5", "away_gf5"})
            self.assertEqual(rows[0]["home_gf5"], "COMPLETE")
            self.assertEqual(rows[1]["away_gf5"], "NO_FIVE_MATCH_SAMPLE")

    def test_missing_archive_manifest_is_explicit_blocker_not_prediction_or_report_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive_path = root / "archive.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("seasons/S1/matches.json", "[]")
            selected_path = root / "selected.csv"
            with selected_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["selected_id", "country", "competition_name"])
                writer.writeheader()
                writer.writerow({"selected_id": "L", "country": "Test", "competition_name": "League"})
            runtime_path = root / "runtime.csv"
            with runtime_path.open("w", newline="", encoding="utf-8") as handle:
                fields = [
                    "fixture_id", "selected_id", "date_utc", "home_team_provider_id",
                    "home_recent5_n", "feature_support_status", "missing_required_features",
                ]
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({
                    "fixture_id": "TARGET", "selected_id": "L",
                    "date_utc": "2026-11-02T12:00:00Z", "home_team_provider_id": "H",
                    "home_recent5_n": "4",
                    "feature_support_status": "BLOCKED_MISSING_REQUIRED_FEATURES",
                    "missing_required_features": "home_gf5",
                })
            out_dir = root / "out"
            argv = [
                "audit_selected50_row_level_history_provenance.py",
                "--archive", str(archive_path),
                "--selected-manifest", str(selected_path),
                "--runtime-report", str(runtime_path),
                "--out-dir", str(out_dir),
            ]
            with patch.object(sys, "argv", argv):
                self.assertEqual(main(), 0)
            qa = json.loads((out_dir / "oracle_selected50_history_provenance_qa.json").read_text())
            self.assertEqual(qa["status"], "BLOCKED_ARCHIVE_MANIFEST_OR_MAPPING")
            self.assertEqual(qa["blocked_team_side_rows_expected"], 1)
            self.assertEqual(qa["blocked_team_side_rows_audited"], 0)
            self.assertEqual(qa["minimum_history_required"], 5)
            self.assertFalse(qa["production_eligible"])
            self.assertFalse(qa["betting_eligible"])

    def test_load_archive_resolves_exact_season_folder_under_nested_archive_root(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "archive.zip"
            manifest = [{"season_id": "S1", "selected_country": "Test",
                         "selected_competition_name": "League"}]
            match = {"id": "M1", "homeID": "H", "awayID": "A",
                     "date_unix": 1000000100, "status": "complete",
                     "homeGoalCount": 2, "awayGoalCount": 1}
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("private-package/metadata/ingestion_manifest.json",
                                 json.dumps(manifest))
                archive.writestr("private-package/seasons/S1/matches.json",
                                 json.dumps([match]))
            rows, mapped = load_archive(archive_path, {("Test", "League"): "L"})
            self.assertEqual(mapped, 1)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["fixture_id"], "M1")
            self.assertEqual(rows[0]["source_file"], "private-package/seasons/S1/matches.json")

    def test_load_archive_fails_closed_when_mapped_season_file_is_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "archive.zip"
            manifest = [{"season_id": "S1", "selected_country": "Test",
                         "selected_competition_name": "League"}]
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("private-package/metadata/ingestion_manifest.json",
                                 json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "matches.json path resolution failed"):
                load_archive(archive_path, {("Test", "League"): "L"})

    def test_unknown_selected_id_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown selected_id"):
            audit([runtime_row(selected_id="UNKNOWN")], [], {"L"})


if __name__ == "__main__":
    unittest.main()

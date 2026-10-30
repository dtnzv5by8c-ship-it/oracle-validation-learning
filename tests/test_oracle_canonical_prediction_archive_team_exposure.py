import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_oracle_canonical_prediction_archive_team_exposure.py"
sys.path.insert(0, str(SCRIPT.parent))
import audit_oracle_canonical_prediction_archive_team_exposure as audit


def row(market, home="Home FC", away="Away FC", **extra):
    base = {
        "prediction_id": f"p-{market}", "run_id": "run-1", "fixture_id": "L-2026-10-10-home-away",
        "competition": "L", "fixture_date": "2026-10-10", "kickoff_time": "15:00:00+0000",
        "home_team": home, "away_team": away, "model": market, "model_version": "V1",
        "model_status": "CHALLENGER", "prediction_timestamp": "2026-10-04T12:00:00+00:00",
        "data_cutoff_date": "2026-09-20", "event_truth_cutoff_date": "2026-09-20",
        "feature_snapshot_id": f"snap-{market}", "source_manifest_hash": "source-hash",
        "raw_probability": "0.60", "display_probability": "0.60", "decision": "NO_BET",
        "selection": market, "data_quality_status": "WATCH", "pre_match_state_hash": "state-hash",
        "model_code_sha": "code-sha", "calibration_id": "RAW_ONLY",
        "calibrated_probability": "", "market_odds": "", "market_implied_probability": "", "model_edge": "",
    }
    base.update(extra)
    return base


class ArchiveExposureTests(unittest.TestCase):
    def setUp(self):
        self.rows = [row(m) for m in sorted(audit.EXPECTED)]
        self.fields = list(self.rows[0])

    def test_complete_fixture_market_set_and_team_sample_counts(self):
        result = audit.audit(self.rows, self.fields)
        pa = result["prediction_archive"]
        self.assertEqual(pa["prediction_rows"], 5)
        self.assertEqual(pa["fixtures"], 1)
        self.assertEqual(pa["fixtures_with_all_five_expected_markets"], 1)
        self.assertEqual(pa["unique_team_labels"], 2)
        self.assertEqual(pa["team_fixture_sample_distribution"], {1: 2})
        self.assertEqual(pa["teams_with_two_or_more_fixtures"], 0)
        self.assertEqual(pa["team_market_exposure_distribution"], {1: 6})
        self.assertFalse(result["interpretation"]["team_market_performance_measurable"])

    def test_strict_pre_kickoff_and_post_kickoff_are_separate(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["prediction_timestamp"] = "2026-10-10T15:00:00+00:00"
        result = audit.audit(rows, self.fields)
        pa = result["prediction_archive"]
        self.assertEqual(pa["strictly_pre_kickoff_rows"], 4)
        self.assertEqual(pa["post_or_equal_kickoff_rows"], 1)
        self.assertEqual(pa["timestamp_unverifiable_rows"], 0)

    def test_naive_timestamp_is_not_accepted_as_point_in_time_proof(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["prediction_timestamp"] = "2026-10-04T12:00:00"
        result = audit.audit(rows, self.fields)
        self.assertEqual(result["prediction_archive"]["timestamp_unverifiable_rows"], 1)
        self.assertEqual(result["prediction_archive"]["strictly_pre_kickoff_rows"], 4)

    def test_empty_snapshot_and_settlement_ledgers_do_not_create_truth(self):
        result = audit.audit(self.rows, self.fields, settlements=[], snapshots=[])
        ev = result["evidence_ledgers"]
        self.assertEqual(ev["settlement_rows"], 0)
        self.assertEqual(ev["official_truth_verified_rows"], 0)
        self.assertEqual(ev["feature_snapshot_manifest_rows"], 0)
        self.assertEqual(ev["feature_snapshot_ids_resolved"], 0)
        self.assertFalse(result["interpretation"]["official_settlement_truth_available"])
        self.assertFalse(result["interpretation"]["point_in_time_feature_snapshot_retrievable"])

    def test_settled_status_alone_is_not_official_truth(self):
        settlement = [{"prediction_id": "p-BTTS_YES", "settlement_status": "SETTLED", "settlement_source": "score feed"}]
        result = audit.audit(self.rows, self.fields, settlements=settlement)
        ev = result["evidence_ledgers"]
        self.assertEqual(ev["settled_status_rows"], 1)
        self.assertEqual(ev["settlement_rows_matching_prediction_ids"], 1)
        self.assertEqual(ev["official_truth_verified_rows"], 0)

    def test_missing_optional_calibration_and_odds_are_reported(self):
        result = audit.audit(self.rows, self.fields)
        optional = result["prediction_archive"]["missing_optional_cells"]
        self.assertEqual(optional["calibrated_probability"], 5)
        self.assertEqual(optional["market_odds"], 5)

    def test_duplicate_prediction_and_observation_keys_are_flagged(self):
        rows = [dict(r) for r in self.rows]
        rows.append(dict(rows[0]))
        result = audit.audit(rows, self.fields)
        self.assertEqual(result["prediction_archive"]["duplicate_prediction_ids"], 1)
        self.assertEqual(result["prediction_archive"]["duplicate_fixture_model_version_observations"], 1)

    def test_data_cutoff_age_is_reported_not_mislabelled_source_freshness(self):
        result = audit.audit(self.rows, self.fields)
        self.assertEqual(result["prediction_archive"]["cutoff_age_days_at_prediction"]["min"], 14.0)
        self.assertEqual(result["prediction_archive"]["cutoff_age_days_at_kickoff"]["min"], 20.0)


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_footystats_endpoint_contracts import validate_paged_response, validate_single_response


class FootyStatsPaginationContractTests(unittest.TestCase):
    def test_league_matches_pager_current_page_variant(self):
        payload = {
            "success": True,
            "pager": {"current_page": 1, "max_page": 2, "results_per_page": 1000, "total_results": 1001},
            "data": [{}] * 1000,
        }
        got = validate_paged_response("league-matches", payload, 1)
        self.assertTrue(got["page_complete"])
        self.assertTrue(got["has_more"])
        self.assertEqual(got["next_page"], 2)
        self.assertEqual(got["expected_page_count"], 2)

    def test_league_teams_pager_page_variant(self):
        payload = {
            "success": True,
            "pager": {"page": 1, "per_page": 50, "total_results": 20},
            "data": [{}] * 20,
        }
        got = validate_paged_response("league-teams", payload, 1)
        self.assertFalse(got["has_more"])
        self.assertEqual(got["returned_rows"], 20)

    def test_empty_season_is_explicitly_complete(self):
        payload = {
            "success": True,
            "pager": {"current_page": 1, "max_page": 1, "results_per_page": 1000, "total_results": 0},
            "data": [],
        }
        got = validate_paged_response("league-matches", payload, 1)
        self.assertTrue(got["page_complete"])
        self.assertEqual(got["total_results"], 0)
        self.assertFalse(got["has_more"])

    def test_missing_pager_or_total_count_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "pager metadata"):
            validate_paged_response("league-matches", {"success": True, "data": []}, 1)
        with self.assertRaisesRegex(ValueError, "total_results"):
            validate_paged_response(
                "league-teams",
                {"success": True, "pager": {"page": 1, "per_page": 50}, "data": []},
                1,
            )

    def test_incomplete_page_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "expected 50"):
            validate_paged_response(
                "league-teams",
                {"success": True, "pager": {"page": 1, "per_page": 50, "total_results": 70}, "data": [{}] * 49},
                1,
            )

    def test_max_page_conflict_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "conflicts"):
            validate_paged_response(
                "league-matches",
                {"success": True, "pager": {"current_page": 1, "max_page": 1, "results_per_page": 1000, "total_results": 1001}, "data": [{}] * 1000},
                1,
            )

    def test_requested_page_must_match_response(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate_paged_response(
                "league-matches",
                {"success": True, "pager": {"current_page": 2, "max_page": 2, "results_per_page": 1000, "total_results": 1001}, "data": [{}]},
                1,
            )

    def test_single_endpoint_shapes_are_explicit(self):
        self.assertEqual(
            validate_single_response("league-tables", {"success": True, "data": {}})["response_status"],
            "SUCCESS_SHAPE_VERIFIED",
        )
        self.assertEqual(
            validate_single_response("league-season", {"success": True, "data": []})["data_shape"],
            "list",
        )
        with self.assertRaisesRegex(ValueError, "documented shape"):
            validate_single_response("match", {"success": True, "data": []})


if __name__ == "__main__":
    unittest.main(verbosity=2)

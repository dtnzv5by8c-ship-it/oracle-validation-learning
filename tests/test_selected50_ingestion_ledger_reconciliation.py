import unittest
from scripts.audit_selected50_ingestion_ledger_reconciliation import analyze

def ledger():
    seasons = []
    for league in range(50):
        for year in range(4):
            seasons.append({"season_id": str(1000 + league * 4 + year),
                "provider_season_year": str(2023 + year), "selected_country": f"Country {league}",
                "selected_competition_name": f"League {league}", "provider_league_id": "NOT_EXPOSED_BY_CATALOGUE",
                "status": "INGESTED", "match_count": 100 + year, "team_count": 16, "matches_pages": 1})
    return {"status": "COMPLETED", "selected_leagues": 50, "selected_season_ids": 200,
        "exact_selected_season_id_matches": 50, "historical_seasons_selected": 200,
        "catalogue_unmatched_ids": [], "ambiguous_exact_ids": [], "seasons_ingested": 200, "seasons_failed": 0,
        "api_requests": 57, "provider_request_window_remaining_last_observed": 1743,
        "provider_request_window_is_not_monthly_credit_proof": True, "production_readiness": "NOT_GRANTED",
        "production_model_logic_changed": False, "production_probabilities_changed": False,
        "sha256": "a" * 64, "season_results": seasons}

class Selected50IngestionLedgerTests(unittest.TestCase):
    def test_reconciles_50_groups_and_200_seasons(self):
        summary, rollup = analyze(ledger())
        self.assertEqual(summary["selected_leagues"], 50)
        self.assertEqual(summary["historical_season_rows"], 200)
        self.assertEqual(len(rollup), 50)
        self.assertEqual(summary["seasons_ingested"], 200)
        self.assertEqual(summary["seasons_failed"], 0)

    def test_rollup_totals_are_reconciled(self):
        summary, rollup = analyze(ledger())
        self.assertEqual(summary["total_match_rows_across_seasons"], 20300)
        self.assertEqual(summary["total_team_season_memberships"], 3200)
        self.assertEqual(sum(r["match_rows_total"] for r in rollup), 20300)

    def test_parent_competition_ids_are_not_inferred(self):
        summary, rollup = analyze(ledger())
        self.assertEqual(summary["provider_parent_competition_ids_exposed"], 0)
        self.assertFalse(any(r["parent_competition_id_exposed"] for r in rollup))

    def test_duplicate_season_ids_are_rejected(self):
        source = ledger()
        source["season_results"][1]["season_id"] = source["season_results"][0]["season_id"]
        with self.assertRaises(ValueError): analyze(source)

    def test_missing_season_in_group_is_rejected(self):
        source = ledger()
        source["season_results"].pop()
        with self.assertRaises(ValueError): analyze(source)

    def test_failed_season_is_rejected(self):
        source = ledger()
        source["season_results"][0]["status"] = "FAILED"
        with self.assertRaises(ValueError): analyze(source)

    def test_source_must_remain_not_production_ready(self):
        source = ledger()
        source["production_readiness"] = "APPROVED"
        with self.assertRaises(ValueError): analyze(source)

if __name__ == "__main__":
    unittest.main()

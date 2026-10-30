import unittest
from scripts.audit_selected50_xg_odds_crossscope_reconciliation import (
    aggregate, pair_summary, wilson, validate_quality, build_xg, belgium_rollup
)

class CrossScopeTests(unittest.TestCase):
    def test_wilson_and_empty_population(self):
        self.assertEqual(wilson(0,0),(None,None))
        self.assertEqual(wilson(20,50),(27.61,53.82))

    def test_current_and_historical_are_separate(self):
        rows = [
            {"scope_id":"C","subset":"primary_window_provider_complete","selected_current_season":"True","field_name":"x","numeric_rows":"50","zero_rows":"20","positive_rows":"30"},
            {"scope_id":"H","subset":"primary_window_provider_complete","selected_current_season":"False","field_name":"x","numeric_rows":"100","zero_rows":"5","positive_rows":"95"},
        ]
        self.assertEqual(aggregate(rows,"x",True)["zero_pct"],40.0)
        self.assertEqual(aggregate(rows,"x",False)["zero_pct"],5.0)

    def test_universe_rollup_includes_unflagged_groups(self):
        rows = []
        for country,zeros in (("A",20),("B",5)):
            for field in ("team_a_xg_prematch","team_b_xg_prematch","total_xg_prematch"):
                for current,scope,n,z in (("True",country+"C",50,zeros),("False",country+"H",100,5)):
                    rows.append({"scope_id":scope,"country":country,"competition_name":"L","subset":"primary_window_provider_complete",
                        "selected_current_season":current,"field_name":field,"numeric_rows":str(n),"zero_rows":str(z),"positive_rows":str(n-z)})
        result = build_xg(rows)
        self.assertEqual(len(result),6)
        self.assertEqual(sum(r["current_n"] for r in result if r["field_name"]=="team_a_xg_prematch"),100)

    def test_pair_orientation_and_counts(self):
        rows = [{"subset":"primary_window_provider_complete","selected_current_season":"True","scope_id":"C",
            "field_a":"team_a_xg_prematch","field_b":"team_a_xg","both_numeric_rows":"10",
            "field_a_zero_rows_on_pair_complete_rows":"4","field_b_zero_rows_on_pair_complete_rows":"1",
            "both_zero_rows":"1","field_a_zero_field_b_nonzero_rows":"3","field_a_nonzero_field_b_zero_rows":"0"}]
        result = next(r for r in pair_summary(rows) if r["prematch_field"]=="team_a_xg_prematch")
        self.assertEqual((result["pre_zero"],result["pre_zero_post_nonzero"],result["scope_count"]),(4,3,1))

    def test_belgium_and_other_group_rates(self):
        rows = []
        for i in range(63):
            rows.append({"scope_id":"BE","country":"Belgium","competition_name":"Pro League","subset":"primary_window_provider_complete",
                "selected_current_season":"True","field_name":"odds_btts_yes","numeric_rows":"1","zero_rows":"1" if i<54 else "0"})
        for i in range(5570):
            rows.append({"scope_id":f"O{i}","country":"Other","competition_name":"League","subset":"primary_window_provider_complete",
                "selected_current_season":"True","field_name":"odds_btts_yes","numeric_rows":"1","zero_rows":"1" if i<29 else "0"})
        result = belgium_rollup(rows)
        be = next(r for r in result if r["population"]=="Belgium Pro League" and r["field_name"]=="odds_btts_yes")
        other = next(r for r in result if r["population"]=="Other selected leagues" and r["field_name"]=="odds_btts_yes")
        self.assertEqual((be["numeric_rows"],be["zero_rows"],be["zero_pct"]),(63,54,85.71))
        self.assertEqual((other["numeric_rows"],other["zero_rows"],other["zero_pct"]),(5570,29,0.52))

    def test_duplicate_quality_rows_fail_closed(self):
        row = {"scope_id":"C","subset":"primary_window_provider_complete","field_name":"x","numeric_rows":"2","zero_rows":"1","positive_rows":"1"}
        with self.assertRaises(ValueError):
            validate_quality([row,dict(row)])
        with self.assertRaises(ValueError):
            validate_quality([{**row,"scope_id":"D","zero_rows":"3"}])

if __name__ == "__main__":
    unittest.main()

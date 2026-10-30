import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_selected50_xg_heterogeneity_team_sample_adequacy.py"
sys.path.insert(0, str(SCRIPT.parent))
import audit_selected50_xg_heterogeneity_team_sample_adequacy as audit


class XgHeterogeneityTests(unittest.TestCase):
    def setUp(self):
        self.rows=[]
        for country,league,cz,hz in [("A","League A",10,1),("B","League B",5,0)]:
            for field in audit.XG_FIELDS:
                self.rows.append({"country":country,"competition_name":league,"field_name":field,
                                  "current_n":"100","current_zero":str(cz),"historical_n":"200","historical_zero":str(hz)})

    def test_league_cluster_summary_and_shrinkage(self):
        detail,summary=audit.audit_xg(self.rows,reps=200,seed=7)
        self.assertEqual(len(detail),6)
        for field in audit.XG_FIELDS:
            self.assertEqual(summary[field]["league_groups"],2)
            self.assertEqual(summary[field]["positive_raw_delta_groups"],2)
            self.assertEqual(summary[field]["positive_shrunk_delta_groups"],2)
            self.assertEqual(summary[field]["bootstrap_unit"],"league group, not match rows")

    def test_duplicate_league_field_rejected(self):
        with self.assertRaises(ValueError): audit.audit_xg(self.rows+[self.rows[0]],reps=100)

    def test_zero_count_greater_than_n_rejected(self):
        bad=[dict(r) for r in self.rows]; bad[0]["current_zero"]="101"
        with self.assertRaises(ValueError): audit.audit_xg(bad,reps=100)


class BelgiumSeasonTests(unittest.TestCase):
    def test_scope_order_is_not_inferred(self):
        rows=[]
        for scope,current,n,z in [("old-a","False",72,0),("old-b","False",313,35),("current","True",63,54)]:
            rows.append({"country":"Belgium","competition_name":"Pro League","field_name":"odds_btts_yes",
                         "scope_id":scope,"selected_current_season":current,"sample_rows":str(n),"zero_rows":str(z)})
        detail=audit.audit_belgium(rows)
        self.assertEqual(len(detail),3)
        self.assertTrue(all("NOT_INFERRED" in r["season_order"] for r in detail))
        self.assertEqual(next(r for r in detail if r["season_scope_id"]=="current")["zero_pct"],85.7143)

    def test_duplicate_scope_market_rejected(self):
        row={"country":"Belgium","competition_name":"Pro League","field_name":"odds_btts_yes","scope_id":"1",
             "selected_current_season":"True","sample_rows":"10","zero_rows":"2"}
        with self.assertRaises(ValueError): audit.audit_belgium([row,dict(row)])


class TeamSampleAdequacyTests(unittest.TestCase):
    def test_exposures_are_not_performance_samples(self):
        base={"provider_team_id":"10","team_name":"A","country":"Belgium","league":"Pro League","fixture_role":"HOME",
              "fixture_appearances":"1","raw_prediction_appearances":"1","blocked_appearances":"0",
              "feature_complete_appearances":"1","feature_incomplete_appearances":"0","latest_form_n_observed":"5",
              "latest_form_n_reported":"5","latest_form_n_mismatch":"False","btts_fixture_probability_exposures":"1",
              "dc_team_side_probability_exposures":"1","canonical_team_join_statuses":"NOT_VERIFIED",
              "settlement_truth_statuses":"NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC","calibration_statuses":"RAW_ONLY_UNCALIBRATED"}
        rows=[dict(base),{**base,"provider_team_id":"11","fixture_appearances":"2","raw_prediction_appearances":"0",
              "blocked_appearances":"2","feature_complete_appearances":"0","feature_incomplete_appearances":"2","latest_form_n_observed":"4"}]
        by,summary=audit.audit_team(rows)
        self.assertEqual(summary["team_role_profiles"],2)
        self.assertEqual(summary["profiles_ge3_fixtures"],0)
        self.assertEqual(summary["form_below5_profiles"],1)
        self.assertEqual(summary["canonical_join_status_counts"]["NOT_VERIFIED"],2)
        self.assertIn("NOT HISTORICAL OUTCOME SAMPLES",summary["interpretation"])
        self.assertEqual(len(by),1)

    def test_boolean_parser(self):
        self.assertTrue(audit.flag("True")); self.assertFalse(audit.flag("False"))
        with self.assertRaises(ValueError): audit.flag("unknown")


if __name__=="__main__": unittest.main()

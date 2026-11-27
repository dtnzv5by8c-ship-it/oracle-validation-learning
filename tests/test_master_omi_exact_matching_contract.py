import re
from pathlib import Path
import unittest

WF = Path(".github/workflows/oracle-master-omi-excel.yml")

class TestMasterOMIExactMatchingContract(unittest.TestCase):
    def test_workflow_exists(self):
        self.assertTrue(WF.exists())

    def test_no_normalized_name_admission_in_team_state_or_history(self):
        text = WF.read_text(encoding="utf-8")
        forbidden = [
            'st.get("home_team",pd.Series([""]*len(st))).astype(str).map(norm)',
            'st.get("away_team",pd.Series([""]*len(st))).astype(str).map(norm)',
            'm["home_team"].astype(str).map(norm)==norm(team)',
            'm["away_team"].astype(str).map(norm)==norm(team)',
            'teammask("home_team",home)',
            'teammask("away_team",away)',
        ]
        for token in forbidden:
            self.assertNotIn(token, text, token)

    def test_exact_fixture_and_provider_id_controls_are_present(self):
        text = WF.read_text(encoding="utf-8")
        self.assertIn('st["fixture_id"].astype(str)==str(r["Fixture ID"])', text)
        self.assertIn('"source_match_id" in mt.columns', text)
        self.assertIn('"provider_home_id" in fx.columns', text)
        self.assertIn('"provider_away_id" in fx.columns', text)

if __name__ == "__main__":
    unittest.main()

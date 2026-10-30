import datetime as dt
import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "derive_selected50_league_scoring_dna.py"
spec = importlib.util.spec_from_file_location("scoring_dna", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ScoringDnaTests(unittest.TestCase):
    def test_score_and_flag_parsing(self):
        self.assertEqual(mod.score(0), 0)
        self.assertEqual(mod.score("2"), 2)
        self.assertIsNone(mod.score(-1))
        self.assertIsNone(mod.score(1.5))
        self.assertEqual(mod.flag("0"), 0)
        self.assertEqual(mod.flag(1), 1)
        self.assertIsNone(mod.flag("unknown"))

    def test_completed_only_and_neutral_excluded_from_1x2(self):
        records = [
            {"fixture_id":"1","date":dt.date(2025,1,1),"status":"complete","home":2,"away":1,"no_home_away":0},
            {"fixture_id":"2","date":dt.date(2025,1,2),"status":"complete","home":0,"away":0,"no_home_away":1},
            {"fixture_id":"3","date":dt.date(2025,1,3),"status":"incomplete","home":0,"away":0,"no_home_away":0},
            {"fixture_id":"4","date":dt.date(2025,1,4),"status":"complete","home":1,"away":3,"no_home_away":None},
        ]
        group={"selected_id":"x","country":"Test","competition_name":"League"}
        row=mod.score_period(group,"TEST",dt.date(2025,1,1),dt.date(2025,12,31),records,4)
        self.assertEqual(row["dated_archive_rows"],4)
        self.assertEqual(row["completed_dated_score_rows"],3)
        self.assertEqual(row["noncomplete_status_rows_with_numeric_scores_excluded"],1)
        self.assertEqual(row["valid_1x2_rows_no_home_away_zero"],1)
        self.assertEqual(row["no_home_away_one_excluded_from_1x2"],1)
        self.assertEqual(row["no_home_away_unknown_excluded_from_1x2"],1)
        self.assertEqual(row["home_win_rate_pct"],100.0)
        self.assertEqual(row["btts_rate_pct"],66.667)
        self.assertEqual(row["over15_rate_pct"],66.667)
        self.assertEqual(row["over25_rate_pct"],66.667)
        self.assertEqual(row["over35_rate_pct"],33.333)
        self.assertEqual(sum(row[k] for k in ("total_goals_0_n","total_goals_1_n","total_goals_2_n","total_goals_3_n","total_goals_4_n","total_goals_5plus_n")),3)

    def test_empty_denominator_is_blank_not_zero(self):
        group={"selected_id":"x","country":"Test","competition_name":"League"}
        row=mod.score_period(group,"EMPTY",dt.date(2025,1,1),dt.date(2025,12,31),[],4)
        self.assertIsNone(row["btts_rate_pct"])
        self.assertIsNone(row["home_win_rate_pct"])
        self.assertEqual(row["score_profile_status"],"NO_COMPLETED_DATED_SCORE_ROWS")

    def test_utc_date_parser(self):
        self.assertEqual(mod.day({"date_unix":1735689600}),dt.date(2025,1,1))

if __name__ == "__main__":
    unittest.main()

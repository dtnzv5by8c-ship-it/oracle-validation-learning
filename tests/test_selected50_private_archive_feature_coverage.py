import unittest
from scripts.qa_selected50_private_archive import field_counts, nested_dict_rows, update_numeric_field_stats, summarize_numeric_field_stats

class PrivateArchiveFeatureCoverageTests(unittest.TestCase):
    def test_field_presence_and_nonempty_counts_are_distinct(self):
        rows = [
            {"a": 1, "b": None, "c": 0, "d": ""},
            {"a": None, "b": "yes", "c": False, "e": []},
        ]
        present, nonempty = field_counts(rows)
        self.assertEqual(present["a"], 2)
        self.assertEqual(nonempty["a"], 1)
        self.assertEqual(present["b"], 2)
        self.assertEqual(nonempty["b"], 1)
        self.assertEqual(nonempty["c"], 2)
        self.assertEqual(nonempty["d"], 0)
        self.assertEqual(nonempty["e"], 0)

    def test_nested_table_and_stats_payloads_are_flattened(self):
        payload = {
            "meta": "table",
            "overall": [{"position": 1, "team": "A"}],
            "home": [{"position": 2, "team": "B"}],
        }
        rows = nested_dict_rows(payload)
        self.assertEqual(len(rows), 3)
        self.assertIn("position", {key for row in rows for key in row})

    def test_empty_and_scalar_payloads_do_not_create_fake_rows(self):
        self.assertEqual(nested_dict_rows(None), [])
        self.assertEqual(nested_dict_rows([]), [])
        self.assertEqual(nested_dict_rows("no-table"), [])

    def test_numeric_feature_quality_counts_zero_and_invalid_values(self):
        stats = {}
        rows = [
            {"team_a_xg": "1.25", "odds_ft_1": "2.10"},
            {"team_a_xg": 0, "odds_ft_1": None},
            {"team_a_xg": "N/A", "odds_ft_1": "-1"},
        ]
        update_numeric_field_stats(stats, rows)
        summary = summarize_numeric_field_stats(stats, len(rows))
        self.assertEqual(summary["team_a_xg"]["numeric_rows"], 2)
        self.assertEqual(summary["team_a_xg"]["zero_rows"], 1)
        self.assertEqual(summary["team_a_xg"]["non_numeric_rows"], 1)
        self.assertEqual(summary["odds_ft_1"]["numeric_rows"], 2)
        self.assertEqual(summary["odds_ft_1"]["negative_rows"], 1)
        self.assertEqual(summary["odds_ft_1"]["nonempty_rows"], 2)

if __name__ == "__main__":
    unittest.main()

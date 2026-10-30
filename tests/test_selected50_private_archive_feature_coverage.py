import unittest
from scripts.qa_selected50_private_archive import field_counts, nested_dict_rows

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

if __name__ == "__main__":
    unittest.main()

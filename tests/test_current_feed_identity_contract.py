import unittest
from scripts.validate_current_feed_identity_contract import classify_match

class CurrentFeedIdentityContractTests(unittest.TestCase):
    def setUp(self):
        self.allowlist = {
            "ENG_E0": {"status": "APPROVED", "league_id": "17", "country": "England"},
            "GER_D1": {"status": "APPROVED", "league_id": "35", "country": "Germany"},
        }

    def test_exact_approved_id_and_country_is_admitted(self):
        row = classify_match({"canonical_competition_code":"ENG_E0","league_id":17,
                              "country":"England","league_name":"Premier League"}, self.allowlist)
        self.assertTrue(row["admitted"])
        self.assertEqual(row["identity_status"], "VERIFIED_ALLOWLIST_MATCH")

    def test_same_display_name_different_id_is_quarantined(self):
        row = classify_match({"canonical_competition_code":"ENG_E0","league_id":522,
                              "country":"Ghana","league_name":"Premier League"}, self.allowlist)
        self.assertFalse(row["admitted"])
        self.assertEqual(row["reason"], "PROVIDER_LEAGUE_ID_MISMATCH")

    def test_wrong_country_is_quarantined_even_if_id_matches(self):
        row = classify_match({"canonical_competition_code":"ENG_E0","league_id":17,
                              "country":"Scotland","league_name":"Premier League"}, self.allowlist)
        self.assertFalse(row["admitted"])
        self.assertEqual(row["reason"], "COUNTRY_CATEGORY_MISMATCH")

    def test_unknown_id_is_quarantined(self):
        row = classify_match({"canonical_competition_code":"ENG_E0","league_id":999,
                              "country":"England","league_name":"Premier League"}, self.allowlist)
        self.assertFalse(row["admitted"])

    def test_missing_country_is_quarantined(self):
        row = classify_match({"canonical_competition_code":"ENG_E0","league_id":17,
                              "league_name":"Premier League"}, self.allowlist)
        self.assertEqual(row["reason"], "MISSING_COUNTRY_CATEGORY")

    def test_unapproved_or_absent_allowlist_fails_closed(self):
        row = classify_match({"canonical_competition_code":"ARG_D1","league_id":123,
                              "country":"Argentina","league_name":"Primera División"}, self.allowlist)
        self.assertFalse(row["admitted"])
        self.assertEqual(row["reason"], "NO_APPROVED_ALLOWLIST_ENTRY")

    def test_display_name_alone_never_admits(self):
        row = classify_match({"canonical_competition_code":"ENG_E0",
                              "league_name":"Premier League"}, self.allowlist)
        self.assertFalse(row["admitted"])
        self.assertEqual(row["reason"], "MISSING_PROVIDER_LEAGUE_ID")

if __name__ == "__main__":
    unittest.main()

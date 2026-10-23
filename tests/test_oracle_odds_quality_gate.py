import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "oracle_fail_closed_quality_gate.py"
SPEC = importlib.util.spec_from_file_location("oracle_fail_closed_quality_gate", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OddsValidityTests(unittest.TestCase):
    def test_valid_decimal_odds(self):
        self.assertTrue(MODULE.usable_positive_number("2.15"))

    def test_rejects_zero_and_one(self):
        self.assertFalse(MODULE.usable_positive_number("0"))
        self.assertFalse(MODULE.usable_positive_number("1"))

    def test_rejects_blank_and_non_numeric(self):
        self.assertFalse(MODULE.usable_positive_number(""))
        self.assertFalse(MODULE.usable_positive_number("N/A"))
        self.assertFalse(MODULE.usable_positive_number(None))

    def test_rejects_non_finite(self):
        self.assertFalse(MODULE.usable_positive_number("nan"))
        self.assertFalse(MODULE.usable_positive_number("inf"))
        self.assertFalse(MODULE.usable_positive_number("-inf"))

    def test_rejects_negative(self):
        self.assertFalse(MODULE.usable_positive_number("-2.4"))


if __name__ == "__main__":
    unittest.main()

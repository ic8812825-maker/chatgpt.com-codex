import importlib
import unittest
from fractions import Fraction as F
m=importlib.import_module("02_MARGIN_ORACLE")


class MarginTests(unittest.TestCase):
    def test_nominal(self):
        q=m.assess((0,109690,109710),(10,109990,110010),1)
        self.assertEqual((q["mark"],q["exit_reserve"],q["balance"]),(-58,29,14971))
        self.assertEqual(q["used_margin"],float(F(220020,30)))
        self.assertTrue(q["eligible"])

    def test_exact_200_boundary_and_capacity(self):
        entry=(0,111000,111020)
        # Equity=14942, Gross=2, leverage=30. Threshold ask floor=112065.
        self.assertTrue(m.assess(entry,(10,112045,112065),1)["eligible"])
        self.assertIn("MARGIN",m.assess(entry,(10,112046,112066),1)["reasons"])
        self.assertIn("EXECUTION",m.assess(entry,(10,112045,112065),1,capacity=199)["reasons"])

    def test_out_of_budget_or_bad_time(self):
        self.assertIn("COST",m.assess((0,109990,110010),(1,110000,110080),1)["reasons"])
        self.assertIn("DATA",m.assess((1,109990,110010),(1,109990,110010),1)["reasons"])

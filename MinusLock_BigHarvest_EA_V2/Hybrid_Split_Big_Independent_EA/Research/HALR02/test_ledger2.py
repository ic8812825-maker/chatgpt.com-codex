import unittest
from execution import Intent, Quote
from ledger2 import Ledger, Limits, TICKS


class LedgerTest(unittest.TestCase):
    def test_exact_cycle_and_no_double_charge(self):
        for orientation in (-1,1):
            b = Ledger(orientation,Limits())
            q = Quote(0)
            self.assertEqual(b.mark(q),-58*TICKS)
            before = b.exit_cost(q)
            self.assertEqual(b.fill(Intent(-1,25,0),25,q),25)
            self.assertEqual(b.tickets[0].units,75)
            self.assertTrue(b.tickets[0].original)
            self.assertEqual(b.mark(q),-58*TICKS)
            self.assertEqual(b.spent+b.exit_cost(q),before)

    def test_shifted_fill_and_separate_limits(self):
        b = Ledger(1,Limits(cost=20))
        b.observe(Quote(0))
        self.assertEqual(b.violations,{"COST"})
        self.assertEqual(b.fill(Intent(1,100),100,Quote(100)),50)
        self.assertEqual((b.net,b.gross),(50,250))
        self.assertIn("MARGIN",b.violations)

import unittest
from money import Ledger, Quote
from preserve import Params
from rebuild import Rebuild


class RebuildTest(unittest.TestCase):
    def test_condition_and_one_attempt(self):
        b = Ledger(1)
        p = Rebuild("B3", Params(attempts=1))
        p.act(b, Quote(0, reject=True), 0)
        self.assertFalse(p.switched)
        p.act(b, Quote(0), 1)
        self.assertTrue(p.switched)
        self.assertEqual(b.snapshot(Quote(0))["pnl"], -58)
        p.act(b, Quote(200), 2)
        self.assertEqual(b.gross, 0)
        p.act(b, Quote(250), 3)
        self.assertEqual(b.net, 20)
        self.assertTrue(all(i >= 2 for i in b.tickets))
        p.act(b, Quote(100), 4)
        p.act(b, Quote(-500), 5)
        self.assertEqual(b.net, 0)
        self.assertLess(b.snapshot(Quote(-500))["pnl"], -58)

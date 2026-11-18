import unittest
from money import Ledger, Quote
from preserve import Preserve, Params, target_net


class PreserveTest(unittest.TestCase):
    def test_original_core(self):
        for orientation in [-1, 1]:
            for variant in ["A1", "A2", "A3"]:
                p = Preserve(variant, Params(), orientation)
                b = Ledger(orientation)
                for i, mid in enumerate([200, -400, 600, -800]):
                    p.act(b, Quote(mid), i)
                    self.assertGreaterEqual(b.tickets[p.loser].units, p.floors[p.loser])
                    self.assertLessEqual(abs(b.net), 50)

    def test_reduce_before_open(self):
        b = Ledger(1)
        target_net(b, Quote(0), 50)
        self.assertEqual(b.gross, 150)
        self.assertEqual(b.snapshot(Quote(0))["pnl"], -58)

import unittest
from money import Ledger, Quote


class MoneyTest(unittest.TestCase):
    def test_round_trip_cash_flows(self):
        for sign in [-1, 1]:
            book = Ledger(sign)
            q = Quote(0)
            self.assertEqual(book.snapshot(q)["pnl"], -58)
            book.fill(q, -1, 50, 0)
            self.assertEqual(book.snapshot(q)["pnl"], -58)
            self.assertTrue(book.flatten(q))
            self.assertEqual(book.realized - book.costs, -58)
            book.fill(q, 1, 10)
            self.assertTrue(book.flatten(Quote(100)))
            self.assertAlmostEqual(book.snapshot(q)["pnl"], -58 + 10 - 2.9)
            with self.assertRaises(ValueError):
                book.fill(q, -1, 1, 0)

    def test_partial_reject_and_gap(self):
        book = Ledger(1)
        self.assertEqual(book.fill(Quote(0, reject=True), 1, 50), 0)
        self.assertEqual(book.fill(Quote(0, fill_cap=23), 1, 50), 23)
        self.assertEqual(book.net, 23)
        self.assertEqual(book.fill(Quote(0), 1, 50), 27)
        self.assertEqual(book.net, 50)
        self.assertLess(book.snapshot(Quote(-10000, 100, 4))["pnl"], -5000)

    def test_slippage_spread_and_carry(self):
        book = Ledger(1)
        q = Quote(0, 100, 4, .02)
        book.carry(q)
        expected = -58 - 80 - 8 - .04
        self.assertAlmostEqual(book.snapshot(q)["pnl"], expected)
        book.flatten(q)
        self.assertAlmostEqual(book.realized - book.costs, expected)

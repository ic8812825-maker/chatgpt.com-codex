import itertools
import unittest
from meta import D, dp, Meta
from money import Ledger, Quote
from preserve import Params


class MetaTest(unittest.TestCase):
    def test_minimax_two_stage_independent_brute_force(self):
        # Flat B, one available directional size. Enumerate first action and
        # all contingent hold-or-exit decisions for the five observations.
        candidates = [-5800]
        for n in (-20, 0, 20):
            first = -5800 - abs(n)*29
            for exits in itertools.product((False, True), repeat=5):
                leaves = []
                for d, close in zip(D, exits):
                    p = first + n*d
                    leaves.extend(p + (0 if close else n*e) for e in D)
                candidates.append(min(leaves))
        self.assertEqual(dp(2, -5800, 0, False, 0, 20, 50000, "minimax"),
                         max(candidates)/100)

    def test_no_original_rebirth(self):
        b = Ledger(1)
        m = Meta(Params(), 250, "probability")
        b.flatten(Quote(0))
        m.act(b, Quote(150), 1)
        self.assertTrue(all(i >= 2 for i in b.tickets))

import itertools
import unittest
from meta import D, dp
from money import Ledger, Quote
from simulate import run


class AuditTest(unittest.TestCase):
    def test_two_event_contingent_policy_enumeration(self):
        budget = 12000
        initial = -5800
        size = 20

        def utility(p, objective):
            if objective == "minimax":
                return p / 100
            if objective == "probability":
                return int(p > 0)
            return 100*int(p > 0) + p/200 - max(0, -p-10000)/100

        def outcomes(pnl, old, target):
            opening = max(0, abs(target)-abs(old)) if target*old > 0 else abs(target)
            mark = pnl - 29*opening
            rows = [mark + target*d for d in D]
            return rows if min(rows) >= -budget else None

        def combine(children, previous, objective):
            if objective == "minimax":
                return min(children)
            return (sum(children) + 5*children[D.index(previous)])/10

        for objective in ("minimax", "probability", "adjusted"):
            values = [utility(initial, objective)]
            for a in (-size, 0, size):
                first = outcomes(initial, 0, a)
                if first is None:
                    continue
                choices = []
                for d, p in zip(D, first):
                    row = [utility(p, objective)]
                    if p <= 0:
                        for b in (-size, 0, size):
                            second = outcomes(p, a, b)
                            if second is not None:
                                row.append(combine([utility(x,objective) for x in second],
                                                   d, objective))
                    choices.append(row)
                for policy in itertools.product(*choices):
                    values.append(combine(policy, 300, objective))
            self.assertAlmostEqual(dp(2,initial,0,False,300,size,budget,objective), max(values))

    def test_strict_preserve_cannot_always_respect_budget(self):
        scenario = (1, (300, 300, -4000, 0, 0, 0), "persistent_failure")
        result = run("A1-strict", scenario)
        self.assertGreater(result.remaining, 0)
        self.assertTrue(result.violations)

    def test_positive_child_cashflow_does_not_erase_deficit(self):
        b = Ledger(1)
        b.flatten(Quote(0))
        b.fill(Quote(0),1,20)
        b.flatten(Quote(150))
        self.assertAlmostEqual(b.snapshot(Quote(150))["pnl"], -33.8)

    def test_constructive_hundred_dollar_policy(self):
        for orientation in (-1, 1):
            for first, second in itertools.product(D, repeat=2):
                book = Ledger(orientation)
                winning_ticket = int(orientation < 0)
                book.fill(Quote(0), -orientation, 14, winning_ticket)
                q = Quote(first * -orientation)
                book.observe(q)
                if first >= 150:
                    q = Quote((first+second) * -orientation)
                    book.observe(q)
                self.assertTrue(book.flatten(q))
                self.assertGreaterEqual(book.low, -100)
                self.assertEqual(book.snapshot(q)["pnl"] > 0, (first >= 150 and first + second >= 450))

    def test_gross_cap_at_every_fill(self):
        b = Ledger(-1)
        for _ in range(4):
            for side in (1,-1):
                b.fill(Quote(0),side,50)
                self.assertLessEqual(b.gross,500)
                self.assertLessEqual(abs(b.net),50)

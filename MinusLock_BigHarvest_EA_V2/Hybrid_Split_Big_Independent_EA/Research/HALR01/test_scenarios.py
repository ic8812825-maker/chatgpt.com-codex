import unittest
from scenarios import exhaustive, sample
from simulate import run


class ScenarioTest(unittest.TestCase):
    def test_exhaustive_support(self):
        self.assertEqual(len(set(exhaustive())), 31250)

    def test_reproducible_and_mirrored(self):
        self.assertEqual(list(sample(99, 20)), list(sample(99, 20)))
        for v in ("K", "A1", "A2", "A3", "B1", "B2", "B3", "B4"):
            a = run(v, (1, (300, 300, -300, 100, -50, 0), "constant"))
            b = run(v, (-1, (-300, -300, 300, -100, 50, 0), "constant"))
            self.assertAlmostEqual(a.pnl, b.pnl)

    def test_adaptive_and_blocked_liquidation(self):
        s = (1, (300, 300, -4000, 0, 0, 0), "persistent_failure")
        self.assertGreater(run("B1", s, budget=100).remaining, 0)
        self.assertTrue(run("B1", s, budget=100).violations)
        self.assertLessEqual(run("M-probability", (1, (0,)*6, "adaptive")).pnl, -58)
        self.assertEqual(run("A1-strict", (1, (0,)*6, "constant")).remaining, 1.5)

    def test_no_lookahead(self):
        for v in ("A3", "B1", "M-probability"):
            a, b = [], []
            run(v, (1, (150, 150, -300), "constant"), trace=a)
            run(v, (1, (150, 150, 300), "constant"), trace=b)
            self.assertEqual(a[:3], b[:3])

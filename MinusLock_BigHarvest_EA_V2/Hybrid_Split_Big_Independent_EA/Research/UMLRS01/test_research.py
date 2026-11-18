import json
import unittest
from itertools import product

from research import Book, Event, FAMILIES, Policy, PROFILES, ROOT, named, path, run, search


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.optimization = json.loads((ROOT/"OPTIMIZATION_RESULTS.json").read_text())

    def policy(self, profile="Balanced", family="J"):
        return Policy(**self.optimization["profiles"][profile][family]["policy"])

    def test_money_invariant_and_no_double_counting(self):
        for side in (1,-1):
            b = Book(100)
            b.fill(-1, Event(-300*side), 100*side)
            b.fill(-1, Event(-300*side), -100*side)
            self.assertEqual(-58, b.mark(Event(0)))
            b.fill(0, Event(0), 100, 0)
            self.assertAlmostEqual(271, b.realized+4.5)
            self.assertAlmostEqual(-329, b.mark(Event(0))-(b.realized+4.5))
            b.fill(0, Event(0), 100, 0)
            self.assertAlmostEqual(-58, b.realized)
            self.assertAlmostEqual(18, b.fees)

    def test_full_harvest_violates_net_before_any_rebalance(self):
        b = Book(50)
        b.fill(-1, Event(-300), 50)
        b.fill(-1, Event(-300), -50)
        b.fill(-1, Event(-300), 50)
        b.fill(-1, Event(-300), -50)
        self.assertEqual(b.bad, 0)
        b.fill(0, Event(0), 50, 0)
        b.fill(0, Event(0), 50, 1)
        self.assertEqual(b.net, -100)
        self.assertEqual(b.bad, 1)

    def test_mirror_and_caps(self):
        for profile, family, seq in product(PROFILES, FAMILIES, named().values()):
            with self.subTest(profile=profile,family=family):
                mirrored = tuple(Event(-q.x,q.spread,q.slip,q.carry,q.reject) for q in seq)
                a = run(self.policy(profile,family), seq)
                b = run(self.policy(profile,family), mirrored, -1)
                self.assertEqual(a["pnl"], b["pnl"])
                self.assertEqual((a["bad"],a["open"]), (0,0))

    def test_frozen_counterexamples(self):
        p = self.policy()
        self.assertEqual(run(p, path([0]*13))["pnl"], -58)
        for seq in (path([0,150,-150,-450]), path([0,-150,150,450])):
            self.assertLess(run(p, seq)["pnl"], -58)
        self.assertGreater(run(p, named()["up"])["pnl"], 0)
        self.assertGreater(run(p, named()["down"])["pnl"], 0)

    def test_flat_just_before_target(self):
        p = self.policy()
        result = run(p, path([0,150,450,662]+[662]*9))
        self.assertAlmostEqual(result["pnl"], -.04)
        self.assertEqual(result["time"], 12)

    def test_balanced_short_adverse_lattice(self):
        p = self.policy()
        for shifts in product((-300,-150,0,150,300),repeat=3):
            for spread,reject in product((20,100),(0,1)):
                seq = [Event(0)]
                for d in shifts:
                    seq.append(Event(seq[-1].x+d,spread,4,.02,reject))
                seq.extend([Event(seq[-1].x,spread,4,.02)]*9)
                for side in (1,-1):
                    r = run(p, tuple(seq), side)
                    self.assertGreaterEqual(r["low"]+1e-8, -p.budget)
                    self.assertEqual((r["bad"],r["open"],r["forced"]), (0,0,False))

    def test_adversarial_paths_replay(self):
        report = json.loads((ROOT/"TEST_RESULTS.json").read_text())
        for label, events in report["adversarial_paths"].items():
            _, profile, family, orientation = label.split("_")
            r = run(self.policy(profile,family),tuple(Event(**e) for e in events),int(orientation))
            self.assertEqual((r["bad"],r["open"]), (0,0))
            if family == "J":
                self.assertGreaterEqual(r["low"] + 1e-8, -self.policy(profile,family).budget)

    def test_branch_bound_agrees_with_exhaustive(self):
        candidates = [Policy(f,50,25) for f in FAMILIES]
        suite = [(k,s,d) for k,s in named().items() for d in (1,-1)]
        bounded, _, _ = search(candidates,suite)
        exhaustive, _, _ = search(candidates,suite,branch_bound=False)
        self.assertEqual(bounded,exhaustive)

    def test_broker_latency_invalidates_same_quote_bound(self):
        b = Book(100)
        b.fill(-1,Event(-300),100)
        b.fill(-1,Event(-300),-100)
        b.fill(0,Event(0),100,0)
        b.attempt = 0
        self.assertFalse(b.fill(0,Event(0,reject=1),100,0))
        adverse = Event(300,100,4,.02)
        b.realized -= adverse.carry
        b.fill(1,adverse,100,0)
        self.assertAlmostEqual(b.realized,-402.02)


if __name__ == "__main__":
    unittest.main()

import unittest
from a3rc import Params
from exhaustive2 import brute, exact
from ledger2 import Limits
from meta_rc import choose_m
from runner import run
from scenarios2 import Scenario, sample, stress


class CoverageTest(unittest.TestCase):
    def test_quotient_matches_uncompressed_both_orientations(self):
        for o in (-1,1):
            for variant, selector in (("A3-RC",None),("M-RC",choose_m),("K-EXECUTABLE",None)):
                p=Params(trigger=0,depth=4)
                limits=Limits(horizon=3)
                actual,_=exact(variant,o,p,limits,selector)
                self.assertEqual(actual,brute(variant,o,p,limits,selector))

    def test_no_lookahead_prefix(self):
        for orientation in (-1,1):
            a,b=[],[]
            run("M-RC",Scenario(orientation,(150,300,-300,0)),Limits(horizon=4),
                selector=choose_m,journal=a)
            run("M-RC",Scenario(orientation,(150,300,300,0)),Limits(horizon=4),
                selector=choose_m,journal=b)
            self.assertEqual([e for e in a if e["step"]<=2],[e for e in b if e["step"]<=2])

    def test_stress_liveness_and_replay(self):
        self.assertEqual(list(sample(5,24)),list(sample(5,24)))
        s=next(s for s in stress(8) if s.name=="no_liquidity")
        self.assertIn("DEADLINE",run("K-EXECUTABLE",s).violations)
        self.assertIn("DEADLINE",run("A3-RC",s).violations)

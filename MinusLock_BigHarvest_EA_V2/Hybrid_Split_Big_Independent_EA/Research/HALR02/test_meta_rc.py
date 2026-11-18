import itertools
import unittest
from execution import Quote
from ledger2 import Limits
from meta_rc import DELEGATES, D, bellman, choose_b, choose_k, weights
from a3rc import choose_a3
from runner import Cycle


class MetaTest(unittest.TestCase):
    def test_delegation_paths(self):
        for label, selector in (("A3",choose_a3),("B4-RC",choose_b),("K",choose_k)):
            expected = Cycle(label,1,Limits(horizon=2),selector=selector)
            actual = Cycle(label,1,Limits(horizon=2),selector=DELEGATES[label])
            for t,x in enumerate((0,150,450)):
                for cycle in (expected,actual):
                    if not cycle.finish:
                        cycle.step(t, Quote(x))
            self.assertEqual(expected.result(),actual.result())

    def test_bellman_against_forward_two_step_forced_hold(self):
        pnl, net, previous = -11600, 20, 300
        p = 0.
        for d,e in itertools.product(D, repeat=2):
            if pnl+2*net*d>0 or pnl+2*net*(d+e)>0:
                p += weights(previous)[D.index(d)]*weights(d)[D.index(e)]
        value = bellman(2,pnl,net,previous,100000,20,-1,58)
        self.assertAlmostEqual(value[0],p)

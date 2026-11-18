import unittest
from execution import Quote
from ledger2 import Limits
from runner import Cycle, ideal


class CycleTest(unittest.TestCase):
    def test_k_nominal_exact_and_sequential(self):
        v = Cycle("K-EXECUTABLE",1,journal=[])
        v.step(0,Quote(0))
        r = v.result()
        self.assertEqual((r.pnl,r.cost),(-58,29))
        self.assertTrue(r.flat)
        self.assertEqual(r.pnl,ideal(Limits()).pnl)
        fills = [e for e in v.v.journal if e["event"]=="FILL"]
        self.assertGreater(len(fills),2)
        self.assertTrue(all(abs(f["net"])<=50 for f in fills))

    def test_k_partial_reject_and_residual(self):
        v = Cycle("K-EXECUTABLE",1,Limits(horizon=2))
        v.step(0,Quote(0,capacity=25))
        v.step(1,Quote(300,capacity=0,unknown=True))
        v.step(2,Quote(600,capacity=0))
        r = v.result()
        self.assertFalse(r.flat)
        self.assertIn("DEADLINE",r.violations)
        self.assertGreater(r.pending,0)
        self.assertNotEqual(r.pnl,-58)

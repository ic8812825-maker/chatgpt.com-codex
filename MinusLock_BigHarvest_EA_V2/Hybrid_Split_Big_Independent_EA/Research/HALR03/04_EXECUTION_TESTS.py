"""Tests for the independently implemented Venue."""
import importlib
import unittest

from baseline_audit import reconcile
from a3rc import Params
from execution import Intent,Quote
from ledger2 import Ledger,Limits

model=importlib.import_module("04_EXECUTION_SIMULATOR")


class ExecutionTests(unittest.TestCase):
    def test_unknown_then_cancel_race(self):
        b=Ledger(1,Limits())
        v=model.Venue(b,[])
        v.advance(0,Quote(0,unknown=True))
        o=v.submit(Intent(1,10),"same",ttl=2)
        self.assertIs(v.submit(o.intent,"same"),o)
        v.cancel(o)
        v.advance(1,Quote(150,unknown=True))
        self.assertEqual(b.net,0)
        v.advance(2,Quote(300,capacity=3,cancel_race=True))
        self.assertEqual((b.net,o.remaining,o.state.value),(3,7,"CANCELLED"))
        self.assertEqual(reconcile(v.journal,1)[0],b.mark(v.quote))

    def test_unknown_not_expired_without_ack(self):
        b=Ledger(1,Limits())
        v=model.Venue(b)
        v.advance(0,Quote(0,unknown=True))
        o=v.submit(Intent(1,10),ttl=0)
        v.advance(1,Quote(150,unknown=True))
        self.assertIn(o,v.active)
        v.advance(2,Quote(150))
        self.assertEqual(o.state.value,"EXPIRED")
        self.assertEqual(b.net,0)

    def test_partial_close_and_liveness_failure(self):
        c=model.Case(-1,(0,)*4,"E6")
        r=model.replay("K-EXECUTABLE",c,Limits(horizon=4),Params())
        self.assertFalse(r.flat)
        self.assertIn("DEADLINE",r.violations)
        self.assertEqual(r.residual,2.0)

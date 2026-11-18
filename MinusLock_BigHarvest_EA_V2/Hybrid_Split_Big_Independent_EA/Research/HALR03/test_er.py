import importlib
from itertools import product
import unittest

from baseline_audit import reconcile
from a3rc import Params
from ledger2 import Limits
from execution import Quote
from meta_rc import D

m=importlib.import_module("04_EXECUTION_SIMULATOR")
a=importlib.import_module("05_A3_ER_POLICY")


class RobustTests(unittest.TestCase):
    def test_all_short_e2_price_paths_with_extreme_spread(self):
        l=Limits(horizon=4)
        p=Params(trigger=0,net=30)
        for orientation in (-1,1):
            for d in product(D,repeat=4):
                c=m.Case(orientation,d,"E2",(20,20,20,20,20))
                r=m.replay("A3-ER",c,l,p,a.choose_er,contract=m.PROFILES["E2"])
                self.assertTrue(r.flat and not r.violations,(c,r))

    def test_detected_service_contract_breach_forces_safe(self):
        meta=importlib.import_module("06_META_ER_POLICY")
        for select in (a.choose_er,meta.choose_meta):
            c=m.ExecutionCycle("A3-ER",1,Limits(horizon=2),
                               Params(trigger=0),m.PROFILES["E1"],selector=select,journal=[])
            c.step(0,Quote(0,capacity=25,delay=1))
            self.assertTrue(c.memory.exiting)
            self.assertFalse(c.finish)
            orders=[event for event in c.v.journal if event["event"]=="CREATED"]
            self.assertTrue(orders and all(event["ticket"] is not None for event in orders))
            c.step(1,Quote(0))
            self.assertTrue(c.finish)

    def test_cost_infeasibility_and_final_flat(self):
        l=Limits(cost=20,horizon=4)
        r=m.replay("A3-ER",m.Case(1,(300,)*4),l,Params(),a.choose_er,
                   contract=m.PROFILES["E0"])
        self.assertTrue(r.flat)
        self.assertEqual(r.violations,"COST")

import unittest
from a3rc import Memory, Params, choose_a3, target
from execution import Quote, Venue
from ledger2 import Ledger, Limits
from risk import Envelope, project


class PreserveTest(unittest.TestCase):
    def test_original_floor_and_closing_projection(self):
        b = Ledger(1,Limits())
        q = Quote(0)
        after = project(b,q,target(b,q,40,core=90))
        self.assertEqual(after.net,40)
        self.assertEqual(after.tickets[1].units,90)
        self.assertFalse(after.tickets[2].original)
        self.assertEqual(b.tickets[1].units,100)

    def test_cost_guard_adopts_safe_smaller_action(self):
        b = Ledger(1,Limits(loss=100,cost=30))
        v = Venue(b)
        v.advance(0,Quote(0))
        result = choose_a3(v,Params(trigger=0,net=40),Memory(),Envelope())
        self.assertEqual(result[0],"ADJUST")
        self.assertEqual(result[-1].net,-10)

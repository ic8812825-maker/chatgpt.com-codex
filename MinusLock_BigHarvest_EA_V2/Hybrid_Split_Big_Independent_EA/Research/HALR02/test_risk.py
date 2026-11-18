import unittest
from execution import Intent, Quote, Venue
from ledger2 import Ledger, Limits
from risk import Envelope, close_plan, gate, reservations


class RiskTest(unittest.TestCase):
    def test_cost_reserve_and_one_step_limit(self):
        b = Ledger(1, Limits(loss=100,cost=30))
        v = Venue(b)
        v.advance(0,Quote(0))
        self.assertEqual(reservations(v,v.quote), (0,5800,0,200))
        self.assertEqual(gate(v,(Intent(-1,15,0),),Envelope())[1],"LOSS")
        self.assertEqual(gate(v,(Intent(-1,14,0),),Envelope())[1],"OK")
        self.assertEqual(gate(v,(Intent(1,9),),Envelope())[1],"COST")
        plan = close_plan(b,v.quote)
        self.assertEqual(sum(i.units for i in plan),200)
        self.assertEqual(gate(v,plan,Envelope())[0].gross,0)

    def test_unconfirmed_exposure_reserves_round_trip_and_blocks(self):
        b = Ledger(1,Limits())
        v = Venue(b)
        v.advance(0,Quote(0,delay=1))
        v.submit(Intent(1,10))
        self.assertEqual(reservations(v,v.quote)[2],580)
        self.assertEqual(gate(v,(),Envelope())[1],"PENDING")

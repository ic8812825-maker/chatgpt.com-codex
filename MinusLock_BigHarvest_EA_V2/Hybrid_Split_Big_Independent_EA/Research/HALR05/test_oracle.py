import unittest
from sim import run

def case():
    return dict(id="fixture",month="201501",orientation=1,
                entry=(0,109690,109710),obs=[(1800000*(i+1),109990+i*150,110010+i*150)
                                             for i in range(13)],complete=True)


class OracleTests(unittest.TestCase):
    def test_full_k_and_realized_cash(self):
        a,t,v=run(case(),"K-EXECUTABLE","QUOTE_FILL")
        self.assertTrue(v["flat"])
        self.assertEqual((v["pnl"],v["paid_cost"],v["reserve_exit"],v["realized_mid"]),
                         (-58,29,0,0))
        self.assertEqual((v["verified_fills"],v["net"]),(3,.5))

    def test_nonflat_is_not_success_and_pending(self):
        e=case()
        e["obs"]=e["obs"][:1]
        a,t,v=run(e,"K-EXECUTABLE","DELAY_ONLY")
        self.assertFalse(a["success"])
        self.assertFalse(v["flat"])
        self.assertEqual((v["pending"],v["residual"],v["reserve_exit"]),(1,2,29))

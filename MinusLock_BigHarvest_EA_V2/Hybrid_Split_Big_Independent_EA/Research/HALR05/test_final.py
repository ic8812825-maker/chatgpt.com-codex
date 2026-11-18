import unittest
from inference import block,decide,summary,tail
from sim import CFG,run
from test_oracle import case


class FinalTests(unittest.TestCase):
    def test_one_month_does_not_create_precision(self):
        r=[dict(month="201501",delta=2,m_pnl=1,k_pnl=-1)]*30000
        self.assertEqual(block(r,CFG["bootstrap"]),{})
        self.assertEqual(tail([1,2,3],.99),3)

    def test_nonflat_stays_in_confirmatory_barrier(self):
        rows=[dict(month="201501",delta=None,m_pnl=20,k_pnl=-58,
                   m_violations="DEADLINE",k_violations="")]
        s=summary(rows,CFG["bootstrap"])
        d=decide(rows,s,CFG,36)
        self.assertEqual(s["paired_flat"],0)
        self.assertIn("NONFLAT_PAIRS",d["failed_barriers"])
        self.assertEqual(d["eligible"],1)

    def test_changed_suffix_cannot_change_actions_before_it(self):
        e=case()
        f=case()
        f["obs"][3:]=[(1800000*(i+1),110190-i*250,110210-i*250) for i in range(3,13)]
        for name in ("M-ER","K-EXECUTABLE"):
            a=run(e,name,"QUOTE_FILL")[1]
            b=run(f,name,"QUOTE_FILL")[1]
            self.assertEqual([r for r in a if r["step"]<3],[r for r in b if r["step"]<3])

    def test_low_capacity_cannot_confirm_flat(self):
        for name in ("M-ER","K-EXECUTABLE"):
            out,_,o=run(case(),name,"LOW_LIQUIDITY")
            self.assertFalse(out["flat"])
            self.assertFalse(out["success"])
            self.assertGreaterEqual(o["residual"],.70)

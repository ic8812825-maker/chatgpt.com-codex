from datetime import date
import importlib
import unittest

from data_scan import DAY,MINUTE,T0,to_units
model=importlib.import_module("04_CAUSAL_REPLAY")


class CausalDataTests(unittest.TestCase):
    def test_activation_and_features_ignore_suffix(self):
        day=(date(2025,2,3).toordinal()-T0)*DAY
        t=day+8*60*MINUTE
        ts=[t-5*MINUTE,t,t+MINUTE,t+2*MINUTE,t+3*MINUTE]
        a=[110010,110010,110310,110710,110000]
        b=[x-20 for x in a]
        altered=a[:3]+[99999,110030]
        x,c=model.s2(ts,b,a,"202502")
        y,d=model.s2(ts,[v-20 for v in altered],altered,"202502")
        self.assertEqual(len(x),5)
        self.assertEqual(c,d)
        self.assertEqual([r["id"] for r in x],[r["id"] for r in y])
        self.assertEqual([r["features"] for r in x],[r["features"] for r in y])
        self.assertEqual([r["obs"][0] for r in x],[r["obs"][0] for r in y])

    def test_grid_point(self):
        self.assertEqual(to_units(b"1.104270"),(110427,6))
        with self.assertRaises(ArithmeticError):
            to_units(b"1.104271")

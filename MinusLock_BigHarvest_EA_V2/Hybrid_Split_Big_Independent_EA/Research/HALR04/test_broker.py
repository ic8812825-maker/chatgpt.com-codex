import importlib
import unittest

broker=importlib.import_module("05_EXECUTION_EVIDENCE")

def e(t,event,**fields):
    return dict(timestamp="2025-01-01T00:00:"+t+"+00:00",event=event,**fields)


class BrokerTests(unittest.TestCase):
    def test_partial_cancel_restart_unknown(self):
        q=[e("00","SEND",order_id="A",lots="1",bid="1.1000",ask="1.1001",side="BUY"),
           e("01","RESTART"), e("02","UNKNOWN",order_id="A"),
           e("03","CANCEL_SENT",order_id="A"),
           e("04","FILL",order_id="A",deal_id="a",lots=".3",price="1.10011",commission="-1"),
           e("05","CANCEL_ACK",order_id="A")]
        a=broker.summarize(q)
        self.assertEqual((a["cancel_race_fills"],a["partial_fills"],a["unresolved_orders"]),(1,1,0))
        self.assertEqual(a["p95_signed_slippage_points"],1)
        self.assertEqual(a["p95_confirmed_send_to_fill_ms"],4000)
        self.assertIsNone(a["guaranteed_capacity"])

    def test_duplicate_fill_and_missing_offset(self):
        q=[e("00","SEND",order_id="A",lots="1",bid="1.1000",ask="1.1001",side="BUY"),
           e("01","FILL",order_id="A",deal_id="a",lots=".1",price="1.1")]
        with self.assertRaises(ValueError):
            broker.summarize(q+[q[-1]])
        with self.assertRaises(ValueError):
            broker.summarize([dict(q[0],timestamp="2025-01-01T00:00:00")])

import importlib
import unittest
m=importlib.import_module("05_FILL_IMPORT")


def e(second,event,**z):
    return dict(timestamp=f"2026-01-01T00:00:{second:02}+00:00",event=event,**z)


class BrokerTests(unittest.TestCase):
    def payload(self):
        return [e(0,"SEND",order_id="o",requested_lots=1,requested_price="1.10",side="BUY"),
                e(1,"CANCEL_SENT",order_id="o"),
                e(2,"FILL",order_id="o",deal_id="d",filled_lots=".25",execution_price="1.10002")]

    def test_late_fill_and_resynchronization(self):
        a=m.analyze(self.payload()+[e(3,"RESTART"),e(4,"RECONCILE",order_id="o",
                      remaining_lots=".75",status="CANCELLED")])
        self.assertEqual((a["cancel_race_fills"],a["unresolved"],a["observed_slip_p95_points"]),(1,0,2))
        self.assertIsNone(a["guaranteed_future_capacity"])

    def test_duplicate_deal_and_invented_fill(self):
        a=self.payload()
        with self.assertRaises(ValueError):
            m.analyze(a+[a[-1]])
        with self.assertRaises(ValueError):
            m.analyze(a+[e(3,"RECONCILE",order_id="o",remaining_lots=0,status="CANCELLED")])

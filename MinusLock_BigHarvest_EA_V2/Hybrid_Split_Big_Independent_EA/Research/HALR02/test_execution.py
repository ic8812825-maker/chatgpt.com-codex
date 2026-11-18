import unittest
from execution import Intent, Quote, State, Venue


class StubBook:
    net = gross = 0

    def apply_carry(self, q):
        pass

    def observe(self, q):
        pass

    def mark(self, q):
        return 0

    def fill(self, intent, size, q):
        self.net += intent.side*size
        return size


class ExecutionTest(unittest.TestCase):
    def test_delay_partial_cancel_race_and_idempotence(self):
        b = StubBook()
        v = Venue(b, [])
        v.advance(0, Quote(0, delay=1))
        i = Intent(1, 20)
        o = v.submit(i, "id")
        self.assertIs(v.submit(i, "id"), o)
        self.assertEqual(b.net, 0)
        v.advance(1, Quote(150, capacity=5))
        self.assertEqual((o.state, b.net), (State.PARTIAL, 5))
        v.cancel(o)
        v.advance(2, Quote(300, capacity=3, cancel_race=True))
        self.assertEqual((o.state, b.net), (State.CANCELLED, 8))
        self.assertEqual([r["mid"] for r in v.journal if r["event"]=="FILL"], [150,300])

    def test_rejection_distinct_key_and_unknown_expiry(self):
        v = Venue(StubBook())
        v.advance(0, Quote(0, rejects=1))
        i = Intent(1, 10)
        self.assertEqual(v.submit(i,"a").state, State.REJECTED)
        self.assertEqual(v.submit(i,"b").state, State.FILLED)
        self.assertEqual(v.submit(i,"c").state, State.FILLED)
        self.assertEqual(v.book.net, 20)
        v.advance(1, Quote(0, unknown=True))
        o = v.submit(i, "d", ttl=0)
        self.assertEqual(o.state, State.UNKNOWN)
        v.advance(2, Quote(0))
        self.assertEqual(o.state, State.EXPIRED)

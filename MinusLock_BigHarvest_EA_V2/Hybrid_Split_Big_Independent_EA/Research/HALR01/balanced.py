"""J Balanced adapter for nominal common-quote execution only."""
from preserve import sign, target_net


class Balanced:
    def __init__(self, params):
        self.p = params
        self.entered = False
        self.stopped = False

    def act(self, book, q, step):
        if step == 0:
            book.flatten(q)
        desired = book.net
        if not self.entered and abs(q.mid) >= self.p.trigger:
            desired = sign(q.mid) * self.p.net
        future_gross = abs(desired) / 100
        entry = abs(desired-book.net) / 100 * (q.spread + q.slip + 9)
        worst = book.snapshot(q)["pnl"] - entry - future_gross * (600 + 48)
        margin = future_gross * (110000 + q.mid + 650) / 30
        if worst < -180 or 15000 + worst < 2 * margin:
            self.stopped = True
            book.flatten(q)
            return
        if desired != book.net and not self.entered:
            target_net(book, q, desired)
            self.entered = bool(book.net)

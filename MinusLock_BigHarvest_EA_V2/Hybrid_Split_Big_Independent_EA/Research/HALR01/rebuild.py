"""Conditional recovery with irreversible removal of original tickets."""
from preserve import sign, target_net


class Rebuild:
    def __init__(self, variant, params):
        self.variant, self.p = variant, params
        self.switched = False
        self.attempts = self.confirm = self.prev_side = 0
        self.anchor = self.entry = 0
        self.exit_pending = False

    def act(self, book, q, step):
        if not self.switched:
            self.switched = book.flatten(q)
            return
        if book.net:
            move = sign(book.net) * (q.mid - self.entry)
            if self.exit_pending or move <= -self.p.trigger / 2:
                self.exit_pending = True
                book.flatten(q)
                self.anchor = q.mid
            elif self.variant == "B4" and move >= self.p.trigger:
                target_net(book, q, round(book.net * (1 - self.p.harvest)))
                self.entry = q.mid
            return

        self.exit_pending = False
        limit = 1 if self.variant == "B1" else self.p.attempts
        if self.attempts >= limit:
            return
        move = q.mid - self.anchor
        side = sign(move) if abs(move) >= self.p.trigger else 0
        self.confirm = self.confirm + 1 if side and side == self.prev_side else int(bool(side))
        self.prev_side = side
        if not side or (self.variant == "B3" and self.confirm < 2):
            return
        self.attempts += 1
        target_net(book, q, side * self.p.net)
        self.entry = q.mid
        self.confirm = self.prev_side = 0

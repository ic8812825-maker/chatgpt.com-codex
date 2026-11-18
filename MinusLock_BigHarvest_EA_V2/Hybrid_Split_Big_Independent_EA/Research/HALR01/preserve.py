"""Portfolio operations and original-ticket preservation policies."""
from dataclasses import dataclass


def sign(x):
    return (x > 0) - (x < 0)


def target_net(book, quote, target, floors=None):
    """Reduce existing opposite exposure before opening a working ticket."""
    floors = floors or {}
    direction = sign(target - book.net)
    for i, ticket in list(book.tickets.items()):
        if ticket.side == -direction:
            amount = min(abs(target - book.net), ticket.units - floors.get(i, 0))
            if amount > 0 and book.fill(quote, direction, amount, i) < amount:
                return
    if target != book.net:
        book.fill(quote, direction, abs(target - book.net))


@dataclass(frozen=True)
class Params:
    net: int = 20
    core: int = 25
    trigger: int = 140
    switches: int = 3
    harvest: float = .5
    attempts: int = 2
    horizon: int = 6
    reserve: float = 0.


class Preserve:
    def __init__(self, variant, params, orientation, strict=False):
        self.variant, self.p, self.strict = variant, params, strict
        self.loser = int(orientation > 0)
        core = 100 if variant == "A1" else params.core
        self.floors = {self.loser: core}
        self.last = self.count = 0
        self.initialized = False

    def act(self, book, quote, step):
        direction = sign(quote.mid - self.last)
        if self.variant != "A3":
            direction = sign(quote.mid)
            if self.initialized or abs(quote.mid) < self.p.trigger:
                return
            self.initialized = True
            ticket = book.tickets[self.loser]
            desired = self.floors[self.loser]
            if ticket.units > desired:
                balance = min(50, ticket.units - desired)
                book.fill(quote, -ticket.side, balance, self.loser)
            target_net(book, quote, direction * self.p.net, self.floors)
            return
        if abs(quote.mid - self.last) >= self.p.trigger and self.count < self.p.switches:
            self.last = quote.mid
            self.count += 1
            desired = direction * self.p.net
            if book.net * desired < 0:
                target_net(book, quote, 0, self.floors)
            target_net(book, quote, desired, self.floors)
        elif book.net:
            harvesting = any(not t.original and t.side * (quote.mid-t.entry) > self.p.trigger
                             for t in book.tickets.values())
            if harvesting:
                target_net(book, quote, round(book.net * (1 - self.p.harvest)), self.floors)

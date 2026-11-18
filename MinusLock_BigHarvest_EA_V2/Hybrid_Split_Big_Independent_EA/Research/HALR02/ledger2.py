"""Exact half-cent ledger. Lots and price offsets are integer units."""
from dataclasses import dataclass, replace
from execution import Intent


TICKS = 200


@dataclass(frozen=True, slots=True)
class Limits:
    loss: int = 180
    cost: int = 50
    net: int = 50
    gross: int = 500
    capital: int = 15000
    leverage: int = 30
    margin_level: int = 20000  # basis points, 200%
    stopout: int = 5000
    commission: int = 9  # half cents per 0.01 lot on each side
    horizon: int = 8


@dataclass(frozen=True, slots=True)
class Ticket:
    side: int
    units: int
    entry: int
    original: bool


def fee(q, limits):
    return q.spread + 2*q.slip + limits.commission


class Ledger:
    def __init__(self, orientation, limits):
        if orientation not in (-1, 1):
            raise ValueError("orientation must be +1 or -1")
        self.limits = limits
        self.orientation = orientation
        entry = -300*orientation
        self.tickets = {0: Ticket(1,100,entry,True), 1: Ticket(-1,100,entry,True)}
        self.next_id = 2
        self.initial_cost = (20+limits.commission)*200
        self.realized = self.commission = self.spread = self.slip = self.swap = 0
        self.peak = self.low = self.dd = self.max_gross = self.max_net = 0
        self.margin_stress = 0.
        self.violations = set()
        self.fills = 0

    def clone(self):
        b = object.__new__(Ledger)
        b.__dict__ = self.__dict__.copy()
        b.tickets = self.tickets.copy()
        b.violations = self.violations.copy()
        return b

    @property
    def net(self):
        return sum(t.side*t.units for t in self.tickets.values())

    @property
    def gross(self):
        return sum(t.units for t in self.tickets.values())

    @property
    def spent(self):
        return self.commission + self.spread + self.slip + self.swap

    def exit_cost(self, q):
        return self.gross * fee(q,self.limits)

    def mark(self, q):
        unrealized = sum(2*t.side*t.units*(q.mid-t.entry) for t in self.tickets.values())
        return self.realized + unrealized - self.initial_cost - self.spent - self.exit_cost(q)

    def margin_numerator(self, q):
        return self.gross * max(0, 220000 + 2*q.mid + q.spread)

    def level_ok(self, q, threshold, mark=None):
        equity = self.limits.capital*TICKS + (self.mark(q) if mark is None else mark)
        return equity*self.limits.leverage*10000 >= self.margin_numerator(q)*threshold

    def observe(self, q):
        mark = self.mark(q)
        self.peak = max(self.peak, mark)
        self.low = min(self.low, mark)
        self.dd = max(self.dd,self.peak-mark)
        self.max_net = max(self.max_net,abs(self.net))
        self.max_gross = max(self.max_gross,self.gross)
        self.margin_stress = max(self.margin_stress, self.margin_numerator(q) /
                                 (self.limits.leverage*max(1,self.limits.capital*TICKS+mark)))
        if mark < -self.limits.loss*TICKS:
            self.violations.add("LOSS")
        if self.spent+self.exit_cost(q) > self.limits.cost*TICKS:
            self.violations.add("COST")
        if not self.level_ok(q,self.limits.margin_level):
            self.violations.add("MARGIN")
        if abs(self.net)>self.limits.net or self.gross>self.limits.gross:
            self.violations.add("EXPOSURE")

    def apply_carry(self, q):
        self.swap += self.gross*q.carry

    def fill(self, intent: Intent, units, q):
        side = intent.side
        if side not in (-1,1) or type(units) is not int or units<=0:
            return 0
        existing = self.tickets.get(intent.ticket)
        if intent.ticket is not None and (existing is None or existing.side != -side):
            return 0
        max_amount = existing.units if existing else self.limits.gross-self.gross
        amount = min(units, max_amount, self.limits.net-side*self.net)
        if amount<=0:
            return 0
        self.commission += self.limits.commission*amount
        self.spread += q.spread*amount
        self.slip += 2*q.slip*amount
        if existing:
            self.realized += 2*existing.side*amount*(q.mid-existing.entry)
            if amount == existing.units:
                del self.tickets[intent.ticket]
            else:
                self.tickets[intent.ticket] = replace(existing,units=existing.units-amount)
        else:
            self.tickets[self.next_id] = Ticket(side,amount,q.mid,False)
            self.next_id += 1
        self.fills += 1
        self.observe(q)
        return amount

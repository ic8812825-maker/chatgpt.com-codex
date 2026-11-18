"""Offline EURUSD ledger. Quantity is an integer number of 0.01 lots."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    commission: float = 4.5
    capital: float = 15000
    net_limit: int = 50
    gross_limit: int = 500
    leverage: float = 30
    stop_out: float = 0.5


@dataclass(frozen=True)
class Quote:
    mid: int
    spread: float = 20
    slip: float = 0
    swap_cost: float = 0
    fill_cap: int = 500
    reject: bool = False
    delay: bool = False


@dataclass
class Ticket:
    side: int
    units: int
    entry: int
    original: bool


class Ledger:
    def __init__(self, orientation, config=Config()):
        if orientation not in (-1, 1):
            raise ValueError("orientation")
        self.config = config
        self.orientation = orientation
        self.tickets = {0: Ticket(1, 100, -300 * orientation, True),
                        1: Ticket(-1, 100, -300 * orientation, True)}
        self.next_id = 2
        self.realized = self.swap = self.slippage = 0.
        self.spread_cost = 20.
        self.commission = 2 * config.commission
        self.turnover = 2.
        self.failures = 0
        self.peak = self.drawdown = self.margin_stress = 0.
        self.low = 0.
        self.observe(Quote(0))

    @property
    def gross(self):
        return sum(t.units for t in self.tickets.values())

    @property
    def net(self):
        return sum(t.side * t.units for t in self.tickets.values())

    @property
    def costs(self):
        return self.spread_cost + self.commission + self.slippage + self.swap

    def snapshot(self, q):
        unrealized = sum(t.side * t.units * (q.mid - t.entry)
                         for t in self.tickets.values()) / 100
        reserve = self.gross / 100 * (q.spread / 2 + self.config.commission + q.slip)
        pnl = self.realized + unrealized - self.costs - reserve
        equity = self.config.capital + pnl
        margin = self.gross / 100 * max(0, 110000 + q.mid + q.spread / 2) / self.config.leverage
        return dict(realized=self.realized, unrealized=unrealized, costs=self.costs,
                    reserve=reserve, pnl=pnl, equity=equity, margin=margin,
                    free_margin=equity-margin, gross=self.gross/100, net=self.net/100)

    def observe(self, q):
        s = self.snapshot(q)
        self.low = min(self.low, s["pnl"])
        self.peak = max(self.peak, s["pnl"])
        self.drawdown = max(self.drawdown, self.peak - s["pnl"])
        ratio = s["margin"] / max(1e-12, s["equity"])
        self.margin_stress = max(self.margin_stress, ratio)
        return bool(s["margin"] and s["equity"] <= self.config.stop_out * s["margin"])

    def carry(self, q):
        self.swap += self.gross / 100 * q.swap_cost

    def fill(self, q, side, units, ticket=None):
        if side not in (-1, 1) or not isinstance(units, int) or units <= 0:
            raise ValueError("invalid order")
        if q.reject or q.delay:
            self.failures += 1
            return 0
        closing = ticket is not None
        t = self.tickets.get(ticket)
        if closing and (t is None or t.side != -side):
            raise ValueError("unknown ticket or wrong side")
        n = min(units, q.fill_cap, self.config.net_limit - side * self.net,
                t.units if closing else self.config.gross_limit - self.gross)
        if n < units:
            self.failures += 1
        if n <= 0:
            return 0
        if not closing:
            projected = self.snapshot(q)
            cost = n / 100 * (q.spread + 2 * (q.slip + self.config.commission))
            margin = (self.gross+n)/100 * max(0,110000+q.mid+q.spread/2)/self.config.leverage
            if projected["equity"] - cost < margin:
                self.failures += 1
                return 0
        lot = n / 100
        self.spread_cost += lot * q.spread / 2
        self.commission += lot * self.config.commission
        self.slippage += lot * q.slip
        self.turnover += lot
        if closing:
            self.realized += lot * t.side * (q.mid - t.entry)
            t.units -= n
            if not t.units:
                del self.tickets[ticket]
        else:
            self.tickets[self.next_id] = Ticket(side, n, q.mid, False)
            self.next_id += 1
        self.observe(q)
        return n

    def flatten(self, q, floors=None):
        floors = floors or {}
        while True:
            for i, t in list(self.tickets.items()):
                n = min(t.units - floors.get(i, 0),
                        self.config.net_limit + t.side * self.net)
                if n > 0 and self.fill(q, -t.side, n, i):
                    if q.fill_cap < 500:
                        return False
                    break
            else:
                return all(t.units <= floors.get(i, 0) for i, t in self.tickets.items())

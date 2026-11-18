"""Deterministic event-driven execution venue for the offline study."""
from dataclasses import dataclass
from enum import Enum


class State(str, Enum):
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCEL_PENDING = "CANCEL_PENDING"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


TERMINAL = {State.FILLED, State.REJECTED, State.CANCELLED, State.EXPIRED}


@dataclass(frozen=True, slots=True)
class Quote:
    mid: int
    spread: int = 20
    slip: int = 0
    carry: int = 0  # half-cents per 0.01 lot per event
    capacity: int = 1000  # total executable volume across orders this event
    rejects: int = 0
    delay: int = 0
    unknown: bool = False
    cancel_race: bool = False


@dataclass(frozen=True, slots=True)
class Intent:
    side: int
    units: int
    ticket: int | None = None


@dataclass(slots=True)
class Order:
    key: str
    intent: Intent
    remaining: int
    eligible: int
    expires: int
    state: State = State.CREATED
    cancellation: int | None = None


class Venue:
    """Serial and capacity-limited. The ledger changes only in the fill callback."""
    def __init__(self, book, journal=None):
        self.book = book
        self.orders = {}
        self.journal = journal
        self.counter = 0
        self.failures = 0

    def emit(self, name, order=None, **extra):
        if self.journal is not None:
            self.journal.append(dict(step=self.step, mid=self.quote.mid, event=name,
                                     order=order.key if order else None, **extra))

    def status(self, order, value):
        order.state = value
        self.emit(value.value, order, remaining=order.remaining)

    @property
    def active(self):
        return tuple(o for o in self.orders.values() if o.state not in TERMINAL)

    def advance(self, step, quote):
        self.step, self.quote = step, quote
        self.capacity, self.rejects = quote.capacity, quote.rejects
        self.emit("QUOTE", spread=quote.spread, slip=quote.slip, capacity=quote.capacity,
                  rejects=quote.rejects, delay=quote.delay, carry=quote.carry)
        if step:
            self.book.apply_carry(quote)
        self.book.observe(quote)
        for order in self.active:
            self.service(order)

    def submit(self, intent, key=None, ttl=4):
        if key is None:
            self.counter += 1
            key = f"order-{self.counter}"
        if key in self.orders:
            prior = self.orders[key]
            if intent != prior.intent:
                raise ValueError("idempotency key reused with different intent")
            self.emit("DUPLICATE_QUERY", prior)
            return prior
        order = Order(key, intent, intent.units, self.step+self.quote.delay, self.step+ttl)
        self.orders[key] = order
        self.emit(State.CREATED.value, order, side=intent.side, units=intent.units,
                  ticket=intent.ticket, eligible=order.eligible, expires=order.expires)
        self.status(order, State.SUBMITTED)
        if self.rejects:
            self.rejects -= 1
            self.failures += 1
            self.status(order, State.REJECTED)
        elif self.quote.unknown:
            self.failures += 1
            self.status(order, State.UNKNOWN)
        else:
            self.status(order, State.ACCEPTED)
            self.service(order)
        return order

    def cancel(self, order):
        if order.state not in TERMINAL and order.cancellation is None:
            order.cancellation = self.step+1
            self.status(order, State.CANCEL_PENDING)

    def service(self, order):
        if order.state in TERMINAL:
            return
        cancel_due = order.cancellation is not None and self.step >= order.cancellation
        if self.step > order.expires:
            self.failures += 1
            self.status(order, State.EXPIRED)
            return
        if cancel_due and not self.quote.cancel_race:
            self.status(order, State.CANCELLED)
            return
        if self.quote.unknown or self.step < order.eligible or not self.capacity:
            return
        if order.state == State.UNKNOWN:
            self.status(order, State.ACCEPTED)
        units = self.book.fill(order.intent, min(order.remaining,self.capacity), self.quote)
        if units:
            self.capacity -= units
            order.remaining -= units
            self.emit("FILL", order, units=units, side=order.intent.side,
                      ticket=order.intent.ticket, pnl=self.book.mark(self.quote),
                      net=self.book.net, gross=self.book.gross)
        if not order.remaining:
            self.status(order, State.FILLED)
        elif cancel_due:
            self.status(order, State.CANCELLED)
        elif not units:
            self.failures += 1
            self.status(order, State.REJECTED)
        else:
            self.status(order, State.PARTIAL if order.cancellation is None else State.CANCEL_PENDING)

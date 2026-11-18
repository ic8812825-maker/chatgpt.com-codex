"""Check an action, every planned fill, and liquidation to the next deadline."""
from dataclasses import dataclass, replace
from execution import Intent, Quote
from ledger2 import TICKS, fee


@dataclass(frozen=True, slots=True)
class Envelope:
    move: int = 300
    spread: int = 20
    slip: int = 0
    carry: int = 0
    window: int = 1  # price events until an assured uninterrupted liquidation quote
    reserve: int = 0  # additional dollar loss room


def reservations(venue, q):
    b = venue.book
    pending_open = sum(o.remaining for o in venue.active if o.intent.ticket is None)
    executed, exit_cost = b.spent, b.exit_cost(q)
    reserved = 2*pending_open*fee(q,b.limits)
    return executed, exit_cost, reserved, b.limits.cost*TICKS-executed-exit_cost-reserved


def close_intent(book):
    for ticket, t in book.tickets.items():
        allowed = book.limits.net + t.side*book.net
        q = min(allowed,t.units)
        if q>0:
            return Intent(-t.side,q,ticket)


def close_plan(book, q):
    trial = book.clone()
    plan = []
    while trial.gross:
        i = close_intent(trial)
        if i is None or not trial.fill(i,i.units,q):
            return None
        plan.append(i)
    return tuple(plan)


def project(book, q, plan):
    trial = book.clone()
    if plan is None:
        return None
    for i in plan:
        if trial.fill(i,i.units,q) != i.units:
            return None
    return trial


def gate(venue, plan, env):
    """Return projected ledger or a binding exclusion code."""
    b, q = venue.book, venue.quote
    if venue.active:
        return None, "PENDING"
    if plan is None:
        return None, "NO_PLAN"
    if plan and (q.delay or q.unknown or venue.rejects or
                 venue.capacity < sum(i.units for i in plan)):
        return None, "FILL_UNCERTAIN"
    trial = project(b,q,plan)
    if trial is None:
        return None, "FILL_LIMIT"
    if trial.violations:
        return None, sorted(trial.violations)[0]
    if not trial.gross:
        return trial, "OK"
    if venue.step+env.window > b.limits.horizon:
        return None, "TIME"
    if b.limits.net <= 0 or q.spread>env.spread or q.slip>env.slip or q.carry>env.carry:
        return None, "ENVELOPE"
    distance = env.move*env.window
    expensive = replace(q,mid=q.mid+distance,spread=env.spread,slip=env.slip)
    exit_fee = trial.exit_cost(expensive)
    carry = env.carry*env.window*trial.gross
    future = trial.mark(q)-2*abs(trial.net)*distance-(exit_fee-trial.exit_cost(q))-carry
    if future < -(b.limits.loss-env.reserve)*TICKS:
        return None, "LOSS"
    if trial.spent+exit_fee+carry > b.limits.cost*TICKS:
        return None, "COST"
    if not trial.level_ok(expensive,b.limits.margin_level,future):
        return None, "MARGIN"
    return trial, "OK"

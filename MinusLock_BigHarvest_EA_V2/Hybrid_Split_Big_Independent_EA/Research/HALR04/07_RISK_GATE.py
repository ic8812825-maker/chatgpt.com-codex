"""Independent exposure, liquidity, cost, and liquidation gate."""
from dataclasses import replace

from dependencies import setup
setup()
from risk import close_intent

TICKS=200


def fee(q,commission):
    return q.spread+2*q.slip+commission


def balances(book,q):
    gross=sum(t.units for t in book.tickets.values())
    net=sum(t.units*t.side for t in book.tickets.values())
    actual=book.commission+book.spread+book.slip+book.swap
    unrealized=sum(t.side*t.units*2*(q.mid-t.entry) for t in book.tickets.values())
    reserve=gross*fee(q,book.limits.commission)
    value=book.realized+unrealized-book.initial_cost-actual-reserve
    return dict(gross=gross,net=net,paid=actual,reserve=reserve,mark=value)


def violations(book,q,points=0,max_spread=None,max_slip=None,carry=0):
    r=balances(book,q)
    l=book.limits
    s=q.spread if max_spread is None else max_spread
    k=q.slip if max_slip is None else max_slip
    upper_fee=s+2*k+l.commission
    extra=max(0,r["gross"]*upper_fee-r["reserve"])
    reserve=r["reserve"]+extra
    lower=r["mark"]-2*abs(r["net"])*points-extra-carry
    bad=[]
    if lower < -TICKS*l.loss:bad.append("LOSS")
    if r["paid"]+reserve+carry > TICKS*l.cost:bad.append("COST")
    if r["gross"]>l.gross or abs(r["net"])>l.net:bad.append("EXPOSURE")
    eq=l.capital*TICKS+lower
    maximum_mid=q.mid+points
    if eq*l.leverage*10000 < r["gross"]*max(0,220000+2*maximum_mid+s)*l.margin_level:
        bad.append("MARGIN")
    return tuple(bad)


def close_orders(book,q):
    b=book.clone()
    orders=[]
    while b.gross:
        i=close_intent(b)
        if i is None or b.fill(i,i.units,q)!=i.units:
            return None
        orders.append(i)
    return tuple(orders)


def service_now(v,required):
    q=v.quote
    return not (q.delay or q.unknown or v.rejects) and v.capacity>=required


def assess(v,plan,execution_contract=None):
    """Return stable reasons and the projected book, with no mutation of v."""
    b,q=v.book,v.quote
    if v.active:
        return ("PENDING",),None
    if plan is None:
        return ("NO_PLAN",),None
    if not service_now(v,sum(i.units for i in plan)):
        return ("SERVICE_UNAVAILABLE",),None
    if violations(b,q):
        return violations(b,q),None
    trial=b.clone()
    for order in plan:
        if trial.fill(order,order.units,q)!=order.units:
            return ("FILL_INCOMPLETE",),None
        bad=violations(trial,q)
        if bad:
            return bad,None
    if not trial.gross:
        return (),trial
    e=execution_contract
    if e is None or e.move is None or e.stride is None:
        return ("NO_CONFIRMED_FUTURE_SERVICE",),None
    if q.spread>e.spread or q.slip>e.slip or q.carry>e.carry:
        return ("OUTSIDE_COST_ENVELOPE",),None
    if v.step%e.stride or not service_now(v,sum(i.units for i in plan)+trial.gross):
        return ("NO_CURRENT_SERVICE_WINDOW",),None
    window=e.next_service(v.step)-v.step
    if v.step+window>b.limits.horizon:
        return ("DEADLINE",),None
    if trial.limits.net<=0 or e.move<0:
        return ("NO_CLOSING_SEQUENCE",),None
    bad=violations(trial,q,e.move*window,e.spread,e.slip,trial.gross*window*e.carry)
    return (bad,None) if bad else ((),trial)


def close_assessment(v):
    return assess(v,close_orders(v.book,v.quote))


def observed_pending(v):
    b=v.book
    q=v.quote
    open_units=sum(o.remaining for o in v.active if o.intent.ticket is None)
    return dict(count=len(v.active),opening_units=open_units,
                exit_and_incremental_reserve=balances(b,q)["reserve"]+
                2*open_units*fee(q,b.limits.commission))

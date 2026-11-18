"""Common decision/confirmation loop for every executable policy."""
from dataclasses import dataclass, replace
from a3rc import Memory, Params, choose_a3, sign
from execution import Quote, State, Venue
from ledger2 import Ledger, Limits, TICKS
from risk import Envelope, close_intent, reservations


@dataclass(frozen=True, slots=True)
class Outcome:
    pnl: float
    low: float
    drawdown: float
    cost: float
    gross: float
    net: float
    margin: float
    forced: int
    residual: float
    pending: int
    failures: int
    violations: str
    success: bool
    flat: bool
    time: int
    core_closed_early: bool
    cost_with_reserve: float
    margin_stopout: bool
    action_counts: tuple


class Cycle:
    def __init__(self, name, orientation, limits=Limits(), params=Params(),
                 envelope=Envelope(), journal=None, selector=None):
        self.name, self.params = name, params
        self.env = replace(envelope,reserve=params.reserve)
        self.book = Ledger(orientation, limits)
        self.v = Venue(self.book,journal)
        self.memory = Memory(exiting=name=="K-EXECUTABLE")
        self.selector = selector or choose_a3
        self.finish = False
        self.forced = 0
        self.stopout = False
        self.core_closed_early = False
        self.max_cost = 0
        self.actions = {}

    def monitor(self):
        b,v = self.book,self.v
        _,_,_,remaining = reservations(v,v.quote)
        self.max_cost = max(self.max_cost,b.limits.cost*TICKS-remaining)
        if remaining<0:
            b.violations.add("COST")
        adds = {s: sum(o.remaining for o in v.active if o.intent.side==s)
                for s in (-1,1)}
        opens = sum(o.remaining for o in v.active if o.intent.ticket is None)
        if b.gross+opens>b.limits.gross or any(s*b.net+adds[s]>b.limits.net for s in adds):
            b.violations.add("PENDING_EXPOSURE")

    def record(self, name):
        self.actions[name] = self.actions.get(name,0)+1
        self.v.emit(name)

    def execute(self, plan):
        for i in plan:
            if self.v.active:
                return False
            o = self.v.submit(i,ttl=3)
            self.monitor()
            if o.state != State.FILLED:
                return False
        return True

    def exit(self):
        v = self.v
        for o in v.active:
            if o.intent.ticket is None:
                v.cancel(o)
        if not v.active:
            while self.book.gross:
                i = close_intent(self.book)
                if i is None or not self.execute((i,)):
                    break
        self.finish = not self.book.gross and not v.active

    def clone_nominal(self):
        """Clone after a confirmed nominal event, discarding archive-only orders."""
        if self.v.active:
            raise ValueError("nominal clone requires all orders terminal")
        out = object.__new__(Cycle)
        out.__dict__ = self.__dict__.copy()
        out.book = self.book.clone()
        out.v = Venue(out.book)
        out.v.step, out.v.quote = self.v.step,self.v.quote
        out.actions = self.actions.copy()
        return out

    def step(self, t, q):
        self.v.advance(t,q)
        self.monitor()
        b,p,m = self.book,self.params,self.memory
        target_hit = b.mark(q)>0
        stop = not b.level_ok(q,b.limits.stopout)
        if self.name!="K-EXECUTABLE" and (stop or (b.violations and self.name.endswith("-RC"))):
            self.forced = 1
        self.stopout |= stop
        if m.exiting or target_hit or stop or t>=b.limits.horizon-p.time_buffer or (
                b.violations and self.name.endswith("-RC")):
            if target_hit:
                self.record("TARGET")
            elif not m.exiting:
                self.record("DEADLINE_OR_FORCED")
                self.core_closed_early |= bool(t<b.limits.horizon and b.gross)
            self.memory = replace(m,exiting=True)
            self.exit()
            return
        if self.v.active:
            self.record("PENDING")
            return
        label,plan,next_memory,_ = self.selector(self.v,p,m,self.env)
        self.record(label)
        if label=="SAFE":
            self.forced = 1
            self.core_closed_early |= bool(b.gross and t<b.limits.horizon)
            self.memory = replace(m,exiting=True)
            self.exit()
        elif self.execute(plan):
            self.memory = next_memory
            if next_memory.exiting:
                self.exit()

    def result(self):
        b,v = self.book,self.v
        mark = b.mark(v.quote)
        flat = not b.gross and not v.active
        violations = b.violations | ({"DEADLINE"} if not flat else set())
        return Outcome(mark/TICKS,b.low/TICKS,b.dd/TICKS,b.spent/TICKS,b.max_gross/100,
                       b.max_net/100,b.margin_stress,self.forced,b.gross/100,len(v.active),
                       v.failures,"|".join(sorted(violations)),flat and mark>0,flat,v.step,
                       self.core_closed_early,self.max_cost/TICKS,self.stopout,
                       tuple(sorted(self.actions.items())))


def ideal(limits):
    # Analytic control. Its $29 future close cost remains visible to feasibility.
    costs = (20+limits.commission)
    loss = 2*costs
    bad = []
    if costs>limits.cost:
        bad.append("COST")
    if loss>limits.loss:
        bad.append("LOSS")
    return Outcome(-loss,-loss,loss,costs,2.,0.,0.,0,0.,0,0,"|".join(bad),
                   False,True,0,False,costs,False,())


def run(name, scenario, limits=Limits(), params=Params(), envelope=Envelope(),
        selector=None, journal=None):
    if name=="K-IDEAL":
        return ideal(limits)
    cycle=Cycle(name,scenario.orientation,limits,params,envelope,journal,selector)
    mid=0
    for t in range(limits.horizon+1):
        cycle.step(t,scenario.quote(t,mid))
        if cycle.finish:
            break
        if t<limits.horizon:
            mid += -300*sign(cycle.book.net) if scenario.adaptive else scenario.moves[t]
    return cycle.result()

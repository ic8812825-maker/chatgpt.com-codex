"""Original Core first, with the independent risk gate upstream of execution."""
from dataclasses import dataclass, replace
from execution import Intent
from risk import gate


@dataclass(frozen=True, slots=True)
class Params:
    core: int = 25
    net: int = 20
    trigger: int = 150
    switches: int = 3
    harvest: int = 50  # integer percent
    attempts: int = 2
    neutral: bool = True
    reserve: int = 0
    depth: int = 2
    time_buffer: int = 0
    direction: int = 1


@dataclass(frozen=True, slots=True)
class Memory:
    anchor: int = 0
    switches: int = 0
    attempts: int = 0
    b_mode: bool = False
    exiting: bool = False


def sign(x):
    return (x>0)-(x<0)


def target(book, quote, desired, core=0, allow_open=True, neutral=False):
    """Return an ordered set of intents with immutable original IDs."""
    b = book.clone()
    plan = []
    loser = 1 if b.orientation>0 else 0
    targets = (0, desired) if neutral and b.net*desired<0 else (desired,)
    for n in targets:
        side = sign(n-b.net)
        ids = sorted(b.tickets, key=lambda i: (b.tickets[i].original,i))
        for i in ids:
            t = b.tickets[i]
            if t.side != -side:
                continue
            volume = min(abs(n-b.net), t.units-(core if i==loser else 0))
            if volume > 0:
                intent = Intent(side, volume, i)
                if b.fill(intent,volume,quote) != volume:
                    return None
                plan.append(intent)
        remainder = abs(n-b.net)
        if remainder and allow_open:
            intent = Intent(side,remainder)
            if b.fill(intent,remainder,quote) != remainder:
                return None
            plan.append(intent)
    return tuple(plan)


def choices_a3(v, p, memory):
    b, q = v.book, v.quote
    move = q.mid-memory.anchor
    direction = sign(move) or -b.orientation
    signal = abs(move)>=p.trigger and memory.switches < p.switches
    if signal:
        for n in dict.fromkeys((p.net,max(1,p.net//2),max(1,p.net//4))):
            desired = direction*p.direction*n
            if desired == b.net:
                break
            plan = target(b,q,desired,p.core,neutral=p.neutral)
            if plan:
                yield "ADJUST", plan, replace(memory,anchor=q.mid,switches=memory.switches+1)
    if b.net*move>0 and abs(move)>=max(1,p.trigger//2) and p.harvest:
        n = sign(b.net)*(abs(b.net)*(100-p.harvest)//100)
        plan = target(b,q,n,p.core,allow_open=False)
        if plan:
            yield "HARVEST",plan,replace(memory,anchor=q.mid)
    yield "WAIT" if not b.gross else "HOLD",(),memory


def choose_a3(v,p,memory,env):
    for label,plan,next_memory in choices_a3(v,p,memory):
        projected, reason = gate(v,plan,env)
        if projected is not None:
            return label,plan,next_memory,projected
    return "SAFE", None, replace(memory,exiting=True), None

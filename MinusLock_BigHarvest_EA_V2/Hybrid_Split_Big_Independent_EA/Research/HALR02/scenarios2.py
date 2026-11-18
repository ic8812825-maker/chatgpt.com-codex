"""Common causal price and independent execution scripts."""
from dataclasses import dataclass, replace
from random import Random

from execution import Quote
from meta_rc import D, weights


@dataclass(frozen=True, slots=True)
class Scenario:
    orientation: int
    moves: tuple
    name: str = "nominal"
    events: tuple = ()
    adaptive: bool = False

    def quote(self, step, mid):
        for t, fields in self.events:
            if t==step:
                return Quote(mid,**dict(fields))
        return Quote(mid)


def sample(seed,n,horizon=12):
    rng=Random(seed)
    for _ in range(n):
        orientation=rng.choice((-1,1))
        moves=[]
        prev=0
        for _ in range(horizon):
            prev=rng.choices(D,weights(prev))[0]
            moves.append(prev)
        yield Scenario(orientation,tuple(moves))


def stress(h):
    scripts = {
        "up": ((150,)*h,{},False),
        "down": ((-150,)*h,{},False),
        "flat": ((0,)*h,{},False),
        "tight": ((30,-30)*h,{},False),
        "wide": ((300,-300)*h,{},False),
        "false_breaks": ((180,-175,-180,175)*h,{},False),
        "rapid_reverse": ((300,300,-300,-300)*h,{},False),
        "trend_flat_reverse": ((300,150,0,0,-300,-300)*h,{},False),
        "adaptive_price": ((0,)*h,{},True),
        "gap": ((300,300,-4000)+(0,)*h,{},False),
        "spread": ((300,300,0,-300)+(0,)*h,{2:dict(spread=100,slip=4,carry=1)},False),
        "partial": ((300,-300)*h,{0:dict(capacity=25),1:dict(capacity=13)},False),
        "second_reject": ((300,-300)*h,{0:dict(capacity=50),1:dict(rejects=1)},False),
        "delay": ((300,-300)*h,{0:dict(delay=2),2:dict(capacity=50)},False),
        "reject_gap": ((300,300,-4000)+(0,)*h,{t:dict(rejects=100) for t in range(2,h+1)},False),
        "unknown": ((300,-300)*h,{t:dict(unknown=True) for t in range(h+1)},False),
        "no_liquidity": ((150,-150)*h,{t:dict(capacity=0) for t in range(h+1)},False),
        "stopout_gap": ((300,300,-90000)+(0,)*h,{2:dict(capacity=0)},False),
        "cancel_race": ((300,300,-300)+(0,)*h,
                        {0:dict(delay=1),1:dict(capacity=5),
                         2:dict(cancel_race=True,spread=100)},False),
        "execution_adversary": ((0,)*h,{t:dict(capacity=23,slip=4,
                                      delay=int(t%3==0),rejects=int(t%3==1))
                                      for t in range(h+1)},True),
        "all_rejected": ((0,)*h,{t:dict(rejects=100) for t in range(h+1)},False),
        "core_carry": ((0,)*h,{t:dict(carry=1) for t in range(1,h+1)},False),
    }
    for orientation in (-1,1):
        for name,(moves,events,adaptive) in scripts.items():
            for mirror in (-1,1):
                yield Scenario(orientation,tuple(mirror*x for x in moves[:h]),name,
                               tuple((i,tuple(d.items())) for i,d in sorted(events.items())),adaptive)

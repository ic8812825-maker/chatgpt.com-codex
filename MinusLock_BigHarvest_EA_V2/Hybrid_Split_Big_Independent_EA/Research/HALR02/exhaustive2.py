"""Exact nominal D-tree with terminal multiplicities and loss-preserving memoization."""
from collections import namedtuple
from itertools import product

from execution import Quote
from ledger2 import Limits, TICKS
from meta_rc import D
from runner import Cycle, run
from scenarios2 import Scenario


Counts = namedtuple("Counts","paths successes violations worst low residual flat")


class NodeLimit(Exception):
    pass


def exact(variant, orientation, params, limits, selector=None, node_limit=150000):
    cache = {}
    h = limits.horizon
    root = Cycle(variant,orientation,limits,params,selector=selector)
    root.step(0,Quote(0))

    def visit(cycle, t):
        b,v = cycle.book,cycle.v
        mark = b.mark(v.quote)
        if cycle.finish or t==h:
            count=5**(h-t)
            flat=not b.gross and not v.active
            return Counts(count,count*int(flat and mark>0),
                          count*int(bool(b.violations) or not flat),mark,mark,
                          count*int(not flat),count*int(flat))
        key=(t,v.quote.mid,cycle.memory,b.realized,b.spent,b.next_id,
             tuple(b.tickets.items()),tuple(sorted(b.violations)))
        if key not in cache:
            if len(cache)>=node_limit:
                raise NodeLimit(len(cache))
            out=[]
            for d in D:
                child=cycle.clone_nominal()
                child.book.low=0
                child.step(t+1,Quote(v.quote.mid+d))
                row=visit(child,t+1)
                out.append(row._replace(low=min(row.low,child.book.low)))
            cache[key]=Counts(sum(x.paths for x in out),sum(x.successes for x in out),
                              sum(x.violations for x in out),min(x.worst for x in out),
                              min(mark,*(x.low for x in out)),sum(x.residual for x in out),
                              sum(x.flat for x in out))
        return cache[key]

    out=visit(root,0)
    return out._replace(low=min(out.low,root.book.low)),len(cache)


def brute(variant,orientation,p,limits=Limits(horizon=3),selector=None):
    outcomes=[run(variant,Scenario(orientation,d),limits,p,selector=selector)
              for d in product(D,repeat=limits.horizon)]
    return Counts(len(outcomes),sum(o.success for o in outcomes),
                  sum(bool(o.violations) for o in outcomes),
                  round(min(o.pnl for o in outcomes)*TICKS),
                  round(min(o.low for o in outcomes)*TICKS),
                  sum(not o.flat for o in outcomes),sum(o.flat for o in outcomes))

"""Audit realized, pending, residual, intracycle risk and paired completed PnL."""
import importlib
import json
from pathlib import Path

from dependencies import setup
setup()
from a3rc import Params
from ledger2 import Limits
from scenarios2 import stress
exe=importlib.import_module("04_EXECUTION_SIMULATOR")
money=importlib.import_module("02_MONEY_ORACLE")


class ArchivedCase:
    def __init__(self,case):
        self.case=case
        self.orientation=case.orientation
    def quote(self,t,mid):
        return self.case.quote(t,mid)
    def next_move(self,t,net):
        return -300*((net>0)-(net<0)) if self.case.adaptive else self.case.moves[t]


def audit():
    h=12
    lim=Limits(horizon=h)
    out={}
    history=list(stress(h))
    settings={"K-EXECUTABLE":None,
              "A3-ER":importlib.import_module("05_A3_ER_POLICY").choose_er,
              "M-ER":importlib.import_module("06_META_ER_POLICY").choose_meta}
    qs={}
    for name,selector in settings.items():
        outcomes=[]
        out[name]=dict(cases=0,fills=0,flat=0,residual=0,pending=0)
        for c in history:
            trace=[]
            outcome=exe.replay(name,ArchivedCase(c),lim,Params(),selector,trace,
                               exe.PROFILES["E1"] if name.endswith("-ER") else None)
            oracle=money.MoneyOracle(c.orientation).replay(trace)
            assert oracle.mark()==200*outcome.pnl or abs(oracle.mark()-200*outcome.pnl)<1e-8
            assert oracle.flat==outcome.flat
            assert oracle.exposure()[0]/100==outcome.residual
            assert len(oracle.active)==outcome.pending
            assert abs(oracle.actual_incremental_cost/200-outcome.cost)<1e-8
            assert min(0,min(row[2] for row in oracle.history))/200==outcome.low
            out[name]["cases"]+=1
            out[name]["fills"]+=sum(e["event"]=="FILL" for e in trace)
            out[name]["flat"]+=outcome.flat
            out[name]["residual"]+=outcome.residual>0
            out[name]["pending"]+=outcome.pending>0
            outcomes.append(outcome)
        qs[name]=outcomes
    for case,v in qs.items():
        diff=[x.pnl-y.pnl for x,y in zip(v,qs["K-EXECUTABLE"]) if x.flat and y.flat]
        out[case]["paired_flat"]=len(diff)
        out[case]["max_additional_loss"]=max(0,-min(diff)) if diff else None
    return out

if __name__=="__main__":
    print(json.dumps(audit(),indent=2))

"""Run the archived 88 stresses through the common new Venue and cash-flow oracle."""
from dataclasses import asdict
import json
from pathlib import Path

from baseline_audit import reconcile
from experiments import GRID,ROUTES,model,summarize,write
from ledger2 import Limits
from scenarios2 import stress


class LegacyStress:
    def __init__(self,scenario):
        self.scenario=scenario
        self.orientation=scenario.orientation

    def quote(self,t,mid):
        return self.scenario.quote(t,mid)

    def next_move(self,t,net):
        return -300*((net>0)-(net<0)) if self.scenario.adaptive else self.scenario.moves[t]


if __name__=="__main__":
    cfg=json.loads(Path("08_FROZEN_GRID.json").read_text())
    indices={r["policy"]:r["grid"] for r in cfg["selected"]
             if r["profile"]=="E1" and r["horizon"]==12}
    summary,detail=[],[]
    for variant,selector in ROUTES.items():
        if variant=="K-IDEAL":
            continue
        outcomes=[]
        fills=0
        contract=model.PROFILES["E1"] if variant.endswith("-ER") else None
        for i,case in enumerate(stress(12)):
            logs=[]
            out=model.replay(variant,LegacyStress(case),Limits(horizon=12),
                             GRID[indices.get(variant,0)],selector,
                             journal=logs,contract=contract)
            mark,n=reconcile(logs,case.orientation)
            assert mark==round(out.pnl*200)
            fills+=n
            outcomes.append(out)
            detail.append(dict(policy=variant,case=case.name,index=i,orientation=case.orientation,
                               pnl=out.pnl,low=out.low,flat=out.flat,residual=out.residual,
                               pending=out.pending,violations=out.violations,confirmed_fills=n))
        summary.append(dict(policy=variant,oracle_fills=fills,**summarize(outcomes)))
    write("08_HALR02_STRESS_BRIDGE",summary)
    write("08_HALR02_STRESS_OUTCOMES",detail)

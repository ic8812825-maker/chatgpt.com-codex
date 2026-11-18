"""Compare adaptive core and strict core on a fixed diagnostic sample."""
from csv import DictWriter
from dataclasses import replace
import importlib
from statistics import mean

from baseline_audit import source
from a3rc import Params
from execution import Intent
from ledger2 import Limits
from scenarios2 import sample

m=importlib.import_module("04_EXECUTION_SIMULATOR")
a=importlib.import_module("05_A3_ER_POLICY")


class Strict(m.ExecutionCycle):
    def exit(self):
        if self.book.mark(self.v.quote)>0:
            return super().exit()
        b,v=self.book,self.v
        loser=1 if b.orientation>0 else 0
        if v.active:
            return
        while b.gross:
            for i,t in b.tickets.items():
                floor=self.params.core if i==loser else 0
                n=min(t.units-floor,b.limits.net+t.side*b.net)
                if n>0:
                    if not self.execute((Intent(-t.side,n,i),)):
                        return
                    break
            else:
                break
        self.finish=not b.gross and not v.active


def trials():
    out=[]
    for key in ("E0","E1","E2"):
        for mode in (m.ExecutionCycle,Strict):
            outcomes=[]
            for s in sample(30105,256,12):
                c=m.Case(s.orientation,s.moves,key)
                l=Limits(horizon=12)
                cy=mode("A3-ER",c.orientation,l,Params(),m.PROFILES[key],selector=a.choose_er)
                mid=0
                for i in range(13):
                    cy.step(i,c.quote(i,mid))
                    if cy.finish:
                        break
                    if i<12:
                        mid+=c.moves[i]
                outcomes.append(cy.result())
            out.append(dict(profile=key,mode=mode.__name__,n=len(outcomes),
                            recoveries=sum(o.success for o in outcomes),flat=sum(o.flat for o in outcomes),
                            risk_violations=sum(bool(o.violations) for o in outcomes),
                            early_core=sum(o.core_closed_early for o in outcomes),
                            worst=min(o.pnl for o in outcomes),mean_new_cost=mean(o.cost for o in outcomes),
                            average_peak_gross=mean(o.gross for o in outcomes),
                            peak_margin=max(o.margin for o in outcomes)))
    return out


if __name__=="__main__":
    rows=trials()
    with open("05_A3_ER_ABLATIONS.csv","w",newline="") as f:
        w=DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

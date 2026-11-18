"""Risk replay independent of controller aggregates."""
import importlib
from fractions import Fraction

money=importlib.import_module("06_MONEY_ORACLE")


def check(episode,trace,limits,out):
    _ ,bid,ask=episode["entry"]
    m=money.Money(bid+ask-220000,ask-bid,limits.commission)
    low=0
    max_gross=max_net=0
    highest=0.
    risk=set()
    peak_total=0
    peak_pending_reserve=0
    for record in trace:
        if m.observe(record):
            pnl=m.mark()
            low=min(low,pnl)
            max_gross=max(max_gross,m.gross)
            max_net=max(max_net,abs(m.net))
            equity=limits.capital*200+pnl
            margin=Fraction(m.gross*max(0,220000+m.mid2+m.spread),limits.leverage)
            highest=max(highest,float(margin/max(1,equity)))
            if pnl < -limits.loss*200:risk.add("LOSS")
            if m.gross>limits.gross or abs(m.net)>limits.net:risk.add("EXPOSURE")
            if margin*limits.margin_level>equity*10000:risk.add("MARGIN")
            if m.spent+m.reserve>200*limits.cost:risk.add("COST")
        if record["event"] in ("QUOTE","FILL","ACCEPTED","UNKNOWN","CANCEL_PENDING","REJECTED","FILLED","CANCELLED","EXPIRED"):
            new_open=sum(n for _,n,t in m.pending.values() if t is None)
            reserved=2*new_open*(m.spread+2*m.slip+m.commission)
            peak_pending_reserve=max(peak_pending_reserve,reserved)
            peak_total=max(peak_total,m.spent+m.reserve+reserved)
    if not m.flat:risk.add("DEADLINE")
    checks={"pnl":m.mark()/200,"low":low/200,"gross":max_gross/100,
            "net":max_net/100,"margin":highest,"cost":m.spent/200,
            "residual":m.gross/100,"pending":len(m.pending),"flat":m.flat}
    for k,v in checks.items():
        if abs(out[k]-v)>1e-8:
            raise AssertionError((k,out[k],v))
    if not risk.issubset(set(out["violations"].split("|"))):
        raise AssertionError((risk,out["violations"]))
    if m.flat and m.mark()!=m.cash:
        raise AssertionError("Nonzero reserve at FLAT")
    return dict(**checks,end_net=m.net/100,verified_fills=sum(r["event"]=="FILL" for r in trace),
                realized_mid=m.realized_mid/200,paid_cost=m.spent/200,
                reserve_exit=m.reserve/200,pending_open_max_reserve=peak_pending_reserve/200,
                conservative_total_reserve_peak=peak_total/200,
                observed_violations="|".join(sorted(risk)))

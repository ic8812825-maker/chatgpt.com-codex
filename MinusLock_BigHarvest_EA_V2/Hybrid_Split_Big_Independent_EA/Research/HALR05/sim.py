"""Route to immutable HALR04 policies, changing only preregistered venue profiles."""
from dataclasses import asdict,replace
import importlib
import json
from pathlib import Path
from pinned import setup
setup()
import replay

CFG=json.loads(Path(__file__).with_name("03_FROZEN_PROTOCOL.json").read_text())
NAMES=("M-ER","K-EXECUTABLE","A3-ER")
PINNED_MODE={"QUOTE_FILL":"quote_fill","BOUNDED_SLIPPAGE":"bounded_slip",
             "DELAYED_PARTIAL":"delayed_partial","COMPOUND_STRESS":"compound_stress"}
oracle=importlib.import_module("06_RISK_ORACLE")


def external(record,t,mode):
    q=replay.quote(record,t,"quote_fill")
    p=CFG["execution"][mode]
    if "delay" in p:
        return replace(q,delay=p["delay"])
    if "capacity" in p:
        return replace(q,capacity=p["capacity"])
    return replace(q,rejects=p.get("rejects_first_event",0) if not t else 0,
                   unknown=p.get("unknown_from",0)<=t<p.get("unknown_until",0))


def run(e,policy,mode):
    trace=[]
    if mode in PINNED_MODE:
        out=replay.run(e,policy,PINNED_MODE[mode],journal=trace)
    else:
        s=replay.venue.ExecutionCycle(policy,e["orientation"],replay.limits(),
                 replay.Params(),selector=replay.DEFAULTS[policy],journal=trace,
                 **({"envelope":replay.venue.PROFILES["E1"]} if policy.endswith("-ER") else {}))
        replay.initial_state(s,e)
        for t,r in enumerate(e["obs"]):
            s.step(t,external(r,t,mode))
            if s.finish:break
        out=asdict(s.result())
        out.update(elapsed_ms=e["obs"][t][0]-e["obs"][0][0],quote_events=t+1,
                   attempts=sum(r["event"]=="CREATED" for r in trace))
    checks=oracle.check(e,trace,replay.limits(),out)
    for record in trace:
        record["quote_utc_ms"]=e["obs"][record["step"]][0]+18000000
    return out,trace,checks

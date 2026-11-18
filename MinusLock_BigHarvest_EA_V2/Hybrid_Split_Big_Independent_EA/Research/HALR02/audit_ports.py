"""Quantify decision-rule port parity under common nominal quotes."""
from dataclasses import replace
from pathlib import Path
import argparse
import json
import sys

from comparators import SETTINGS
from ledger2 import Limits
from runner import run
from scenarios2 import sample


def audit(source):
    sys.path.insert(0,str(source.resolve()))
    from simulate import run as reference
    from preserve import Params as LegacyParams
    archive = {"A3-original": "A3", "B4":"B4", "M-original":"M-probability", "J-Balanced":"J Balanced"}
    results = []
    paths = list(sample(20261119,256,8))
    for case,old in archive.items():
        p,selector=SETTINGS[case]
        lp=LegacyParams(net=p.net,core=p.core,trigger=p.trigger,switches=p.switches,
                        harvest=p.harvest/100,attempts=p.attempts,horizon=12 if case=="J-Balanced" else 8,reserve=p.reserve)
        errors=[]
        for s in paths:
            original=reference(old,(s.orientation,s.moves,"stochastic"),lp,180)
            port=run(case,s,Limits(),p,selector=selector)
            errors.append(abs(original.pnl-port.pnl))
        results.append(dict(policy=case,n=len(paths),equal=sum(e<1e-7 for e in errors),max_error=max(errors)))
    return results


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path)
    print(json.dumps(audit(p.parse_args().source),indent=2))

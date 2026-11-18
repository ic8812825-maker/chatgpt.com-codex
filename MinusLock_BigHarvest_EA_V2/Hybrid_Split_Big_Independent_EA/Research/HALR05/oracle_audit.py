"""Validate oracle on unchanged archived cohorts before the new holdout."""
from collections import Counter
import importlib
import json
from pathlib import Path
import sys

from sim import NAMES,CFG,run,replay


def audit(folder):
    raw=json.loads((Path(folder)/"episodes.json").read_text())
    cases=[e for e in raw if e["fold"]=="final_test" and e["scheme"]=="S2" and e["interval"]==30]
    assert len(cases)==69
    c=Counter()
    for e in cases:
        for mode in CFG["execution"]:
            for name in NAMES:
                out,trace,checked=run(e,name,mode)
                c["paths"]+=1
                c["fills"]+=checked["verified_fills"]
                c["flat"]+=out["flat"]
                c["residual_or_pending"]+=not out["flat"]
                if mode=="QUOTE_FILL":
                    assert out==replay.run(e,name,"quote_fill")
                    c["exact_dispatch_parities"]+=1
    return dict(c,source="HALR04 prior cohort; not new test",passed=True)


if __name__=="__main__":
    a=audit(sys.argv[1])
    Path("06_AUDIT_RESULTS.json").write_text(json.dumps(a,indent=2)+"\n")
    print(a)

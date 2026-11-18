"""Verify the unchanged HALR03 episode definition and its historical controls."""
import csv
import json
from pathlib import Path
import sys

from dependencies import setup
h2,h3=setup()
from replay import run

path=Path(sys.argv[1])
with path.open() as f:
    cases=[e for e in json.load(f) if e["month"]=="202407" and e["scheme"]=="S1"]
assert len(cases)==9
with (h3/"07_HISTORICAL_RESULTS.csv").open() as f:
    obs={(r["execution"],r["variant"]):r for r in csv.DictReader(f) if r["month"]=="202407"}
comp=[]
for mode in ("quote_fill","bounded_slip","delayed_partial"):
    for policy in ("A3-ER","M-ER","K-EXECUTABLE"):
        r=[run(e,policy,mode) for e in cases]
        original=obs[mode,policy]
        n,fl,v=sum(o["success"] for o in r),sum(o["flat"] for o in r),sum(bool(o["violations"]) for o in r)
        assert (n,fl,v)==tuple(int(original[k]) for k in ("recoveries","flat","violations"))
        assert abs(min(o["pnl"] for o in r)-float(original["worst_liquidation_mark"]))<1e-8
        comp.append(dict(mode=mode,policy=policy,episodes=len(r),recovered=n,flat=fl,violations=v))
print(json.dumps(comp,indent=2))

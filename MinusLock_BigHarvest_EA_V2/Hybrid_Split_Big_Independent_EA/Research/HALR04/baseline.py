"""Verifiable baseline manifest and frozen economic control."""
from csv import DictReader
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from dependencies import setup
h2,h3=setup()
from ledger2 import Ledger,Limits
from execution import Quote

def runs():
    before={p.name:sha256(p.read_bytes()).hexdigest() for p in h3.glob("08*.csv")}
    before["10_INCREMENTAL_VALUE_VS_K.csv"]=sha256((h3/"10_INCREMENTAL_VALUE_VS_K.csv").read_bytes()).hexdigest()
    for name in ("verify_halr03.py","experiments.py"):
        args=["--frozen"] if name=="experiments.py" else []
        subprocess.run([sys.executable,"-B",name,*args],cwd=h3,check=True)
    return {k:sha256((h3/k).read_bytes()).hexdigest()==v for k,v in before.items()}

def evidence():
    q=Quote(0)
    controls=[]
    for sign in (-1,1):
        b=Ledger(sign,Limits())
        assert b.mark(q)==-11600 and b.initial_cost==5800 and b.exit_cost(q)==5800
        controls.append(dict(orientation=sign,mark=b.mark(q)/200,
                             initial_cost=b.initial_cost/200,exit_reserve=b.exit_cost(q)/200,
                             gross=b.gross,net=b.net))
    with (h3/"08_ROBUSTNESS_MATRIX.csv").open() as f:
        e=next(r for r in DictReader(f) if r["panel"]=="E1/12/markov/180/50" and r["policy"]=="A3-ER")
    return dict(initial=controls,e1={k:e[k] for k in ("seed","grid","n","recoveries","mean_pnl","worst_pnl","cvar99")},
                baseline_test_report=json.loads((h3/"TEST_RESULTS.json").read_text()),
                python=sys.version.split()[0])

if __name__=="__main__":
    result=evidence()
    if "--run" in sys.argv:
        result["replay_csv_identical"]=runs()
        assert all(result["replay_csv_identical"].values())
    print(json.dumps(result,indent=2))

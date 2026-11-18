"""Verify the archived controls and byte-compare the full independent replay."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def verify(original, replay):
    names = ("COMPARISON_RESULTS.csv","EXHAUSTIVE_RESULTS.csv","ADVERSARIAL_RESULTS.csv",
             "COST_BUDGET_FRONTIER.csv","PAIRED_COMPARISON.csv","OPTIMAL_PARAMETERS.csv")
    checks = {}
    for name in names:
        a,b = original/name,replay/name
        checks[name] = dict(archived=hashlib.sha256(a.read_bytes()).hexdigest(),
                            replay=hashlib.sha256(b.read_bytes()).hexdigest(),
                            identical=a.read_bytes()==b.read_bytes())
    a3 = next(r for r in rows(replay/"COMPARISON_RESULTS.csv") if r["label"]=="A3-selected")
    horizons = [r for r in rows(replay/"EXHAUSTIVE_RESULTS.csv")
                if r["label"]=="A3-selected" and r["horizon"]=="12"]
    stresses = rows(replay/"ADVERSARIAL_RESULTS.csv")
    tests = json.loads((replay/"TEST_RESULTS.json").read_text())
    controls = dict(successes=int(a3["recoveries"]), trials=int(a3["n"]),
                    wilson=[float(a3["wilson_lo"]),float(a3["wilson_hi"])],
                    mean=float(a3["mean_pnl"]),worst_sample=float(a3["worst_pnl"]),
                    worst_tree=min(float(r["low"]) for r in horizons),
                    paths=sum(int(r["paths"]) for r in horizons),
                    orientations=sorted(int(r["orientation"]) for r in horizons),
                    worst_stress=min(float(r["pnl"]) for r in stresses if r["label"]=="A3-selected"),
                    stress_counts={p:sum(bool(r["violations"]) for r in stresses if r["label"]==p)
                                   for p in ("A3-selected","K-EXECUTABLE")},
                    tests=tests["tests"],tests_passed=tests["passed"])
    assert all(c["identical"] for c in checks.values()), checks
    assert controls["paths"]==488281250 and controls["orientations"]==[-1,1]
    assert controls["successes"]==981 and controls["worst_tree"]==-175
    assert controls["stress_counts"]=={"A3-selected":32,"K-EXECUTABLE":24}
    assert controls["tests_passed"] and controls["tests"]==15
    return dict(controls=controls, comparisons=checks)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("archived",type=Path)
    parser.add_argument("replay",type=Path)
    parser.add_argument("--run",action="store_true")
    args=parser.parse_args()
    if args.run:
        shutil.copytree(args.archived,args.replay)
        for command in (("study2.py",),("audit2.py",)):
            subprocess.run([sys.executable,"-B",*command],cwd=args.replay,check=True,
                           stdout=sys.stderr)
    print(json.dumps(verify(args.archived,args.replay),indent=2))

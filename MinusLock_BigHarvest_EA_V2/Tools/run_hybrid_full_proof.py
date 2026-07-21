#!/usr/bin/env python3
"""Run tests, compile proof tools, generate evidence and compute final status."""
from __future__ import annotations
import csv, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; REPORTS=ROOT/"Reports"; TOOLS=ROOT/"Tools"
def run(cmd): return subprocess.run(cmd,cwd=ROOT.parent,text=True).returncode==0
def rows(name):
    with (REPORTS/name).open(encoding="utf-8") as f:return list(csv.DictReader(f))
def main():
    pytest_ok=run([sys.executable,"-m","pytest","-q",str(ROOT/"Tests")])
    files=[TOOLS/x for x in ("prove_hybrid_split_big.py","hybrid_geometry_model.py","optimize_hybrid_geometry.py","simulate_hybrid_split_big.py")]
    compile_ok=run([sys.executable,"-m","py_compile",*map(str,files)])
    if not (pytest_ok and compile_ok): return 1
    if not run([sys.executable,str(TOOLS/"prove_hybrid_split_big.py"),"--seed","20260721","--reports",str(REPORTS),"--pytest-status","PASS","--pycompile-status","PASS"]): return 1
    big=rows("HYBRID_BIG_100_SCENARIOS.csv"); small=rows("HYBRID_SMALL_100_REVERSALS.csv"); stress=rows("HYBRID_STRESS_TEST.csv"); counter=rows("HYBRID_COUNTEREXAMPLES.csv"); stability=rows("HYBRID_PARAMETER_STABILITY.csv"); money=rows("HYBRID_MONEY_CONSERVATION.csv")
    accepted_big=[r for r in big if r["Result"]=="PASS"]; accepted_small=[r for r in small if r["Result"]=="PASS"]
    law1=bool(accepted_big) and all(r["Law1Status"]=="PASS" for r in accepted_big)
    law2=bool(accepted_big) and all(r["Law2Status"]=="PASS" and r["PointSweep"]=="True" for r in accepted_big)
    law3=bool(accepted_small) and all(r["Law3Status"]=="PASS" and r["Completion"] in {"CYCLE_FULLY_CLOSED","VALID_SMALLER_NEXT_CYCLE"} for r in accepted_small)
    conservation=all(abs(float(r["Residual"]))<=1e-8 for r in money)
    values=dict(Law1="PASS" if law1 else "FAIL",Law2="PASS" if law2 else "FAIL",Law3="PASS" if law3 else "FAIL",Pytest="PASS" if pytest_ok else "FAIL",PyCompile="PASS" if compile_ok else "FAIL",BigScenarios="PASS" if law1 and law2 else "FAIL",SmallScenarios="PASS" if law3 else "FAIL",StressScenarios="PASS" if all(r["Result"] in {"PASS","SAFE_REJECTED"} for r in stress) else "FAIL",Counterexamples="PASS" if all(r["Result"]=="PASS" for r in counter) else "FAIL",MoneyConservation="PASS" if conservation else "FAIL",ParameterStability="PASS" if all(r["Result"]=="PASS" for r in stability) else "FAIL")
    overall=all(v=="PASS" for v in values.values()); manual=(ROOT/"Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md").is_file() and overall
    values.update(Repository="ic8812825-maker/chatgpt.com-codex",Branch="work",SourceCodeCommit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT.parent,text=True).strip(),ReportsCommit="PENDING_FINAL_COMMIT",FinalRepositoryHead="PENDING_FINAL_COMMIT",ManualCreated=str(manual).lower(),OverallResult="PASS" if overall else "FAIL")
    with (REPORTS/"HYBRID_FINAL_LAW_STATUS.csv").open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=values,lineterminator="\n");w.writeheader();w.writerow(values)
    return 0 if overall else 1
if __name__=="__main__":raise SystemExit(main())

#!/usr/bin/env python3
"""The sole authority that runs checks and derives final proof status."""
from __future__ import annotations
import csv,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPORTS=ROOT/"Reports"; TOOLS=ROOT/"Tools"
def run(cmd): return subprocess.run(cmd,cwd=ROOT.parent).returncode==0
def rows(n):
 with (REPORTS/n).open(encoding="utf-8") as f:return list(csv.DictReader(f))
def status(ok): return "PASS" if ok else "FAIL"
def main():
 files=[TOOLS/x for x in ("prove_hybrid_split_big.py","hybrid_geometry_model.py","hybrid_big_sequence_model.py","hybrid_small_state_machine.py","validate_hybrid_proof_reports.py","check_russian_commit_messages.py","run_hybrid_full_proof.py")]
 pytest_ok=run([sys.executable,"-m","pytest","-q",str(ROOT/"Tests")]); compile_ok=run([sys.executable,"-m","py_compile",*map(str,files)])
 proof_ok=pytest_ok and compile_ok and run([sys.executable,str(TOOLS/"prove_hybrid_split_big.py"),"--seed","20260721","--reports",str(REPORTS)])
 if not proof_ok or not run([sys.executable,str(TOOLS/"validate_hybrid_proof_reports.py")]): return 1
 big=rows("HYBRID_BIG_100_SCENARIOS.csv");trace=rows("HYBRID_RECOVERY_POINT_SWEEP.csv");small=rows("HYBRID_SMALL_100_REVERSALS.csv");seq=rows("HYBRID_BIG_LEVEL_SEQUENCE.csv");bm=rows("HYBRID_BIG_MONEY_CONSERVATION.csv");sm=rows("HYBRID_SMALL_MONEY_CONSERVATION.csv");counter=rows("HYBRID_COUNTEREXAMPLES.csv");stress=rows("HYBRID_STRESS_TEST.csv");stability=rows("HYBRID_PARAMETER_STABILITY.csv")
 accepted_trace=[r for r in trace if r["Result"]=="PASS"];accepted_seq=[r for r in seq if r["Result"]=="PASS"]
 point=bool(accepted_trace) and all(r["Status"]=="PASS" for r in accepted_trace); sequence=bool(accepted_seq) and all(r["Law1SequenceStatus"]=="PASS" for r in accepted_seq); coverage=sequence and all(float(r["CoverageDeficitBefore"])<=1e-9 or float(r["CoverageDeficitAfter"])<float(r["CoverageDeficitBefore"]) for r in accepted_seq)
 big_money=bool(bm) and all(abs(float(r["Residual"]))<=1e-8 for r in bm); small_money=bool(sm) and all(abs(float(r["Residual"]))<=1e-8 and r["FinalReserveUsedForTransition"]=="False" for r in sm)
 accepted_small=[r for r in small if r["Result"]=="PASS"];small_ok=bool(accepted_small) and all(r["Completion"] in {"VALID_SMALLER_NEXT_CYCLE","CYCLE_FULLY_CLOSED"} and r["NoOldFar"]=="True" and r["NoOldTrend"]=="True" and r["NoOldSmall"]=="True" for r in accepted_small)
 c_ok=len(counter)>=15 and all(r["Result"]=="PASS" and r["ExpectedRejectReason"]==r["ActualRejectReason"] for r in counter) and any(r["ActualRejectReason"]=="TRANSITION_LOSS" for r in counter)
 stress_ok=bool(stress) and all(r["Result"] in {"PASS","SAFE_REJECTED"} for r in stress); stab_ok=bool(stability) and all(r["Result"]=="PASS" for r in stability)
 law1=bool(big) and point and sequence and coverage and big_money and c_ok;law2=point and stress_ok and c_ok;law3=small_ok and small_money and c_ok
 manual_path=ROOT/"Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md";manual_exists=manual_path.is_file();manual_valid=manual_exists and manual_path.stat().st_size>4000
 values={"Repository":"ic8812825-maker/chatgpt.com-codex","Branch":"work","SourceCodeCommit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT.parent,text=True).strip(),"EvidenceGenerationCommit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT.parent,text=True).strip(),"Law1":status(law1),"Law2":status(law2),"Law3":status(law3),"Pytest":status(pytest_ok),"PyCompile":status(compile_ok),"BigSequentialCatchUp":status(sequence and coverage),"PointSweep":status(point),"SmallStateMachine":status(small_ok),"BigMoneyConservation":status(big_money),"SmallMoneyConservation":status(small_money),"StressScenarios":status(stress_ok),"Counterexamples":status(c_ok),"ParameterStability":status(stab_ok),"ManualFileExists":str(manual_exists).lower(),"ManualValidated":str(manual_valid).lower()}
 overall=all(v=="PASS" for k,v in values.items() if k not in {"Repository","Branch","SourceCodeCommit","EvidenceGenerationCommit","ManualFileExists","ManualValidated"}) and manual_valid;values.update(ManualAllowed=str(overall).lower(),ManualCreated=str(manual_exists and overall).lower(),OverallResult=status(overall),ReportsCommit="PENDING_COMMIT",ManualCommit="PENDING_COMMIT",FinalStatusCommit="PENDING_COMMIT",RemoteWorkHeadAtVerification="PENDING_PUSH")
 with (REPORTS/"HYBRID_FINAL_LAW_STATUS.csv").open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=values,lineterminator="\n");w.writeheader();w.writerow(values)
 return 0 if overall else 1
if __name__=="__main__":raise SystemExit(main())

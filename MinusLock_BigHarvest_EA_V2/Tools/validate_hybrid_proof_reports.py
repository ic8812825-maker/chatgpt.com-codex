#!/usr/bin/env python3
"""Structural validator used independently from final status aggregation."""
import csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/"Reports"
FILES=("HYBRID_BIG_100_SCENARIOS.csv","HYBRID_BIG_LEVEL_SEQUENCE.csv","HYBRID_RECOVERY_POINT_SWEEP.csv","HYBRID_SMALL_100_REVERSALS.csv","HYBRID_SMALL_STATE_MACHINE.csv","HYBRID_STRESS_TEST.csv","HYBRID_COUNTEREXAMPLES.csv","HYBRID_PARAMETER_STABILITY.csv","HYBRID_BIG_MONEY_CONSERVATION.csv","HYBRID_SMALL_MONEY_CONSERVATION.csv","HYBRID_NEXT_CYCLE_RISK.csv","HYBRID_FINAL_LAW_STATUS.csv")
def main():
 missing=[]
 for n in FILES:
  p=R/n
  if not p.is_file() or p.stat().st_size==0:missing.append(n)
 if missing: print("Отсутствуют отчёты:",", ".join(missing));return 1
 seq=list(csv.DictReader((R/"HYBRID_BIG_LEVEL_SEQUENCE.csv").open()));counter=list(csv.DictReader((R/"HYBRID_COUNTEREXAMPLES.csv").open()))
 if {int(x["Level"]) for x in seq}!={1,2,3,4,5,6,7} or len(counter)<15 or not any(x["ActualRejectReason"]=="TRANSITION_LOSS" for x in counter):return 1
 print("Структура доказательных CSV проверена");return 0
if __name__=="__main__":raise SystemExit(main())

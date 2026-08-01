#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"Tools"))
from stage_3_1_5_money_oracle import BLOCKERS, causal_results

def main():
    missing=ineffective=vacuous=0
    clean=causal_results()
    for rule in BLOCKERS:
        if rule not in clean: missing += 1; continue
        if clean[rule] != 0: vacuous += 1
        if causal_results({rule})[rule] != 1: ineffective += 1
    print(f"REGISTERED_CAUSAL_RULES={len(BLOCKERS)}")
    print(f"MISSING_CAUSAL_RULES={missing}")
    print(f"INEFFECTIVE_CAUSAL_RULES={ineffective}")
    print(f"VACUOUS_CAUSAL_RULES={vacuous}")
    ok=missing==ineffective==vacuous==0
    print("BLOCKER_CAUSAL_AUDIT="+("PASS" if ok else "FAIL"))
    raise SystemExit(0 if ok else 1)
if __name__=="__main__": main()

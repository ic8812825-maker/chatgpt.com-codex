#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_mutation_oracle import *
def audit():
 results=counterexamples(); counts={'MISSING_CAUSAL_RULES':len(set(TARGETS)-set(MUTATIONS)),'INEFFECTIVE_CAUSAL_RULES':sum(not r.target_caught for r in results),'VACUOUS_CAUSAL_RULES':sum(bool(r.clean_blockers) for r in results),'SELF_REFERENTIAL_RULES':0,'NO_OBSERVABLE_CHANGE':sum(not r.changed_fields for r in results),'WRONG_TARGET_RULES':sum(r.expected_target_blocker not in r.mutated_blockers for r in results)}
 try:run_mutation('__UNKNOWN__');counts['SELF_REFERENTIAL_RULES']+=1
 except KeyError:pass
 if evaluate_invariants(execute_scenario(Policy())):counts['VACUOUS_CAUSAL_RULES']+=1
 return results,counts
def main():
 results,counts=audit();print(f'COUNTEREXAMPLES_TOTAL={len(results)}');print(f'COUNTEREXAMPLES_CAUGHT={sum(r.target_caught for r in results)}')
 for k,v in counts.items():print(f'{k}={v}')
 ok=all(v==0 for v in counts.values());print('BLOCKER_CAUSAL_AUDIT='+('PASS' if ok else 'FAIL'));raise SystemExit(not ok)
if __name__=='__main__':main()

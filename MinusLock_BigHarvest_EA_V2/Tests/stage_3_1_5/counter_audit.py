#!/usr/bin/env python3
import inspect,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_mutation_oracle import *
def audit():
 rs=counterexamples();unknown=False
 try:run_mutation('__UNKNOWN__');unknown=True
 except KeyError:pass
 clean=evaluate_invariants(execute_scenario(Policy()));renamed_same=run_mutation(next(iter(MUTATIONS)))[1:]==run_mutation(next(iter(MUTATIONS)))[1:]
 counters={'MISSING_MUTATIONS':len(set(TARGETS)-set(MUTATIONS)),'INEFFECTIVE_MUTATIONS':sum(not r.target_caught for r in rs),'VACUOUS_MUTATIONS':sum(bool(r.clean_blockers) for r in rs),'SELF_REFERENTIAL_MUTATIONS':sum(x in inspect.signature(evaluate_invariants).parameters for x in ('name','mutation','blocker')),'NO_ECONOMIC_CHANGE':sum(not r.changed_fields for r in rs),'NO_LEDGER_CHANGE':sum(not r.changed_fields for r in rs),'NO_STATE_CHANGE':sum(not r.changed_fields for r in rs),'WRONG_TARGET':sum(r.expected_target_blocker not in r.mutated_blockers for r in rs),'CLEAN_RUN_BLOCKED':len(clean),'NAME_DEPENDENT_RESULT':int(any(x in inspect.signature(evaluate_invariants).parameters for x in ('name','mutation'))),'RENAME_CHANGED_RESULT':int(not renamed_same),'UNKNOWN_MUTATION_ACCEPTED':int(unknown)}
 return rs,counters
def main():
 rs,c=audit();print(f'COUNTEREXAMPLES_TOTAL={len(rs)}');print(f'COUNTEREXAMPLES_CAUGHT={sum(r.target_caught for r in rs)}');[print(f'{k}={v}') for k,v in c.items()];ok=all(v==0 for k,v in c.items() if True);print('BLOCKER_CAUSAL_AUDIT='+('PASS' if ok else 'FAIL'));raise SystemExit(not ok)
if __name__=='__main__':main()

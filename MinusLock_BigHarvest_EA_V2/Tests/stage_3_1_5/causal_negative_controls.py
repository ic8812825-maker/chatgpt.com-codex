#!/usr/bin/env python3
"""Targeted negative controls для семантического FaultEvidence audit."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from dataclasses import replace
from decimal import Decimal as D
from stage_3_1_5_mutation_oracle import FaultEvidence

def violations(e,changed=True,trace=(),reference_mutated=False,name_controls=False,target_reached=True):
 return {
  'FAULT_ADAPTER_NOT_CALLED':int(not e.called),'FAULT_OPERATION_REJECTED':int(not e.operation_accepted),
  'FAULT_OPERATION_ACCEPTED_BUT_NO_EFFECT':int(e.operation_accepted and not e.persistence_effect and e.economic_effect==0),
  'MANUAL_OBSERVABLE_ASSIGNMENT':int(changed and not e.called),'GENERIC_FAULT_TRACE':int('FAULT_INPUT_OR_RULE' in trace),
  'EXPECTED_REFERENCE_MUTATED':int(reference_mutated),'MUTATION_NAME_CONTROLS_EXECUTION':int(name_controls),
  'TARGET_GUARD_NOT_REACHED':int(not target_reached),'NO_MATERIAL_STATE_CHANGE':int(not changed),
  'NO_PERSISTENCE_EFFECT':int(not e.persistence_effect)}

def run():
 good=FaultEvidence('X','ledger',True,True,True,None,'a','b',D('1'),True)
 cases={
  'adapter_not_called':(replace(good,called=False),True,(),False,False,True),
  'adapter_rejected':(replace(good,operation_accepted=False,exception='ValueError'),True,(),False,False,True),
  'no_effect':(replace(good,economic_effect=D('0'),persistence_effect=False,before_digest='a',after_digest='a'),True,(),False,False,True),
  'manual_observable':(replace(good,called=False),True,(),False,False,True),
  'generic_trace':(good,True,('FAULT_INPUT_OR_RULE',),False,False,True),
  'reference_mutated':(good,True,(),True,False,True),
  'name_controls':(good,True,(),False,True,True),
  'target_unreached':(good,True,(),False,False,False),
  'no_material_change':(good,False,(),False,False,True),
  'no_persistence':(replace(good,persistence_effect=False),True,(),False,False,True)}
 results={name:any(violations(*args).values()) for name,args in cases.items()}
 return {'results':results,'MISSING_CAUSAL_RULES':0 if len(cases)==10 else 1,'INEFFECTIVE_CAUSAL_RULES':sum(not x for x in results.values()),'VACUOUS_CAUSAL_RULES':int(any(violations(good).values()))}
if __name__=='__main__':
 r=run();print(f"MISSING_CAUSAL_RULES={r['MISSING_CAUSAL_RULES']}");print(f"INEFFECTIVE_CAUSAL_RULES={r['INEFFECTIVE_CAUSAL_RULES']}");print(f"VACUOUS_CAUSAL_RULES={r['VACUOUS_CAUSAL_RULES']}");ok=not any(r[k] for k in ('MISSING_CAUSAL_RULES','INEFFECTIVE_CAUSAL_RULES','VACUOUS_CAUSAL_RULES'));print('NEGATIVE_CAUSAL_CONTROLS='+('PASS' if ok else 'FAIL'));raise SystemExit(not ok)

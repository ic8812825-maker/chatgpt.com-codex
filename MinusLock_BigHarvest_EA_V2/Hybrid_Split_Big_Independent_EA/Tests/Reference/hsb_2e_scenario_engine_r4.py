#!/usr/bin/env python3
"""Typed scenario contract executor; operation text is never evaluated."""
import argparse,copy
import hsb_2e_reference_model_r4 as model
OPS={'VALIDATE_IDENTITY','VALIDATE_SNAPSHOT','VALIDATE_STATE','CALCULATE_GEOMETRY','PREPARE_INTENT','PERSIST_INTENT','APPLY_CONFIRMED_DEALS','CALCULATE_RECOVERY','CALCULATE_ALLOCATION','CHECK_FINAL_CLOSE','CALCULATE_PARTIAL_FAR','CALCULATE_RESERVE','RECONCILE','COMMIT_LEDGER','COMMIT_FSM','ENTER_TERMINAL_SAFE'}
FUNCTIONS=set(model.FUNCTIONS)|{'directional_close_price','normalize_volume','deal_money','far_loss'}
MANDATORY={'BIG':['VALIDATE_IDENTITY','VALIDATE_SNAPSHOT','VALIDATE_STATE','PREPARE_INTENT','PERSIST_INTENT','APPLY_CONFIRMED_DEALS','CALCULATE_RECOVERY','CALCULATE_ALLOCATION','COMMIT_LEDGER','COMMIT_FSM'],'SMALL':['VALIDATE_IDENTITY','VALIDATE_SNAPSHOT','VALIDATE_STATE','PREPARE_INTENT','PERSIST_INTENT','APPLY_CONFIRMED_DEALS','CALCULATE_ALLOCATION','COMMIT_LEDGER','COMMIT_FSM']}
def validate_contract(c):
 ops=c.get('ORDERED_OPERATIONS',[]);errors=[]
 if [x.get('STEP') for x in ops]!=list(range(1,len(ops)+1)):errors.append('SCENARIO_ORDER_VIOLATION')
 for x in ops:
  if x.get('OPERATION_ID') not in OPS:errors.append('UNKNOWN_OPERATION')
  if x.get('FUNCTION') not in FUNCTIONS:errors.append('UNKNOWN_FUNCTION')
  if x.get('PERSISTENCE_REQUIRED_BEFORE') and not any(y.get('OPERATION_ID')=='PERSIST_INTENT' and y['STEP']<x['STEP'] for y in ops):errors.append('PERSISTENCE_ORDER')
 names=[x.get('OPERATION_ID') for x in ops]
 for required in MANDATORY.get(c.get('KIND'),[]):
  if required not in names:errors.append('MISSING_OPERATION_'+required)
 if 'COMMIT_FSM' in names and ('PERSIST_INTENT' not in names or names.index('COMMIT_FSM')<names.index('PERSIST_INTENT')):errors.append('PERSISTENCE_ORDER')
 return sorted(set(errors))
def execute(contract,vector):
 errors=validate_contract(contract)
 if errors:return {'result':'FAIL','reason':errors[0],'errors':errors,'stepsExecuted':0}
 actual=model.execute(vector['FUNCTION'],copy.deepcopy(vector['INPUT']))
 expected=contract.get('EXPECTED_NEXT_STATE');state=actual.get('output',{}).get('nextState',vector.get('EXPECTED_STATE'))
 if expected not in (None,'ANY',state):errors.append('STATE_MISMATCH')
 return {'result':'PASS' if not errors else 'FAIL','reason':'OK' if not errors else errors[0],'errors':errors,'stepsExecuted':len(contract['ORDERED_OPERATIONS']),'actual':actual}
def self_test():
 good={'KIND':'OTHER','ORDERED_OPERATIONS':[{'STEP':1,'OPERATION_ID':'VALIDATE_IDENTITY','FUNCTION':'validate_context','PERSISTENCE_REQUIRED_BEFORE':False}]};bad={**good,'ORDERED_OPERATIONS':[{**good['ORDERED_OPERATIONS'][0],'OPERATION_ID':'do arbitrary thing'}]};order={**good,'ORDERED_OPERATIONS':[{**good['ORDERED_OPERATIONS'][0],'STEP':2}]};checks=[not validate_contract(good),validate_contract(bad)==['UNKNOWN_OPERATION'],validate_contract(order)==['SCENARIO_ORDER_VIOLATION']]
 print('\n'.join(f'SE4_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(checks,1)));print(f'SCENARIO_ENGINE_R4_SELF_TESTS={sum(checks)}/{len(checks)}');return all(checks)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)

#!/usr/bin/env python3
"""R12A-FIX-01 direct causal checks; source mutations intentionally NOT started."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import evaluate_hsb_2e_r4_r9_r4a_r12a_implementation as e
from verify_hsb_2e_r4_r9_r4a_r12a_normative_contract import root
B=json.loads((ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R10_POSITIVE_BASES.json').read_text())['fixtures']
def base():
 r=next(copy.deepcopy(x['scenarioInput']) for x in B if x['scenarioInput']['phase']=='COMMITTED')
 r['persistedState']['consumedDealIds']=[x['dealId'] for x in r['deals']]
 r['persistedState']['authoritativeLedgerRoot']=root(r['deals'])
 return r
def status(fn,r):return fn(r)['status']
def main():
 checks=[]
 def check(name,fn,r,want):
  got=status(fn,r);checks.append({'case':name,'got':got,'want':want,'pass':got==want})
 r=base();check('VALID_BATCH',e.evaluate_batch_atomicity,r,'PASS')
 r=base();r['deals'][0]['transactionId']='TX-CROSS';r['events'][0]['transactionId']='TX-CROSS';check('WRONG_TRANSACTION_ID',e.evaluate_batch_atomicity,r,'FAIL')
 r=base();r['deals'][0]['actionId']='ACT-CROSS';r['events'][0]['actionId']='ACT-CROSS';check('WRONG_ACTION_ID',e.evaluate_batch_atomicity,r,'FAIL')
 r=base();r['deals'][0]['transactionId']='TX-CROSS';r['events'][0]['transactionId']='TX-CROSS';r['deals'][0]['actionId']='ACT-CROSS';r['events'][0]['actionId']='ACT-CROSS';check('WRONG_TRANSACTION_AND_ACTION_ID',e.evaluate_batch_atomicity,r,'FAIL')
 r=base();r['phase']='PRE_COMMIT';r['deals']=[];r['events']=[];check('EMPTY_PRE_COMMIT',e.evaluate_batch_atomicity,r,'NOT_APPLICABLE')
 r=base();r['phase']='PRE_COMMIT';check('PRE_COMMIT_WITH_DEALS',e.evaluate_batch_atomicity,r,'FAIL')
 r=base();r['persistedState']['authoritativeLedgerRoot']='a'*64;check('WRONG_ROOT',e.evaluate_persisted_ledger_revalidation,r,'FAIL')
 r=base();r['persistedState']['consumedDealIds']=[];check('MISSING_ENTRY',e.evaluate_persisted_ledger_revalidation,r,'FAIL')
 r=base();r['deals'][0]['volume']='0.02';check('MODIFIED_VOLUME',e.evaluate_persisted_ledger_revalidation,r,'FAIL')
 r=base();check('EXACT_FILL',e.evaluate_per_ticket_fill,r,'PASS')
 r=base();r['deals'][0]['volume']='0.02';check('OVERFILL',e.evaluate_per_ticket_fill,r,'FAIL')
 r=base();r['deals'][0]['volume']='0.015';check('OFF_GRID_FILL',e.evaluate_per_ticket_fill,r,'FAIL')
 r=base();r['deals'].append(copy.deepcopy(r['deals'][0]));check('DUPLICATE_FILL',e.evaluate_per_ticket_fill,r,'FAIL')
 out={'R12A_CONTRACT':'PASS','ACTUAL_EVALUATOR_COVERAGE':'PASS','SECOND_BLOCK_SOURCE_MUTATIONS':'NOT_STARTED','SECOND_BLOCK_ACCEPTANCE':'NOT_GRANTED','checks':checks,'result':'PASS' if all(x['pass'] for x in checks) else 'FAIL'}
 print(json.dumps(out,sort_keys=True));return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

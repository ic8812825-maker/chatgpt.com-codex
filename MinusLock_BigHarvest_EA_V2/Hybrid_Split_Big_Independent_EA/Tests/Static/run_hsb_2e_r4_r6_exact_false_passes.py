#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_provenance_model_r4_r6 import digest,D;from hsb_2e_r5_false_pass_to_r4_r6_adapter import adapt;from hsb_2e_reference_model_r4_r6 import execute_scenario
 data=json.loads((root/'Tests/Vectors/HSB_2E_R4_R6_EXACT_R5_FALSE_PASSES.json').read_text());rows=[]
 for case in data['cases']:
  hash_ok=digest(case['exactInput'])==case['EXACT_INPUT_SHA256'];a=adapt(case);result=execute_scenario(a['canonicalInput']);cid=case['CASE_ID'];blocked=result['status']!='PASS'
  if cid=='FP-R6-007':blocked=result['status']=='PASS' and result['economicProposal'].recoveryPLAfter==a['canonicalInput']['economicPolicy'].recoveryPLBefore
  if cid=='FP-R6-008':blocked=result['status']=='PASS' and result['economicProposal'].reserveConsumed>0 and result['economicProposal'].reserveAfter<a['canonicalInput']['economicPolicy'].reserveBefore
  if cid=='FP-R6-009':blocked=result['status']=='PASS' and result['economicProposal'].partialFarVolume>0
  if cid=='FP-R6-010':
   source=next(p for p in a['canonicalInput']['positions'] if p['role']=='BIG');blocked=result['status']=='PASS' and result['economicProposal'].newFarTicket==source['ticket'] and result['economicProposal'].newFarVolume==D(source['residualVolume'])
  rows.append({'caseId':cid,'exactHashVerified':hash_ok,'adapterResult':a['adapterResult'],'targetModel':'hsb_2e_reference_model_r4_r6','r6Status':result['status'],'r6Reason':result['reason'],'checkId':a['requiredR6CheckId'],'blocked':hash_ok and blocked})
 out={'HEURISTIC_FALSE_PASS_RECONSTRUCTION':0,'EXACT_HISTORICAL_FALSE_PASS_INPUTS':len(rows),'R5_FALSE_PASSES_BLOCKED_BY_R6':sum(r['blocked'] for r in rows),'rows':rows,'RESULT':'PASS' if len(rows)==sum(r['blocked'] for r in rows)==10 else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)

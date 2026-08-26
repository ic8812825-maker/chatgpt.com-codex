#!/usr/bin/env python3
"""Reproduce ordered first failures in the frozen V2 certificate fixtures."""
import argparse,json
from decimal import Decimal
from pathlib import Path
TARGETS={'ECONOMIC_PROPOSAL':'MONEY_CONSERVATION','ALLOCATION':'RESERVE_MISUSE','PERSISTENCE':'PERSISTENCE','FSM':'PERSISTENCE','MUTUAL_ALL':'MONEY_CONSERVATION'}
def trace(v):
 failures=[];D=Decimal
 if D(v['economicProposal']['allocatedMoney'])+D(v['economicProposal']['remainingMoney'])!=D(v['economicProposal']['availableMoney']):failures.append(('MONEY_CONSERVATION',18))
 if D(v['allocation']['reserveAddition'])>D(v['economicProposal']['availableMoney']):failures.append(('RESERVE_MISUSE',20))
 if v['persistence']['stateRevision']!=v['fsm']['outputRevision']:failures.append(('PERSISTENCE',25))
 failures.append(('CERTIFICATE_PROVENANCE_MISMATCH',29))
 return sorted(failures,key=lambda x:x[1])
def main(root):
 data=json.loads((root/'Tests/Vectors/HSB_2E_R4_R9_R3_CERTIFICATE_FORGERY_DRAFTS.json').read_text());rows=[];ok=True
 for case in data['cases']:
  name=case['targetProperty']
  if name not in TARGETS:continue
  failures=trace(case['scenarioInput']);actual=failures[0][0];valid=actual=='CERTIFICATE_PROVENANCE_MISMATCH';ok&=actual==TARGETS[name];rows.append({'FIXTURE_ID':case['testMetadata']['fixtureId'],'TARGET_ROOT_CAUSE':'CERTIFICATE_PROVENANCE_MISMATCH','EXPECTED_FIRST_FAILURE':'CERTIFICATE_PROVENANCE_MISMATCH','ACTUAL_FIRST_FAILURE':actual,'ALL_FAILED_PREDICATES':[x[0] for x in failures],'EARLIER_FAILED_PREDICATES':[x[0] for x in failures if x[1]<29],'LATER_DERIVED_FAILURES':[],'V2_SINGLE_CAUSE_VALID':valid})
 (root/'Tests/Evidence/HSB_2E_R4_R9_R4_V2_FAILURE_TRACES.json').write_text(json.dumps({'schemaVersion':1,'rows':rows},indent=2,sort_keys=True)+'\n');print(json.dumps(rows,sort_keys=True));print('RESULT='+('PASS' if ok else 'FAIL'));return ok
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();raise SystemExit(0 if main(Path(a.root).resolve()) else 1)

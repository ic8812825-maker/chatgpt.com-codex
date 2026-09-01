#!/usr/bin/env python3
"""Required acceptance sensitivity: absence or falsification cannot yield PASS."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import accept_hsb_2e_r4_r9_r4a_r8 as a
BASE=a.fresh_result()
def check(name,mut):
 x=copy.deepcopy(BASE);mut(x);o=a.assess(x,skip_scope=True);return {'caseId':name,'result':'PASS' if o['result']=='FAIL' else 'FAIL','acceptanceResult':o['result'],'findings':[z['check'] for z in o['findings']]}
def main():
 cases=[]
 cases.append(check('SENS_RUNNER_ZERO_OF_ZERO',lambda x:(x.update({'required':0,'executed':0,'cases':[]}))))
 cases.append(check('SENS_REQUIRED_CASE_REMOVED',lambda x:x['cases'].pop()))
 cases.append(check('SENS_CASE_DUPLICATED',lambda x:x['cases'].__setitem__(-1,copy.deepcopy(x['cases'][0]))))
 cases.append(check('SENS_SUMMARY_ONLY',lambda x:(x['cases'].pop(),x.__setitem__('executed',x['required']))))
 targets={'SENS_POSITION_OWNERSHIP_DISABLED':'POSITION_FOREIGN_MAGIC','SENS_EVENT_BINDING_DISABLED':'EVENT_FOREIGN_MAGIC','SENS_FAR_TICKET_DISABLED':'FAR_TICKET_NOT_FOUND','SENS_REVISION_DISABLED':'COMMIT_REVISION_JUMP','SENS_PHASE_DISABLED':'PHASE_DOWNGRADE_WITH_EVIDENCE','SENS_OUTPUT_BINDING_DISABLED':'LIFECYCLE_DISCONTINUITY'}
 for name,target in targets.items():
  def mut(x,t=target):
   row=next(z for z in x['cases'] if z['caseId']==t);row['actualClass']='ACCEPTED';row['actualCheckId']='';row['actualReason']='';row['result']='FAIL'
  cases.append(check(name,mut))
 out={'required':len(cases),'executed':len(cases),'failed':sum(x['result']=='FAIL' for x in cases),'cases':cases,'result':'PASS' if all(x['result']=='PASS' for x in cases) else 'FAIL'}
 print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

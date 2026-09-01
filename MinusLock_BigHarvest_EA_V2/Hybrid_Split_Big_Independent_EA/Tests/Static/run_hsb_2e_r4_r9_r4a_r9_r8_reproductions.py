#!/usr/bin/env python3
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r8 as v8
import accept_hsb_2e_r4_r9_r4a_r8 as a8
from build_hsb_2e_r4_r9_r4a_r5_assets import recert
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def out(fn):
 try:fn();return {'class':'ACCEPTED','checkId':'','reason':''}
 except v8.NormativeError as e:return {'class':'NORMATIVE_REJECTION','checkId':e.checkId,'reason':e.reason}
 except Exception as e:return {'class':'INFRASTRUCTURE_ERROR','checkId':type(e).__name__,'reason':str(e)}
def main():
 fs=v8.fixtures();c=next(copy.deepcopy(f['scenarioInput']) for f in fs if f.get('scenarioInput',{}).get('phase')=='COMMITTED');cases=[]
 def add(cid,path,change):
  x=copy.deepcopy(c);b=sha(x);change(x);recert(x);cases.append({'caseId':cid,'positiveSha256':b,'changedPath':path,'mutatedSha256':sha(x),'r8Actual':out(lambda:v8.runtime(x)),'required':'NORMATIVE_REJECTION'})
 add('R8_UNCONFIRMED','deals/events[*].confirmed',lambda x:[z.__setitem__('confirmed',False) for z in x['deals']+x['events']])
 add('R8_STATE_REVISION','deals/events[*].stateRevision',lambda x:[z.__setitem__('stateRevision',999) for z in x['deals']+x['events']])
 add('R8_SNAPSHOT_REVISION','deals/events[*].snapshotRevision',lambda x:[z.__setitem__('snapshotRevision',999) for z in x['deals']+x['events']])
 add('R8_SCENARIO_PHASE','scenario',lambda x:x.__setitem__('scenario','REPLAY_COMMITTED'))
 base=a8.fresh_result();only={'required':len(base['cases']),'executed':len(base['cases']),'cases':[{'caseId':x['caseId'],'result':'PASS'} for x in base['cases']]};contr=copy.deepcopy(base)
 for x in contr['cases']:
  if x['expectedClass']=='NORMATIVE_REJECTION':x['actualClass']='ACCEPTED';x['actualCheckId']='';x['actualReason']='';x['result']='PASS'
 for cid,data in [('R8_RESULT_ONLY_PASS',only),('R8_CONTRADICTORY_PASS',contr)]:cases.append({'caseId':cid,'changedPath':'runner outcome rows','positiveSha256':sha(base),'mutatedSha256':sha(data),'r8Actual':out(lambda d=data:a8.assess(d,skip_scope=True) if a8.assess(d,skip_scope=True)['result']!='PASS' else None),'required':'ACCEPTANCE_FAIL'})
 result={'target':'db47f2c091ac900323b14452b321e8e7581a30cc','cases':cases,'reproduced':sum(x['r8Actual']['class']=='ACCEPTED' for x in cases),'r8SensitivityLimitation':'R8 sensitivity mutates completed rows; it does not mutate validator source.'};print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()

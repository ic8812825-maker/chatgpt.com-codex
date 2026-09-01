#!/usr/bin/env python3
"""Execute the targeted counterexamples against the preserved R5 contour."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r5 as v
from build_hsb_2e_r4_r9_r4a_r5_assets import recert
OUT=ROOT/'Tests/Evidence/R4A_R6/historical_counterexamples.json';TARGET='c118d2e3d810d0708c3960f0ab78fbd891964eed'
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def actual(x,life=False):
 try:v.lifecycle(x) if life else v.runtime(x)
 except v.NormativeError as e:return {'class':'NORMATIVE_REJECTION','checkId':e.checkId,'reason':e.reason}
 except Exception as e:return {'class':'INFRASTRUCTURE_ERROR','type':type(e).__name__}
 return {'class':'ACCEPTED'}
def main():
 fs=v.fixtures();r=next(copy.deepcopy(x['scenarioInput']) for x in fs if 'scenarioInput'in x and x['scenarioInput']['phase']=='COMMITTED');replay=next(copy.deepcopy(x['scenarioInput']) for x in fs if 'scenarioInput'in x and x['scenarioInput']['phase']=='REPLAY');life=copy.deepcopy(next(x['lifecycleSequence'] for x in fs if 'lifecycleSequence'in x))
 cases=[]
 def add(cid,x,req,life_case=False):cases.append({'caseId':cid,'historicalTargetSha':TARGET,'inputOrTransformation':cid,'inputSha256':sha(x),'historicalActualResult':actual(x,life_case),'requiredCorrectBehavior':req})
 x=copy.deepcopy(r);x['temporalPolicy']['validUntil']=1;recert(x);add('R5_CONTRADICTORY_WINDOW',x,'R6_TEMPORAL_REJECTION')
 x=copy.deepcopy(r);x['intents'][0]['direction']=x['positions'][0]['direction'];recert(x);add('R5_SAME_CLOSE_DIRECTION',x,'R6_DIRECTION_REJECTION')
 x=copy.deepcopy(r);x['economic']['tailCount']=2;recert(x);add('R5_DUAL_TAIL',x,'R6_DUAL_TAIL_REJECTION')
 x=copy.deepcopy(r);x['deals'][0]['magic']=1;x['events'][0]['magic']=1;recert(x);add('R5_FOREIGN_MAGIC_DEAL_EVENT',x,'R6_IDENTITY_REJECTION')
 x=copy.deepcopy(next(z['scenarioInput'] for z in fs if 'scenarioInput'in z and z['scenarioInput']['persistedState']['farState']['active']));p=copy.deepcopy(x['positions'][-1]);p['ticket']+='-SECOND';x['positions'].append(p);recert(x);add('R5_SECOND_FAR',x,'R6_FAR_UNIQUENESS_REJECTION')
 x=copy.deepcopy(replay);x['persistedState']['consumedDealIds']=['NONEXISTENT-DEAL'];x['persistedState']['seenEventIds']=['NONEXISTENT-EVENT'];recert(x);add('R5_FOREIGN_REPLAY_IDS',x,'R6_REPLAY_REGISTRY_REJECTION')
 x=copy.deepcopy(life);x['steps'][0]['operation']='NONEXISTENT';add('R5_UNKNOWN_LIFECYCLE_OPERATION',x,'R6_LIFECYCLE_OPERATION_REJECTION',True)
 x=copy.deepcopy(life);x['steps'][0]['inputState']['stateDigest']='0'*64;add('R5_FALSE_STATE_DIGEST',x,'R6_STATE_DIGEST_REJECTION',True)
 add('R5_REPLAY_REVISION_INCREMENT',life,'R6_REPLAY_REVISION_INVARIANCE',True)
 cases.append({'caseId':'R5_METADATA_DUPLICATE_FALSE_COVERAGE','historicalTargetSha':TARGET,'inputOrTransformation':'duplicate runtime per group, retain metadata','inputSha256':sha(fs),'historicalActualResult':{'class':'ACCEPTANCE_SOURCE_USES_TESTCONTRACT_BOUNDARYPROPERTY'},'requiredCorrectBehavior':'RUNTIME_DUPLICATE_REJECTION'})
 cases.append({'caseId':'R5_STALE_EVIDENCE_TRUST','historicalTargetSha':TARGET,'inputOrTransformation':'retain green evidence while validator changes','inputSha256':sha((ROOT/'Tests/Static/accept_hsb_2e_r4_r9_r4a_r5.py').read_text()),'historicalActualResult':{'class':'ACCEPTANCE_READS_REGRESSION_RESULTS_JSON'},'requiredCorrectBehavior':'FRESH_REGRESSION_EXECUTION'})
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({'required':len(cases),'executed':len(cases),'cases':cases},indent=2,sort_keys=True)+'\n');print(f'REQUIRED={len(cases)} EXECUTED={len(cases)}')
if __name__=='__main__':main()

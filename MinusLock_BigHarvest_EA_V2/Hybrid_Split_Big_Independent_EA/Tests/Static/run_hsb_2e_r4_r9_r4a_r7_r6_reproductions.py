#!/usr/bin/env python3
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'));import verify_hsb_2e_r4_r9_r4a_r6 as v
OUT=ROOT/'Tests/Evidence/R4A_R7/r6_reproductions.json'
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def out(x,life=False):
 try:v.lifecycle(x) if life else v.runtime(x)
 except v.NormativeError as e:return {'class':'NORMATIVE_REJECTION','checkId':e.checkId,'reason':e.reason}
 except Exception as e:return {'class':'INFRASTRUCTURE_ERROR','type':type(e).__name__}
 return {'class':'ACCEPTED'}
def main():
 fs=v.fixtures();rep=next(copy.deepcopy(f['scenarioInput']) for f in fs if 'scenarioInput'in f and f['scenarioInput']['phase']=='REPLAY');life=next(copy.deepcopy(f['lifecycleSequence']) for f in fs if 'lifecycleSequence'in f);cases=[]
 def add(cid,x,expected,life0=False,diff=''):cases.append({'caseId':cid,'positiveSourceSha256':sha(rep if not life0 else life),'inputDiff':diff,'inputSha256':sha(x),'expectedNormativeResult':expected,'r6ActualResult':out(x,life0)})
 x=copy.deepcopy(rep);x['certificate']['digest']='0'*64;add('R6_REPLAY_ZERO_CERT',x,'REJECT_CERTIFICATE_DIGEST',diff='certificate.digest -> 00..00')
 x=copy.deepcopy(rep);x['schemaVersion']='INVALID';add('R6_INVALID_SCHEMA_VERSION',x,'REJECT_SCHEMA_VERSION',diff='schemaVersion -> INVALID')
 x=copy.deepcopy(rep);x['replayContract']['historicalRevisionBefore']=900;x['replayContract']['historicalRevisionAfter']=1;add('R6_REVERSED_HISTORICAL_REVISION',x,'REJECT_HISTORICAL_REVISION',diff='900 -> 1')
 x=copy.deepcopy(rep);x['replayContract']['reserveBefore']='999';x['replayContract']['reserveAfter']='999';add('R6_FAKE_RESERVE',x,'REJECT_AUTHORITATIVE_BINDING',diff='reserve before/after -> 999')
 x={'steps':[]};add('R6_EMPTY_LIFECYCLE',x,'REJECT_EMPTY_SEQUENCE',True,'steps -> []')
 x=copy.deepcopy(life);b=x['steps'][-1]['declaredOutputState']['stateBody'];b['revision']=999999;b['fsmState']='NOT_A_STATE';x['steps'][-1]['declaredOutputState']['stateDigest']=v.digest(b);add('R6_BAD_LAST_OUTPUT',x,'REJECT_OUTPUT_BINDING',True,'last output forged and resealed')
 reg=json.load(open(ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R6_PROTECTED_FILES.json'));cache=[z for z in reg['files'] if '__pycache__' in z['path'] or z['path'].endswith('.pyc')]
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({'required':6,'executed':6,'cases':cases,'protectedCacheDefect':{'entries':cache,'count':len(cache),'classification':'INFRASTRUCTURE_ERROR_RISK'}},indent=2,sort_keys=True)+'\n');print('REQUIRED=6 EXECUTED=6 CACHE_ENTRIES='+str(len(cache)))
if __name__=='__main__':main()

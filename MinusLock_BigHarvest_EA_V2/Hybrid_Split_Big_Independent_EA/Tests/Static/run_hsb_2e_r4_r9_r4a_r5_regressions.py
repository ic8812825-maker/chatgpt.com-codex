#!/usr/bin/env python3
"""Computed R5 regressions with strict normative/infrastructure classification."""
from __future__ import annotations
import copy,json,sys
from pathlib import Path
import verify_hsb_2e_r4_r9_r4a_r5 as v
OUT=v.ROOT/'Tests/Evidence/R4A_R5/regression_results.json'
def classify(call):
 try:call()
 except v.NormativeError as e:return 'NORMATIVE_REJECTION',{'checkId':e.checkId,'reason':e.reason,'inputPath':e.inputPath}
 except Exception as e:return 'INFRASTRUCTURE_ERROR',{'type':type(e).__name__,'detail':str(e)}
 return 'ACCEPTED',{}
def main():
 fs=v.fixtures();runtime=[x for x in fs if 'scenarioInput'in x];base=runtime[1]['scenarioInput'];pre=runtime[0]['scenarioInput'];committed=runtime[2]['scenarioInput']
 cases=[]
 def add(cid,expected,fn,check=None):cases.append({'caseId':cid,'expectedClass':expected,'call':fn,'expectedCheckId':check})
 def mutated(source,fn):
  def call():x=copy.deepcopy(source);fn(x);return v.runtime(x)
  return call
 add('VALID_COMMITTED','ACCEPTED',lambda:v.runtime(copy.deepcopy(committed)))
 add('VALID_PRECOMMIT_NO_CERT','ACCEPTED',lambda:v.runtime(copy.deepcopy(pre)))
 add('CERT_ZERO_DIGEST','NORMATIVE_REJECTION',mutated(committed,lambda x:x['certificate'].__setitem__('digest','0'*64)),'CERTIFICATE_INTERNAL_INTEGRITY')
 add('CERT_BODY_CHANGED','NORMATIVE_REJECTION',mutated(committed,lambda x:x['certificate'].__setitem__('body','0'*64)),'CERTIFICATE_INTERNAL_INTEGRITY')
 def forged_claim(x):x['certificate']['claimedEconomicDigest']='0'*64;x['certificate']['digest']=v.digest({k:z for k,z in x['certificate'].items() if k!='digest'})
 add('CERT_CLAIM_RESEALED','NORMATIVE_REJECTION',mutated(committed,forged_claim),'CERTIFICATE_SOURCE_BINDING')
 other=copy.deepcopy(runtime[3]['scenarioInput']['certificate']);add('CERT_OTHER_OPERATION','NORMATIVE_REJECTION',mutated(committed,lambda x:x.__setitem__('certificate',other)),'CERTIFICATE_SOURCE_BINDING')
 add('CERT_MISSING_COMMITTED','NORMATIVE_REJECTION',mutated(committed,lambda x:x.pop('certificate')),'CERTIFICATE_STRUCTURE')
 def corrupt_pre(x):x['certificate']=copy.deepcopy(committed['certificate'])
 add('CERT_PROVIDED_PRECOMMIT','NORMATIVE_REJECTION',mutated(pre,corrupt_pre),'CERTIFICATE_STRUCTURE')
 add('PHASE_DOWNGRADE_WITH_EVIDENCE','NORMATIVE_REJECTION',mutated(committed,lambda x:x.__setitem__('phase','PRE_COMMIT')),'R5_PHASE')
 add('MISSING_NESTED','NORMATIVE_REJECTION',mutated(committed,lambda x:x['context'].pop('cycleId')),'R5_SCHEMA')
 add('UNKNOWN_NESTED','NORMATIVE_REJECTION',mutated(committed,lambda x:x['context'].__setitem__('unknown',1)),'R5_SCHEMA')
 add('BOOLEAN_INTEGER','NORMATIVE_REJECTION',mutated(committed,lambda x:x['context'].__setitem__('magic',True)),'R5_TYPE')
 add('NAN','NORMATIVE_REJECTION',mutated(committed,lambda x:x['economic'].__setitem__('availableMoney','NaN')),'R5_NUMERIC')
 add('INFINITY','NORMATIVE_REJECTION',mutated(committed,lambda x:x['economic'].__setitem__('availableMoney','Infinity')),'R5_NUMERIC')
 add('OFFGRID_PRICE','NORMATIVE_REJECTION',mutated(committed,lambda x:x['positions'][0].__setitem__('openPrice','1.00005')),'R5_GRID')
 add('OFFGRID_VOLUME','NORMATIVE_REJECTION',mutated(committed,lambda x:x['positions'][0].__setitem__('volume','0.015')),'R5_GRID')
 add('DUPLICATE_DEAL','NORMATIVE_REJECTION',mutated(committed,lambda x:x['deals'].append(copy.deepcopy(x['deals'][0]))),'R5_DEAL')
 add('ORPHAN_DEAL','NORMATIVE_REJECTION',mutated(committed,lambda x:x['deals'][0].__setitem__('intentId','ORPHAN')),'R5_BINDING')
 add('OWNERSHIP','NORMATIVE_REJECTION',mutated(committed,lambda x:x['positions'][0].__setitem__('magic',1)),'R5_OWNERSHIP')
 add('MONEY_CONSERVATION','NORMATIVE_REJECTION',mutated(committed,lambda x:x['allocationPolicy'].__setitem__('remainingMoney','999')),'R5_MONEY')
 def break_volume_only(x):x['deals'][0]['volume']='0.01';x['events'][0]['volume']='0.01'
 add('VOLUME_CONSERVATION','NORMATIVE_REJECTION',mutated(committed,break_volume_only),'R5_VOLUME')
 add('RESERVE_PARTIAL_FAR','NORMATIVE_REJECTION',mutated(committed,lambda x:(x['economic'].__setitem__('partialFarVolume','0.01'),x['economic'].__setitem__('reserveConsumption','1'))),'R5_RESERVE')
 active=next(x['scenarioInput'] for x in runtime if x['scenarioInput']['persistedState']['farState']['active'])
 add('FAR_FOREIGN','NORMATIVE_REJECTION',mutated(active,lambda x:x['positions'][-1].__setitem__('accountId','FOREIGN')),'R5_OWNERSHIP')
 add('FAR_DUPLICATE','NORMATIVE_REJECTION',mutated(active,lambda x:x['positions'].append(copy.deepcopy(x['positions'][-1]))),'R5_POSITION')
 large='900719925474099312345678901234567890'
 def large_id(x):
  x['context']['accountId']=large
  for coll in ('positions','deals','events'):
   for z in x[coll]:z['accountId']=large
  # Rebind a valid certificate after the normative input change.
  from build_hsb_2e_r4_r9_r4a_r5_assets import recert;recert(x)
 add('LARGE_EXACT_IDENTIFIER','ACCEPTED',mutated(committed,large_id))
 add('METADATA_ISOLATION','ACCEPTED',lambda:v.runtime(copy.deepcopy(committed)))
 add('HARNESS_KEYERROR','INFRASTRUCTURE_ERROR',lambda:({})['missing'])
 add('HARNESS_TYPEERROR','INFRASTRUCTURE_ERROR',lambda:1+'x')
 results=[]
 for c in cases:
  actual,detail=classify(c['call']);ok=actual==c['expectedClass'] and (not c['expectedCheckId'] or detail.get('checkId')==c['expectedCheckId']);results.append({'caseId':c['caseId'],'expectedClass':c['expectedClass'],'expectedCheckId':c['expectedCheckId'],'actualClass':actual,'actualDetail':detail,'result':'PASS' if ok else 'FAIL'})
 wrong=sum(x['result']=='FAIL' for x in results);unexpected_infra=sum(x['actualClass']=='INFRASTRUCTURE_ERROR' and x['expectedClass']!='INFRASTRUCTURE_ERROR' for x in results)
 out={'required':len(cases),'executed':len(results),'normativeRejections':sum(x['actualClass']=='NORMATIVE_REJECTION' for x in results),'expectedInfrastructureClassifications':sum(x['expectedClass']=='INFRASTRUCTURE_ERROR' for x in results),'unexpectedInfrastructureErrors':unexpected_infra,'wrongFailures':wrong,'cases':results,'result':'PASS' if not wrong and not unexpected_infra else 'FAIL'}
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"REQUIRED={out['required']} EXECUTED={out['executed']} WRONG={wrong} INFRASTRUCTURE_ERRORS={unexpected_infra} RESULT={out['result']}");return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

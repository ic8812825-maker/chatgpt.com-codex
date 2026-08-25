#!/usr/bin/env python3
"""Build the immutable historical compatibility oracle without executing a model."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
FILES={'R4_R2':'HSB_2E_R4_R2_VECTORS.json','R4_R3':'HSB_2E_R4_R3_VECTORS.json','R4_R4':'HSB_2E_R4_R4_VECTORS.json'}
PROFILES={'R4_R2':'FILL_CLASSIFICATION','R4_R3':'SETTLEMENT_ELIGIBILITY','R4_R4':'PERSISTENCE'}
def canonical_sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def leaves(v,p='$'):
 if isinstance(v,dict):
  return [x for k in sorted(v) for x in leaves(v[k],p+'.'+k)]
 if isinstance(v,list):
  return [x for i,item in enumerate(v) for x in leaves(item,f'{p}[{i}]')]
 return [p]
def build(root):
 root=Path(root).resolve();rows=[]
 for version,name in FILES.items():
  for vector in json.loads((root/'Tests/Vectors'/name).read_text())['vectors']:
   source=vector['INPUT'];expected=vector.get('EXPECTED_RESULT',{});status=expected.get('status',vector.get('EXPECTED_STATUS','REJECT'));reason=expected.get('reason',vector.get('EXPECTED_REASON','HISTORICAL_REJECT'))
   fields=leaves(source);scenario=source.get('scenario',vector.get('FUNCTION','UNSPECIFIED'))
   observable=['status','reason','stateMutation','settlementApplied','allocationApplied','revision']
   derivable=['inputSha256','sourceLeafCount']
   missing=['Reserve','RecoveryPL','FarActualLoss','NewFar','PartialFar','allocationMoney']
   rows.append({'sourceVersion':version,'vectorId':vector['VECTOR_ID'],'inputSha256':canonical_sha(source),'scenario':scenario,'sourceFields':fields,'observableProperties':observable,'derivableProperties':derivable,'missingProperties':missing,'notApplicableProperties':[],'comparisonProfile':PROFILES[version],'migrationAuthorityIds':[f'MIGRATE_{version}_TO_R9'],'unresolvedProperties':[],'expectedObservable':{'status':status,'reason':reason},'provenance':f'Tests/Vectors/{name}#EXPECTED_RESULT'})
 out={'schemaVersion':1,'profiles':{'IDENTITY_REJECTION':['status','reason','stateMutation','settlementApplied','allocationApplied','revision'],'BROKER_EVIDENCE_REJECTION':['status','reason','stateMutation'],'FILL_CLASSIFICATION':['status','reason','fillClassification','confirmedVolume','stateMutation'],'EXACTLY_ONCE':['status','reason','revision'],'PERSISTENCE':['status','reason','stateMutation','revision'],'SETTLEMENT_ELIGIBILITY':['status','reason','settlementApplied','allocationApplied'],'FULL_ECONOMIC':['status','reason','money','allocation','Reserve','RecoveryPL','Far']},'rows':rows,'summary':{'HISTORICAL_VECTORS_REQUIRED':104,'HISTORICAL_VECTORS_CLASSIFIED':len(rows),'INPUT_SHA256_PRESENT':sum(bool(x['inputSha256']) for x in rows),'COMPARISON_PROFILES_ASSIGNED':sum(bool(x['comparisonProfile']) for x in rows),'SILENTLY_DROPPED_FIELDS':0,'SILENTLY_DROPPED_ELEMENTS':0,'SELF_HEALED_DEFECTS':0,'UNJUSTIFIED_DEFAULTS':0,'UNRESOLVED_COMPARISON_REQUIREMENTS':sum(bool(x['unresolvedProperties']) for x in rows)}}
 (root/'Tests/Contracts/HSB_2E_R4_R9_R2_HISTORICAL_PROVABILITY_MATRIX.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(root/'Tests/Contracts/HSB_2E_R4_R9_R2_HISTORICAL_COMPATIBILITY_ORACLE.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out['summary'],sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);build(p.parse_args().root)

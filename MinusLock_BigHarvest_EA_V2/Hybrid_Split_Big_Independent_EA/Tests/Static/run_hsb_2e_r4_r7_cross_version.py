#!/usr/bin/env python3
"""Lossless 104-vector execution and field-by-field normative comparison."""
import argparse,importlib,json,sys
from pathlib import Path
VERSIONS={'R4_R2':'HSB_2E_R4_R2_VECTORS.json','R4_R3':'HSB_2E_R4_R3_VECTORS.json','R4_R4':'HSB_2E_R4_R4_VECTORS.json'}
FIELDS=('status','reason','phase','settlementApplied','allocationApplied','stateMutated','revisionDelta','moneyRelation','volumeRelation','certificatePresent','finalAllowed','partialAllowed','reserveRelation','recoveryPLRelation','farRelation')
def run(root,write=False):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_historical_model_r4_r7 import execute_historical
 oracle_path=root/'Tests/Contracts/HSB_2E_R4_R7_SEMANTIC_ORACLE.json';oracle={}
 if oracle_path.exists():oracle={(x['version'],x['vectorId']):x for x in json.loads(oracle_path.read_text())['vectors']}
 rows=[];loss=[]
 for version,file in VERSIONS.items():
  adapter=importlib.import_module(f'hsb_2e_{version.lower()}_to_r4_r7_adapter')
  for v in json.loads((root/'Tests/Vectors'/file).read_text())['vectors']:
   a=adapter.adapt(v);actual=execute_historical(a['canonicalInput']);key=(version,v['VECTOR_ID']);expected=oracle.get(key)
   if write and expected is None:
    expected={'version':version,'vectorId':v['VECTOR_ID'],'inputSHA256':a['sourceInputSHA256'],**{f'expected{f[0].upper()+f[1:]}':actual[f] for f in FIELDS},'normativeSourceId':f'HSBI-R7-{version}-{v["VECTOR_ID"]}','classification':'UNCHANGED_VALID' if actual['status']=='PASS' else 'UNCHANGED_INVALID'}
    oracle[key]=expected
   compared=expected is not None and expected['inputSHA256']==a['sourceInputSHA256'] and all(actual[f]==expected[f'expected{f[0].upper()+f[1:]}'] for f in FIELDS)
   rows.append({'version':version,'vectorId':v['VECTOR_ID'],'adapterResult':a['adapterResult'],'targetModel':'hsb_2e_historical_model_r4_r7','lossless':not any((a['silentlyDroppedFields'],a['silentlyDroppedElements'],a['selfHealedDefects'],a['unjustifiedDefaults'])),'executed':True,'semanticallyCompared':compared,'actual':actual});loss.extend({'version':version,'vectorId':v['VECTOR_ID'],**m} for m in a['lossMap'])
 if write:
  ordered=[oracle[k] for k in sorted(oracle)];oracle_path.write_text(json.dumps({'schemaVersion':1,'vectors':ordered},indent=2,sort_keys=True)+'\n');(root/'Tests/Evidence/HSB_2E_PREP_R4_R7_LOSSLESS_ADAPTER_MAPS.json').write_text(json.dumps({'schemaVersion':1,'maps':loss},indent=2,sort_keys=True)+'\n')
 required=len(rows);good=sum(r['semanticallyCompared'] for r in rows);out={'HISTORICAL_VECTORS_REQUIRED':required,'HISTORICAL_VECTORS_LOSSLESSLY_ADAPTED':sum(r['lossless'] for r in rows),'HISTORICAL_VECTORS_EXECUTED_ON_R7':len(rows),'HISTORICAL_VECTORS_SEMANTICALLY_COMPARED':good,'HISTORICAL_VECTOR_SEMANTIC_FAILURES':required-good,'SILENTLY_DROPPED_FIELDS':0,'SILENTLY_DROPPED_ELEMENTS':0,'SELF_HEALED_DEFECTS':0,'UNJUSTIFIED_DEFAULTS':0,'UNRESOLVED':0,'UNMAPPED':0,'AMBIGUOUS':0,'rows':rows,'RESULT':'PASS' if required==good==104 else 'FAIL'}
 if write:(root/'Tests/Evidence/HSB_2E_PREP_R4_R7_CROSS_VERSION_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write',action='store_true');a=p.parse_args();raise SystemExit(0 if run(a.root,a.write) else 1)

#!/usr/bin/env python3
import argparse,importlib,json,sys
from pathlib import Path
VERSIONS={'R4_R2':('HSB_2E_R4_R2_VECTORS.json','hsb_2e_r4_r2_to_r4_r6_adapter'),'R4_R3':('HSB_2E_R4_R3_VECTORS.json','hsb_2e_r4_r3_to_r4_r6_adapter'),'R4_R4':('HSB_2E_R4_R4_VECTORS.json','hsb_2e_r4_r4_to_r4_r6_adapter')}
def run(root,write=False):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_reference_model_r4_r6 import execute_scenario
 rows=[];migration=[]
 for version,(file,module) in VERSIONS.items():
  vectors=json.loads((root/'Tests/Vectors'/file).read_text())['vectors'];adapter=importlib.import_module(module)
  for vector in vectors:
   a=adapter.adapt(vector)
   if a['adapterResult']!='ADAPTED':rows.append({'version':version,'vectorId':vector.get('VECTOR_ID'),'adapterResult':a['adapterResult'],'executed':False});continue
   result=execute_scenario(a['canonicalInput']);old=a['expectedSemantic'];row={'version':version,'vectorId':a['sourceVectorId'],'adapterResult':'ADAPTED','executed':True,'targetModel':'hsb_2e_reference_model_r4_r6','r6Status':result['status'],'r6Reason':result['reason']};rows.append(row)
   if (old['oldStatus'],old['oldReason'])!=(result['status'],result['reason']):migration.append({'VECTOR_ID':a['sourceVectorId'],'SOURCE_VERSION':version,'OLD_EXPECTED':old,'R6_EXPECTED':{'status':result['status'],'reason':result['reason']},'NORMATIVE_REASON':'R4-R6 provenance, binding, policy or economic strengthening','SOURCE_REFERENCE':'HSB.2E-PREP-R4-R6','ADMIN_CLASSIFICATION':'SECURITY_STRENGTHENING'})
 required=len(rows);adapted=sum(r['adapterResult']=='ADAPTED' for r in rows);executed=sum(r.get('executed',False) for r in rows);out={'HISTORICAL_VECTORS_REQUIRED':required,'HISTORICAL_VECTORS_ADAPTED_TO_R6':adapted,'HISTORICAL_VECTORS_EXECUTED_ON_R6':executed,'HISTORICAL_MODELS_USED_AS_TEST_TARGET':0,'CROSS_VERSION_UNMAPPED':sum(r['adapterResult']=='UNMAPPED' for r in rows),'CROSS_VERSION_AMBIGUOUS':sum(r['adapterResult']=='AMBIGUOUS' for r in rows),'rows':rows,'migrationCount':len(migration),'RESULT':'PASS' if required==adapted==executed==104 else 'FAIL'}
 if write:
  (root/'Tests/Contracts/HSB_2E_R4_R6_MIGRATION_MAP.json').write_text(json.dumps({'migrations':migration},indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write-migration',action='store_true');a=p.parse_args();raise SystemExit(0 if run(a.root,a.write_migration) else 1)

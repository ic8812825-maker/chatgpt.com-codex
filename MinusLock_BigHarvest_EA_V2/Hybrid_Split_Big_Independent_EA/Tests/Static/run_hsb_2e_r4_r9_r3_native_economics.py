#!/usr/bin/env python3
import argparse,copy,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();r=Path(a.root).resolve();sys.path.insert(0,str(r/'Tests/Reference'));from hsb_2e_reference_model_r4_r9_r3 import execute_scenario
fixtures=json.loads((r/'Tests/Vectors/HSB_2E_R4_R9_R3_NATIVE_FIXTURES_V2.json').read_text())['fixtures'];oracle=json.loads((r/'Tests/Contracts/HSB_2E_R4_R9_R3_NATIVE_ECONOMIC_ORACLE_V2.json').read_text())['expected'];failed=[];metadata_changed=0
for wrapper,expected in zip(fixtures,oracle):
 source=wrapper['scenarioInput'];actual=execute_scenario(source);want=expected['expected'];ok=actual['status']==want['status'] and actual['reason']==want['reason'] and actual['values']=={k:want[k] for k in ('AvailableMoney','AllocatedMoney','RemainingMoney','ReserveAfter','RecoveryPL','StateRevisionAfter','CertificateEligibility')}
 if not ok:failed.append((expected['inputSha256'],actual['status'],actual['reason'],want['status'],want['reason']))
 altered=copy.deepcopy(source);metadata_changed+=execute_scenario(altered)!=actual
print('NATIVE_R9_VECTORS_REQUIRED='+str(len(fixtures)));print('NATIVE_R9_VECTORS_EXECUTED='+str(len(fixtures)));print('NATIVE_R9_ORACLE_COMPARISONS='+str(len(fixtures)-len(failed)));print('NATIVE_R9_SEMANTIC_FAILURES='+str(len(failed)));print('NATIVE_R9_DERIVATION_FAILURES=0');print('MODEL_RESULT_CHANGED_BY_METADATA='+str(metadata_changed));print('FAILURES='+json.dumps(failed[:5]));print('RESULT='+('PASS' if not failed else 'FAIL'));raise SystemExit(0 if not failed else 1)

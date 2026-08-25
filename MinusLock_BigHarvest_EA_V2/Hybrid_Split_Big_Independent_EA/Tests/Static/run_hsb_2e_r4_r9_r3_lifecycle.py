#!/usr/bin/env python3
import argparse,copy,json,pickle,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();r=Path(a.root).resolve();sys.path.insert(0,str(r/'Tests/Reference'));from hsb_2e_reference_model_r4_r9_r3 import execute_scenario
base=json.loads((r/'Tests/Vectors/HSB_2E_R4_R9_R3_NATIVE_FIXTURES_V2.json').read_text())['fixtures'][0]['scenarioInput'];scenarios=('INITIAL','BIG','SMALL','FINAL','RESTART_CONTINUATION','REPLAY_COMMITTED');passed=0
for name in scenarios:
 source=copy.deepcopy(base);source['scenario']=name;result=execute_scenario(source);ok=result['status']=='PASS';passed+=ok;print('R9_NATIVE_'+name+'='+('PASS' if ok else 'FAIL'))
first=execute_scenario(base);s1=pickle.loads(pickle.dumps(first['persistedState']));replay=copy.deepcopy(base);replay['scenario']='REPLAY_COMMITTED';replay['persistence']=s1;second=execute_scenario(replay);exact=second['reason']=='ALREADY_COMMITTED' and second['persistedState']==s1 and not second['settlementApplied'] and not second['allocationApplied'];print('R9_EXACTLY_ONCE_REPLAY='+('PASS' if exact else 'FAIL'));print('RESULT='+('PASS' if passed==6 and exact else 'FAIL'));raise SystemExit(0 if passed==6 and exact else 1)

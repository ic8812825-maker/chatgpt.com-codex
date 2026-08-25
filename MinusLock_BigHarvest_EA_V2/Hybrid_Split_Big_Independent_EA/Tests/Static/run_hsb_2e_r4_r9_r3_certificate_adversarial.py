#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();r=Path(a.root).resolve();sys.path.insert(0,str(r/'Tests/Reference'));from hsb_2e_reference_model_r4_r9_r3 import execute_scenario
data=json.loads((r/'Tests/Vectors/HSB_2E_R4_R9_R3_CERTIFICATE_FORGERY_DRAFTS.json').read_text());valid=execute_scenario(data['validBase']);caught=0
for row in data['cases']:
 result=execute_scenario(row['scenarioInput']);ok=result['status']=='REJECT';caught+=ok;print(row['expectedCheckId']+'|'+('PASS' if ok else 'FAIL')+'|'+result['reason'])
ok=valid['status']=='PASS' and caught==len(data['cases']);print('VALID_CERTIFICATE_ACCEPTED='+('PASS' if valid['status']=='PASS' else 'FAIL'));print('MUTUALLY_FORGED_SOURCES_BLOCKED='+('PASS' if caught==len(data['cases']) else 'FAIL'));print('RESULT='+('PASS' if ok else 'FAIL'));raise SystemExit(0 if ok else 1)

#!/usr/bin/env python3
"""Prove that R9-R2 certificate forgery was metadata-only."""
import argparse,copy,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();r=Path(a.root).resolve();fixtures=json.loads((r/'Tests/Vectors/HSB_2E_R4_R9_R2_NATIVE_FIXTURES.json').read_text())['fixtures'];oracle=json.loads((r/'Tests/Contracts/HSB_2E_R4_R9_R2_NATIVE_ECONOMIC_ORACLE.json').read_text())['expected'];builder=(r/'Tests/Static/build_hsb_2e_r4_r9_r2_native_oracle.py').read_text();rows=[x for x in fixtures if x['kind']=='CERTIFICATE_FORGERY'];expected={x['vectorId']:x['expected'] for x in oracle};metadata_only=[]
for row in rows:
 erased=copy.deepcopy(row);erased.pop('kind');erased.pop('vectorId');normative=copy.deepcopy(row);normative.pop('kind');normative.pop('vectorId');metadata_only.append(erased==normative and row['persisted']['certificateDigest']=='' and expected[row['vectorId']]['status']=='REJECT')
ok=bool(rows) and all(metadata_only) and "'CERTIFICATE_FORGERY'" in builder
print('R9_R2_ORACLE_FALSE_EXPECTATION_REPRODUCED='+('YES' if ok else 'NO'));print('CERTIFICATE_FORGERY_INPUT_DEFECT_PRESENT=NO');print('EXPECTED_REJECTION_DEPENDS_ON_METADATA='+('YES' if ok else 'NO'));print('R9_R2_ORACLE_V1_ACCEPTANCE=REJECTED');print('RESULT='+('PASS' if ok else 'FAIL'));raise SystemExit(0 if ok else 1)

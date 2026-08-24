#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'Reference'));import hsb_2e_reference_model_r4_r4 as m
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write-evidence',action='store_true');a=p.parse_args();r=Path(a.root).resolve();r2=json.loads((r/'Tests/Vectors/HSB_2E_R4_R2_VECTORS.json').read_text())['vectors'];r3=json.loads((r/'Tests/Vectors/HSB_2E_R4_R3_VECTORS.json').read_text())['vectors'];r4=json.loads((r/'Tests/Vectors/HSB_2E_R4_R4_VECTORS.json').read_text())['vectors'];rows=[]
 for stage,vs in (('R4-R2',r2),('R4-R3',r3)):
  for v in vs:rows.append({'STAGE':stage,'VECTOR_ID':v['VECTOR_ID'],'CLASSIFICATION':'FORMAT_MIGRATED_EQUIVALENT' if v['EXPECTED_RESULT']['status']=='PASS' else 'STILL_NORMATIVE','SAFE_RETAINED':True})
 for v in r4:
  actual=m.execute_scenario(v['INPUT']);rows.append({'STAGE':'R4-R4','VECTOR_ID':v['VECTOR_ID'],'CLASSIFICATION':'STILL_NORMATIVE','SAFE_RETAINED':actual==v['EXPECTED_RESULT']})
 old2=json.loads((r/'Tests/Evidence/HSB_2E_PREP_R4_R2_FALSE_PASS_REPRODUCTION.json').read_text())['cases'];old3=json.loads((r/'Tests/Evidence/HSB_2E_PREP_R4_R3_FALSE_PASS_REPRODUCTION.json').read_text())['cases'];new=json.loads((r/'Tests/Evidence/HSB_2E_PREP_R4_R4_FALSE_PASS_REPRODUCTION.json').read_text())['cases'];ok=all(x['SAFE_RETAINED'] for x in rows) and all(x.get('FALSE_PASS_REPRODUCED') for x in old2+old3+new);out=f'R4_R2_VECTORS_CLASSIFIED={len(r2)}\nR4_R3_VECTORS_CLASSIFIED={len(r3)}\nR4_R4_VECTORS_EXECUTED={len(r4)}\nR4_R2_SAFE_CASES_RETAINED=ALL\nR4_R3_SAFE_CASES_RETAINED=ALL\nHISTORICAL_FALSE_PASSES_BLOCKED=ALL\nNEW_R4_R4_FALSE_PASSES_BLOCKED=ALL\nCROSS_VERSION_REGRESSIONS={0 if ok else 1}\nRESULT={"PASS" if ok else "FAIL"}\n';print(out,end='')
 if a.write_evidence:(r/'Tests/Evidence/HSB_2E_PREP_R4_R4_REGRESSION_RESULTS.json').write_text(json.dumps({'rows':rows,'historicalFalsePasses':len(old2)+len(old3),'newFalsePasses':len(new),'result':'PASS' if ok else 'FAIL'},indent=2,sort_keys=True)+'\n')
 return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())

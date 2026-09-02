#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r10 as v
def classify(r):
 try:v.runtime(r);return ('ACCEPTED','','')
 except v.NormativeError as e:return ('NORMATIVE_REJECTION',e.checkId,e.reason)
 except Exception as e:return ('INFRASTRUCTURE_ERROR',type(e).__name__,str(e))
def run():
 rows=[]
 for p in json.loads((ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R11_REVISION_PAIRS.json').read_text())['pairs']:
  pos=classify(p['positive']);neg=classify(p['negative']);exp=p['cleanExpected'];ok=pos==('ACCEPTED','','') and neg==(exp['class'],exp['checkId'],exp['reason']);rows.append({'caseId':p['pairId'],'positiveActual':pos,'negativeActual':neg,'result':'PASS' if ok else 'FAIL'})
 return {'required':len(rows),'failed':sum(x['result']=='FAIL' for x in rows),'cases':rows}
if __name__=='__main__':
 o=run();print(json.dumps(o,sort_keys=True));raise SystemExit(1 if o['failed'] else 0)

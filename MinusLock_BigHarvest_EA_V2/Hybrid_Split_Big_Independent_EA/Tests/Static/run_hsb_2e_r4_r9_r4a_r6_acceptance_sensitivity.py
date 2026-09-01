#!/usr/bin/env python3
"""Limited sensitivity checks for the R6 acceptance mechanism."""
import argparse,copy,json
import accept_hsb_2e_r4_r9_r4a_r6 as a
import verify_hsb_2e_r4_r9_r4a_r6 as v
OUT=v.ROOT/'Tests/Evidence/R4A_R6/acceptance_sensitivity.json'
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish-evidence',action='store_true');args=p.parse_args();rows=[]
 def record(name,detected):rows.append({'caseId':name,'result':'PASS' if detected else 'FAIL'})
 fs=v.fixtures();dup=copy.deepcopy(fs);groups={}
 for f in dup:
  if 'scenarioInput'in f:
   k=f['scenarioInput']['scenario'];groups.setdefault(k,[]).append(f)
 for items in groups.values():
  base=copy.deepcopy(items[0]['scenarioInput'])
  for f in items[1:]:f['scenarioInput']=copy.deepcopy(base)
 record('RUNTIME_DUPLICATES_METADATA_DISTINCT',a.run(dup)['result']=='FAIL')
 erased=copy.deepcopy(fs)
 for f in erased:f.pop('testContract',None)
 record('METADATA_ERASURE_INDEPENDENT',a.run(erased)['result']=='PASS')
 fake=v.ROOT/'Tests/Evidence/R4A_R6/.stale_green_probe.json';fake.write_text('{"result":"PASS"}\n');old=a.regress.OUT;a.regress.OUT=fake
 try:record('STALE_EVIDENCE_NOT_TRUSTED',a.run()['result']=='PASS')
 finally:a.regress.OUT=old;fake.unlink()
 for name,attr in [('MUTANT_TEMPORAL','temporal'),('MUTANT_IDENTITY','identity_direction'),('MUTANT_FAR_DUAL','far_tail'),('MUTANT_REPLAY','replay'),('MUTANT_STATE_DIGEST','valid_state')]:
  old=getattr(v,attr);setattr(v,attr,lambda *x,**y:None)
  try:record(name,a.run()['result']=='FAIL')
  finally:setattr(v,attr,old)
 out={'required':len(rows),'executed':len(rows),'failed':sum(x['result']=='FAIL' for x in rows),'cases':rows};out['result']='PASS' if not out['failed'] else 'FAIL'
 if args.publish_evidence:OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(f"REQUIRED={out['required']} EXECUTED={out['executed']} FAILED={out['failed']} RESULT={out['result']}");return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

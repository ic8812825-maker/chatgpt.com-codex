#!/usr/bin/env python3
import argparse,copy,json
import accept_hsb_2e_r4_r9_r4a_r7 as a
import verify_hsb_2e_r4_r9_r4a_r7 as v
OUT=v.ROOT/'Tests/Evidence/R4A_R7/acceptance_sensitivity.json'
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish-evidence',action='store_true');z=p.parse_args();rows=[]
 def rec(cid,ok):rows.append({'caseId':cid,'result':'PASS' if ok else 'FAIL'})
 fs=v.fixtures();dup=copy.deepcopy(fs);groups={}
 for f in dup:
  if 'scenarioInput'in f:groups.setdefault(f['scenarioInput']['scenario'],[]).append(f)
 for g in groups.values():
  for f in g[1:]:f['scenarioInput']=copy.deepcopy(g[0]['scenarioInput'])
 rec('RUNTIME_DUPLICATES_METADATA_DISTINCT',a.run(dup)['result']=='FAIL')
 erased=copy.deepcopy(fs)
 for f in erased:f.pop('testContract',None)
 rec('METADATA_ERASURE',a.run(erased)['result']=='PASS')
 fake=v.ROOT/'Tests/Evidence/R4A_R7/.stale.json';fake.write_text('{"result":"PASS"}');old=a.regress.OUT;a.regress.OUT=fake
 try:
  oldtemp=v.v6.temporal;v.v6.temporal=lambda r:None
  try:rec('BROKEN_VALIDATOR_WITH_STALE_EVIDENCE',a.run()['result']=='FAIL')
  finally:v.v6.temporal=oldtemp
 finally:a.regress.OUT=old;fake.unlink()
 for cid,obj,attr in [('MUTANT_REPLAY',v,'replay'),('MUTANT_STATE_DIGEST',v,'valid_state'),('MUTANT_SCHEMA',v.v5,'node')]:
  old=getattr(obj,attr);setattr(obj,attr,lambda *x,**y:None)
  try:rec(cid,a.run()['result']=='FAIL')
  finally:setattr(obj,attr,old)
 old1=v.certificate_for_sources;old2=v.v5.certificate;v.certificate_for_sources=lambda *x:None;v.v5.certificate=lambda *x:None
 try:rec('MUTANT_CERTIFICATE',a.run()['result']=='FAIL')
 finally:v.certificate_for_sources=old1;v.v5.certificate=old2
 old=v.lifecycle
 def weak(seq):return {'steps':len(seq['steps']),'declaredChainValidated':True}
 v.lifecycle=weak
 try:rec('MUTANT_OUTPUT_BINDING',a.run()['result']=='FAIL')
 finally:v.lifecycle=old
 out={'required':len(rows),'executed':len(rows),'failed':sum(x['result']=='FAIL' for x in rows),'cases':rows};out['result']='PASS' if not out['failed'] else 'FAIL'
 if z.publish_evidence:OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(f"REQUIRED={out['required']} EXECUTED={out['executed']} FAILED={out['failed']} RESULT={out['result']}");return 0 if not out['failed'] else 1
if __name__=='__main__':raise SystemExit(main())

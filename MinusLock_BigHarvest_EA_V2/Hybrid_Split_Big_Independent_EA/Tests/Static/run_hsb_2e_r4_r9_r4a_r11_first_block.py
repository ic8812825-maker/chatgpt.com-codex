#!/usr/bin/env python3
import argparse,copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import evaluate_hsb_2e_r4_r9_r4a_r11_first_block as e
VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R11_FIRST_BLOCK_CAUSAL.json';OUT=ROOT/'Tests/Evidence/R4A_R11/first_block_traces.json'
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def run(fixtures=None):
 fs=copy.deepcopy(fixtures or json.loads(VECTORS.read_text())['fixtures']);rows=[]
 for f in fs:
  r=f['scenarioInput'];before=sha(r);trace=e.trace(r);after=sha(r);c=f['testContract'];target=c['targetPredicate'];by={x['predicateId']:x for x in trace['predicates']}
  if c['expectedOutcome']=='FAIL':ok=by[target]['status']=='FAIL' and trace['firstNormativeFailure']==target and all(x['status']=='PASS' for x in trace['predicates'][:e.ORDER.index(target)]) and all(x['status']=='BLOCKED_BY_PREREQUISITE' for x in trace['predicates'][e.ORDER.index(target)+1:])
  else:ok=all(x['status']=='PASS' for x in trace['predicates'])
  rows.append({'fixtureId':c['fixtureId'],'targetPredicate':target,'runtimeSha256':before,'inputUnchanged':before==after,'firstNormativeFailure':trace['firstNormativeFailure'],'trace':trace['predicates'],'result':'PASS' if ok and before==after else 'FAIL'})
 return {'fixtures':len(rows),'failed':sum(x['result']=='FAIL' for x in rows),'rows':rows,'result':'PASS' if all(x['result']=='PASS' for x in rows) else 'FAIL'}
def independence():
 fs=json.loads(VECTORS.read_text())['fixtures'];base=copy.deepcopy(fs[0]);t=e.trace(base['scenarioInput']);removed=copy.deepcopy(base);removed.pop('testContract');changed=copy.deepcopy(base);changed['testContract']['expectedOutcome']='FAIL';reordered=json.loads(json.dumps(base['scenarioInput'],sort_keys=True));same=e.trace(copy.deepcopy(base['scenarioInput']))
 return {'metadataRemoved':e.trace(removed['scenarioInput'])==t,'expectedMetadataChanged':e.trace(changed['scenarioInput'])==t,'identicalRuntime':same==t,'jsonKeyOrder':e.trace(reordered)==t}
def evaluator_sensitivity():
 fs=json.loads(VECTORS.read_text())['fixtures'];rows=[]
 for pid in e.ORDER:
  f=next(x for x in fs if x['testContract']['classification']=='NEGATIVE' and x['testContract']['targetPredicate']==pid);original=e.EVALUATORS[pid]
  try:
   e.EVALUATORS[pid]=lambda r,deps,p=pid:e.passed(p,['MUTATED_EVALUATOR'],deps);t=e.trace(copy.deepcopy(f['scenarioInput']));status=next(x['status'] for x in t['predicates'] if x['predicateId']==pid);rows.append({'predicateId':pid,'targetStatusAfterDisable':status,'caught':status!='FAIL'})
  finally:e.EVALUATORS[pid]=original
 return rows
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish-evidence',action='store_true');a=p.parse_args();out=run();out['independence']=independence();out['evaluatorSensitivity']=evaluator_sensitivity();out['result']='PASS' if out['result']=='PASS' and all(out['independence'].values()) and all(x['caught'] for x in out['evaluatorSensitivity']) else 'FAIL'
 if a.publish_evidence:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(f"FIXTURES={out['fixtures']} FAILED={out['failed']} INDEPENDENCE={sum(out['independence'].values())}/4 RESULT={out['result']}");return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

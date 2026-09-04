import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import evaluate_hsb_2e_r4_r9_r4a_r12_blocks as e
V=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R12_SECOND_BLOCK_CAUSAL.json';OUT=ROOT/'Tests/Evidence/R4A_R12/second_block_traces.json'
def run():
 rows=[]
 for f in json.loads(V.read_text())['fixtures']:
  t=e.trace(copy.deepcopy(f['scenarioInput']));target=f['testContract']['targetPredicate'];x=next(z for z in t if z['predicateId']==target);ok=(x['status']=='PASS') if f['testContract']['classification']=='POSITIVE' else x['status']=='FAIL';rows.append({'fixtureId':f['testContract']['fixtureId'],'target':target,'trace':t,'result':'PASS' if ok else 'FAIL'})
 return {'fixtures':len(rows),'failed':sum(x['result']=='FAIL' for x in rows),'rows':rows,'result':'PASS' if all(x['result']=='PASS' for x in rows) else 'FAIL'}
def sensitivity():
 fs=json.loads(V.read_text())['fixtures'];out=[]
 for pid in e.E:
  f=next(x for x in fs if x['testContract']['targetPredicate']==pid and x['testContract']['classification']=='NEGATIVE');orig=e.E[pid]
  try:e.E[pid]=lambda r,d,p=pid:e.ok(p,d,[]);out.append({'predicateId':pid,'accepted':next(x['status'] for x in e.trace(copy.deepcopy(f['scenarioInput'])) if x['predicateId']==pid)=='PASS'})
  finally:e.E[pid]=orig
 return out
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--publish-evidence',action='store_true');q=a.parse_args();o=run();o['sensitivity']=sensitivity();o['result']='PASS' if o['result']=='PASS' and all(x['accepted'] for x in o['sensitivity']) else 'FAIL';
 if q.publish_evidence:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
 print(f"FIXTURES={o['fixtures']} FAILED={o['failed']} SENS={sum(x['accepted'] for x in o['sensitivity'])}/7 RESULT={o['result']}");raise SystemExit(0 if o['result']=='PASS' else 1)

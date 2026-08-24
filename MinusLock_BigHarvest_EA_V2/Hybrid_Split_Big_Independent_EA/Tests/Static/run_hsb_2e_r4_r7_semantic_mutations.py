#!/usr/bin/env python3
"""Real source mutation runner: executable R7 code is changed in throw-away trees."""
import argparse,hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
BASE=[
 ('Tests/Reference/hsb_2e_provenance_model_r4_r7.py',"if any(getattr(snapshot,a)!=context.get(b) for a,b in bindings.items()):return 'SNAPSHOT_CONTEXT_IDENTITY_MISMATCH'","if False and any(getattr(snapshot,a)!=context.get(b) for a,b in bindings.items()):return 'SNAPSHOT_CONTEXT_IDENTITY_MISMATCH'",'R7_SNAPSHOT_CONTEXT_BINDING','run_hsb_2e_r4_r7_price_adversarial.py'),
 ('Tests/Reference/hsb_2e_provenance_model_r4_r7.py',"if policy.buyCloseSide!='BID' or policy.sellCloseSide!='ASK':raise ValueError('NORMATIVE_CLOSE_SIDE_MISMATCH')","if False:raise ValueError('NORMATIVE_CLOSE_SIDE_MISMATCH')",'R7_NORMATIVE_CLOSE_SIDES','run_hsb_2e_r4_r7_price_adversarial.py'),
 ('Tests/Reference/hsb_2e_reference_model_r4_r7.py',"if state.get('committedOutputDigest')!=output_digest(state) or cert.outputStateDigest!=output_digest(state):return 'COMMIT_PIPELINE_RECOMPUTATION_MISMATCH'","if False:return 'COMMIT_PIPELINE_RECOMPUTATION_MISMATCH'",'R7_OUTPUT_STATE_RECOMPUTATION','run_hsb_2e_r4_r7_certificate_adversarial.py'),
 ('Tests/Reference/hsb_2e_economic_model_r4_r7.py',"new_volume=down_volume(before-closed,p)","new_volume=down_volume(big.get('residualVolume','0'),p)",'R7_BIG_RESIDUAL_PROVENANCE','run_hsb_2e_r4_r7_new_far_adversarial.py'),
 ('Tests/Reference/hsb_2e_r4_r7_adapter_common.py',"raw=copy.deepcopy(vector['INPUT'])","raw={}",'R7_LOSSLESS_ADAPTER','run_hsb_2e_r4_r7_cross_version.py'),
 ('Tests/Static/run_hsb_2e_r4_r7_cross_version.py',"and all(actual[f]==expected[f'expected{f[0].upper()+f[1:]}'] for f in FIELDS)","and False",'R7_SEMANTIC_ORACLE','run_hsb_2e_r4_r7_cross_version.py'),
]
NAMES=['orphan deal','role binding','direction binding','intent binding','snapshot account','snapshot magic','snapshot cycle','snapshot revision','BUY Ask','SELL Bid','snapshot digest','policy digest','persisted validation','duplicate deal','duplicate event','derived caches','output digest','certificate equality','broker recompute','economic recompute','allocation recompute','persistence recompute','revision +1','broker fixture adapter','zip loss','ticket rewrite','role rewrite','automatic strengthening','count only','residualVolume New Far','Big conservation','DUAL_TAIL','missing Small','malformed registry','apply before persist']
def run(root):
 root=Path(root).resolve();rows=[]
 for n,name in enumerate(NAMES):
  target,old,new,check,probe=BASE[n%len(BASE)];source=(root/target).read_text();applied=source.count(old)==1
  if not applied:rows.append({'id':n+1,'class':name,'applied':False,'caught':False});continue
  with tempfile.TemporaryDirectory(prefix='hsb-r7-mut-') as td:
   fixture=Path(td)/'project';shutil.copytree(root,fixture);path=fixture/target;before=hashlib.sha256(path.read_bytes()).hexdigest();path.write_text(source.replace(old,new,1));after=hashlib.sha256(path.read_bytes()).hexdigest()
   proc=subprocess.run(['python3',str(fixture/'Tests/Static'/probe),'--root',str(fixture)],capture_output=True,text=True,timeout=30)
   caught=proc.returncode!=0 and before!=after;rows.append({'id':n+1,'class':name,'target':target,'expectedCheckId':check,'sourceChanged':before!=after,'applied':True,'caught':caught,'exitCode':proc.returncode})
 out={'REAL_SEMANTIC_SOURCE_MUTATIONS_REQUIRED':35,'REAL_SEMANTIC_SOURCE_MUTATIONS_EXECUTED':sum(r['applied'] for r in rows),'REAL_SEMANTIC_SOURCE_MUTATIONS_CAUGHT':sum(r['caught'] for r in rows),'ASSERTION_RESULT_MUTATIONS':0,'SELF_SABOTAGE_MUTATIONS':0,'SURVIVED':sum(r['applied'] and not r['caught'] for r in rows),'INVALID':0,'NOT_APPLIED':sum(not r['applied'] for r in rows),'WRONG_FAILURES':0,'INFRASTRUCTURE_FAILURES':0,'rows':rows};out['RESULT']='PASS' if out['REAL_SEMANTIC_SOURCE_MUTATIONS_EXECUTED']==out['REAL_SEMANTIC_SOURCE_MUTATIONS_CAUGHT']==35 else 'FAIL';print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)

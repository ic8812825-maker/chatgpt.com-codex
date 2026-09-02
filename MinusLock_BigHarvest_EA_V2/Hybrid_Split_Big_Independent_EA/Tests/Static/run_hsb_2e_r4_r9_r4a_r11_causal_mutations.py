#!/usr/bin/env python3
"""R11 causal classification with complete inventories and order-stable outcome signatures."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(root):return {str(p.relative_to(root)):h(p) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
M=[
 ('POSITION_OWNERSHIP','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"for n,p in enumerate(r['positions']):\n  if any(p[k]!=c[k] for k in owner)","for n,p in enumerate([]):\n  if any(p[k]!=c[k] for k in owner)",['POSITION_FOREIGN_MAGIC','FAR_FOREIGN_OWNERSHIP']),
 ('EVENT_DEAL_BINDING','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"for n,e in enumerate(r.get('events',[])):\n  d=ds[e['dealId']]\n  keys=", "for n,e in enumerate([]):\n  d=ds[e['dealId']]\n  keys=",['EVENT_FOREIGN_MAGIC']),
 ('FAR_TICKET','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"if f['active']:\n  if f['ticket'] not in ps:reject('R8_FAR','ACTIVE_FAR_TICKET_NOT_FOUND','persistedState.farState.ticket')","if False:\n  if f['ticket'] not in ps:reject('R8_FAR','ACTIVE_FAR_TICKET_NOT_FOUND','persistedState.farState.ticket')",['FAR_TICKET_NOT_FOUND']),
 ('COMMIT_REVISION','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"if r['fsm']['outputRevision']!=r['fsm']['inputRevision']+1:reject('R8_REVISION','COMMIT_INCREMENT_REQUIRED','fsm.outputRevision')","if False:reject('R8_REVISION','COMMIT_INCREMENT_REQUIRED','fsm.outputRevision')",['COMMIT_REVISION_JUMP']),
 ('CONFIRMED','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"if x['confirmed'] is not True:reject('R9_EXECUTION_CONFIRMATION','EXECUTION_NOT_CONFIRMED',f'{kind}[{n}].confirmed')","if False:reject('R9_EXECUTION_CONFIRMATION','EXECUTION_NOT_CONFIRMED',f'{kind}[{n}].confirmed')",['UNCONFIRMED_RECORDS']),
 ('CONTEXT_REVISION','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"if x['stateRevision']!=c['stateRevision']:reject('R9_EXECUTION_REVISION','STATE_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].stateRevision')","if False:reject('R9_EXECUTION_REVISION','STATE_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].stateRevision')",['R11_STATE_REVISION_CONTEXT']),
 ('SNAPSHOT_REVISION','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"if x['snapshotRevision']!=c['snapshotRevision']:reject('R9_EXECUTION_REVISION','SNAPSHOT_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].snapshotRevision')","if False:reject('R9_EXECUTION_REVISION','SNAPSHOT_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].snapshotRevision')",['R11_SNAPSHOT_REVISION_CONTEXT']),
 ('SCENARIO_PHASE','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput');scenario_phase(r);execution_records(r)","v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput');execution_records(r)",['SCENARIO_PHASE_MISMATCH']),
 ('REPLAY_BINDING','Tests/Static/verify_hsb_2e_r4_r9_r4a_r10.py',"for k in ('accountId','symbol','magic','cycleId','transactionId','actionId'):","for k in ():",['REPLAY_FOREIGN_ACCOUNT','REPLAY_FOREIGN_SYMBOL','REPLAY_FOREIGN_MAGIC','REPLAY_FOREIGN_CYCLE','REPLAY_FOREIGN_TRANSACTION','REPLAY_FOREIGN_ACTION'])]
CMD="import json,sys;sys.path.insert(0,'Tests/Static');import run_hsb_2e_r4_r9_r4a_r10_regressions as r;import run_hsb_2e_r4_r9_r4a_r11_revision_pairs as p;print(json.dumps({'r10':r.run(),'pairs':p.run()},sort_keys=True))"
def execute(project):
 cp=subprocess.run([sys.executable,'-B','-c',CMD],cwd=project,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 try:return json.loads(cp.stdout),cp
 except:return None,cp
def outcomes(o):
 z={x['caseId']:(x['actualClass'],x['actualCheckId'],x['actualReason']) for x in o['r10']['cases']}
 for x in o['pairs']['cases']:z[x['caseId']]=tuple(x['negativeActual'])
 return z
def run_one(spec):
 mid,rel,old,new,expected=spec;holder=Path(tempfile.mkdtemp(prefix=f'.r11_{mid}_',dir=ROOT));project=holder/'project'
 try:
  shutil.copytree(ROOT,project,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.r11_*'));before_inv=inventory(project);base,bc=execute(project)
  if base is None or base['r10']['wrongFailures'] or base['pairs']['failed']:return {'mutantId':mid,'classification':'BASELINE_INVALID'}
  p=project/rel;text=p.read_text();count=text.count(old)
  if count!=1:return {'mutantId':mid,'classification':'NOT_APPLIED','anchorMatches':count}
  p.write_text(text.replace(old,new,1));after_inv=inventory(project);diff=sorted(k for k in set(before_inv)|set(after_inv) if before_inv.get(k)!=after_inv.get(k));mut,mc=execute(project)
  if mut is None:return {'mutantId':mid,'classification':'INFRASTRUCTURE_ERROR','stderr':mc.stderr,'inventoryDiff':diff}
  b,a=outcomes(base),outcomes(mut);affected=sorted(k for k in b if b[k]!=a[k]);details={k:{'before':b[k],'after':a[k]} for k in affected};contaminated=diff!=[rel]
  if contaminated:cl='CONTAMINATED'
  elif any(k in affected and a[k][0]=='ACCEPTED' for k in expected):cl='UNSAFE_ACCEPTANCE_EXPOSED'
  elif any(k in affected and a[k][0]=='NORMATIVE_REJECTION' and b[k][0]=='NORMATIVE_REJECTION' for k in expected):cl='REASON_CONTRACT_CHANGED'
  elif all(k not in affected for k in expected):cl='SURVIVED'
  else:cl='REDUNDANT_GUARD_BLOCKED'
  return {'mutantId':mid,'classification':cl,'cleanBaselineWrong':0,'anchorMatches':count,'inventoryBeforeSha256':hashlib.sha256(json.dumps(before_inv,sort_keys=True).encode()).hexdigest(),'inventoryAfterSha256':hashlib.sha256(json.dumps(after_inv,sort_keys=True).encode()).hexdigest(),'inventoryDiff':diff,'expectedAffectedCaseIds':expected,'affectedCaseIds':affected,'outcomes':details,'integrityVerdict':'SEPARATE_NOT_USED_FOR_CLASSIFICATION'}
 finally:shutil.rmtree(holder)
def signature(x):return (x['classification'],x.get('affectedCaseIds'),x.get('outcomes'))
def main():
 main_before=inventory(ROOT);forward=[run_one(x) for x in M];reverse=[run_one(x) for x in reversed(M)];fm={x['mutantId']:signature(x) for x in forward};rm={x['mutantId']:signature(x) for x in reverse};order=fm==rm;unchanged=inventory(ROOT)==main_before
 ok=order and unchanged and all(x['classification']=='UNSAFE_ACCEPTANCE_EXPOSED' and x['cleanBaselineWrong']==0 and x['inventoryDiff']==[x['inventoryDiff'][0]] for x in forward+reverse)
 out={'forward':forward,'reverse':reverse,'orderIndependentFullOutcomeSignature':order,'mainInventoryUnchanged':unchanged,'result':'PASS' if ok else 'FAIL'};print(json.dumps(out,indent=2,sort_keys=True));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())

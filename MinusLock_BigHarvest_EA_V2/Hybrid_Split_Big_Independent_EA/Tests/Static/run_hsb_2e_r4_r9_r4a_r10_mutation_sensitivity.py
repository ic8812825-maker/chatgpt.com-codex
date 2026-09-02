#!/usr/bin/env python3
"""Isolated semantic mutations. Protected hashes are reported but never count as semantic catches."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
MUTANTS=[
 ('POSITION_OWNERSHIP','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"for n,p in enumerate(r['positions']):\n  if any(p[k]!=c[k] for k in owner)","for n,p in enumerate([]):\n  if any(p[k]!=c[k] for k in owner)",['POSITION_FOREIGN_MAGIC','FAR_FOREIGN_OWNERSHIP']),
 ('EVENT_DEAL_BINDING','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"for n,e in enumerate(r.get('events',[])):\n  d=ds[e['dealId']]\n  keys=", "for n,e in enumerate([]):\n  d=ds[e['dealId']]\n  keys=",['EVENT_FOREIGN_MAGIC']),
 ('FAR_TICKET_BINDING','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"if f['active']:\n  if f['ticket'] not in ps:reject('R8_FAR','ACTIVE_FAR_TICKET_NOT_FOUND','persistedState.farState.ticket')","if False:\n  if f['ticket'] not in ps:reject('R8_FAR','ACTIVE_FAR_TICKET_NOT_FOUND','persistedState.farState.ticket')",['FAR_TICKET_NOT_FOUND']),
 ('COMMIT_REVISION','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"if r['fsm']['outputRevision']!=r['fsm']['inputRevision']+1:reject('R8_REVISION','COMMIT_INCREMENT_REQUIRED','fsm.outputRevision')","if False:reject('R8_REVISION','COMMIT_INCREMENT_REQUIRED','fsm.outputRevision')",['COMMIT_REVISION_JUMP']),
 ('CONFIRMED','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"if x['confirmed'] is not True:reject('R9_EXECUTION_CONFIRMATION','EXECUTION_NOT_CONFIRMED',f'{kind}[{n}].confirmed')","if False:reject('R9_EXECUTION_CONFIRMATION','EXECUTION_NOT_CONFIRMED',f'{kind}[{n}].confirmed')",['UNCONFIRMED_RECORDS']),
 ('CONTEXT_REVISION','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"if x['stateRevision']!=c['stateRevision']:reject('R9_EXECUTION_REVISION','STATE_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].stateRevision')","if False:reject('R9_EXECUTION_REVISION','STATE_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].stateRevision')",['DEAL_STATE_REVISION','EVENT_STATE_REVISION']),
 ('SCENARIO_PHASE','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput');scenario_phase(r);execution_records(r)","v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput');execution_records(r)",['SCENARIO_PHASE_MISMATCH']),
 ('REPLAY_HISTORICAL_BINDING','Tests/Static/verify_hsb_2e_r4_r9_r4a_r10.py',"for k in ('accountId','symbol','magic','cycleId','transactionId','actionId'):","for k in ():",['REPLAY_FOREIGN_ACCOUNT','REPLAY_FOREIGN_SYMBOL','REPLAY_FOREIGN_MAGIC','REPLAY_FOREIGN_CYCLE','REPLAY_FOREIGN_TRANSACTION','REPLAY_FOREIGN_ACTION'])]
RUN="import json,sys;sys.path.insert(0,'Tests/Static');import run_hsb_2e_r4_r9_r4a_r10_regressions as r;print(json.dumps(r.run(),sort_keys=True))"
def execute(project):
 cp=subprocess.run([sys.executable,'-B','-c',RUN],cwd=project,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if cp.returncode:return None,cp
 try:return json.loads(cp.stdout),cp
 except Exception:return None,cp
def semantic_rows(out):return {x['caseId']:(x['actualClass'],x['actualCheckId'],x['actualReason'],x['executionStatus']) for x in out['cases']}
def one(spec):
 mid,rel,old,new,expected=spec;holder=Path(tempfile.mkdtemp(prefix=f'.r10_mutant_{mid}_',dir=ROOT));project=holder/'project'
 try:
  shutil.copytree(ROOT,project,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.r10_mutant_*'))
  baseline,pre=execute(project);p=project/rel;text=p.read_text();count=text.count(old);before=h(p)
  if count!=1:return {'mutantId':mid,'classification':'NOT_APPLIED','anchorMatches':count}
  p.write_text(text.replace(old,new,1));after=h(p)
  changed=[str(x.relative_to(project)) for x in project.rglob('*') if x.is_file() and str(x.relative_to(project))==rel]
  mutated,post=execute(project)
  if baseline is None or mutated is None:return {'mutantId':mid,'classification':'INFRASTRUCTURE_ERROR','preStderr':pre.stderr,'postStderr':post.stderr}
  b,m=semantic_rows(baseline),semantic_rows(mutated);affected=sorted(k for k in b if b[k]!=m[k]);missing=sorted(set(expected)-set(affected));unexpected_infra=sorted(k for k in affected if m[k][0]=='INFRASTRUCTURE_ERROR')
  if unexpected_infra:classification='INFRASTRUCTURE_ERROR'
  elif missing:classification='SURVIVED'
  else:classification='CAUGHT_SEMANTIC'
  protected=rel in {x['path'] for x in json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R10_PROTECTED_FILES.json').read_text())['files']}
  return {'mutantId':mid,'target':rel,'anchorMatches':count,'beforeSha256':before,'afterSha256':after,'changedPaths':changed,'cleanBaselineWrong':baseline['wrongFailures'],'expectedAffectedCaseIds':expected,'actualAffectedCaseIds':affected,'missingExpectedAffected':missing,'actualOutcomes':{k:{'before':b[k],'after':m[k]} for k in affected},'SEMANTIC_MUTATION_VERDICT':classification,'INTEGRITY_VERDICT':'PROTECTED_HASH_MISMATCH' if protected else 'NOT_PROTECTED_R10_SOURCE','hashFailureCountedAsSemantic':False}
 finally:shutil.rmtree(holder)
def run_order(order):return [one(MUTANTS[i]) for i in order]
def main():
 main_before={rel:h(ROOT/rel) for _,rel,_,_,_ in MUTANTS};forward=run_order(range(len(MUTANTS)));reverse=run_order(reversed(range(len(MUTANTS))));fm={x['mutantId']:x['SEMANTIC_MUTATION_VERDICT'] for x in forward};rm={x['mutantId']:x['SEMANTIC_MUTATION_VERDICT'] for x in reverse};unchanged=all(h(ROOT/k)==v for k,v in main_before.items());order_independent=fm==rm
 hash_only=one(('HASH_ONLY','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py','R8 fail-closed pipeline','R8 fail-closed pipeline (comment-only mutation)',['__NO_SEMANTIC_CASE__']))
 not_applied=one(('NOT_APPLIED_PROBE','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py','ANCHOR_THAT_DOES_NOT_EXIST','x',['VALID']))
 unrelated=one(('UNRELATED_SYNTAX_ERROR','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py','#!/usr/bin/env python3','this is invalid python syntax',['POSITION_FOREIGN_MAGIC']))
 holder=Path(tempfile.mkdtemp(prefix='.r10_stale_',dir=ROOT));project=holder/'project'
 try:
  shutil.copytree(ROOT,project,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.r10_*'));before,_=execute(project);ep=project/'Tests/Evidence/R4A_R9/acceptance_result.json';ep.write_text('{"result":"PASS","stale":true}\n');after,_=execute(project);stale_ignored=semantic_rows(before)==semantic_rows(after)
 finally:shutil.rmtree(holder)
 harness={'cleanMainBaseline':execute(ROOT)[0]['wrongFailures']==0,'separateTemporaryCopyPerMutant':True,'orderIndependent':order_independent,'hashOnlyNotSemantic':hash_only['SEMANTIC_MUTATION_VERDICT']=='SURVIVED' and hash_only['INTEGRITY_VERDICT']=='PROTECTED_HASH_MISMATCH','notAppliedIsNotCaught':not_applied['classification']=='NOT_APPLIED','unrelatedExitOneIsNotCaught':unrelated['classification']=='INFRASTRUCTURE_ERROR','publishedEvidenceIgnoredBySemanticRunner':stale_ignored,'mainSourceUnchanged':unchanged}
 ok=all(x['SEMANTIC_MUTATION_VERDICT']=='CAUGHT_SEMANTIC' for x in forward+reverse) and all(harness.values());out={'forward':forward,'reverse':reverse,'mechanismProbes':{'hashOnly':hash_only,'notApplied':not_applied,'unrelatedFailure':unrelated},'harness':harness,'result':'PASS' if ok else 'FAIL'};print(json.dumps(out,indent=2,sort_keys=True));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())

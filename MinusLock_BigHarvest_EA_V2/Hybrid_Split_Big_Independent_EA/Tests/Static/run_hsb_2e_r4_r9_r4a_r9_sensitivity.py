#!/usr/bin/env python3
"""Outcome-format probes plus real source mutations in isolated project copies."""
import copy,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import accept_hsb_2e_r4_r9_r4a_r9 as a
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def format_probes():
 base=a.fresh_result();probes=[]
 variants={
  'FORMAT_RESULT_ONLY':{'required':len(base['cases']),'executed':len(base['cases']),'cases':[{'caseId':x['caseId'],'result':'PASS'} for x in base['cases']]},
  'FORMAT_EMPTY_0_OF_0':{'required':0,'executed':0,'cases':[]},
  'FORMAT_MISSING_ROW':copy.deepcopy(base),'FORMAT_DUPLICATE_ID':copy.deepcopy(base),'FORMAT_CONTRADICTORY_PASS':copy.deepcopy(base)}
 variants['FORMAT_MISSING_ROW']['cases'].pop();variants['FORMAT_DUPLICATE_ID']['cases'][-1]=copy.deepcopy(variants['FORMAT_DUPLICATE_ID']['cases'][0])
 row=next(x for x in variants['FORMAT_CONTRADICTORY_PASS']['cases'] if x['actualClass']=='NORMATIVE_REJECTION');row.update(actualClass='ACCEPTED',actualCheckId='',actualReason='',result='PASS')
 for cid,data in variants.items():
  o=a.assess(data,skip_scope=True);probes.append({'caseId':cid,'acceptanceResult':o['result'],'caught':o['result']=='FAIL','findings':[x['check'] for x in o['findings']]})
 return probes
MUTANTS=[
 ('MUT_POSITION_OWNERSHIP','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"ps,ins,ds=references(r);identity(r,ps,ins,ds);phase_revision(r);far(r,ps)","ps,ins,ds=references(r);phase_revision(r);far(r,ps)"),
 ('MUT_EVENT_DEAL_BINDING','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"for n,e in enumerate(r.get('events',[])):\n  d=ds[e['dealId']]\n  keys=", "for n,e in enumerate([]):\n  d=ds[e['dealId']]\n  keys="),
 ('MUT_FAR_TICKET','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"phase_revision(r);far(r,ps)","phase_revision(r)"),
 ('MUT_COMMIT_REVISION','Tests/Static/verify_hsb_2e_r4_r9_r4a_r8.py',"if r['fsm']['outputRevision']!=r['fsm']['inputRevision']+1:reject('R8_REVISION','COMMIT_INCREMENT_REQUIRED','fsm.outputRevision')","if False:reject('R8_REVISION','COMMIT_INCREMENT_REQUIRED','fsm.outputRevision')"),
 ('MUT_CONFIRMED','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"if x['confirmed'] is not True:reject('R9_EXECUTION_CONFIRMATION','EXECUTION_NOT_CONFIRMED',f'{kind}[{n}].confirmed')","if False:reject('R9_EXECUTION_CONFIRMATION','EXECUTION_NOT_CONFIRMED',f'{kind}[{n}].confirmed')"),
 ('MUT_CONTEXT_REVISION','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"if x['stateRevision']!=c['stateRevision']:reject('R9_EXECUTION_REVISION','STATE_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].stateRevision')","if False:reject('R9_EXECUTION_REVISION','STATE_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].stateRevision')"),
 ('MUT_SCENARIO_PHASE','Tests/Static/verify_hsb_2e_r4_r9_r4a_r9.py',"v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput');scenario_phase(r);execution_records(r)","v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput');execution_records(r)")]
def mutations():
 rows=[];tmp=ROOT/'.r9_mutation_workspace'
 if tmp.exists():shutil.rmtree(tmp)
 try:
  shutil.copytree(ROOT,tmp,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.r9_mutation_workspace'))
  for cid,rel,old,new in MUTANTS:
   # restore pristine project file before every mutant
   shutil.copy2(ROOT/rel,tmp/rel);p=tmp/rel;before=h(p);s=p.read_text()
   if old not in s:raise RuntimeError(f'mutation anchor missing: {cid}')
   p.write_text(s.replace(old,new,1));after=h(p)
   cp=subprocess.run([sys.executable,'Tests/Static/accept_hsb_2e_r4_r9_r4a_r9.py'],cwd=tmp,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   rows.append({'caseId':cid,'sourcePath':rel,'beforeSha256':before,'afterSha256':after,'sourceChanged':before!=after,'exitCode':cp.returncode,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip(),'caught':cp.returncode==1})
  return rows
 finally:
  if tmp.exists():shutil.rmtree(tmp)
def main():
 f=format_probes();m=mutations();out={'formatProbes':f,'sourceMutants':m,'mainSourceUnchanged':all(h(ROOT/x[1])==xhash for x,xhash in [(z,h(ROOT/z[1])) for z in MUTANTS]),'result':'PASS' if all(x['caught'] for x in f+m) else 'FAIL'}
 print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

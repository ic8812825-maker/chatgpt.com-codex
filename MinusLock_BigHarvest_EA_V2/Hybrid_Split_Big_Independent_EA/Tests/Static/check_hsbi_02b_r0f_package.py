#!/usr/bin/env python3
"""Read-only R0F integrity verification; --seal writes only new R0F preservation."""
import json,sys,copy,tempfile,shutil
from pathlib import Path
import check_hsbi_02b_r0f_common as a

def strict(text):
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('duplicate key '+k)
   out[k]=v
  return out
 return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))

def verify(root,manifest):
 errors=[]
 def check(ok,label):
  if not ok:errors.append(label)
 try:
  check(manifest['Existing']==a.tree(),'baseline inventory')
  check(len(manifest['Production'])==74 and all(manifest['Existing'].get(k)==v for k,v in manifest['Production'].items()),'production inventory')
  for p,h in manifest['ArtifactHashes'].items():check(a.sha(root/p)==h,'artifact '+p)
  check(manifest['VerifierHash']==a.sha(__file__),'verifier source')
  def load(n,folder='Tests/Evidence'):return strict((root/folder/f'NEXT_STAGE_02B_R0F_{n}.json').read_text())
  admin=load('ADMIN_DECISIONS','Tests/Contracts');tests=load('TEST_RESULTS');cons=load('CONSISTENCY');ver=load('VERIFICATION');matrix=load('CONTRACT_MATRIX','Tests/Contracts');r1=load('R1_ACCEPTANCE_MATRIX','Tests/Contracts');gap=load('STATUS_GAP')
  import hsbi_02b_r0f_decisions as decisions
  check(admin['Rows']==decisions.rows() and len(admin['Rows'])==16 and admin['Approved']==0,'admin ballots')
  check(matrix['CodecSelected'] is None and matrix['TransitionPolicySelected'] is None,'no selected policy')
  for d,count in [(tests,116),(cons,22)]:
   rows=d['Rows'];check(type(d['Pass']) is int and d['Pass']==count and d['Fail']==0 and len(rows)==count and d['ExitCode']==0,'test totals')
   check(len({r['TestID'] for r in rows})==count,'unique tests')
   check(all(r['Result']=='PASS' and r['Actual']==r['Expected'] for r in rows),'test outcomes')
  check(tests['CandidateSourceHash']==a.sha(root/'Tests/Reference/hsbi_02b_r0f_contract_candidate.py'),'candidate execution hash')
  check(tests['FixtureSourceHash']==a.sha(root/'Tests/Reference/hsbi_02b_r0f_independent_fixtures.py'),'fixture execution hash')
  for d in [tests,cons,ver]:
   for p,h in d['SourceHashes'].items():check(a.sha(root/p)==h,'execution source '+p)
  check(ver['RegressionBaselineMatch'] is True and [(r['PassCount'],r['FailCount'],r['ExitCode']) for r in ver['Runs']]==[(57,5,1),(35,46,1)],'historical failures')
  check(ver['C3Errors']==[] and ver['C3FreshReferenceRerun'].startswith('NOT_RUN:'),'C3 scope')
  check(ver['MQL5_COMPILE']==ver['MQL5_TESTS']=='NOT_RUN','native scope')
  check(gap['Rows']==gap['IndependentExpected'] and gap['Result']=='PASS','status gap')
  check(r1['Variants'][0]['ProductionAllowlist']==['Include/Money/HSBI_EconomicLedgerTypes.mqh'] and r1['R1_1_START_ALLOWED'] is False,'R1 scope')
  verdict=(root/'Reports/NEXT_STAGE_02B_R0F_FINAL_VERDICT_RU.md').read_text()
  for field in ['ADMIN_APPROVAL_COMPLETE','R1_1_START_ALLOWED','PRODUCTION_REMEDIATION_ALLOWED','TRADING_LOGIC_START_ALLOWED','BROKER_DISPATCH_ALLOWED','REAL_TRADING_ALLOWED']:
   check(verdict.count('\n'+field+'=NO\n')==1 and verdict.count('\n'+field+'=')==1,'policy '+field)
 except (ValueError,KeyError,TypeError,OSError) as e:errors.append(type(e).__name__+': '+str(e))
 return errors

def main():
 p=a.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0F_PRESERVATION.json'
 if '--seal' in sys.argv:
  old=a.tree();files=[f for f in a.ROOT.rglob('*') if f.is_file() and ('NEXT_STAGE_02B_R0F_' in f.name or 'hsbi_02b_r0f_' in f.name) and '__pycache__' not in str(f)]
  hashes={str(f.relative_to(a.ROOT)):a.sha(f) for f in files if f!=p and not f.name.endswith('PACKAGE_RESULTS.json')}
  data=dict(a.meta(__file__),Existing=old,Production={k:v for k,v in old.items() if k.startswith('Include/') and k.endswith('.mqh') or '/' not in k and k.endswith('.mq5')},ArtifactHashes=hashes,VerifierHash=a.sha(__file__))
  a.save('PRESERVATION',data)
 manifest=strict(p.read_text());errors=verify(a.ROOT,manifest)
 if '--selftest' in sys.argv:
  probes=[]
  for kind in ['missing-baseline','bad-artifact','wrong-verifier','missing-production']:
   d=copy.deepcopy(manifest)
   if kind=='missing-baseline':d['Existing'].pop(next(iter(d['Existing'])))
   if kind=='bad-artifact':d['ArtifactHashes'][next(iter(d['ArtifactHashes']))]='0'*64
   if kind=='wrong-verifier':d['VerifierHash']='0'*64
   if kind=='missing-production':d['Production'].pop(next(iter(d['Production'])))
   probes.append(dict(ProbeID=kind,Result='PASS' if verify(a.ROOT,d) else 'FAIL'))
  for text in ['{"a":1,"a":1}','{"a":{"x":0,"x":1}}','{"a":NaN}','{"a":Infinity}']:
   try:strict(text);rejected=False
   except ValueError:rejected=True
   probes.append(dict(ProbeID='strict-json-'+str(len(probes)),Result='PASS' if rejected else 'FAIL'))
  a.save('PACKAGE_RESULTS',dict(a.meta(__file__),Positive='PASS' if not errors else 'FAIL',Errors=errors,NegativeProbes=probes,ExitCode=int(bool(errors) or any(r['Result']!='PASS' for r in probes))))
 print('PACKAGE',errors);return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())

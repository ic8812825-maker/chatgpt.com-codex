"""New output destinations; historical modules and fixtures unchanged. No historical main writers."""
import sys,json,re,importlib
from pathlib import Path
import HSBI_FULL_SYSTEM_AUDIT_02_verify as a

def main():
 jobs=[]
 for n,f in [('R7','verify_hsb_2d_v1_r7.py'),('R0','check_hsbi_02b_r0_ledger_integrity.py'),('R8','accept_hsb_2e_r4_r9_r4a_r8.py'),('R10','accept_hsb_2e_r4_r9_r4a_r10.py'),('C1','check_hsbi_02b_r0e_c1_contracts.py'),('C2','check_hsbi_02b_r0e_c2_contracts.py')]:
  cmd=[sys.executable,str(a.ROOT/'Tests/Static'/f)]
  if n=='R7':cmd+=['--root',str(a.ROOT),'--skip-seal']
  if n in ('R0','C1','C2'):cmd+=(['--enforce-contract'] if n=='R0' else [])+['--output',str(a.ROOT/'Tests/Evidence'/(a.TAG+n+'_REGRESSION.json'))]
  jobs.append((n,f,cmd))
 rows=[]
 for n,f,cmd in jobs:
  x=a.run(cmd);x.update(ID=n,SubjectRunnerSHA256=a.sha(a.ROOT/'Tests/Static'/f),SubjectSourceHashes={s['File']:s['SHA256'] for s in a.inv() if s['Production']},PassCount=None,FailCount=None,CountScope='See unchanged CLI actual stdout; no invented comparable scenario total')
  if n in ('R8','R10'):
   code='import '+Path(f).stem+' as m;import json;print(json.dumps(m.run(),default=str))';detail=a.run([sys.executable,'-c','import sys;sys.path.insert(0,"Tests/Static");'+code]);x['FindingDetails']=detail
  x['Classification']='EXPECTED_HISTORICAL_FAILURE' if n in ('R7','R0') and x['ExitCode']==1 else 'SCOPE_POLICY_FAILURE_REVIEW_DETAILS' if n in ('R8','R10') and x['ExitCode']==1 else 'PASS' if x['ExitCode']==0 else 'UNVERIFIED_NEW_FAILURE'
  rows.append(x);a.save('REGRESSIONS',dict(Runs=rows,Completed=False));print(n,x['ExitCode'],flush=True)
 for n,mod,code in [('R0F','check_hsbi_02b_r0f_contracts','r=[(c["TestID"],c["Run"]()==c["Expected"]) for c in m.cases()];print(json.dumps(r));assert all(v for _,v in r)'),('R0G','check_hsbi_02b_r0g_contracts','r=m.execute();print(json.dumps(r,default=str));assert all(c["Result"]=="PASS" for c in r)'),('R0H','check_hsbi_02b_r0h_verify','r=m.evaluate();print(json.dumps(r,default=str));assert all(c["Result"]=="PASS" for c in r)')]:
  x=a.run([sys.executable,'-c','import sys,json;sys.path[:0]=["Tests/Static","Tests/Reference"];import '+mod+' as m;'+code]);x.update(ID=n,HistoricalAPI='Actual callable evaluation; original main/save not called',SubjectRunnerSHA256=a.sha(a.ROOT/'Tests/Static'/(mod+'.py')),SubjectSourceHashes={str(p.relative_to(a.ROOT)):a.sha(p) for p in (a.ROOT/'Tests/Reference').glob('hsbi_02b*.py')},Classification='PASS' if x['ExitCode']==0 else 'INFRASTRUCTURE_OR_TEST_FAILURE');rows.append(x);print(n,x['ExitCode'],flush=True)
 a.save('REGRESSIONS',dict(BaseSHA=a.BASE,Runs=rows,Completed=True,RunnerSHA256=a.sha(__file__),Boundary='Selected requested suites only. No native MQL5. Fresh Run calls for R0F; stdout per-row outcomes retained.'))
if __name__=='__main__':main()

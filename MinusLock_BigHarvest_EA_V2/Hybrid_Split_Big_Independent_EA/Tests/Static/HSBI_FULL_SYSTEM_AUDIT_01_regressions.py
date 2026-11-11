"""Safe fresh frozen CLIs with new output paths and real process exits.
No --publish-evidence, old orchestrators, package sealing or native-MQL claims.
"""
import os,sys,subprocess,json,re
from pathlib import Path
import HSBI_FULL_SYSTEM_AUDIT_01_common as a

def main():
 started=a.now();jobs=[]
 for name,file in [('R8','accept_hsb_2e_r4_r9_r4a_r8.py'),('R10','accept_hsb_2e_r4_r9_r4a_r10.py'),('R12','accept_hsb_2e_r4_r9_r4a_r12_second_block.py'),('R12A','check_hsb_2e_r4_r9_r4a_r12a_fix_01.py')]:jobs.append((name,[sys.executable,str(a.ROOT/'Tests/Static'/file)],0))
 jobs.append(('R7_FROZEN',[sys.executable,str(a.ROOT/'Tests/Static/verify_hsb_2d_v1_r7.py'),'--root',str(a.ROOT),'--skip-seal'],1))
 jobs.append(('R0',[sys.executable,str(a.ROOT/'Tests/Static/check_hsbi_02b_r0_ledger_integrity.py'),'--enforce-contract','--output',str(a.ROOT/'Tests/Evidence/HSBI_FULL_SYSTEM_AUDIT_01_R0_RECHECK.json')],1))
 for name,file in [('R0A','check_hsbi_02b_r0a_normative_contracts.py'),('R0B','check_hsbi_02b_r0b_contracts.py'),('R0C','check_hsbi_02b_r0c_contracts.py'),('R0D','check_hsbi_02b_r0d_contracts.py'),('R0E','check_hsbi_02b_r0e_contracts.py'),('C1','check_hsbi_02b_r0e_c1_contracts.py'),('C2','check_hsbi_02b_r0e_c2_contracts.py')]:jobs.append((name,[sys.executable,str(a.ROOT/'Tests/Static'/file),'--output',str(a.ROOT/'Tests/Evidence'/('HSBI_FULL_SYSTEM_AUDIT_01_'+name+'_RECHECK.json'))],0))
 runs=[]
 for name,cmd,historical_exit in jobs:
  begin=a.now();p=subprocess.run(cmd,cwd=a.ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));parsed={};target=Path(cmd[cmd.index('--output')+1]) if '--output' in cmd else None
  if target and target.exists():parsed=json.loads(target.read_text())
  passcount=failcount=None;countscope='Actual CLI stdout retained; aggregate acceptance findings separate from scenario counts'
  if name=='R7_FROZEN':
   mp=re.search(r'^CLEAN_PASS=(\d+)',p.stdout,re.M);mf=re.search(r'^CLEAN_FAIL=(\d+)',p.stdout,re.M)
   if mp and mf:passcount=int(mp[1]);failcount=int(mf[1]);countscope='Frozen static checks'
  elif name=='R0':passcount=sum(r['contractPass'] for r in parsed.get('nativeCases',[]));failcount=parsed.get('normativeMismatchCount');countscope='Frozen extracted C++ contract cases; not MQL5 native'
  elif parsed:
   passcount=parsed.get('passed',parsed.get('Pass'));failcount=parsed.get('failed',parsed.get('Fail'));countscope='Historical runner own test/execution counting; contexts not distinct scenarios'
  detail=None
  if name in ('R8','R10','R12','R12A') and p.returncode:
   # Independent read-only module call for exact finding details; no publication flag.
   mod=Path(cmd[1]).stem;code='import sys,json;sys.path.insert(0,"Tests/Static");import '+mod+' as m;print(json.dumps(m.run(),ensure_ascii=False,default=str))'
   dp=subprocess.run([sys.executable,'-c',code],cwd=a.ROOT,text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));detail=dict(Command=[sys.executable,'-c',code],ExitCode=dp.returncode,Stdout=dp.stdout,Stderr=dp.stderr)
  runs.append(dict(ID=name,Command=cmd,StartedUtc=begin,FinishedUtc=a.now(),TestedSHA=a.BASE,RunnerSourceHash=a.sha(Path(__file__)),SubjectSourceHash=a.sha(Path(cmd[1])),ExitCode=p.returncode,PassCount=passcount,FailCount=failcount,CountScope=countscope,HistoricalC3ExitCode=historical_exit,ExitMatchesC3=p.returncode==historical_exit,Stdout=p.stdout,Stderr=p.stderr,EvidencePath=str(target.relative_to(a.ROOT)) if target else 'HSBI_FULL_SYSTEM_AUDIT_01_REGRESSIONS.json#'+name,AcceptanceDetail=detail))
  print(name,'exit',p.returncode,'pass',passcount,'fail',failcount,flush=True)
  a.save('REGRESSIONS',dict(a.meta(__file__),StartedUtc=started,FinishedUtc=a.now(),Runs=runs,Completed=False))
 # Latest reference-only APIs invoked without their historical main()/save().
 for name,code in [('R0F','import check_hsbi_02b_r0f_contracts as m; print(len(m.cases()))'),('R0G','import check_hsbi_02b_r0g_contracts as m; r=m.execute(); print(len(r),sum(x["Result"]=="PASS" for x in r)); assert all(x["Result"]=="PASS" for x in r)'),('R0H','import check_hsbi_02b_r0h_verify as m; r=m.evaluate(); print(len(r),sum(x["Result"]=="PASS" for x in r)); assert all(x["Result"]=="PASS" for x in r)')]:
  prefix='import sys;sys.path[:0]=["Tests/Static","Tests/Reference"];';cmd=[sys.executable,'-c',prefix+code];begin=a.now();p=subprocess.run(cmd,cwd=a.ROOT,capture_output=True,text=True)
  runs.append(dict(ID=name+'_API',Command=cmd,StartedUtc=begin,FinishedUtc=a.now(),TestedSHA=a.BASE,RunnerSourceHash=a.sha(Path(__file__)),ExitCode=p.returncode,PassCount=None,FailCount=None,CountScope='Direct immutable API run; see actual stdout',Stdout=p.stdout,Stderr=p.stderr,EvidencePath='HSBI_FULL_SYSTEM_AUDIT_01_REGRESSIONS.json#'+name))
 a.save('REGRESSIONS',dict(a.meta(__file__),StartedUtc=started,FinishedUtc=a.now(),Runs=runs,Completed=True,HistoricalResultsNotOverwritten=True,NewOrchestratorScope='Fresh selected suites; full279 executable tests not all run',C3FullSuite='HISTORICAL_EVIDENCE_ONLY; source/event audits current separately'))
 return 0
if __name__=='__main__':raise SystemExit(main())

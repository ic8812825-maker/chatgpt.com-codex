#!/usr/bin/env python3
"""Historical commands; new R0E outputs only. Baseline package in disposable tree."""
import hashlib,json,os,subprocess,sys,tempfile,tarfile,io
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
BASE='2d34c3378edc5f2df064282fa067bb4af2a1e3b0'
def now():return datetime.now(timezone.utc).isoformat()
def main():
 old=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0D_REGRESSIONS.json').read_text());runs=[]
 jobs=[]
 for row in old['runs']:
  if not row.get('Command'):continue
  cmd=row['Command'][:]
  if '--output' in cmd:cmd[cmd.index('--output')+1]=str(ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0E_'+row['id']+'_RECHECK.json'))
  jobs.append((row['id'],cmd,row['ExpectedBaselineExit'],row['PassCount'],row['FailCount'],row['CountScope']))
 for name,script in [('R0D_reference','check_hsbi_02b_r0d_contracts.py'),('R0D_mutations','check_hsbi_02b_r0d_mutations.py')]:jobs.append((name,[sys.executable,str(ROOT/'Tests/Static'/script),'--output',str(ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0E_'+name+'_RECHECK.json'))],0,None,None,'frozen R0D cases / mutation probes'))
 def execute(name,cmd,expected,pc,fc,scope):
  start=now();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  if '--output' in cmd and Path(cmd[cmd.index('--output')+1]).exists():
   d=json.loads(Path(cmd[cmd.index('--output')+1]).read_text())
   if 'nativeCases' in d:pc=sum(r['contractPass'] for r in d['nativeCases']);fc=d['normativeMismatchCount']
   elif 'mutations' in d:pc=d.get('killed',len(d['mutations'])-d.get('finalSurvivors',d.get('survived',0)));fc=d.get('finalSurvivors',d.get('survived',0))
   elif 'passed' in d:pc=d['passed'];fc=d.get('failed',0)
  sources={str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
  for arg in cmd:
   f=Path(arg)
   if f.suffix=='.py' and f.is_file() and f.is_relative_to(ROOT):sources[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
  runs.append(dict(id=name,Command=cmd,StartedUtc=start,FinishedUtc=now(),TestedSHA=BASE,SourceHashes=sources,ExitCode=p.returncode,PassCount=pc,FailCount=fc,CountScope=scope,BaselineMatch=p.returncode==expected,ExpectedBaselineExit=expected,Classification='EXPECTED_HISTORICAL_FAILURE' if p.returncode==expected and expected else 'PASS' if p.returncode==0 else 'NEW_REGRESSION',Stdout=p.stdout,Stderr=p.stderr,EvidencePath='Tests/Evidence/NEXT_STAGE_02B_R0E_REGRESSIONS.json#'+name))
  print(name,p.returncode,pc,fc,flush=True)
 for job in jobs:execute(*job)
 # Frozen strict package inventory cannot include later R0E files; verify exact Git baseline.
 with tempfile.TemporaryDirectory(prefix='R0E_baseline_',dir=ROOT/'Tests') as td:
  raw=subprocess.check_output(['git','archive',BASE,PREFIX],cwd=REPO)
  with tarfile.open(fileobj=io.BytesIO(raw)) as tar:tar.extractall(td,filter='data')
  candidate=Path(td)/PREFIX
  execute('R0D_package_baseline',[sys.executable,str(ROOT/'Tests/Static/check_hsbi_02b_r0d_package.py'),'--root',str(candidate),'--repo',str(REPO)],0,None,None,'frozen checker on disposable exact 2d34c33 tree; stdout preserved')
 runs.append(dict(id='02A_standalone',Command=None,ExitCode=None,PassCount=None,FailCount=None,Classification='NOT_RUN',Reason='No standalone executable suite; archived execution commands rerun above, including no-trade scan.'))
 out=dict(BaseSHA=BASE,UTC=now(),runs=runs,BaselineMatch=all(r['BaselineMatch'] for r in runs if 'BaselineMatch' in r),RegressionStatus='FAIL' if any(r.get('ExitCode') not in (0,None) for r in runs) else 'PASS')
 (ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_REGRESSIONS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');return int(not out['BaselineMatch'])
if __name__=='__main__':raise SystemExit(main())

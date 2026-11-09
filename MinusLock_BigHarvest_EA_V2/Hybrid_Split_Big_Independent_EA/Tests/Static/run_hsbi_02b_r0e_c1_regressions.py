#!/usr/bin/env python3
"""Frozen suites, new C1 outputs only; archived strict packages never resealed."""
import hashlib,io,json,os,runpy,subprocess,sys,tarfile,tempfile
from pathlib import Path
import check_hsbi_02b_r0e_c1_contracts as t
ROOT=t.ROOT;REPO=ROOT.parents[1];PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
def main():
 started=t.now();old=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_REGRESSIONS.json').read_text());runs=[];counter=runpy.run_path(str(ROOT/'Tests/Static/run_hsbi_02b_r0b_regressions.py'))['counts']
 with tempfile.TemporaryDirectory(prefix='R0E_C1_archive_',dir=ROOT/'Tests') as td:
  archives={}
  for ref in (t.BASE,'2d34c3378edc5f2df064282fa067bb4af2a1e3b0'):archives[ref]=Path(td)/ref/PREFIX
  jobs=[]
  for row in old['runs']:
   if not row.get('Command'):continue
   cmd=row['Command'][:]
   if '--output' in cmd:cmd[cmd.index('--output')+1]=str(ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0E_C1_'+row['id']+'_RECHECK.json'))
   if row['id']=='R0D_package_baseline':cmd[cmd.index('--root')+1]=str(archives['2d34c3378edc5f2df064282fa067bb4af2a1e3b0'])
   jobs.append((row['id'],cmd,row['ExitCode'],row['PassCount'],row['FailCount'],row['CountScope']))
  jobs.append(('R0E_reference',[sys.executable,str(ROOT/'Tests/Static/check_hsbi_02b_r0e_contracts.py'),'--output',str(ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C1_R0E_reference_RECHECK.json')],0,728,0,'91 scenarios ×8 contexts; 1456 top-level comparisons'))
  code="import sys,json;from pathlib import Path;sys.path.insert(0,"+repr(str(ROOT/'Tests/Static'))+");import check_hsbi_02b_r0e_package as p;errors=p.verify(Path("+repr(str(archives[t.BASE]))+"));print(json.dumps(errors));raise SystemExit(bool(errors))"
  jobs.append(('R0E_package_baseline',[sys.executable,'-c',code],0,None,None,'Frozen strict checker on exact 074165b archive; not current C1 inventory'))
  for name,cmd,expected,oldpc,oldfc,scope in jobs:
   # Materialize only AFTER recursive historical scanners have finished.
   if name in ('R0D_package_baseline','R0E_package_baseline'):
    ref=t.BASE if name=='R0E_package_baseline' else '2d34c3378edc5f2df064282fa067bb4af2a1e3b0'
    dest=Path(td)/ref;dest.mkdir();raw=subprocess.check_output(['git','archive',ref,PREFIX],cwd=REPO)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:tar.extractall(dest,filter='data')
   start=t.now();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
   pc,fc,countscope=counter(name,p.stdout)
   if '--output' in cmd:
    file=Path(cmd[cmd.index('--output')+1])
    if file.exists():
     data=json.loads(file.read_text())
     if 'nativeCases' in data:pc=sum(r['contractPass'] for r in data['nativeCases']);fc=data['normativeMismatchCount']
     elif 'mutations' in data:pc=data.get('killed',len(data['mutations'])-data.get('finalSurvivors',data.get('survived',0)));fc=data.get('finalSurvivors',data.get('survived',0))
     elif 'passed' in data:pc,fc=data['passed'],data['failed']
   if name=='02A_no_trade_scan':d=json.loads(p.stdout);pc,fc=d['files']-len(d['forbidden']),len(d['forbidden'])
   hashes={str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
   for item in cmd:
    path=Path(item)
    if path.suffix=='.py' and path.is_file() and path.is_relative_to(ROOT):hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
   if name=='R0E_package_baseline':hashes['Tests/Static/check_hsbi_02b_r0e_package.py']=hashlib.sha256((ROOT/'Tests/Static/check_hsbi_02b_r0e_package.py').read_bytes()).hexdigest()
   countmatch=oldpc is None or (pc,fc)==(oldpc,oldfc)
   runs.append(dict(ID=name,Command=cmd,StartedUtc=start,FinishedUtc=t.now(),TestedSHA=t.metadata()['TestedSHA'],SourceHashes=hashes,ExitCode=p.returncode,PassCount=pc,FailCount=fc,CountScope=scope,ExpectedBaselineExit=expected,ExpectedPass=oldpc,ExpectedFail=oldfc,BaselineMatch=p.returncode==expected and countmatch,Classification='EXPECTED_HISTORICAL_FAILURE' if expected and p.returncode==expected else 'PASS' if p.returncode==0 else 'NEW_REGRESSION',Stdout=p.stdout,Stderr=p.stderr,EvidencePath='Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REGRESSIONS.json#'+name));print(name,p.returncode,pc,fc,flush=True)
 repro=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REPRODUCTION.json').read_text());sm=repro['StockMutations']
 runs.append(dict(ID='R0E_mutations',Command=repro['Command'],StartedUtc=repro['StartedUtc'],FinishedUtc=repro['FinishedUtc'],TestedSHA=repro['TestedSHA'],SourceHashes=repro['SourceHashes'],ExitCode=repro['ExitCode'],PassCount=sum(r['Killed'] for r in sm),FailCount=sum(not r['Killed'] for r in sm),CountScope='Original13 catalog executed during autonomous reproduction; referenced execution, not second standalone CLI run',BaselineMatch=all(r['Killed'] for r in sm),ExpectedBaselineExit=0,ExpectedPass=13,ExpectedFail=0,ExecutionRef='Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REPRODUCTION.json#StockMutations',Stdout='See independently stored original/mutant control outcomes',Stderr='',Classification='PASS',EvidencePath='Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REGRESSIONS.json#R0E_mutations'))
 out=dict(t.metadata(),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=t.now(),SourceHashes={**t.hashes(),str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},Runs=runs,BaselineMatch=all(r['BaselineMatch'] for r in runs),RegressionStatus='FAIL' if any(r['ExitCode'] for r in runs) else 'PASS',Standalone02A='NOT_RUN: no standalone executable; archived commands covered by named suites',MQL5_COMPILE='NOT_RUN',MQL5_TESTS='NOT_RUN',STRATEGY_TESTER='NOT_RUN');out['ExitCode']=int(not out['BaselineMatch']);t.save(ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REGRESSIONS.json',out);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())

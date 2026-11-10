#!/usr/bin/env python3
"""Safe regression runner: current source hash; only new C2 outputs; historical exits preserved."""
import argparse,copy,io,json,os,runpy,subprocess,sys,tarfile,tempfile,types,importlib
from pathlib import Path
import check_hsbi_02b_r0e_c3_common as t
SELF=str(Path(__file__).resolve());PREFIX=t.ROOT.relative_to(t.REPO).as_posix()+'/'
def role(name,path=None):
 if name in ('C1_mutations','C2_mutations'):
  mu=importlib.import_module('check_hsbi_02b_r0e_c1_mutations' if name.startswith('C1') else 'check_hsbi_02b_r0e_c2_mutations')
  r=mu.run();print(json.dumps(dict(PassCount=r['Killed'],FailCount=r['UnexplainedSurvivors']+r['InfrastructureErrors'],RedundantSurvivors=r['RedundantSurvivors'])));return int(r['UnexplainedSurvivors']+r['InfrastructureErrors']>0)
 if name=='R0E_mutations':
  import check_hsbi_02b_r0e_contracts as old
  import check_hsbi_02b_r0e_mutations as mu
  source=Path(old.model.__file__).read_text();specs={r['TestID']:r for r in old.cases()};rows=[]
  for n,f,p,q,edits in mu.catalog():
   s=source
   for a,b in edits:s=s.replace(a,b)
   m=types.ModuleType(n);m.__file__=n;exec(compile(s,n,'exec'),m.__dict__);pos,neg=specs[p],specs[q];pe=old.view(pos['Expected']);ne=old.view(neg['Expected']);op,mp,on,mn=[old.view(c['run'](sub)) for c,sub in ((pos,old.model),(pos,m),(neg,old.model),(neg,m))];rows.append(op==mp==pe and on==ne and mn!=ne)
  print(json.dumps(dict(PassCount=sum(rows),FailCount=len(rows)-sum(rows))));return int(not all(rows))
 if name in ('C1_package_baseline','C2_package_baseline','R0E_package_baseline'):
  mod=importlib.import_module('check_hsbi_02b_r0e_c1_package' if name.startswith('C1') else 'check_hsbi_02b_r0e_c2_package' if name.startswith('C2') else 'check_hsbi_02b_r0e_package');errors=mod.verify(Path(path),t.REPO) if name.startswith(('C1','C2')) else mod.verify(Path(path));print(json.dumps(errors));return int(bool(errors))
 raise ValueError(name)
def main():
 p=argparse.ArgumentParser();p.add_argument('--role');p.add_argument('--root');args=p.parse_args()
 if args.role:return role(args.role,args.root)
 started=t.now();old=json.loads((t.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C1_REGRESSIONS.json').read_text());runs=[];counter=runpy.run_path(str(t.ROOT/'Tests/Static/run_hsbi_02b_r0b_regressions.py'))['counts']
 jobs=[dict(r) for r in old['Runs']];jobs += [dict(ID='C1_reference',Command=[sys.executable,str(t.ROOT/'Tests/Static/check_hsbi_02b_r0e_c1_contracts.py'),'--output','PLACEHOLDER'],ExitCode=0,PassCount=840,FailCount=0,CountScope='105 C1 scenarios x8'),dict(ID='C1_mutations',Command=[sys.executable,SELF,'--role','C1_mutations'],ExitCode=0,PassCount=54,FailCount=0,CountScope='55 C1 catalog:54 kills +1 explained survivor'),dict(ID='C1_package_baseline',Command=[],ExitCode=0,PassCount=None,FailCount=None,CountScope='Strict checker on exact C1 Git archive')]
 jobs += [dict(ID='C2_reference',Command=[sys.executable,str(t.ROOT/'Tests/Static/check_hsbi_02b_r0e_c2_contracts.py'),'--output','PLACEHOLDER'],ExitCode=0,PassCount=1264,FailCount=0,CountScope='158 C2 scenarios x8, schema separately'),dict(ID='C2_mutations',Command=[sys.executable,SELF,'--role','C2_mutations'],ExitCode=0,PassCount=64,FailCount=0,CountScope='70 C2 catalog:64 killed +6 reported redundant, independent C3 classification elsewhere'),dict(ID='C2_package_baseline',Command=[],ExitCode=0,PassCount=None,FailCount=None,CountScope='C2 checker exact Git archive3737116')]
 # Archives materialize lazily after recursive scanners, then are always removed.
 with tempfile.TemporaryDirectory(prefix='R0E_C3_reg_archive_',dir=t.ROOT/'Tests') as td:
  refs={'R0D_package_baseline':'2d34c3378edc5f2df064282fa067bb4af2a1e3b0','R0E_package_baseline':'074165b38f1b6d6253a9629c7d2def988e8e286a','C1_package_baseline':'fae7dfc18ca2d61af2f3446826ef3031825bbfd8','C2_package_baseline':t.BASE}
  for spec in jobs:
   name=spec['ID'];cmd=spec['Command'][:]
   if '--output' in cmd:cmd[cmd.index('--output')+1]=str(t.ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0E_C3_C2_C1_'+name+'_RECHECK.json'))
   if name=='R0E_mutations':cmd=[sys.executable,SELF,'--role',name]
   if name in refs:
    dest=Path(td)/refs[name];dest.mkdir();raw=subprocess.check_output(['git','archive',refs[name],PREFIX],cwd=t.REPO)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:tar.extractall(dest,filter='data')
    archive=dest/PREFIX
    if name=='R0D_package_baseline':cmd[cmd.index('--root')+1]=str(archive)
    else:cmd=[sys.executable,SELF,'--role',name,'--root',str(archive)]
   start=t.now();p=subprocess.run(cmd,cwd=t.ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));pc,fc,scope=counter(name,p.stdout)
   if '--output' in cmd:
    file=Path(cmd[cmd.index('--output')+1])
    if file.exists():
     data=json.loads(file.read_text())
     if 'nativeCases' in data:pc=sum(r['contractPass'] for r in data['nativeCases']);fc=data['normativeMismatchCount']
     elif 'mutations' in data:pc=data.get('killed',len(data['mutations'])-data.get('finalSurvivors',data.get('survived',0)));fc=data.get('finalSurvivors',data.get('survived',0))
     elif 'passed' in data:pc,fc=data['passed'],data['failed']
     elif 'Pass' in data:pc,fc=data['Pass'],data['Fail']
   if name in ('C1_mutations','C2_mutations','R0E_mutations'):d=json.loads(p.stdout.splitlines()[-1]);pc,fc=d['PassCount'],d['FailCount']
   if name=='02A_no_trade_scan':d=json.loads(p.stdout);pc,fc=d['files']-len(d['forbidden']),len(d['forbidden'])
   pins={**t.pins(),str(Path(__file__).relative_to(t.ROOT)):t.sha(Path(__file__))}
   for arg in cmd:
    f=Path(arg)
    if f.suffix=='.py' and f.is_file() and f.is_relative_to(t.ROOT):pins[str(f.relative_to(t.ROOT))]=t.sha(f)
   if name.endswith('package_baseline'):file='Tests/Static/check_hsbi_02b_r0e_c2_package.py' if name.startswith('C2') else 'Tests/Static/check_hsbi_02b_r0e_c1_package.py' if name.startswith('C1') else 'Tests/Static/check_hsbi_02b_r0e_package.py' if name.startswith('R0E') else 'Tests/Static/check_hsbi_02b_r0d_package.py';pins[file]=t.sha(t.ROOT/file)
   if name=='C1_mutations':pins['Tests/Static/check_hsbi_02b_r0e_c1_mutations.py']=t.sha(t.ROOT/'Tests/Static/check_hsbi_02b_r0e_c1_mutations.py')
   match=p.returncode==spec['ExitCode'] and (spec['PassCount'] is None or (pc,fc)==(spec['PassCount'],spec['FailCount']))
   runs.append(dict(ID=name,Command=cmd,StartedUtc=start,FinishedUtc=t.now(),TestedSHA=t.metadata(__file__)['TestedSHA'],SourceHashes=pins,SubjectSourceHashes=pins,RunnerSourceHash=t.sha(Path(__file__)),ExitCode=p.returncode,PassCount=pc,FailCount=fc,CountScope=spec['CountScope'],ExpectedBaselineExit=spec['ExitCode'],BaselineMatch=match,Classification='EXPECTED_HISTORICAL_FAILURE' if p.returncode and match else 'PASS' if match else 'NEW_REGRESSION',Stdout=p.stdout,Stderr=p.stderr,EvidencePath='Tests/Evidence/NEXT_STAGE_02B_R0E_C3_REGRESSIONS.json#'+name));print(name,p.returncode,pc,fc,match,flush=True)
 out=dict({k:v for k,v in t.metadata(__file__).items() if k!='SourceHashes'},Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=t.now(),SourceHashes={**t.pins(),str(Path(__file__).relative_to(t.ROOT)):t.sha(Path(__file__))},Runs=runs,BaselineMatch=all(r['BaselineMatch'] for r in runs),RegressionStatus='FAIL' if any(r['ExitCode'] for r in runs) else 'PASS',Standalone02A='NOT_RUN: no standalone executable; report commands/no-trade scan repeated',MQL5_COMPILE='NOT_RUN',MQL5_TESTS='NOT_RUN',STRATEGY_TESTER='NOT_RUN');out['ExitCode']=int(not out['BaselineMatch']);t.save('REGRESSIONS',out);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())

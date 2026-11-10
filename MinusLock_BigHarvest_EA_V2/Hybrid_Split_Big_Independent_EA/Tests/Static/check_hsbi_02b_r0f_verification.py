#!/usr/bin/env python3
"""Read-only C3 evidence validation + fresh required historical regressions. No old outputs."""
import subprocess,sys,io,tarfile,tempfile,json,os
from pathlib import Path
import check_hsbi_02b_r0f_common as a

def main():
 started=a.now();pins={**a.meta(__file__)['SourceHashes']};old=a.tree();required=[f'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_{s}.json' for s in ('BASELINE','C2_REFERENCE','C2_MUTATIONS','C2_PACKAGE','REPRODUCTION','SURVIVORS','INDEPENDENT_TESTS','NATIVE_SUBSET','REGRESSIONS','EXECUTIONS','DEVELOPMENT','PRESERVATION','PACKAGE_RESULTS')];assert all(p in old for p in required)
 import check_hsbi_02b_r0e_c3_package as archived
 with tempfile.TemporaryDirectory(prefix='02B_R0F_C3_archive_',dir=a.ROOT/'Tests') as td:
  raw=subprocess.check_output(['git','archive',a.BASE,a.PREFIX],cwd=a.REPO)
  with tarfile.open(fileobj=io.BytesIO(raw)) as tf:tf.extractall(td,filter='data')
  errors=archived.verify(Path(td)/a.PREFIX,True)
 pins[str(Path(archived.__file__).relative_to(a.ROOT))]=a.sha(Path(archived.__file__))
 # No archive/disposable worker remains while the frozen recursive R7 scanner runs.
 jobs=[('R7_frozen',[sys.executable,str(a.ROOT/'Tests/Static/verify_hsb_2d_v1_r7.py'),'--root',str(a.ROOT),'--skip-seal'],57,5),('02B_R0',[sys.executable,str(a.ROOT/'Tests/Static/check_hsbi_02b_r0_ledger_integrity.py'),'--output',str(a.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0F_02B_R0_RECHECK.json')],35,46)]
 # Obtain the real archived R0 command; do not guess a historical filename/interface.
 c3=json.loads((a.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_REGRESSIONS.json').read_text());r0=next(r for r in c3['Runs'] if r['ID']=='02B_R0')['Command'][:];r0[r0.index('--output')+1]=str(a.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0F_02B_R0_RECHECK.json');jobs[1]=('02B_R0',r0,35,46)
 runs=[]
 for name,cmd,expected_pass,expected_fail in jobs:
  begin=a.now();p=subprocess.run(cmd,cwd=a.ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));pc,fc=None,None
  if name=='R7_frozen':
   import re
   pc=int(re.search(r'^CLEAN_PASS=(\d+)',p.stdout,re.M)[1]);fc=int(re.search(r'^CLEAN_FAIL=(\d+)',p.stdout,re.M)[1])
  else:
   d=json.loads(Path(cmd[cmd.index('--output')+1]).read_text());pc=sum(r['contractPass'] for r in d['nativeCases']);fc=d['normativeMismatchCount']
  hashes={str(Path(__file__).relative_to(a.ROOT)):a.sha(Path(__file__))}
  for part in cmd:
   path=Path(part)
   if path.suffix=='.py' and path.is_file() and path.is_relative_to(a.ROOT):hashes[str(path.relative_to(a.ROOT))]=a.sha(path)
  match=(p.returncode,pc,fc)==(1,expected_pass,expected_fail);runs.append(dict(ID=name,Command=cmd,StartedUtc=begin,FinishedUtc=a.now(),TestedSHA=a.BASE,SourceHashes=hashes,RunnerSourceHash=a.sha(Path(__file__)),ExitCode=p.returncode,PassCount=pc,FailCount=fc,ExpectedExitCode=1,BaselineMatch=match,Classification='EXPECTED_HISTORICAL_FAILURE' if match else 'UNEXPECTED_DIFFERENCE',Stdout=p.stdout,Stderr=p.stderr,CountScope='Frozen historical assertions; FAIL remains FAIL',EvidencePath='Tests/Evidence/NEXT_STAGE_02B_R0F_VERIFICATION.json#'+name))
 result=dict(a.meta(__file__),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=a.now(),C3EvidenceStatus='ARCHIVED_EVIDENCE_VERIFIED' if not errors else 'FAIL',C3Errors=errors,C3RequiredEvidence={p:old[p]['SHA256'] for p in required},C3FreshReferenceRerun='NOT_RUN: archived C3 evidence/code validated; R0F new contracts tested separately',Runs=runs,RegressionStatus='FAIL',RegressionBaselineMatch=all(r['BaselineMatch'] for r in runs),MQL5_COMPILE='NOT_RUN',MQL5_TESTS='NOT_RUN',STRATEGY_TESTER='NOT_RUN');result['SourceHashes'].update(pins);result['ExitCode']=int(bool(errors) or not result['RegressionBaselineMatch']);a.save('VERIFICATION',result);print('VERIFICATION',result['ExitCode'],[(r['ID'],r['PassCount'],r['FailCount']) for r in runs]);return result['ExitCode']
if __name__=='__main__':raise SystemExit(main())

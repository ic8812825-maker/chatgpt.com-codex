#!/usr/bin/env python3
"""Capture real child-process commands, source hashes, exit codes, separated stdout/stderr."""
import subprocess,sys,os,json
from pathlib import Path
import check_hsbi_02b_r0e_c3_common as a
JOBS={'reproduction':'check_hsbi_02b_r0e_c3_reproduction.py','independent':'check_hsbi_02b_r0e_c3_independent.py','native':'check_hsbi_02b_r0e_c3_native.py','regressions':'run_hsbi_02b_r0e_c3_regressions.py'}
def main():
 selected=[n for n in sys.argv[1:] if n!='--continue'] or list(JOBS)
 prior=a.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_EXECUTIONS.json'
 previous=json.loads(prior.read_text()) if '--continue' in sys.argv and prior.exists() else {}
 rows=[r for r in previous.get('Rows',[]) if r['ID'] not in selected];started=a.now()
 for name in selected:
  runner=a.ROOT/'Tests/Static'/JOBS[name];cmd=[sys.executable,str(runner)];begin=a.now();p=subprocess.run(cmd,cwd=a.ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  rows.append(dict(ID=name,Command=cmd,StartedUtc=begin,FinishedUtc=a.now(),TestedSHA=a.BASE,SourceHashes={**a.pins(),str(runner.relative_to(a.ROOT)):a.sha(runner)},RunnerSourceHash=a.sha(runner),ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr,CountScope='Parent CLI process. Role-specific counts in linked evidence; no invented independent subprocess for direct function roles.',EvidencePath='Tests/Evidence/NEXT_STAGE_02B_R0E_C3_EXECUTIONS.json#'+name));print(name,p.returncode,flush=True)
  a.save('EXECUTIONS',dict(a.metadata(__file__),StartedUtc=started,FinishedUtc=a.now(),Command=[sys.executable,*sys.argv],Rows=rows,PriorExecutionCommand=previous.get('Command'),PriorExecutionFinishedUtc=previous.get('FinishedUtc'),ExitCode=int(any(r['ExitCode'] for r in rows))))
 return int(any(r['ExitCode'] for r in rows))
if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""Read-only historical commands, all fresh output paths belong to R0D."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_hsbi_02b_r0d_contracts as t
ROOT=t.ROOT


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='Tests/Evidence/NEXT_STAGE_02B_R0D_REGRESSIONS.json');a=parser.parse_args()
    historical=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0C_REGRESSIONS.json').read_text());jobs=[]
    for row in historical['runs']:
        if not row.get('Command'):continue
        cmd=row['Command'][:]
        if '--output' in cmd:cmd[cmd.index('--output')+1]=str(ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0D_'+row['id']+'_RECHECK.json'))
        jobs.append((row['id'],cmd,row['ExitCode'],row.get('passCount'),row.get('failCount'),row.get('countScope')))
    for name,script,counts in [('R0C_reference','check_hsbi_02b_r0c_contracts.py',(221,0)),('R0C_mutations','check_hsbi_02b_r0c_mutations.py',(30,0)),('R0C_package','check_hsbi_02b_r0c_package.py',(None,None))]:
        cmd=['python3',str(ROOT/'Tests/Static'/script)]
        if name!='R0C_package':cmd+=['--output',str(ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0D_'+name+'_RECHECK.json'))]
        jobs.append((name,cmd,0,*counts,'historical reference/mutation/package check'))
    counter=runpy.run_path(str(ROOT/'Tests/Static/run_hsbi_02b_r0b_regressions.py'))['counts'];rows=[]
    for name,cmd,expected,_,__,oldscope in jobs:
        start=datetime.now(timezone.utc).isoformat();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        passed,failed,scope=counter(name,p.stdout)
        if '--output' in cmd:
            data=json.loads(Path(cmd[cmd.index('--output')+1]).read_text())
            if 'nativeCases' in data:passed,failed=sum(r['contractPass'] for r in data['nativeCases']),data['normativeMismatchCount'];scope='native proposed-contract comparisons'
            elif 'mutations' in data:passed=len(data['mutations'])-data.get('finalSurvivors',data.get('survived',0));failed=data.get('finalSurvivors',data.get('survived',0));scope='historical planned mutation catalog; raw infrastructure counts retained'
            else:passed,failed=data['passed'],data['failed'];scope='historical reported semantic cases'
        if name=='02A_no_trade_scan':
            d=json.loads(p.stdout);passed=d['files']-len(d['forbidden']);failed=len(d['forbidden']);scope='static production files; scanner controls separate'
        sources={str(Path(__file__).resolve().relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        for item in cmd:
            path=Path(item)
            if path.suffix=='.py' and path.is_file() and path.is_relative_to(ROOT):sources[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        row=dict(id=name,Command=cmd,StartedUtc=start,FinishedUtc=datetime.now(timezone.utc).isoformat(),TestedSHA=t.metadata()['testedSHA'],SourceHashes=sources,ExitCode=p.returncode,PassCount=passed,FailCount=failed,CountScope=scope,Stdout=p.stdout,Stderr=p.stderr,EvidencePath=a.output+'#'+name,BaselineMatch=p.returncode==expected,ExpectedBaselineExit=expected)
        rows.append(row);print(name,'exit',p.returncode,'PASS',passed,'FAIL',failed,flush=True)
    rows.append(dict(id='02A',Command=None,ExitCode=None,PassCount=None,FailCount=None,status='NOT_RUN_AS_SEPARATE_SUITE',reason='No standalone suite; executable commands of archived 02A report rerun in named R8/R10/R12/R12A/R7 and static scan. Native/broker NOT_RUN.'))
    out=dict(t.metadata(),runs=rows,BaselineMatch=all(r['BaselineMatch'] for r in rows if 'BaselineMatch' in r),RegressionStatus='FAIL' if any(r['ExitCode'] not in (0,None) for r in rows) else 'PASS')
    t.save(ROOT/a.output,out);return int(not out['BaselineMatch'])


if __name__=='__main__':raise SystemExit(main())

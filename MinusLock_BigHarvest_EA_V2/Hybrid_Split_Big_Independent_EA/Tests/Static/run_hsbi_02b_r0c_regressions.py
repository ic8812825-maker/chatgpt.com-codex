#!/usr/bin/env python3
"""Replay recorded commands into NEW R0C evidence; preserve original exits."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_hsbi_02b_r0c_contracts as t
ROOT=t.ROOT


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scan-only',action='store_true');parser.add_argument('--output',default='Tests/Evidence/NEXT_STAGE_02B_R0C_REGRESSIONS.json');args=parser.parse_args()
    recorded=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0B_REGRESSIONS.json').read_text())
    jobs=[]
    for old in recorded['runs']:
        if not old.get('command') or old['id']=='02A_no_trade_scan':continue
        cmd=old['command'][:]
        if '--output' in cmd:
            cmd[cmd.index('--output')+1]=str(ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0C_'+old['id']+'_RECHECK.json'))
        jobs.append((old['id'],cmd,old['exitCode']))
    for name,script in [('R0B_reference','check_hsbi_02b_r0b_contracts.py'),('R0B_mutations','check_hsbi_02b_r0b_mutations.py')]:
        jobs.append((name,['python3',str(ROOT/'Tests/Static'/script),'--output',str(ROOT/('Tests/Evidence/NEXT_STAGE_02B_R0C_'+name+'_RECHECK.json'))],0))
    scan=r"""from pathlib import Path
import re,json
pattern=re.compile(r'\b(?:OrderSend|OrderSendAsync|CTrade|PositionOpen|PositionClose|TRADE_ACTION_\w*|OnTradeTransaction)\b')
positive=['OrderSend(r,s);','OrderSendAsync(r,s);','CTrade trade;','PositionOpen();','PositionClose();','TRADE_ACTION_DEAL','void OnTradeTransaction(){}']
negative=['SafeOrderSender','PositionClosed','no trade calls']
assert all(pattern.search(x) for x in positive) and not any(pattern.search(x) for x in negative)
fs=list(Path('Include').rglob('*.mqh'))+list(Path('.').glob('*.mq5'))
bad=[str(p) for p in fs if pattern.search(p.read_text())]
print(json.dumps(dict(files=len(fs),forbidden=bad,positiveScannerControls=len(positive),negativeScannerControls=len(negative))))
raise SystemExit(bool(bad))
"""
    scanjob=('02A_no_trade_scan',['python3','-c',scan],0)
    if args.scan_only:
        prior=json.loads((ROOT/args.output).read_text());rows=[r for r in prior['runs'] if r['id'] not in ('02A_no_trade_scan','02A')];jobs=[scanjob]
    else:rows=[];jobs.append(scanjob)
    for name,cmd,expected in jobs:
        start=datetime.now(timezone.utc).isoformat()
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        counts=dict(passCount=None,failCount=None,countScope='See raw stdout; no invented counters')
        # Reuse only historical stdout parser, NOT evaluator/oracle outcomes.
        import runpy
        counter=runpy.run_path(str(ROOT/'Tests/Static/run_hsbi_02b_r0b_regressions.py'))['counts']
        passed,failed,scope=counter(name,p.stdout);counts=dict(passCount=passed,failCount=failed,countScope=scope)
        if name in ('02B_R0','02B_R0A','R0B_reference','R0B_mutations') and '--output' in cmd:
            result=json.loads(Path(cmd[cmd.index('--output')+1]).read_text())
            if name=='02B_R0':counts=dict(passCount=sum(x['contractPass'] for x in result['nativeCases']),failCount=result['normativeMismatchCount'],countScope='native proposed-contract comparisons')
            elif name=='R0B_mutations':counts=dict(passCount=len(result['mutations'])-result['finalSurvivors'],failCount=result['finalSurvivors'],countScope='planned mutation catalog; infrastructureErrors retained in raw result')
            else:counts=dict(passCount=result['passed'],failCount=result['failed'],countScope='historical runner semantic cases')
        if name=='02A_no_trade_scan':
            d=json.loads(p.stdout);counts=dict(passCount=d['files']-len(d['forbidden']),failCount=len(d['forbidden']),countScope='static files; 7 positive and 3 negative scanner controls, not MQL5 runtime')
        sourceHashes={str(Path(__file__).resolve().relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        for arg in cmd:
            f=Path(arg)
            if f.suffix=='.py' and f.is_file() and f.is_relative_to(ROOT):sourceHashes[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
        rows.append(dict(Command=cmd,StartedUtc=start,FinishedUtc=datetime.now(timezone.utc).isoformat(),TestedSHA=t.metadata()['testedSHA'],SourceHashes=sourceHashes,ExitCode=p.returncode,ExpectedBaselineExit=expected,BaselineMatch=p.returncode==expected,Stdout=p.stdout,Stderr=p.stderr,EvidencePath=str(Path(args.output).relative_to(ROOT)) if Path(args.output).is_absolute() else args.output,id=name,**counts))
        print(name,'exit',p.returncode,'PASS',counts['passCount'],'FAIL',counts['failCount'],flush=True)
    rows.append(dict(id='02A',Command=None,ExitCode=None,passCount=None,failCount=None,status='NOT_RUN_AS_SEPARATE_SUITE',EvidencePath='Reports/NEXT_STAGE_02A_TEST_EXECUTION_RU.md',reason='Standalone executable absent; recorded available commands replayed as R8/R10/R12/R12A/R7; native/broker NOT_RUN'))
    out=dict(t.metadata(),runs=rows,baselineMatch=all(x['BaselineMatch'] for x in rows if 'BaselineMatch' in x),regressionStatus='FAIL' if any(x.get('ExitCode') not in (0,None) for x in rows) else 'PASS')
    t.save(ROOT/args.output,out)
    return int(not out['baselineMatch'])


if __name__=='__main__':raise SystemExit(main())

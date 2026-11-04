#!/usr/bin/env python3
"""Read-only historical runners; evidence written only to new R0B files."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]


def counts(name,stdout):
    def match(pattern):
        m=re.search(pattern,stdout);return int(m[1]) if m else None
    if name=='R7_frozen':return match(r'CLEAN_PASS=(\d+)'),match(r'CLEAN_FAIL=(\d+)'),'frozen static checks'
    if name=='R12A_canonicalizer':return 0,0,'hash-only computation: zero test assertions'
    if name in ('R8','R10'):
        n=match(r'EXECUTED=(\d+)');return n,0 if n is not None else None,'acceptance cases; see raw findings'
    if name=='R12':return match(r'SECOND=(\d+)'),match(r'FINDINGS=(\d+)'),'second block fixtures; R10/sensitivity separate in stdout'
    if name=='R8_legacy':
        n=match(r'CHECKS_EXECUTED=(\d+)');bad=re.search(r'^FAILURE_IDS=(.*)$',stdout,re.M)
        failed=len([x for x in bad[1].split(',') if x]) if bad else None
        return n-failed if n is not None and failed is not None else None,failed,'wrapper checks; historical vector counts in stdout'
    if name=='R10_verify':return match(r'FIXTURES=(\d+)'),0 if 'RESULT=PASS' in stdout else None,'fixture cases; lifecycle steps reported separately'
    try:
        data=json.loads(stdout)
        if name=='R12A':return sum(x['pass'] for x in data['checks']),sum(not x['pass'] for x in data['checks']),'causal checks'
        if name in ('R8_properties','R10_properties'):
            values=[v for v in data.values() if type(v) is bool];return sum(values),sum(not v for v in values),'boolean properties'
        if 'executed' in data and 'failed' in data:return data['executed']-data['failed'],data['failed'],'runner case counters'
        if name=='R10_mutations':
            values=[v['SEMANTIC_MUTATION_VERDICT']=='CAUGHT_SEMANTIC' for v in data['forward']]
            return sum(values),sum(not v for v in values),'forward semantic mutations; reverse/harness/probes kept separately in stdout'
        if name=='R12_alignment':return data['predicates'] if not data['findings'] else None,len(data['findings']),'predicate alignments; failures are findings'
        if name=='R12A_coverage':return sum(v['status']=='PASS' for v in data['rows']),sum(v['status']!='PASS' for v in data['rows']),'AST coverage rows, not runtime assertions'
        if 'passed' in data:return data['passed'],data['failed'],'runner-reported semantic cases'
    except (ValueError,KeyError,TypeError):pass
    return None,None,'runner does not publish comparable case counters; not invented'


def main():
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    jobs=[('R8','accept_hsb_2e_r4_r9_r4a_r8.py',[]),('R8_legacy','verify_hsb_2e_prep_r4_r8.py',['--root',str(ROOT)]),
          ('R8_properties','run_hsb_2e_r4_r9_r4a_r8_properties.py',[]),('R8_sensitivity','run_hsb_2e_r4_r9_r4a_r8_acceptance_sensitivity.py',[]),
          ('R10','accept_hsb_2e_r4_r9_r4a_r10.py',[]),('R10_verify','verify_hsb_2e_r4_r9_r4a_r10.py',[]),
          ('R10_properties','run_hsb_2e_r4_r9_r4a_r10_properties.py',[]),('R10_mutations','run_hsb_2e_r4_r9_r4a_r10_mutation_sensitivity.py',[]),
          ('R12','accept_hsb_2e_r4_r9_r4a_r12_second_block.py',[]),('R12_alignment','verify_hsb_2e_r4_r9_r4a_r12_alignment.py',[]),
          ('R12A','check_hsb_2e_r4_r9_r4a_r12a_fix_01.py',[]),('R12A_coverage','audit_hsb_2e_r4_r9_r4a_r12a_actual_coverage.py',[]),
          ('R12A_canonicalizer','verify_hsb_2e_r4_r9_r4a_r12a_normative_contract.py',[]),
          ('R7_frozen','verify_hsb_2d_v1_r7.py',['--root',str(ROOT),'--skip-seal']),
          ('02B_R0','check_hsbi_02b_r0_ledger_integrity.py',['--enforce-contract','--output',str(ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0B_R0_RECHECK.json')]),
          ('02B_R0A','check_hsbi_02b_r0a_normative_contracts.py',['--output',str(ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0B_R0A_RECHECK.json')])]
    rows=[]
    with tempfile.TemporaryDirectory(prefix='r0b-regression-',dir=ROOT/'Tests') as scratch:
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=scratch)
        for name,script,args in jobs:
            cmd=['python3',str(ROOT/'Tests/Static'/script),*args];started=datetime.now(timezone.utc).isoformat()
            proc=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env)
            passed,failed,scope=counts(name,proc.stdout)
            if name=='02B_R0':scope='native proposed-contract comparisons; counts read from fresh result JSON'
            if name=='02B_R0A':
                d=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0B_R0A_RECHECK.json').read_text());passed,failed=d['passed'],d['failed']
            if name=='02B_R0':
                d=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0B_R0_RECHECK.json').read_text());passed=sum(x['contractPass'] for x in d['nativeCases']);failed=d['normativeMismatchCount']
            expected=1 if name in ('R7_frozen','02B_R0') else 0
            rows.append(dict(id=name,command=cmd,startedUtc=started,finishedUtc=datetime.now(timezone.utc).isoformat(),testedSha=head,
                exitCode=proc.returncode,expectedBaselineExit=expected,baselineOutcomeMatches=proc.returncode==expected,
                passCount=passed,failCount=failed,countScope=scope,stdout=proc.stdout,stderr=proc.stderr,
                evidencePath='Tests/Evidence/NEXT_STAGE_02B_R0B_REGRESSIONS.json#'+name,
                failureReason='Frozen status/manifest expectations' if name=='R7_frozen' else 'Known 46 unremediated proposed-contract mismatches' if name=='02B_R0' else None))
            print(name,proc.returncode,passed,failed,flush=True)
    # 02A had no separate runner. Its recorded commands were rerun above; no
    # fictitious test execution/counts are manufactured from its JSON matrix.
    rows.append(dict(id='02A',command=None,startedUtc=datetime.now(timezone.utc).isoformat(),testedSha=head,exitCode=None,
        passCount=None,failCount=None,status='NOT_RUN_AS_SEPARATE_SUITE',
        reason='No stage-02A executable exists; all executable commands in NEXT_STAGE_02A_TEST_EXECUTION_RU.md rerun as R8/R10/R12/R12A/R7. Broker/MQL5 commands remain NOT_RUN.',
        evidencePath='Reports/NEXT_STAGE_02A_TEST_EXECUTION_RU.md'))
    result=dict(testedSha=head,runs=rows,noHistoricalPublishFlags=True,MQL5_COMPILE='NOT_RUN',STRATEGY_TESTER='NOT_RUN')
    (ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0B_REGRESSIONS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return int(any(not r['baselineOutcomeMatches'] for r in rows if 'baselineOutcomeMatches' in r))


if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""Independent Git-tree inventory and semantic evidence checker. Default read-only."""
import argparse
import ast
import copy
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
PREFIX='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
BASE='ec7ae40fe22e1d6e5bed035450750502a1162ab5'
PRES='Tests/Evidence/NEXT_STAGE_02B_R0D_PRESERVATION.json'
RESULT='Tests/Evidence/NEXT_STAGE_02B_R0D_PACKAGE_RESULTS.json'
MANDATORY=[
 'Docs/NEXT_STAGE_02B_R0D_NUMERIC_CONTRACT_RU.md','Docs/NEXT_STAGE_02B_R0D_SNAPSHOT_IDENTITY_CONTRACT_RU.md','Docs/NEXT_STAGE_02B_R0D_NORMATIVE_ADDENDUM_RU.md',
 'Reports/NEXT_STAGE_02B_R0D_REPRODUCTION_RU.md','Reports/NEXT_STAGE_02B_R0D_TEST_AND_MUTATION_RESULTS_RU.md','Reports/NEXT_STAGE_02B_R0D_ADMIN_DECISIONS_RU.md','Reports/NEXT_STAGE_02B_R0D_FINAL_VERDICT_RU.md',
 'Tests/Reference/hsbi_02b_r0d_independent_oracle.py','Tests/Static/check_hsbi_02b_r0d_contracts.py','Tests/Static/check_hsbi_02b_r0d_mutations.py','Tests/Static/check_hsbi_02b_r0d_package.py','Tests/Static/run_hsbi_02b_r0d_regressions.py','Tests/Contracts/NEXT_STAGE_02B_R0D_VERIFICATION_MATRIX.json',
 'Tests/Evidence/NEXT_STAGE_02B_R0D_REPRODUCTION.json','Tests/Evidence/NEXT_STAGE_02B_R0D_TEST_RESULTS.json','Tests/Evidence/NEXT_STAGE_02B_R0D_MUTATION_RESULTS.json',RESULT,'Tests/Evidence/NEXT_STAGE_02B_R0D_REGRESSIONS.json',PRES]


def git_inventory(repo):
    rows=subprocess.check_output(['git','-C',str(repo),'ls-tree','-rz',BASE,'--',PREFIX]);out={}
    for row in rows.split(b'\0'):
        if row:
            meta,name=row.split(b'\t',1);mode,kind,oid=meta.decode().split()
            if kind!='blob' or mode not in ('100644','100755'):raise ValueError('unsupported baseline Git entry')
            out[name.decode()[len(PREFIX):]]=oid
    return out


def read(root,path):return json.loads((root/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root,repo,strict=True):
    errors=[]
    def fail(code,path=''):errors.append(dict(code=code,path=path))
    expected=git_inventory(repo)
    try:proof=read(root,PRES)
    except (OSError,ValueError):return [dict(code='PRESERVATION_MISSING_OR_MALFORMED',path=PRES)]
    if proof.get('baseSHA')!=BASE:fail('BASELINE_REFERENCE')
    if set(proof.get('existingFiles',{}))!=set(expected):fail('BASELINE_INVENTORY')
    for path,oid in expected.items():
        f=root/path
        if not f.is_file() or f.is_symlink():fail('HISTORICAL_FILE_MISSING',path);continue
        content=f.read_bytes();actual=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        if actual!=oid:fail('HISTORICAL_GIT_BLOB',path)
        row=proof.get('existingFiles',{}).get(path,{})
        if row.get('gitBlob')!=oid or row.get('sha256')!=hashlib.sha256(content).hexdigest():fail('HISTORICAL_HASH',path)
    actualFiles={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    additions=actualFiles-set(expected)
    if additions!=set(proof.get('newFiles',[])) or len(proof.get('newFiles',[]))!=len(additions):fail('NEW_INVENTORY')
    for path in additions:
        if path.split('/')[0] not in ('Docs','Reports','Tests') or 'r0d' not in path.lower() or (root/path).is_symlink():fail('OUTSIDE_ALLOWED_SCOPE',path)
    for path in MANDATORY:
        if path not in additions or not (root/path).is_file() or not (root/path).stat().st_size:fail('MANDATORY_ARTIFACT',path)
    hashes=proof.get('newArtifactHashes',{})
    if set(hashes)!=set(proof.get('newFiles',[]))-{PRES,RESULT}:fail('NEW_HASH_INVENTORY')
    for path,h in hashes.items():
        if not (root/path).is_file() or sha(root/path)!=h:fail('NEW_HASH',path)
    try:
        tests=read(root,'Tests/Evidence/NEXT_STAGE_02B_R0D_TEST_RESULTS.json');mut=read(root,'Tests/Evidence/NEXT_STAGE_02B_R0D_MUTATION_RESULTS.json');matrix=read(root,'Tests/Contracts/NEXT_STAGE_02B_R0D_VERIFICATION_MATRIX.json');reg=read(root,'Tests/Evidence/NEXT_STAGE_02B_R0D_REGRESSIONS.json');repro=read(root,'Tests/Evidence/NEXT_STAGE_02B_R0D_REPRODUCTION.json')
        rows=tests['tests'];ids={r['id'] for r in rows};contexts=len(tests['contextConfigurations'])
        if len(rows)!=tests['executions'] or len(ids)!=tests['scenarios'] or len(rows)!=len(ids)*contexts or len({(r['id'],r['context']) for r in rows})!=len(rows):fail('TEST_TOTAL')
        if tests['passed']!=sum(r['result']=='PASS' for r in rows) or tests['failed']!=sum(r['result']=='FAIL' for r in rows) or tests['infrastructureErrors']!=sum(r['result']=='INFRASTRUCTURE_ERROR' for r in rows):fail('TEST_AGGREGATES')
        if tests['comparisonPredicates']!=sum(r['predicates'] for r in rows):fail('COMPARISON_TOTAL')
        if any(r['result']!='PASS' or r['actual']!=r['expected'] or not r.get('contextUnchanged',False) for r in rows):fail('TEST_ROW_VERDICT')
        if set(matrix['scenarioIDs'])!=ids:fail('MATRIX_REFERENCE')
        functions={n.name:n.lineno for n in ast.walk(ast.parse((root/'Tests/Reference/hsbi_02b_r0d_independent_oracle.py').read_text())) if isinstance(n,ast.FunctionDef)}
        for r in matrix['cases']:
            if r['TestID'] not in ids or functions.get(r['SourceFunction'])!=r['SourceLine']:fail('MATRIX_SOURCE_REFERENCE',r['TestID'])
        if mut['catalogSize']!=len(mut['mutations']) or mut['killed']!=len(mut['mutations']) or any(r['Verdict']!='MUTATION_KILLED' for r in mut['mutations']) or mut['survived'] or mut['infrastructureErrors']:fail('MUTATION_VERDICT')
        for r in mut['mutations']:
            if r['CausalTestID'] not in ids or not r.get('PositiveControlPass') or not r.get('OriginalNegativePass') or r['OriginalNegativeOutcome']!=r['IndependentExpected'] or r['MutantNegativeOutcome']==r['IndependentExpected']:fail('MUTATION_CAUSALITY',r['MutationID'])
        if not reg['BaselineMatch'] or reg['BaselineMatch']!=all(r['ExitCode']==r['ExpectedBaselineExit'] for r in reg['runs'] if 'ExpectedBaselineExit' in r):fail('REGRESSION_BASELINE')
        if reg['RegressionStatus']!=('FAIL' if any(r['ExitCode'] not in (0,None) for r in reg['runs']) else 'PASS'):fail('REGRESSION_AGGREGATE')
        for evidence in (tests,mut,repro):
            for path,h in evidence['SourceHashes'].items():
                if not (root/path).is_file() or sha(root/path)!=h:fail('SOURCE_HASH',path)
        for row in reg['runs']:
            for path,h in row.get('SourceHashes',{}).items():
                if not (root/path).is_file() or sha(root/path)!=h:fail('SOURCE_HASH',path)
        admin=(root/'Reports/NEXT_STAGE_02B_R0D_ADMIN_DECISIONS_RU.md').read_text()
        for label in ('AdministratorDecision','ApprovalDate','ApprovalIdentifier'):
            if admin.count(label+':\n\n')!=4:fail('ADMIN_APPROVAL_FIELD',label)
        if strict:
            results=read(root,RESULT)
            probes=results.get('negativeChecks',[])
            if len({r['id'] for r in probes})!=7 or any(r.get('detected')!=any(e['code']==r['expectedFinding'] for e in r['actualFindings']) for r in probes):fail('PACKAGE_SELFTEST_ROWS')
            for path,h in results.get('SourceHashes',{}).items():
                if sha(root/path)!=h:fail('PACKAGE_SELFTEST_SOURCE',path)
            if results.get('status')!='PASS' or not results.get('positivePass') or any(not r['detected'] for r in results.get('negativeChecks',[])) or len(results.get('negativeChecks',[]))!=7:fail('PACKAGE_SELFTEST_VERDICT')
    except (KeyError,TypeError,ValueError,OSError) as e:fail('EVIDENCE_SCHEMA',type(e).__name__)
    return errors


def selftest(repo):
    positive=verify(ROOT,repo,strict=False);paths=[p.relative_to(ROOT) for p in ROOT.rglob('*') if p.is_file()];checks=[]
    # All mutations below are disposable project copies; Git tree remains original/read-only.
    with tempfile.TemporaryDirectory(prefix='r0d-package-',dir=ROOT/'Tests') as scratch:
        for name in ('missing-inventory','historical-content','source-hash','test-total','fail-row','mandatory-artifact','outside-scope'):
            candidate=Path(scratch)/name
            for rel in paths:
                dest=candidate/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
            proof=read(candidate,PRES)
            target=None
            if name=='missing-inventory':proof['existingFiles'].pop(next(iter(proof['existingFiles'])))
            elif name=='historical-content':
                target=next(p for p in proof['existingFiles'] if p.startswith('Include/') and p.endswith('.mqh'));(candidate/target).write_bytes((candidate/target).read_bytes()+b'\n// disposable test fault\n')
            elif name in ('source-hash','test-total','fail-row'):
                target='Tests/Evidence/NEXT_STAGE_02B_R0D_TEST_RESULTS.json';data=read(candidate,target)
                if name=='source-hash':data['SourceHashes'][next(iter(data['SourceHashes']))]='0'*64
                elif name=='test-total':data['executions']+=1
                else:data['tests'][0]['result']='FAIL'  # aggregate PASS intentionally retained
                (candidate/target).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');proof['newArtifactHashes'][target]=sha(candidate/target)
            elif name=='mandatory-artifact':(candidate/MANDATORY[0]).unlink()
            else:(candidate/'UNAUTHORIZED.txt').write_text('synthetic outside-scope marker')
            (candidate/PRES).write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
            errors=verify(candidate,repo,strict=False)
            required={'missing-inventory':'BASELINE_INVENTORY','historical-content':'HISTORICAL_GIT_BLOB','source-hash':'SOURCE_HASH','test-total':'TEST_TOTAL','fail-row':'TEST_ROW_VERDICT','mandatory-artifact':'MANDATORY_ARTIFACT','outside-scope':'OUTSIDE_ALLOWED_SCOPE'}[name]
            checks.append(dict(id=name,expectedFinding=required,actualFindings=errors,detected=any(e['code']==required for e in errors)))
    return dict(status='PASS' if not positive and all(c['detected'] for c in checks) else 'FAIL',positivePass=not positive,positiveFindings=positive,negativeChecks=checks,baselineSHA=BASE,executedUtc=datetime.now(timezone.utc).isoformat(),scope='Independent Git inventory + disposable copies; own result and preservation self hashes deliberately excluded to avoid self reference')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--repo',type=Path);args=parser.parse_args()
    repo=args.repo or Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
    if args.self_test:
        started=datetime.now(timezone.utc).isoformat();out=selftest(repo);out.update(Command=__import__('sys').argv,StartedUtc=started,FinishedUtc=datetime.now(timezone.utc).isoformat(),TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),ExitCode=int(out['status']!='PASS'),SourceHashes={str(Path(__file__).resolve().relative_to(ROOT)):sha(Path(__file__).resolve())});(ROOT/RESULT).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False));return int(out['status']!='PASS')
    errors=verify(args.root.resolve(),repo);print(json.dumps(dict(status='FAIL' if errors else 'PASS',findings=errors),ensure_ascii=False));return int(bool(errors))


if __name__=='__main__':raise SystemExit(main())

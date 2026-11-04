#!/usr/bin/env python3
"""Read-only package/preservation check; hashes are checked, not just file names."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]


def read(name):return json.loads((ROOT/name).read_text())


def main():
    proof=read('Tests/Evidence/NEXT_STAGE_02B_R0C_PRESERVATION.json')
    for path,expected in proof['existingProjectFiles'].items():
        data=(ROOT/path).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==expected['gitBlob'],path
        assert hashlib.sha256(data).hexdigest()==expected['sha256'],path
    for path,expected in proof['newArtifactHashes'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    tests=read('Tests/Evidence/NEXT_STAGE_02B_R0C_TEST_RESULTS.json');mut=read('Tests/Evidence/NEXT_STAGE_02B_R0C_MUTATION_RESULTS.json');matrix=read('Tests/Contracts/NEXT_STAGE_02B_R0C_VERIFICATION_MATRIX.json');reg=read('Tests/Evidence/NEXT_STAGE_02B_R0C_REGRESSIONS.json');rep=read('Tests/Evidence/NEXT_STAGE_02B_R0C_REPRODUCTION.json')
    assert tests['failed']==0 and tests['passed']==len(tests['tests'])==tests['scenarios']
    assert len(set(r['id'] for r in tests['tests']))==tests['scenarios']
    assert tests['assertions']==sum(r['assertions'] for r in tests['tests'])
    assert mut['killed']==len(mut['mutations']) and mut['survived']==mut['infrastructureErrors']==0
    assert all(r['PositiveControlPass'] and r['OriginalNegativePass'] and r['MutationVerdict']=='MUTATION_KILLED' for r in mut['mutations'])
    assert rep['allFourConfirmed'] and all(r['OldSuitePassed']==141 and r['OldSuiteFailed']==0 for r in rep['fourMutations'])
    assert reg['baselineMatch'] and reg['regressionStatus']=='FAIL'
    assert {r['TestID'] for r in matrix['evidenceMatrix']}=={r['id'] for r in tests['tests']}
    source=ROOT/'Tests/Reference/hsbi_02b_r0c_independent_oracle.py'
    lines={n.name:n.lineno for n in ast.walk(ast.parse(source.read_text())) if isinstance(n,ast.FunctionDef)}
    for row in matrix['evidenceMatrix']:assert row['SourceLine']==lines[row['SourceFunction']]
    for data in (tests,mut,rep):
        for path,h in data.get('sourceHashes',data.get('SourceHashes',{})).items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
    for row in reg['runs']:
        for path,h in row.get('SourceHashes',{}).items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
    for row in mut['mutations']:assert hashlib.sha256((ROOT/row['TargetFile']).read_bytes()).hexdigest()==row['OriginalSourceHash']
    admin=(ROOT/'Reports/NEXT_STAGE_02B_R0C_ADMIN_DECISIONS_RU.md').read_text()
    for label in ('AdministratorDecision','ApprovalDate','ApprovalIdentifier'):assert admin.count(label+':\n\n')==8
    assert proof['initialRemoteSHA']==proof['initialLocalSHA']==proof['baseSHA']
    assert all(p.split('/')[0] in ('Docs','Reports','Tests') and 'r0c' in p.lower() for p in proof['newFiles'])
    assert len(proof['newFiles'])==len(set(proof['newFiles']))
    print(json.dumps(dict(status='PASS',baselineFiles=len(proof['existingProjectFiles']),newFiles=len(proof['newFiles']),scenarios=tests['scenarios'],comparisonPredicates=tests['assertions'],causalMutations=mut['killed'],historicalFilesUnchanged=True,productionChanges=False,approval='AWAITING'),ensure_ascii=False))


if __name__=='__main__':main()

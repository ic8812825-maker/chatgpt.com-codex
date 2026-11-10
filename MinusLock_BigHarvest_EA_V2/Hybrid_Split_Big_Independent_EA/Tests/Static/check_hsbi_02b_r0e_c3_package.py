#!/usr/bin/env python3
"""C3 independent audit-package verifier; immutable Git baseline and literal audit expectations."""
import argparse,copy,hashlib,json,re,shutil,subprocess,tempfile,sys
from pathlib import Path
import check_hsbi_02b_r0e_c3_common as a
import check_hsbi_02b_r0e_c3_independent as independent
from hsbi_02b_r0e_c3_decision_proposals import decisions
VERIFIER_HASH=a.sha(Path(__file__))
PRES='Tests/Evidence/NEXT_STAGE_02B_R0E_C3_PRESERVATION.json';RESULT='Tests/Evidence/NEXT_STAGE_02B_R0E_C3_PACKAGE_RESULTS.json'
MANDATORY=[f'Reports/NEXT_STAGE_02B_R0E_C3_{s}_RU.md' for s in ('FINAL_VERDICT','REPRODUCTION','MUTATION_AUDIT','MONEY_CONTRACT_AUDIT','ADMIN_DECISION_MATRIX','R1_READINESS')]+[f'Docs/NEXT_STAGE_02B_R0E_C3_{s}_RU.md' for s in ('CONTRACT_CLARIFICATIONS','VERIFICATION_BOUNDARIES')]+[f'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_{s}.json' for s in ('BASELINE','C2_REFERENCE','C2_MUTATIONS','C2_PACKAGE','REPRODUCTION','SURVIVORS','INDEPENDENT_TESTS','NATIVE_SUBSET','REGRESSIONS','EXECUTIONS','DEVELOPMENT')]+['Tests/Contracts/NEXT_STAGE_02B_R0E_C3_GUARD_MATRIX.json','Tests/Contracts/NEXT_STAGE_02B_R0E_C3_ADMIN_MATRIX.json']
PROBES=('inventory','source-hash','reference-row','survivor-whitewash','admin-approval','dispatch','duplicate-json','guard-omission','regression-exit','empty-package-catalog','verifier-source')

def load(root,path):return a.subject.evidence.loads((root/path).read_text())
def files(root):return {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def seal():
 old=a.inventory();added=files(a.ROOT)-set(old);added.add(PRES);assert all(p.split('/')[0] in ('Docs','Reports','Tests') and 'r0e_c3' in Path(p).name.lower() for p in added)
 a.save('PRESERVATION',dict(a.metadata(__file__),Existing=old,NewFiles=sorted(added),ArtifactHashes={p:a.sha(a.ROOT/p) for p in added-{PRES,RESULT}},SelfHashExclusions=[PRES,RESULT],NoTrade=__import__('check_hsbi_02b_r0e_package').scan(a.ROOT)))
def verify(root=a.ROOT,with_results=True):
 errors=[]
 def require(ok,code):
  if not ok:errors.append(code)
 def provenance(d):
  if type(d) is dict:
   if 'SourceHashes' in d:
    require(bool(d['SourceHashes']),'SOURCE_INVENTORY')
    for p,h in d['SourceHashes'].items():
     safe=type(p) is str and not Path(p).is_absolute() and '..' not in Path(p).parts
     require(safe and (root/p).is_file() and a.sha(root/p)==h,'SOURCE_HASH')
   for v in d.values():provenance(v)
  elif type(d) is list:
   for v in d:provenance(v)
 try:
  old=a.inventory();proof=load(root,PRES);require(a.sha(root/str(Path(__file__).relative_to(a.ROOT)))==VERIFIER_HASH,'VERIFIER_SOURCE_IDENTITY');require(set(proof['Existing'])==set(old),'BASELINE_INVENTORY')
  for p,v in old.items():
   f=root/p;require(f.is_file() and not f.is_symlink() and a.sha(f)==v['SHA256'] and bool(f.stat().st_mode&0o111)==(v['mode']=='100755'),'BASELINE_BYTES_MODES');require(proof['Existing'].get(p)==v,'BASELINE_OBJECTS')
  added=files(root)-set(old);require(set(proof['NewFiles'])==added,'NEW_INVENTORY');require(all(p.split('/')[0] in ('Docs','Reports','Tests') and 'r0e_c3' in Path(p).name.lower() for p in added),'SCOPE')
  require(set(proof['ArtifactHashes'])==added-{PRES,RESULT},'HASH_INVENTORY')
  for p,h in proof['ArtifactHashes'].items():require((root/p).is_file() and a.sha(root/p)==h,'ARTIFACT_HASH')
  require(all((root/p).is_file() and (root/p).stat().st_size>0 for p in MANDATORY),'MANDATORY')
  for p in added:
   if p.endswith('.json'):
    data=load(root,p)
    if not p.endswith('DEVELOPMENT.json') and (p!=RESULT or with_results):provenance(data)
  baseline=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_BASELINE.json');require(baseline['Existing']==old and len(baseline['Production'])==74,'BASELINE_RECORD')
  c2=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_C2_REFERENCE.json');cat=load(root,'Tests/Contracts/NEXT_STAGE_02B_R0E_C2_REQUIRED_CATALOG.json');pairs=[(r['TestID'],r['ContextID']) for r in c2['Rows']]
  require((c2['Scenarios'],c2['Executions'],c2['SchemaProbes'],c2['Comparisons'],c2['Pass'],c2['Fail'],c2['InfrastructureErrors'])==(158,1264,2462,9914,1264,0,0),'C2_REFERENCE_COUNTS')
  require(set(pairs)=={(i,j) for i in cat['RequiredTestIDs'] for j in range(8)} and len(set(pairs))==len(pairs),'C2_REFERENCE_INVENTORY');require(all(r['Result']=='PASS' and r['Actual']==r['IndependentExpected'] for r in c2['Rows']) and len(c2['SchemaRows'])==2462 and all(r['Result']=='PASS' for r in c2['SchemaRows']),'C2_REFERENCE_ROWS')
  mu=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_C2_MUTATIONS.json');require((mu['CatalogSize'],mu['Killed'],mu['RedundantSurvivors'],mu['UnexplainedSurvivors'],mu['InfrastructureErrors'])==(70,64,6,0,0),'FROZEN_MUTATION_COUNTS');require({r['MutationID'] for r in mu['Rows']}==set(cat['RequiredMutationIDs']) and len(mu['Rows'])==70,'FROZEN_MUTATION_INVENTORY')
  for row in mu['Rows']:
   src=(root/row['TargetFile']).read_text();require(hashlib.sha256(src.encode()).hexdigest()==row['OriginalSourceHash'],'MUTATION_SOURCE')
   for e in row['ExactEdit']:require(src.count(e['old'])==1,'EXACT_EDIT');src=src.replace(e['old'],e['new'])
   require(hashlib.sha256(src.encode()).hexdigest()==row['MutantSourceHash'],'MUTANT_HASH');require(row['ControlsPass'] is True,'MUTATION_CONTROLS')
  pkg=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_C2_PACKAGE.json');original=__import__('check_hsbi_02b_r0e_c2_package');require(pkg['Positive']=='PASS' and pkg['NegativePassed']==58 and pkg['NegativeFailed']==0 and {r['ProbeID'] for r in pkg['Negative']}==set(original.PROBE_IDS) and len(pkg['Negative'])==58 and all(r['Result']=='PASS' for r in pkg['Negative']),'C2_PACKAGE')
  ind=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_INDEPENDENT_TESTS.json');expected={r['TestID']:r for r in independent.test_cases()[0]};require({r['TestID'] for r in ind['Rows']}==set(expected) and len(ind['Rows'])==len(expected),'INDEPENDENT_INVENTORY')
  for row in ind['Rows']:require(row['Result']=='PASS' and a.view(row['Actual'])==a.view(expected[row['TestID']]['Expected']) and a.view(row['Expected'])==a.view(expected[row['TestID']]['Expected']),'INDEPENDENT_ROW')
  require(ind['ExitCode']==0 and ind['Fail']==0 and ind['InfrastructureErrors']==0 and ind['IndependentOracleHash']==a.sha(root/'Tests/Reference/hsbi_02b_r0e_c3_mathematical_oracle.py'),'INDEPENDENT_TOTALS')
  sur=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_SURVIVORS.json');require(len(sur['Rows'])==6 and sur['StatusGaps']==1,'SURVIVOR_INVENTORY')
  for r in sur['Rows']:
   gap=r['MutationID']=='C2-MUT-cost-shape-caller';require(r['Classification']==('NOT_GLOBALLY_REDUNDANT_STATUS_GAP' if gap else 'REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN'),'SURVIVOR_CLASSIFICATION')
   require(all(p['OriginalMatchesExpected'] and p['StateDeltaZero'] and p['PositiveOriginal']['Status']==p['PositiveMutant']['Status'] for p in r['IndependentCallerAudit']),'CALLER_CONTROLS')
   if gap:
    pair=next(p for p in r['IndependentCallerAudit'] if p['PublicCaller']=='cost_coverage');require(pair['OriginalOutcome']['Status']=='CONFLICT' and pair['MutantOutcome']['Status']=='UNAVAILABLE','STATUS_GAP')
  reg=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_REGRESSIONS.json');require(reg['ExitCode']==0 and reg['BaselineMatch'] is True and reg['RegressionStatus']=='FAIL' and len(reg['Runs'])==34,'REGRESSION')
  for row in reg['Runs']:require(row['BaselineMatch'] and row['ExitCode']==row['ExpectedBaselineExit'],'REGRESSION_ROW')
  hist={r['ID']:r for r in reg['Runs']};require((hist['R7_frozen']['ExitCode'],hist['R7_frozen']['PassCount'],hist['R7_frozen']['FailCount'])==(1,57,5) and (hist['02B_R0']['ExitCode'],hist['02B_R0']['PassCount'],hist['02B_R0']['FailCount'])==(1,35,46),'HISTORICAL_FAILURES')
  exe=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_EXECUTIONS.json');require({r['ID'] for r in exe['Rows']}=={'reproduction','independent','native','regressions'} and exe['ExitCode']==0 and all(r['ExitCode']==0 and type(r['Stdout']) is str and type(r['Stderr']) is str for r in exe['Rows']),'EXECUTIONS')
  native=load(root,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_NATIVE_SUBSET.json');require(native['Actual']=='1 1 1' and native['Finding']=='L01_L02_CONFIRMED' and native['NormativeResult']=='FAIL' and native['MQL5_COMPILE']=='NOT_RUN','NATIVE_BOUNDARY')
  admin=load(root,'Tests/Contracts/NEXT_STAGE_02B_R0E_C3_ADMIN_MATRIX.json');require(admin['Rows']==decisions() and len(admin['Rows'])==16 and all(r['ApprovalStatus']=='AWAITING_ADMIN_APPROVAL' and r['AdministratorDecision']=='' for r in admin['Rows']),'ADMIN_APPROVAL')
  mat=load(root,'Tests/Contracts/NEXT_STAGE_02B_R0E_C3_GUARD_MATRIX.json');require({r['ClauseID'] for r in mat['FrozenGuardRows']}=={r['ClauseID'] for r in cat['Guards']} and len(mat['FrozenGuardRows'])==70 and len(mat['PublicAPIMatrix'])==7 and set(mat['IndependentTestIDs'])==set(expected),'GUARD_MATRIX')
  text=(root/'Reports/NEXT_STAGE_02B_R0E_C3_FINAL_VERDICT_RU.md').read_text()
  for name in ('ADMIN_APPROVAL_COMPLETE','R1_1_START_ALLOWED','PRODUCTION_REMEDIATION_ALLOWED','TRADING_LOGIC_START_ALLOWED','BROKER_DISPATCH_ALLOWED','REAL_TRADING_ALLOWED'):require(re.findall('^'+name+'=(.*)$',text,re.M)==['NO'],'POLICY')
  require(proof['NoTrade']==dict(files=74,forbidden=[],controls=True,guard=True),'NO_TRADE')
  if with_results:
   final=load(root,RESULT);require(final['Positive']=='PASS' and final['NegativePassed']==len(PROBES) and final['NegativeFailed']==0 and {r['ProbeID'] for r in final['Rows']}==set(PROBES) and all(r['Result']=='PASS' for r in final['Rows']),'C3_PACKAGE_RESULTS')
 except (OSError,KeyError,ValueError,TypeError,AssertionError,StopIteration) as e:errors.append('SCHEMA:'+type(e).__name__+':'+str(e))
 return sorted(set(errors))

def probes():
 errors=verify(with_results=False)
 if errors:return dict(Positive='FAIL',Errors=errors,Rows=[],NegativePassed=0,NegativeFailed=0)
 rows=[];paths=files(a.ROOT)
 with tempfile.TemporaryDirectory(prefix='R0E_C3_pkg_',dir=a.ROOT/'Tests') as td:
  template=Path(td)/'template'
  for name in paths:
   f=template/name;f.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a.ROOT/name,f)
  def j(root,path,fn):data=load(root,path);fn(data);(root/path).write_text(json.dumps(data,ensure_ascii=False,indent=2))
  def altered_verifier(root):
   target='Tests/Static/check_hsbi_02b_r0e_c3_package.py';f=root/target;f.write_text(f.read_text()+'\n# synthetic identity probe\n');j(root,RESULT,lambda d:(d.setdefault('SourceHashes',{}).__setitem__(target,a.sha(f)),d.__setitem__('RunnerSourceHash',a.sha(f))));j(root,PRES,lambda d:(d['SourceHashes'].__setitem__(target,a.sha(f)),d.__setitem__('RunnerSourceHash',a.sha(f))))
  specs=[('inventory','BASELINE_INVENTORY',lambda r:j(r,PRES,lambda d:d['Existing'].pop(next(iter(d['Existing']))))),('source-hash','SOURCE_HASH',lambda r:j(r,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_INDEPENDENT_TESTS.json',lambda d:d['SourceHashes'].__setitem__('Tests/Reference/hsbi_02b_r0e_c2_contract_model.py','0'*64))),('reference-row','C2_REFERENCE_ROWS',lambda r:j(r,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_C2_REFERENCE.json',lambda d:d['Rows'][0].__setitem__('Result','FAIL'))),('survivor-whitewash','SURVIVOR_CLASSIFICATION',lambda r:j(r,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_SURVIVORS.json',lambda d:next(x for x in d['Rows'] if x['MutationID']=='C2-MUT-cost-shape-caller').__setitem__('Classification','REDUNDANT_IN_DECLARED_PUBLIC_DOMAIN'))),('admin-approval','ADMIN_APPROVAL',lambda r:j(r,'Tests/Contracts/NEXT_STAGE_02B_R0E_C3_ADMIN_MATRIX.json',lambda d:d['Rows'][0].__setitem__('ApprovalStatus','APPROVED'))),('dispatch','POLICY',lambda r:(r/'Reports/NEXT_STAGE_02B_R0E_C3_FINAL_VERDICT_RU.md').write_text((r/'Reports/NEXT_STAGE_02B_R0E_C3_FINAL_VERDICT_RU.md').read_text().replace('BROKER_DISPATCH_ALLOWED=NO','BROKER_DISPATCH_ALLOWED=YES'))),('duplicate-json','SCHEMA',lambda r:(r/'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_REPRODUCTION.json').write_text((r/'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_REPRODUCTION.json').read_text().replace('"ExitCode": 0','"ExitCode": 1, "ExitCode": 0',1))),('guard-omission','GUARD_MATRIX',lambda r:j(r,'Tests/Contracts/NEXT_STAGE_02B_R0E_C3_GUARD_MATRIX.json',lambda d:d['FrozenGuardRows'].pop())),('regression-exit','REGRESSION_ROW',lambda r:j(r,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_REGRESSIONS.json',lambda d:next(x for x in d['Runs'] if x['ID']=='R7_frozen').__setitem__('ExitCode',0))),('empty-package-catalog','C2_PACKAGE',lambda r:j(r,'Tests/Evidence/NEXT_STAGE_02B_R0E_C3_C2_PACKAGE.json',lambda d:d.update(Negative=[],NegativePassed=0,NegativeFailed=0)))]
  specs.append(('verifier-source','VERIFIER_SOURCE_IDENTITY',altered_verifier))
  assert tuple(s[0] for s in specs)==PROBES
  for name,expected,edit in specs:
   candidate=Path(td)/'candidate';shutil.copytree(template,candidate);edit(candidate);proof=load(candidate,PRES)
   for path in proof['ArtifactHashes']:
    f=candidate/path
    if f.exists():proof['ArtifactHashes'][path]=a.sha(f)
   (candidate/PRES).write_text(json.dumps(proof,ensure_ascii=False,indent=2));actual=verify(candidate,False);ok=any(e.startswith(expected) for e in actual);rows.append(dict(ProbeID=name,ExpectedError=expected,ActualErrors=actual,Result='PASS' if ok else 'FAIL',PositiveControl='unmodified frozen template passed'));shutil.rmtree(candidate);print(name,rows[-1]['Result'],flush=True)
 return dict(Positive='PASS',Errors=[],Rows=rows,NegativePassed=sum(r['Result']=='PASS' for r in rows),NegativeFailed=sum(r['Result']!='PASS' for r in rows))
def main():
 p=argparse.ArgumentParser();p.add_argument('--seal',action='store_true');p.add_argument('--self-test',action='store_true');args=p.parse_args()
 if args.seal:seal()
 started=a.now()
 if args.self_test:result=probes();result.update(a.metadata(__file__),StartedUtc=started,FinishedUtc=a.now(),Command=[sys.executable,*sys.argv]);result['ExitCode']=int(result['Positive']!='PASS' or result['NegativeFailed']>0);a.save('PACKAGE_RESULTS',result)
 else:errors=verify();result=dict(Positive='PASS' if not errors else 'FAIL',Errors=errors,ExitCode=int(bool(errors)))
 print({k:v for k,v in result.items() if k!='Rows'});return result['ExitCode']
if __name__=='__main__':raise SystemExit(main())
